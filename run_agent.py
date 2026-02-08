import os
import json
import subprocess
from datetime import datetime
from google import genai
from google.genai import types

# 1. Initialize the new Client
# The client automatically picks up GEMINI_API_KEY from environment
client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

def log_action(data):
    with open("agent.log", "a") as f:
        data["timestamp"] = datetime.now().isoformat()
        f.write(json.dumps(data) + "\n")

# --- Tool Definitions (Annotated for Auto-Function Calling) ---
def read_file(path: str) -> str:
    """Reads a file from the filesystem. Use this to examine code."""
    try:
        with open(path, 'r') as f: return f.read()
    except Exception as e: return str(e)

def write_file(path: str, content: str) -> str:
    """Writes or overwrites a file. Use this to apply fixes."""
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'w') as f: f.write(content)
        return f"Successfully wrote to {path}"
    except Exception as e: return str(e)

def run_bash(command: str) -> str:
    """Executes a bash command in the /testbed directory. Use this to run tests."""
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, cwd="/testbed")
        return f"STDOUT: {result.stdout}\nSTDERR: {result.stderr}"
    except Exception as e: return str(e)

def main():
    # Use the latest high-capability model
    MODEL_ID = "gemini-2.5-pro" 
    
    instruction = (
        "Improve ISBN import logic in OpenLibrary. "
        "Use local staged records instead of external API calls. "
        "Test file: openlibrary/tests/core/test_imports.py"
    )

    # Automatic Tool Calling setup
    # Note: tools are passed as a list of functions
    config = types.GenerateContentConfig(
        tools=[read_file, write_file, run_bash],
        automatic_function_calling=True,
        system_instruction="You are a senior software engineer. Fix the provided issue using the tools."
    )

    log_action({"type": "request", "content": instruction})

    # Start the agent loop
    response = client.models.generate_content(
        model=MODEL_ID,
        contents=instruction,
        config=config
    )

    # Log the final outcome
    log_action({
        "type": "response",
        "content": response.text,
        "usage": {
            "input_tokens": response.usage_metadata.prompt_token_count,
            "output_tokens": response.usage_metadata.candidates_token_count
        }
    })
    
    print(f"Agent Task Finished. Summary: {response.text[:100]}...")

if __name__ == "__main__":
    main()
