import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
import os
from dotenv import load_dotenv

# 1. Load Environment Variables
load_dotenv()  # This loads the variables from .env

st.set_page_config(page_title="AI Clone Demo", page_icon="🤖")

# 2. Configuration & Key Handling
# Try to get key from .env first
api_key = os.getenv("GOOGLE_API_KEY")

# If not in .env (e.g., for a user testing it live), allow manual entry
if not api_key:
    with st.sidebar:
        st.header("Setup")
        api_key = st.text_input("Enter Google API Key", type="password")
        st.caption("Key not found in .env file.")

# 3. Load Knowledge Base
def load_knowledge():
    try:
        with open("knowledge.txt", "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return "Error: knowledge.txt not found."

context_text = load_knowledge()

# 4. The Logic
st.title("Ask the AI Clone 💬")
st.write("I answer based ONLY on the influencer's past posts.")

user_question = st.text_input("What do you want to ask?")

if user_question:
    if not api_key:
        st.warning("⚠️ No API Key found. Please add it to .env or the sidebar.")
        st.stop()

    # Initialize Gemini
    try:
        llm = ChatGoogleGenerativeAI(model="gemini-pro", google_api_key=api_key)
        

        # The Strict Prompt
        template = """
        You are an AI clone of a specific Instagram Influencer.
        Use the following context (their past posts) to answer the user's question.
        
        RULES:
        1. Answer exactly in the tone of the context.
        2. If the answer is NOT in the context, say: "I haven't posted about that yet! DM me if you want me to cover it."
        3. Keep answers short and punchy (Instagram style).

        CONTEXT:
        {context}

        USER QUESTION:
        {question}
        """
        
        prompt = PromptTemplate(template=template, input_variables=["context", "question"])
        chain = prompt | llm
        
        with st.spinner("Thinking..."):
            response = chain.invoke({"context": context_text, "question": user_question})
            st.write(response.content)

    except Exception as e:
        st.error(f"An error occurred: {e}")