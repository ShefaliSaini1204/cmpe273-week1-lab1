from flask import Flask, request, jsonify
import time
import logging
import requests

app = Flask(__name__)

# --- Safe logger: prevents crashes when Werkzeug logs without extra fields ---
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
# --------------------------------------------------------------------------

SERVICE_NAME = "service-b"
SERVICE_A_URL = "http://127.0.0.1:8080"
TIMEOUT_SECONDS = 0.5  # required timeout

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

@app.get("/call-echo")
def call_echo():
    start = time.time()
    msg = request.args.get("msg", "")

    try:
        resp = requests.get(
            f"{SERVICE_A_URL}/echo",
            params={"msg": msg},
            timeout=TIMEOUT_SECONDS,
        )
        resp.raise_for_status()

        log_request("/call-echo", 200, start, f"called service-a msg={msg}")
        return jsonify({
            "service_b": "ok",
            "service_a_response": resp.json()
        }), 200

    except requests.exceptions.Timeout:
        log_request("/call-echo", 503, start, "timeout calling service-a")
        return jsonify({"error": "service-a timeout"}), 503

    except requests.exceptions.RequestException as e:
        log_request("/call-echo", 503, start, f"service-a unavailable: {e}")
        return jsonify({"error": "service-a unavailable"}), 503

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8081)

