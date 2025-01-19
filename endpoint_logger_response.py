from mitmproxy import http
from datetime import datetime
import json
import os
import time
import base64

class EndpointLogger:
    def __init__(self):
        # Specify a proper log file path
        log_dir = "/app/logs"
        os.makedirs(log_dir, exist_ok=True)  # Create logs directory if it doesn't exist
        self.log_file = os.path.join(log_dir, "mitmproxy_endpoint_log.jsonl")
        print(f"Log file path: {self.log_file}")
        self.requests_log = {}
        self.blacklist = ["google", "facebook", "twitter", "linkedin", "r10", "r11", "firefox", "mozilla", "chrome"]

    def is_blacklisted(self, url: str) -> bool:
        return any(blacklist_item in url for blacklist_item in self.blacklist)

    def request(self, flow: http.HTTPFlow) -> None:
        request = flow.request
        if self.is_blacklisted(request.url):
            print(f"Skipped blacklisted request: {request.url}")
            return
        print(f"Processing request: {flow.request.url}")

        body_text = base64.b64encode(request.content).decode('utf-8') if request.content else None

        log_entry = {
            "event": "request",
            "method": request.method,
            "url": request.url,
            "path": request.path,
            "host": request.host,
            "port": request.port,
            "query": dict(request.query),
            "headers": dict(request.headers),
            "body": body_text,
            "timestamp": int(time.time())
        }

        # Store the request by its unique flow ID (this helps with pairing later)
        self.requests_log[flow.id] = request.url

        if request.url:
            try:
                print("Attempting to write request log...")
                with open(self.log_file, "a") as f:
                    json.dump(log_entry, f)
                    f.write("\n")
                    f.flush()  # Force immediate write
                print("Request log written successfully.")
            except Exception as e:
                print(f"Error writing request log: {e}")

    def response(self, flow: http.HTTPFlow) -> None:
        response = flow.response
        url = self.requests_log.pop(flow.id, None)
        if url and self.is_blacklisted(url):
            print(f"Skipped blacklisted request: {url}")
            return
        print(f"Processing response: {flow.response.status_code}")

        body_text = base64.b64encode(response.content).decode('utf-8') if response.content else None
        log_entry = {
            "event": "response",
            "url": url,
            "cookies": dict(response.cookies),
            "status_code": response.status_code,
            "headers": dict(response.headers),
            "body": body_text,
            "timestamp": int(time.time())
        }

        if url:
            try:
                print("Attempting to write response log...")
                with open(self.log_file, "a") as f:
                    json.dump(log_entry, f)
                    f.write("\n")
                    f.flush()  # Force immediate write
            except Exception as e:
                print(f"Error writing response log: {e}")

addons = [
    EndpointLogger()
]
