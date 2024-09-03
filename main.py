from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel
from services import process_url, process_pdf, chat_with_content

app = FastAPI()


class URLRequest(BaseModel):
    url: str
    method: str = 'GET'  # Default value
    headers: dict = None  # Optional field


# Creating an instance of URLRequest
url_request_instance = URLRequest(url="https://aws.amazon.com/what-is/api/", method="POST",
                                  headers={"Content-Type": "application/json"})

# Accessing the attributes
print(url_request_instance.url)  # Output: https://aws.amazon.com/what-is/api/
print(url_request_instance.method)  # Output: POST
print(url_request_instance.headers)  # Output: {'Content-Type': 'application/json'}


class ChatRequest(BaseModel):
    chat_id: str
    question: str


example_request = ChatRequest(chat_id="12345", question="What is API?")
print(example_request)


@app.post("/process_url")
async def process_web_url(request_data: URLRequest):  # Renamed parameter
    chat_id = await process_url(request_data.url)
    return {"chat_id": chat_id, "message": "URL content processed and stored successfully."}


@app.post("/process_pdf")
async def process_pdf_document(file: UploadFile = File(...)):
    # Check if the uploaded file is a PDF
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Invalid file type. Please upload a PDF file.")

    # Process the PDF file (assuming process_pdf handles the file correctly)
    chat_id = await process_pdf(file)

    return {"chat_id": chat_id, "message": "PDF content processed and stored successfully."}


@app.post("/chat")
async def chat(chat_request: ChatRequest):  # Renamed parameter
    response = await chat_with_content(chat_request.chat_id, chat_request.question)
    return {"response": response}
