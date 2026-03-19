
from ai_client import call_llm

query = input("Ask Travel Copilot: ")

response = call_llm(query)

print("\n--- AI RESPONSE ---")
print(response)