import streamlit as st
import re
import os

def clean_and_combine_transcript(content, interviewer, interviewee):
    # Regex pattern to match lines like '1\n00:00:02.890 --> 00:00:07.700\n'
    pattern = re.compile(r'\d+\n\d{2}:\d{2}:\d{2}\.\d{3} --> \d{2}:\d{2}:\d{2}\.\d{3}\n')
    # Remove timestamps and response numbers
    cleaned_content = re.sub(pattern, '', content)

    # Split the cleaned content into lines
    lines = cleaned_content.split('\n')

    # Initialize variables to store responses
    combined_responses = []
    current_response = []

    for line in lines:
        if line.startswith(interviewer):
            # When an interviewer's response is found, save the current response of the interviewee
            if current_response:
                combined_responses.append(f"{interviewee}: " + " ".join(current_response))
                current_response = []
            # Add the interviewer's response
            combined_responses.append(line)
        elif line.startswith(interviewee):
            # Collect the interviewee's response
            current_response.append(line[len(interviewee) + 2:].strip())
        else:
            # Append any non-empty lines to the current response
            if line.strip():
                current_response.append(line.strip())

    # Add the last collected response of the interviewee
    if current_response:
        combined_responses.append(f"{interviewee}: " + " ".join(current_response))

    # Combine all responses into a single string
    return '\n\n'.join(combined_responses)



st.set_page_config(page_title="Zoom Transcript Cleaner", page_icon=":pencil:", layout="centered")
st.title('Zoom Transcript Cleaner')

uploaded_file = st.file_uploader("Upload your VTT or TXT file", type=["vtt", "txt"])

if uploaded_file is not None:
    interviewer = st.text_input("Enter the interviewer's name (exactly as it appears in the transcript)", "Anoushka Jagadeesh Puranik (RIT Student)")
    interviewee = st.text_input("Enter the interviewee's name (exactly as it appears in the transcript)")
    
    if st.button("**Clean Transcript**", type="primary"):
        file_content = uploaded_file.read().decode('utf-8')
        # Ensure newline characters are properly retained
        original_transcript = file_content.replace('\r\n', '\n').replace('\r', '\n')
        cleaned_transcript = clean_and_combine_transcript(original_transcript, interviewer, interviewee)
        
        col1, col2 = st.columns(2)
        
        with col1:
            with st.expander("**Original Transcript**"):
                st.write(original_transcript)
        
        with col2:
            with st.expander("**Cleaned Transcript**"):
                st.code(cleaned_transcript, language=None)
        
        # Get the original file name and append "_cleaned"
        original_filename = uploaded_file.name
        cleaned_filename = os.path.splitext(original_filename)[0] + '_cleaned.txt'
        
        st.download_button(
            label="Download cleaned transcript",
            data=cleaned_transcript,
            file_name=cleaned_filename,
            mime='text/plain'
        )
