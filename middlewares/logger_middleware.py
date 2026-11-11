"""
Logger Middleware
Logs incoming HTTP requests and responses to the terminal in the format:
time HH:MM:SS  method METHOD  route /path  res. type STATUS  duration Xms
"""
import time
import os
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOGS_DIR = os.path.join(BASE_DIR, "logs")
ERROR_LOG_PATH = os.path.join(LOGS_DIR, "error.log")


class LoggerMiddleware:
    """
    Middleware that captures request start time and formats request/response lifecycle metrics.
    Also logs 4xx and 5xx client/server errors to logs/error.log.
    """

    @staticmethod
    def start_timer() -> float:
        """Starts timing request processing in fractional seconds (high-precision)."""
        return time.perf_counter()

    @staticmethod
    def log(method: str, path: str, status_code: int, start_time: float) -> str:
        """
        Calculates elapsed duration and logs formatted output to terminal stdout.
        If status code >= 400, also logs to logs/error.log.
        Example output:
            time 10:20:30  method POST  route /user    res. type 201    duration 18ms
        """
        now_dt = datetime.now()
        now_time = now_dt.strftime("%H:%M:%S")
        elapsed_ms = round((time.perf_counter() - start_time) * 1000)

        log_line = (
            f"time {now_time}  "
            f"method {method.upper():<6}  "
            f"route {path:<20}  "
            f"res. type {status_code:<5}  "
            f"duration {elapsed_ms}ms"
        )
        print(log_line, flush=True)

        # Log errors (4xx and 5xx) to logs/error.log
        if status_code >= 400:
            try:
                os.makedirs(LOGS_DIR, exist_ok=True)
                with open(ERROR_LOG_PATH, "a", encoding="utf-8") as f:
                    f.write(f"[{now_dt.strftime('%Y-%m-%d %H:%M:%S')}] {log_line}\n")
            except Exception:
                pass

        return log_line
