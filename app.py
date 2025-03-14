import streamlit as st
import google.generativeai as genai

# Configure the API key for the Gemini API
api_key = "AIzaSyDjBJ5AR_NaUBSnKRMo0wr7zVmvDI3C4mY"
genai.configure(api_key=api_key)

# Configure the model generation settings
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 1024,
    "response_mime_type": "text/plain",
}

# Create the generative model instance
def generate_resume(name, job_title):
    model = genai.GenerativeModel(
        model_name="gemini-1.5-pro",
        generation_config=generation_config,
    )
    
    # Construct context dynamically based on input
    context = f"name:{name}\njob_title:{job_title}\nwrite a resume on above data."
    
    # Start the chat session with the generative model
    chat_session = model.start_chat(
        history=[
            {
                "role": "user",
                "parts": [context],
            },
        ]
    )
    
    # Get the response from the model
    response = chat_session.send_message(context)
    
    # Extract and return the resume content
    text = response.candidates[0].content if isinstance(response.candidates[0].content, str) else response.candidates[0].content.parts[0].text
    return text

# Function to clean resume text
def clean_resume_text(text):
    cleaned_text = text.replace("[Add Email Address]", "[Your Email Address]")
    cleaned_text = cleaned_text.replace("[Add Phone Number]", "[Your Phone Number]")
    cleaned_text = cleaned_text.replace("[Add LinkedIn Profile URL (optional)]", "[Your LinkedIn URL (optional)]")
    cleaned_text = cleaned_text.replace("[University Name]", "[Your University Name]")
    cleaned_text = cleaned_text.replace("[Graduation Year]", "[Your Graduation Year]")
    return cleaned_text

# Streamlit UI for taking user inputs
st.title("Resume Generator")

# Textboxes for name and job title input
name = st.text_input("Enter your name")
job_title = st.text_input("Enter your job title")

# Submit button
if st.button("Generate Resume"):
    if name and job_title:
        resume = generate_resume(name, job_title)
        cleaned = clean_resume_text(resume)
        st.markdown("### Generated Resume")
        st.markdown(cleaned)
    else:
        st.warning("Please enter both your name and job title.")
