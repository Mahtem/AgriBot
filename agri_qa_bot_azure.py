import streamlit as st
import json
import os
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential

# --- Streamlit title ---
st.title("🌱 Agriculture Q&A Bot with Key Phrases")
# Dataset acknowledgment
st.markdown(
    """
    ---
    ℹ️ **Dataset Acknowledgment:** This bot uses the Agriculture Q&A dataset by 
    [Mahesh2841 on Hugging Face](https://huggingface.co/datasets/Mahesh2841/Agriculture).  
    All credit goes to the original data creator.
    ---
    """,
    unsafe_allow_html=True
)
st.write("Ask a question about crops, pests, or fertilizers:")

# --- Azure setup ---

key = os.getenv("AZURE_KEY")
endpoint = os.getenv("AZURE_ENDPOINT")

client = TextAnalyticsClient(endpoint=endpoint, credential=AzureKeyCredential(key))

# Get the path relative to this script
current_dir = os.path.dirname(__file__)
qa_file_path = os.path.join(current_dir, "agri_qa.json")

# Open the JSON file
with open(qa_file_path, "r", encoding="utf-8") as f:
    qa_pairs = json.load(f)

# --- User input ---
user_question = st.text_input("Your question here:")

if user_question:
    question_words = user_question.lower().split()

    # Flexible keyword search
    matched_answers = []
    for entry in qa_pairs:
        entry_text = entry["user"].lower()
        if any(word in entry_text for word in question_words):
            matched_answers.append(entry["assistant"])

    if matched_answers:
        st.subheader("Answer(s):")
        # Show top 3 answers
        for i, answer in enumerate(matched_answers[:3], 1):
            st.write(f"{i}. {answer}")

            # Extract key phrases using Azure
            try:
                keyphrase_result = client.extract_key_phrases([answer])[0]
                st.write("Key Phrases:", keyphrase_result.key_phrases)
            except Exception as e:
                st.write("Azure Key Phrase extraction failed:", e)
    else:
        st.write("Sorry, I don't have an answer for that question yet.")
# Add keys and endpoint
# Redeploy trigger - no code change
# "Update Azure key and endpoint with real values"
#