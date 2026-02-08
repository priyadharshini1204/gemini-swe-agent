import os
import json
import subprocess
from datetime import datetime
from google import genai
from google.genai import types

# Initialize Client
client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

def log_action(data):
    with open("agent.log", "a") as f:
        data["timestamp"] = datetime.now().isoformat()
        f.write(json.dumps(data) + "\n")

# Tools for the Agent
def read_file(path: str) -> str:
    """Reads a file. Use this to examine the OpenLibrary codebase."""
    try:
        with open(path, 'r') as f: return f.read()
    except Exception as e: return str(e)

def write_file(path: str, content: str) -> str:
    """Writes a file. Use this to apply your ISBN logic fix."""
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'w') as f: f.write(content)
        return f"Successfully wrote to {path}"
    except Exception as e: return str(e)

def run_bash(command: str) -> str:
    """Executes bash. Use this to run the pre/post verification tests."""
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, cwd="/testbed")
        return f"STDOUT: {result.stdout}\nSTDERR: {result.stderr}"
    except Exception as e: return str(e)

def main():
    # MUST USE gemini-3-flash-preview TO AVOID 404
    MODEL_ID = "gemini-3-flash-preview" 
    
    instruction = (
        "TASK: Improve ISBN import logic in OpenLibrary. "
        "Logic: Use local staged records instead of external API calls. "
        "Test location: openlibrary/tests/core/test_imports.py. "
        "Start by reading that test file to understand the requirement."
    )

    # Configuration for the 3-series Agentic Workflow
    config = types.GenerateContentConfig(
        tools=[read_file, write_file, run_bash],
        automatic_function_calling=True,
        system_instruction="You are an expert SWE Agent. Use tools to fix the ISBN logic issue."
    )

    log_action({"type": "request", "content": instruction})

    # Execute the agentic loop
    response = client.models.generate_content(
        model=MODEL_ID,
        contents=instruction,
        config=config
    )

    log_action({
        "type": "response",
        "content": response.text,
        "usage": {
            "input_tokens": response.usage_metadata.prompt_token_count,
            "output_tokens": response.usage_metadata.candidates_token_count
        }
    })
    
    print(f"Agent Task Finished successfully with {MODEL_ID}")

if __name__ == "__main__":
    main()
