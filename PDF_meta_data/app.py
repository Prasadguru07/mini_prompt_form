from fastapi import FastAPI, File, UploadFile, HTTPException
from pypdf import PdfReader
import io

app = FastAPI(title="Smart PDF Metadata Extractor")

@app.post("/upload")
async def extract_pdf_metadata(file: UploadFile = File(...)):
    
    # 1. Validation: Ensure the uploaded file is actually a PDF
    if file.content_type != "application/pdf":
        raise HTTPException(
            status_code=400, 
            detail=f"Invalid file type: {file.content_type}. Please upload a PDF."
        )
    
    try:
        # 2. Read the file into memory asynchronously
        # This prevents the server from freezing while receiving large files.
        file_content = await file.read()
        
        # 3. Load the raw bytes into pypdf's PdfReader
        pdf = PdfReader(io.BytesIO(file_content))
        
        # 4. Extract metadata and page count
        # pypdf uses Python's len() function to count the total pages
        num_pages = len(pdf.pages) 
        metadata = pdf.metadata
        
        # Safely extract author and title (they might be None in some PDFs)
        author = metadata.author if metadata and metadata.author else "Unknown"
        title = metadata.title if metadata and metadata.title else "Unknown"
        
        return {
            "filename": file.filename,
            "content_type": file.content_type,
            "total_pages": num_pages,
            "author": author,
            "title": title
        }
        
    except Exception as e:
        # 5. Catch-all error handling for corrupted PDFs
        raise HTTPException(status_code=500, detail=f"Error processing PDF: {str(e)}")