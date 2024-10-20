Here's a `README.md` for your FastAPI project, detailing its purpose and steps for usage:

```markdown
# FastAPI Project

## Purpose

This FastAPI project is designed to provide an API for processing web URLs and PDF documents, as well as facilitating chat interactions based on the content extracted from these sources. The main functionalities include:

1. **Processing URLs**: Extract content from a specified URL.
2. **Processing PDF Documents**: Handle and extract content from uploaded PDF files.
3. **Chat Interaction**: Allow users to ask questions about the processed content.

## Requirements

- Python 3.7 or higher
- FastAPI
- Uvicorn (for serving the application)
- Pydantic (for data validation)

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. Install the required packages:
   ```bash
   pip install fastapi uvicorn pydantic
   ```

## Code Explanation

### Main Application

The main application is defined in `app.py`:

```python
from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel
from services import process_url, process_pdf, chat_with_content

app = FastAPI()
```

### Data Models

#### URLRequest

This model is used to validate requests for processing URLs.

```python
class URLRequest(BaseModel):
    url: str
    method: str = 'GET'  # Default value
    headers: dict = None  # Optional field
```

**Example Usage**:
```python
url_request_instance = URLRequest(url="https://aws.amazon.com/what-is/api/", method="POST", headers={"Content-Type": "application/json"})
```

#### ChatRequest

This model is used for chat interactions.

```python
class ChatRequest(BaseModel):
    chat_id: str
    question: str
```

**Example Usage**:
```python
example_request = ChatRequest(chat_id="12345", question="What is API?")
```

### API Endpoints

1. **Process URL**
   - **Endpoint**: `/process_url`
   - **Method**: `POST`
   - **Description**: Accepts a URL and processes its content.
   - **Request Body**: `URLRequest` object.

   ```python
   @app.post("/process_url")
   async def process_web_url(request_data: URLRequest):
       chat_id = await process_url(request_data.url)
       return {"chat_id": chat_id, "message": "URL content processed and stored successfully."}
   ```

2. **Process PDF**
   - **Endpoint**: `/process_pdf`
   - **Method**: `POST`
   - **Description**: Accepts a PDF file and processes its content.
   - **Request Body**: File upload.

   ```python
   @app.post("/process_pdf")
   async def process_pdf_document(file: UploadFile = File(...)):
       if not file.filename.endswith('.pdf'):
           raise HTTPException(status_code=400, detail="Invalid file type. Please upload a PDF file.")
       chat_id = await process_pdf(file)
       return {"chat_id": chat_id, "message": "PDF content processed and stored successfully."}
   ```

3. **Chat**
   - **Endpoint**: `/chat`
   - **Method**: `POST`
   - **Description**: Facilitates a chat based on the processed content.
   - **Request Body**: `ChatRequest` object.

   ```python
   @app.post("/chat")
   async def chat(chat_request: ChatRequest):
       response = await chat_with_content(chat_request.chat_id, chat_request.question)
       return {"response": response}
   ```

## Running the Application

To run the FastAPI application, use Uvicorn:

```bash
uvicorn app:app --reload
```

Visit `http://127.0.0.1:8000/docs` for the interactive API documentation.

## Conclusion

This project provides a robust framework for processing web content and facilitating chat interactions through a clean and efficient API built with FastAPI. Feel free to extend its functionality or integrate it into larger applications.
```

Feel free to modify any sections to better fit your project's specifics!
