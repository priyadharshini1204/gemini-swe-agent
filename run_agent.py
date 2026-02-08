import os
import json
import time
import argparse
import subprocess
import google.generativeai as genai
from datetime import datetime

# Setup Gemini
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

def log_action(data):
    with open("agent.log", "a") as f:
        data["timestamp"] = datetime.now().isoformat()
        f.write(json.dumps(data) + "\n")

# --- Tool Definitions ---
def read_file(path: str):
    """Reads a file from the filesystem."""
    try:
        with open(path, 'r') as f: return f.read()
    except Exception as e: return str(e)

def write_file(path: str, content: str):
    """Writes or overwrites a file."""
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'w') as f: f.write(content)
        return f"Successfully wrote to {path}"
    except Exception as e: return str(e)

def run_bash(command: str):
    """Executes a bash command in the /testbed directory."""
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, cwd="/testbed")
        return f"STDOUT: {result.stdout}\nSTDERR: {result.stderr}"
    except Exception as e: return str(e)

tools = [read_file, write_file, run_bash]
model = genai.GenerativeModel('gemini-1.5-pro', tools=tools)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--task_id", required=True)
    args = parser.parse_args()

    # Task definition from task.yaml (simplified for prompt)
    instruction = (
        "Improve ISBN import logic in OpenLibrary. "
        "Use local staged records instead of external API calls. "
        "Test file: openlibrary/tests/core/test_imports.py"
    )
    
    with open("prompts.md", "w") as f: f.write(f"# System Prompt\nYou are an expert SWE.\n\n# Task\n{instruction}")

    chat = model.start_chat(enable_automatic_function_calling=True)
    
    log_action({"type": "request", "content": instruction})
    response = chat.send_message(instruction)
    
    # Log usage
    log_action({
        "type": "response", 
        "content": response.text,
        "usage": {
            "prompt_tokens": response.usage_metadata.prompt_token_count,
            "candidates_tokens": response.usage_metadata.candidates_token_count
        }
    })

if __name__ == "__main__":
    main()
