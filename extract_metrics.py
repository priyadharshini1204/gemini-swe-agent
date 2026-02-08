import json
import os

def main():
    resolved = False
    # Check if post-verification passed
    if os.path.exists("post_verification.log"):
        with open("post_verification.log", "r") as f:
            content = f.read()
            if " 1 passed" in content or "PASSED" in content.upper():
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
                try:
                    data = json.loads(line)
                    if data.get("type") == "response" and "usage" in data:
                        metrics["tokens"]["input"] += data["usage"].get("input_tokens", 0)
                        metrics["tokens"]["output"] += data["usage"].get("output_tokens", 0)
                except: continue

    # Calculate approximate cost for Gemini 3 Flash ($0.50/1M in, $3.00/1M out)
    metrics["total_cost_usd"] = (metrics["tokens"]["input"] * 0.0000005) + (metrics["tokens"]["output"] * 0.000003)

    with open("result.json", "w") as f:
        json.dump(metrics, f, indent=2)

if __name__ == "__main__":
    main()
