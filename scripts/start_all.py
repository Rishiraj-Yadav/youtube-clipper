import os
import signal
import subprocess
import sys
import time


PROCESSES: list[subprocess.Popen] = []


def _start(cmd: list[str], env: dict[str, str]) -> subprocess.Popen:
    return subprocess.Popen(cmd, env=env)


def _terminate_all() -> None:
    for proc in PROCESSES:
        if proc.poll() is None:
            proc.terminate()

    deadline = time.time() + 10
    while time.time() < deadline:
        if all(proc.poll() is not None for proc in PROCESSES):
            return
        time.sleep(0.2)

    for proc in PROCESSES:
        if proc.poll() is None:
            proc.kill()


def _handle_signal(signum, frame):
    _terminate_all()
    sys.exit(0)


def main() -> int:
    env = os.environ.copy()

    # Public port used by platforms like Render; frontend should bind here.
    frontend_port = int(env.get("PORT", "8501"))
    backend_port = int(env.get("BACKEND_PORT", "8000"))
    worker_port = int(env.get("WORKER_PORT", "8001"))

    # Prevent accidental port collisions.
    if backend_port == frontend_port:
        backend_port = frontend_port + 1
    if worker_port in {frontend_port, backend_port}:
        worker_port = max(frontend_port, backend_port) + 1

    # In all-in-one mode frontend must call backend over internal localhost,
    # regardless of external env values configured on the platform.
    env["API_BASE_URL"] = f"http://127.0.0.1:{backend_port}/api/v1"

    signal.signal(signal.SIGINT, _handle_signal)
    signal.signal(signal.SIGTERM, _handle_signal)

    backend_cmd = [
        sys.executable,
        "-m",
        "uvicorn",
        "backend.app.main:app",
        "--host",
        "0.0.0.0",
        "--port",
        str(backend_port),
    ]

    worker_cmd = [
        sys.executable,
        "-m",
        "uvicorn",
        "worker.web:app",
        "--host",
        "0.0.0.0",
        "--port",
        str(worker_port),
    ]

    frontend_cmd = [
        sys.executable,
        "-m",
        "streamlit",
        "run",
        "frontend/app.py",
        "--server.address",
        "0.0.0.0",
        "--server.port",
        str(frontend_port),
    ]

    PROCESSES.append(_start(backend_cmd, env))
    PROCESSES.append(_start(worker_cmd, env))
    PROCESSES.append(_start(frontend_cmd, env))

    try:
        while True:
            for proc in PROCESSES:
                code = proc.poll()
                if code is not None:
                    _terminate_all()
                    return code
            time.sleep(1)
    except KeyboardInterrupt:
        _terminate_all()
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
