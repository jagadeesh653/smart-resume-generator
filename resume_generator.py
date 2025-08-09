import streamlit as st
import google.generativeai as genai

# ---------------- Configuration ----------------
#api_key = "YOUR_API_KEY"  # 🔐 Replace with your API key
api_key = st.secrets["GEMINI_API_KEY"]
genai.configure(api_key=api_key)

generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 1024,
    "response_mime_type": "text/plain"
}

# ---------------- Resume Generator Function ----------------
def generate_resume(name, job_title):
    context = f"""
    Generate a professional resume for a person named {name}, targeting a role as a {job_title}.
    Include a summary, skills, dummy professional experience, projects, and education.
    Use markdown formatting and placeholders for: 
    - [Your Email Address]
    - [Your Phone Number]
    - [Your LinkedIn URL (optional)]
    - [Your University Name]
    - [Your Graduation Year]
    """

    model = genai.GenerativeModel("gemini-pro", generation_config=generation_config)
    chat = model.start_chat(history=[])
    response = chat.send_message(context)

    if isinstance(response.text, str):
        text = response.text
    else:
        text = response.parts[0].text

    return clean_resume_text(text)

# ---------------- Clean Placeholders ----------------
def clean_resume_text(text):
    text = text.replace("[Add Email Address]", "[Your Email Address]")
    text = text.replace("[Add Phone Number]", "[Your Phone Number]")
    text = text.replace("[Add LinkedIn Profile URL (optional)]", "[Your LinkedIn URL (optional)]")
    text = text.replace("[University Name]", "[Your University Name]")
    text = text.replace("[Graduation Year]", "[Your Graduation Year]")
    return text

# ---------------- Streamlit UI ----------------
st.set_page_config(page_title="SmartResume Generator", layout="centered")
st.title("📄 SmartResume Generator")
st.write("Create a custom resume using AI in just seconds.")

name = st.text_input("Enter your name")
job_title = st.text_input("Enter your job title")

if st.button("Generate Resume"):
    if name and job_title:
        with st.spinner("Generating your resume..."):
            resume_text = generate_resume(name, job_title)
            st.markdown("### ✨ Your AI-Generated Resume:")
            st.markdown(resume_text)
    else:
        st.warning("Please enter both name and job title.")
