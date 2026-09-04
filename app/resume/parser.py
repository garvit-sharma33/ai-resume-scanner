import pdfplumber
import re
from docx import Document


# Extract text from all pages of a PDF resume
def extract_text_from_pdf(file_path):
    text = ""

    try:
        with pdfplumber.open(file_path) as pdf:

            for page in pdf.pages:
                page_text = page.extract_text()

                if page_text:
                    text += page_text + "\n"

    except FileNotFoundError:
        print("Error: Resume file was not found.")

    except PermissionError:
        print("Error: Permission denied while reading the resume.")

    except Exception as error:
        print(f"Error while processing PDF: {error}")

    return text


# Extract text from a DOCX resume
def extract_text_from_docx(file_path):
    text = ""

    try:
        document = Document(file_path)

        # Read readable text from each paragraph
        for paragraph in document.paragraphs:
            if paragraph.text.strip():
                text += paragraph.text + "\n"

    except FileNotFoundError:
        print("Error: DOCX resume file was not found.")

    except PermissionError:
        print("Error: Permission denied while reading the DOCX resume.")

    except Exception as error:
        print(f"Error while processing DOCX: {error}")

    return text


# Clean the extracted resume text
def clean_resume_text(text):

    # Normalize spaces and remove unnecessary blank lines
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n+", "\n", text)

    return text.strip()


# Detect file type, extract text, clean it, and validate the result
def extract_resume_text(file_path):

    file_extension = file_path.lower().split(".")[-1]

    if file_extension == "pdf":
        text = extract_text_from_pdf(file_path)

    elif file_extension == "docx":
        text = extract_text_from_docx(file_path)

    else:
        print("Error: Unsupported resume file type.")
        return ""

    cleaned_text = clean_resume_text(text)

    # Stop empty or unreadable resumes from entering the AI pipeline
    if not cleaned_text:
        print("Error: Resume file contains no readable text.")
        return ""

    return cleaned_text


# Test the complete resume processing pipeline
if __name__ == "__main__":

    file_path = "test_resume/test_resume.pdf"

    cleaned_text = extract_resume_text(file_path)

    if cleaned_text:
        print("\n----- CLEANED RESUME TEXT -----\n")
        print(cleaned_text)