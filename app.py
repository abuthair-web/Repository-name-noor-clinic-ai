import os
import json
import streamlit as st
from google import genai

st.set_page_config(
    page_title="NoorCare AI",
    page_icon="🏥"
)

# Get API key
api_key = os.environ.get("GEMINI_API_KEY")

if not api_key:
    st.error("GEMINI_API_KEY was not found.")
    st.stop()


# Load knowledge base once
with open("clinic_knowledge.json", "r", encoding="utf-8") as file:
    clinic_data = json.load(file)

knowledge_base = json.dumps(clinic_data, indent=2)


system_prompt = f"""
You are NoorCare, the AI assistant for CarePlus Multispeciality Clinic.

Answer ONLY using the clinic knowledge base below.

Rules:
- Never invent information.
- If information is unavailable, say:
  "I'm sorry, I don't have that information. Please contact the clinic directly."
- Be polite and concise.
- Do not diagnose medical conditions.
- Do not prescribe medicines.
- For emergencies, advise the user to seek immediate emergency medical care.

CLINIC KNOWLEDGE BASE:
{knowledge_base}
"""


# Keep the Gemini client alive between Streamlit reruns
@st.cache_resource
def get_client():
    return genai.Client(api_key=api_key)


client = get_client()


# Create chat once per browser session
if "chat" not in st.session_state:
    st.session_state.chat = client.chats.create(
        model="gemini-3.6-flash",
        config={
            "system_instruction": system_prompt
        }
    )


if "messages" not in st.session_state:
    st.session_state.messages = []


st.title("🏥 NoorCare")
st.caption("Your Smart Clinic Assistant")


# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# Chat input
user_question = st.chat_input(
    "Ask NoorCare about the clinic..."
)


if user_question:

    # Display user message
    st.session_state.messages.append({
        "role": "user",
        "content": user_question
    })

    with st.chat_message("user"):
        st.markdown(user_question)

    # Generate response
    with st.chat_message("assistant"):

        with st.spinner("NoorCare is thinking..."):

            response = st.session_state.chat.send_message(
                message=user_question
            )

        st.markdown(response.text)

    # Save response
    st.session_state.messages.append({
        "role": "assistant",
        "content": response.text
    })