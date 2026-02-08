import json
import os

def main():
    resolved = False
    if os.path.exists("post_verification.log"):
        with open("post_verification.log", "r") as f:
            if " 1 passed" in f.read():
                resolved = True

    metrics = {
        "resolved": resolved,
        "duration_seconds": 0,
        "total_cost_usd": 0,
        "tokens": {"input": 0, "output": 0},
        "tool_usage": {"read": 0, "write": 0, "bash": 0}
    }

    if os.path.exists("agent.log"):
        with open("agent.log", "r") as f:
            for line in f:
                data = json.loads(line)
                if "usage" in data:
                    metrics["tokens"]["input"] += data["usage"]["prompt_tokens"]
                    metrics["tokens"]["output"] += data["usage"]["candidates_tokens"]
                # Add logic here to count specific tool usage from logs

    with open("result.json", "w") as f:
        json.dump(metrics, f, indent=2)

if __name__ == "__main__":
    main()
