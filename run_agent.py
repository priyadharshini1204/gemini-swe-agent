# run_agent.py

from google import genai
from google.genai import types


def main():
    client = genai.Client()

    # No automatic_function_calling at all
    config = types.GenerateContentConfig()

    response = client.models.generate_content(
        model="gemini-1.5-pro",
        contents="Explain Artificial Intelligence in very simple words",
        config=config
    )

    print(response.text)


if __name__ == "__main__":
    main()
