# run_agent.py
# Compatible with Python 3.12 and Pydantic v2

from google.generativeai import types
import google.generativeai as genai
import os


def main():
    # Set API key (use environment variable)
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

    # ✅ CORRECT CONFIG (NO BOOLEAN ERROR)
    config = types.GenerateContentConfig(
        temperature=0.7,
        top_p=0.95,
        max_output_tokens=2048,
        automatic_function_calling={
            "enabled": True
        }
    )

    model = genai.GenerativeModel(
        model_name="models/gemini-1.5-pro",
        generation_config=config
    )

    response = model.generate_content(
        "Explain Artificial Intelligence in simple words"
    )

    print(response.text)


if __name__ == "__main__":
    main()

