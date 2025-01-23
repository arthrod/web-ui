# app.py
import os
import shutil
import logging
import time

from fastapi import FastAPI, Request
from webui import run_browser_agent
from filter_mitm_logs import filter_jsonl_file
app = FastAPI()


def copy_folder(source_folder, destination_folder):
    try:

        if not os.path.exists(source_folder):
            raise FileNotFoundError(f"Source folder does not exist: {source_folder}")
        shutil.copytree(source_folder, os.path.join(destination_folder, os.path.basename(source_folder)),dirs_exist_ok=True)
        logging.info(f"Successfully copied {source_folder} to {destination_folder}")

    except FileNotFoundError as e:
        logging.info(f"Could not find the folder: {source_folder}")
    except Exception as e:
        print(f"An unexpected error occurred when copying folder: {e}")


def copy_file(source_file, destination_folder):
    try:

        if not os.path.isfile(source_file):
            logging.info(f"Could not find the file: {source_file}")
        if not os.path.exists(destination_folder):
            os.makedirs(destination_folder)
        shutil.copy(source_file, destination_folder)
        print(f"Successfully copied {source_file} to {destination_folder}")

    except FileNotFoundError as e:
        logging.info(f"Could not find the file: {source_file}")
    except Exception as e:
        logging.warning(f"An unexpected error occurred when copying file: {e}")


@app.post("/trigger_bt")
async def trigger_function(request: Request):
    body = await request.json()

    task = body.get("task")
    url = body.get("url")
    add_infos = body.get("add_infos")
    context = body.get("gbc")

    # Set the desired configuration values
    agent_type = "custom"
    llm_provider = "openai"
    llm_model_name = "gpt-4o"
    llm_temperature = 1.0
    llm_base_url = ""
    llm_api_key = ""
    use_own_browser = False
    keep_browser_open = True
    headless = False
    disable_security = False
    window_w = 1280
    window_h = 1100
    save_recording_path = "./tmp/record_videos"
    save_agent_history_path = "./tmp/agent_history"
    save_trace_path = "./tmp/traces"
    enable_recording = False
    max_steps = 100
    use_vision = True
    max_actions_per_step = 10
    tool_call_in_content = True

    # Run the agent
    result = await run_browser_agent(
        agent_type=agent_type,
        llm_provider=llm_provider,
        llm_model_name=llm_model_name,
        llm_temperature=llm_temperature,
        llm_base_url=llm_base_url,
        llm_api_key=llm_api_key,
        use_own_browser=use_own_browser,
        keep_browser_open=keep_browser_open,
        headless=headless,
        disable_security=disable_security,
        window_w=window_w,
        window_h=window_h,
        save_recording_path=save_recording_path,
        save_agent_history_path=save_agent_history_path,
        save_trace_path=save_trace_path,
        enable_recording=enable_recording,
        task=task,
        add_infos=add_infos,
        max_steps=max_steps,
        use_vision=use_vision,
        max_actions_per_step=max_actions_per_step,
        tool_call_in_content=tool_call_in_content,
        gbc=context
    )

    final_result, errors, model_actions, model_thoughts, latest_video, trace_file, history_file, sc, final_dom, _, _ = result

    output_file = f"logs/filtered_mitmproxy_endpoint_log_{final_dom}.jsonl"
    try:
        input_file = "logs/mitmproxy_endpoint_log.jsonl"
        filter_jsonl_file(input_file, output_file, url)
    except Exception as e:
        print(f"Error filtering logs: {e}")

    copy_folder("/app/logs", "/shared")
    copy_folder("/app/Downloads", "/shared")


    return {
        "final_result": final_result,
        "errors": errors,
        "model_actions": model_actions,
        "sc": sc,
        "mitm_logfile": output_file if os.path.exists(output_file) else None,
        "dom_file": f"final_dom_{final_dom}.html",
        "external_js_dom_file": f"external_js_dom_{final_dom}.txt",
    }
