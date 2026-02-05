from flask import Flask, request, jsonify
import time
import logging

app = Flask(__name__)

class SafeExtraFormatter(logging.Formatter):
    def format(self, record):
        if not hasattr(record, "service"):
            record.service = "-"
        if not hasattr(record, "endpoint"):
            record.endpoint = "-"
        if not hasattr(record, "status"):
            record.status = "-"
        if not hasattr(record, "latency_ms"):
            record.latency_ms = "-"
        return super().format(record)

handler = logging.StreamHandler()
handler.setFormatter(
    SafeExtraFormatter(
        "%(asctime)s %(levelname)s service=%(service)s endpoint=%(endpoint)s status=%(status)s latency_ms=%(latency_ms)s msg=%(message)s"
    )
)

root = logging.getLogger()
root.setLevel(logging.INFO)
root.handlers = [handler]

SERVICE_NAME = "service-a"

def log_request(endpoint, status, start, message=""):
    latency_ms = int((time.time() - start) * 1000)
    logging.info(
        message,
        extra={
            "service": SERVICE_NAME,
            "endpoint": endpoint,
            "status": status,
            "latency_ms": latency_ms,
        },
    )

@app.get("/health")
def health():
    start = time.time()
    log_request("/health", 200, start, "health ok")
    return jsonify({"status": "ok"}), 200

@app.get("/echo")
def echo():
    start = time.time()
    msg = request.args.get("msg", "")
    log_request("/echo", 200, start, f"echo msg={msg}")
    return jsonify({"echo": msg}), 200

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080)

