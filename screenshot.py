import os

# Define project details
project_title = "📚 Information Retrieval System"
description = """
This is an AI-powered information retrieval system that allows users to upload PDFs and ask questions based on their content. It uses NLP and vector embeddings to fetch the most relevant answers.

## 🚀 Features
- Upload multiple PDF files
- AI-powered question-answering system
- Real-time chat interface
- Vector-based text search
- Elegant UI with Streamlit
"""

# Screenshot file (Update this path)
screenshot_path = r"C:\Users\Dell\OneDrive\Desktop\GENAI\Info-retrieval-Model-system\image-1.png"

# Check if the file exists
if os.path.exists(screenshot_path):
    screenshot_filename = os.path.basename(screenshot_path)  # Extracts the filename
    screenshot_md = f"![Screenshot]({screenshot_filename})"
else:
    screenshot_md = "No screenshot available."

# README content
readme_content = f"# {project_title}\n\n{description}\n\n## 📸 Screenshot\n{screenshot_md}\n\n## 🔧 Setup\n```\npip install -r requirements.txt\nstreamlit run app.py\n```"

# Save README.md
readme_path = os.path.join(os.path.dirname(screenshot_path), "README.md")
with open(readme_path, "w", encoding="utf-8") as file:
    file.write(readme_content)

print("✅ README.md updated successfully!")
