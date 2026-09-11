import os
import json
from google import genai

api_key = os.environ.get("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY was not found.")

client = genai.Client(api_key=api_key)

with open("clinic_knowledge.json", "r", encoding="utf-8") as file:
    clinic_data = json.load(file)

knowledge_base = json.dumps(clinic_data, indent=2)

system_prompt = f"""
You are NoorCare, the AI assistant for CarePlus Multispeciality Clinic.

Your job is to help patients with questions about the clinic.

IMPORTANT RULES:
1. Answer using ONLY the information provided in the clinic knowledge base.
2. Do not invent or assume information.
3. If the requested information is not available, say:
   "I'm sorry, I don't have that information. Please contact the clinic directly."
4. Be polite, clear and concise.
5. Do not diagnose medical conditions or prescribe medicines.
6. For emergencies, advise the user to seek immediate emergency medical care.

CLINIC KNOWLEDGE BASE:
{knowledge_base}
"""

chat = client.chats.create(
    model="gemini-3.6-flash",
    config={
        "system_instruction": system_prompt
    }
)

print("\n================================")
print("        NoorCare AI Assistant")
print("================================")
print("Type 'exit' to close the chatbot.\n")

while True:
    user_question = input("You: ")

    if user_question.lower() == "exit":
        print("NoorCare: Thank you for contacting CarePlus Clinic. Goodbye!")
        break

    if not user_question.strip():
        continue

    response = chat.send_message(
        message=user_question
    )

    print("\nNoorCare:", response.text)
    print()