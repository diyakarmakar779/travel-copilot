import os
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()

client = Anthropic(
    api_key=os.getenv("ANTHROPIC_API_KEY")
)

def call_llm(user_input: str, mode="decision"):
    
    if mode == "decision":
        system_prompt = """
        You are a travel AI assistant.

        You have tools:
        - itinerary(destination, days)
        - captions(destination)
        - reels(destination)

        RULES:
        - Choose ONLY necessary tools
        - Return ONLY JSON
        - No explanation
        - Output must start with [ and end with ]

        Example:
        [
          {
            "tool": "captions",
            "args": { "destination": "Goa" }
          }
        ]
        """

    else:  
        system_prompt = """
        You are a helpful travel assistant.

        Your job:
        - Take tool results
        - Convert into a clean, human-friendly response
        - DO NOT return JSON
        - DO NOT mention tools
        """

    response = client.messages.create(
        model="claude-3-haiku-20240307",
        max_tokens=800,
        system=system_prompt,
        messages=[
            {
                "role": "user",
                "content": [{"type": "text", "text": user_input}]
            }
        ]
    )

    return response.content[0].text