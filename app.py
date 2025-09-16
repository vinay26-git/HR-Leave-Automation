import sys
import os
import subprocess
import json
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

SCRIPTS = {
    "daily": r"C:\Users\jejja\OneDrive\Desktop\project\HR Automation\Daily Approvals",
    "monthly": r"C:\Users\jejja\OneDrive\Desktop\project\HR Automation\Monthly Summary"
}

pending_requests = []
PYTHON_PATH = sys.executable  # use current python interpreter

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/run', methods=['POST'])
def run_script():
    script_name = request.form.get('script')
    folder = SCRIPTS.get(script_name)
    if not folder:
        return jsonify({"error": "Invalid script name"})

    try:
        if script_name == 'daily':
            result = subprocess.run(
                [PYTHON_PATH, "main.py", "fetch"],
                cwd=folder,
                capture_output=True,
                text=True,
                encoding="utf-8",
                env=os.environ
            )

            # Debug
            print("STDOUT:", result.stdout)
            print("STDERR:", result.stderr)

            stdout = result.stdout.strip()
            try:
                pending = json.loads(stdout) if stdout else []
            except json.JSONDecodeError:
                pending = []

            global pending_requests
            pending_requests = pending if isinstance(pending, list) else []
            return jsonify(pending_requests)

        elif script_name == 'monthly':
            result = subprocess.run(
                [PYTHON_PATH, "main.py", "monthly"],
                cwd=folder,
                capture_output=True,
                text=True,
                encoding="utf-8",
                env=os.environ
            )
            return jsonify({"output": result.stdout.strip()})

    except Exception as e:
        return jsonify({"error": str(e)})

@app.route('/decision', methods=['POST'])
def decision():
    name = request.form.get('name')
    action = request.form.get('decision')
    folder = SCRIPTS['daily']
    try:
        subprocess.run(
            [PYTHON_PATH, "main.py", "decision", name, action],
            cwd=folder,
            text=True,
            encoding="utf-8",
            env=os.environ
        )
        global pending_requests
        pending_requests = [r for r in pending_requests if r.get('employee') != name]
        return jsonify({"message": f"{action.upper()} recorded for {name}"})
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    print("Starting Flask server at http://127.0.0.1:5000")
    app.run(debug=True)
