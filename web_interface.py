from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse, FileResponse
from io import StringIO
import json
import socket

# FastAPI app initialization
app = FastAPI()

# Constants for server communication
SERVER_HOST = "server"  
SERVER_PORT = 17000

def send_code_to_server(code: str) -> str:
    """
    Sends the code to the server and receives the commented code back.
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((SERVER_HOST, SERVER_PORT))
        request = json.dumps({"code": code})
        client_socket.sendall(request.encode('utf-8'))
        response = client_socket.recv(4096).decode('utf-8')
        response_data = json.loads(response)
        return response_data.get("commented_code", "")

@app.get("/", response_class=HTMLResponse)
async def home():
    """
    Displays the HTML form for users to input their code.
    """
    return """
    <html>
        <head>
            <title>Code Commenter</title>
        </head>
        <body>
            <h1>Upload Your Code for Commenting</h1>
            <form action="/submit_code" method="post">
                <textarea name="code" rows="10" cols="50" placeholder="Paste your code here..."></textarea><br>
                <button type="submit">Submit Code</button>
            </form>
        </body>
    </html>
    """

@app.post("/submit_code")
async def submit_code(code: str = Form(...)):
    """
    Handles the code submission, communicates with the server,
    and returns the commented code as a downloadable file.
    """
    commented_code = send_code_to_server(code)

    output_file = "commented_code.py"
    with open(output_file, "w") as f:
        f.write(commented_code)

    return FileResponse(output_file, filename="commented_code.py", media_type="application/octet-stream")
