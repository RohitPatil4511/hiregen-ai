import subprocess
import threading
import time
import os

def run_fastapi():
    subprocess.run([
        "uvicorn", "backend.main:app",
        "--host", "0.0.0.0", "--port", "8000"
    ])

# Start FastAPI in a background thread
fastapi_thread = threading.Thread(target=run_fastapi, daemon=True)
fastapi_thread.start()

# Give FastAPI a moment to start
time.sleep(3)

# Start Streamlit in the foreground (this is what HF Spaces shows)
os.system(
    "streamlit run frontend/app.py "
    "--server.port 7860 "
    "--server.address 0.0.0.0 "
    "--server.enableXsrfProtection false"
)

