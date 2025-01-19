# app.py
from fastapi import FastAPI, Request
from webui import run_browser_agent
from filter_mitm_logs import filter_jsonl_file
app = FastAPI()


@app.post("/trigger_bt")
async def trigger_function(request: Request):
    body = await request.json()

    task = body.get("task")
    url = body.get("url")
    add_infos = body.get("add_infos")

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
    disable_security = True
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
        tool_call_in_content=tool_call_in_content
    )

    final_result, errors, model_actions, model_thoughts, latest_video, trace_file, history_file, _, _ = result

    try:
        input_file = "logs/mitmproxy_endpoint_log.jsonl"
        output_file = "logs/filtered_mitmproxy_endpoint_log.jsonl"
        filter_jsonl_file(input_file, output_file, url)
    except Exception as e:
        print(f"Error filtering logs: {e}")


    return {
        "final_result": final_result,
        "errors": errors,
        "model_actions": model_actions,
        #"sc_name": screenshot,
    }
