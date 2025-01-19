import json
import logging
import os
from datetime import datetime
from urllib.parse import urlparse

# INPUT_FILE = "mitmproxy_endpoint_log.jsonl"
# OUTPUT_FILE = "filtered_mitmproxy_endpoint_log.jsonl"

logging.basicConfig(level=logging.INFO)


def extract_domain(url):
    try:
        parsed_url = urlparse(url)
        return parsed_url.netloc
    except Exception as e:
        logging.error(f"Error extracting domain: {e}")
        return None


def convert_date_to_unix(date_str):
    try:
        dt = datetime.strptime(date_str, "%a, %d %b %Y %H:%M:%S %Z")
        unix_timestamp = dt.timestamp()
        return int(unix_timestamp)
    except ValueError as e:
        print(f"Error converting date: {e}")
        return None


def clean_malformed_json(line):
    # Basic attempts to clean common issues
    try:
        # Fix unmatched brackets by trimming
        if line.count('{') > line.count('}'):
            line += '}'
        elif line.count('}') > line.count('{'):
            line = line.rstrip('}')

        # Remove trailing commas
        line = line.replace(",}", "}")
        line = line.replace(",]", "]")

        # Fix incomplete strings
        line = line.replace('":,', '":null,')  # Handle cases where value is missing after a key
    except Exception as e:
        print(f"Error during cleaning: {e}")
    return line


def filter_jsonl_file(input_file, output_file, url):
    try:

        if url:
            os.environ["SCOPE_URL"] = url
        else:
            url = os.environ.get("SCOPE_URL")

        dom = extract_domain(url)

        logging.info(f"Dom extracted from file-{dom}")

        if not dom:
            return

        os.makedirs(os.path.dirname(output_file), exist_ok=True) #Ensure output file exists
        line_number = 1

        with open(input_file, "r", encoding="utf-8") as infile, open(output_file, "w", encoding="utf-8") as outfile:
            for line in infile:
                try:
                    try:
                        record = json.loads(line)
                    except json.JSONDecodeError:
                        logging.error(f"Skipping line {line_number}: Invalid JSON format. Retrying")
                        try:
                            cleaned_line = clean_malformed_json(line)
                            record = json.loads(cleaned_line)
                        except json.JSONDecodeError:
                            logging.error(f"Skipping line {line_number}: Invalid JSON format after cleaning. Skipping.")
                            line_number += 1
                            continue
                    if not record.get("url"):
                        line_number += 1
                        continue

                    if "url" in record and dom == extract_domain(record["url"]):
                        outfile.write(json.dumps(record) + "\n")
                        line_number += 1
                        continue

                    if record.get("event") == "response" and "headers" in record:
                        headers = record["headers"]
                        if "Referer" in headers and dom in headers["Referer"]:
                            outfile.write(json.dumps(record) + "\n")
                        elif "Origin" in headers and dom in headers["Origin"]:
                            outfile.write(json.dumps(record) + "\n")
                        elif "Host" in headers and dom in headers["Host"]:
                            outfile.write(json.dumps(record) + "\n")
                except KeyError as e:
                    logging.error(f"Skipping line: {e}")

        logging.info(f"Filtered output written to: {output_file}")
    except FileNotFoundError:
        logging.error(f"Error: The file {input_file} was not found.")
        return None

    except IOError as e:
        logging.error(f"Error reading/writing files: {e}")
        return None

if __name__ == "__main__":
    URL = "https://shinobi.security"
    # filter_jsonl_file(INPUT_FILE, OUTPUT_FILE, URL)
