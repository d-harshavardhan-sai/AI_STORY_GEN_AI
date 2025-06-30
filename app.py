import os
import streamlit as st
from huggingface_hub import InferenceClient

# Set HuggingFace token
HF_TOKEN = st.secrets["HF_TOKEN"]

client = InferenceClient(api_key=HF_TOKEN)

def generate_story(prompt):
    system_message = "You are a creative writing assistant."
    user_message = f"Write a short, imaginative story based on this prompt: {prompt}"
    messages = [
        {"role": "system", "content": system_message},
        {"role": "user", "content": user_message}
    ]
    response = client.chat.completions.create(
        model="meta-llama/Meta-Llama-3.1-8B-Instruct",
        messages=messages,
        max_tokens=512,
        temperature=0.8,
    )
    return response.choices[0].message.content.strip()

# Streamlit UI
st.set_page_config(page_title="AI Story Generator", layout="centered")
st.title("📚 AI Story Generator from Prompts")
st.markdown("Enter a creative prompt and let AI write a story for you!")

prompt = st.text_area("✍️ Enter your story prompt:", height=150)

if st.button("🚀 Generate Story"):
    if not prompt.strip():
        st.warning("⚠️ Please enter a story prompt.")
    else:
        with st.spinner("🧠 Generating..."):
            try:
                story = generate_story(prompt)
                st.success("🎉 Here's your story:")
                st.write(story)
            except Exception as e:
                st.error(f"❌ Error: {e}")
