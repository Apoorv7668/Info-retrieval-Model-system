import streamlit as st
from src.helper import get_pdf_text, get_text_chunks, get_vector_store, get_conversational_chain

def user_input(user_question):
    """Handles user input and displays conversation history."""
    response = st.session_state.conversation({'question': user_question})
    st.session_state.chatHistory = response['chat_history']
    
    for i, message in enumerate(st.session_state.chatHistory):
        if i % 2 == 0:
            st.chat_message("user").markdown(f"**👤 User:** {message.content}")
        else:
            st.chat_message("assistant").markdown(f"**🤖 AI:** {message.content}")

def main():
    st.set_page_config(page_title="AI PDF Assistant", layout="wide")
    
    # Custom CSS for a more elegant look
    st.markdown(
        """
        <style>
        body {font-family: 'Arial', sans-serif;}
        .stChatMessage {padding: 12px; border-radius: 10px; margin-bottom: 10px; font-size: 16px;}
        .user {background-color: #E3F2FD; text-align: left; border-left: 4px solid #42A5F5; padding-left: 10px;}
        .assistant {background-color: #FFEBEE; text-align: left; border-left: 4px solid #EF5350; padding-left: 10px;}
        .sidebar .css-1d391kg {background-color: #f4f4f4; border-radius: 10px; padding: 15px;}
        .stButton>button {border-radius: 8px; background-color: #008CBA; color: white; font-size: 16px;}
        </style>
        """, unsafe_allow_html=True
    )
    
    st.title("📖 AI-Powered Information Retrieval System")
    st.subheader("Effortlessly search through your PDFs using AI-powered insights.")
    
    # User Input Section
    st.markdown("**💬 Ask a Question:**")
    user_question = st.text_input("", placeholder="Type your question here and press Enter...")
    
    # Initialize session state
    if "conversation" not in st.session_state:
        st.session_state.conversation = None
    if "chatHistory" not in st.session_state:
        st.session_state.chatHistory = []
    
    if user_question:
        user_input(user_question)
    
    # Sidebar for File Upload
    with st.sidebar:
        st.header("📂 Upload Your Files")
        pdf_docs = st.file_uploader("Drag and drop your PDFs or browse", accept_multiple_files=True, type=["pdf"], help="Supports multiple files")
        
        if st.button("🚀 Process Files"):
            with st.spinner("🔄 Extracting insights from PDFs..."):
                raw_text = get_pdf_text(pdf_docs)
                text_chunks = get_text_chunks(raw_text)
                vector_store = get_vector_store(text_chunks)
                st.session_state.conversation = get_conversational_chain(vector_store)
                st.success("✅ Processing Complete! You can now ask questions.")
    
    # Dark Mode Toggle
    theme_toggle = st.sidebar.toggle("🌙 Dark Mode")
    if theme_toggle:
        st.markdown("""
            <style>
            body {background-color: #222; color: white;}
            .stButton>button {background-color: #444; color: white;}
            </style>
        """, unsafe_allow_html=True)
    
if __name__ == "__main__":
    main()