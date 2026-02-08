# run_agent.py
# Stable version for Python 3.12 + GitHub Actions

import os
import google.generativeai as genai


def main():
    api_key = os.getenv("GOOGLE_API_KEY")

    if not api_key:
        raise ValueError("GOOGLE_API_KEY not found in environment variables")

    genai.configure(api_key=api_key)

    model = genai.GenerativeModel(
        model_name="models/gemini-1.5-pro"
    )

    response = model.generate_content(
        "Explain Artificial Intelligence in simple words"
    )

    print("===== Gemini Output =====")
    print(response.text)


if __name__ == "__main__":
    main()
