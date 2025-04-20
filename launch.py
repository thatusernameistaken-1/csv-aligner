# launch.py
import sys, subprocess, os

# point to your real Streamlit script
SCRIPT = os.path.join(os.path.dirname(__file__), "app.py")

# run Streamlit
subprocess.call([sys.executable, "-m", "streamlit", "run", SCRIPT])