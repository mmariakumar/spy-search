from ...utils import read_config, write_config
from fastapi import UploadFile
import fitz  # PyMuPDF
"""
    This files should handle 
"""
def select_folder_handler(folder_name:str):
    folder_path = f"./local_files/{folder_name}"

    config = read_config()
    config['db'] = folder_path

    write_config(config)
    return folder_path


def delete_folder_handler():
    pass 

def get_folder_handler():
    pass 

def upload_file_handler():
    pass 

def delete_file_handler():
    pass

def download_file_handler():
    pass 


async def extract_text_from_pdf_file(file: UploadFile) -> str:
    # Read bytes asynchronously
    file_bytes = await file.read()
    # Open PDF using PyMuPDF (fitz)
    import fitz
    doc = fitz.open(stream=file_bytes, filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text