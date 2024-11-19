import socket
import json
import io  # Import io module

# Constants
SERVER_HOST = "0.0.0.0"
SERVER_PORT = 17000

def comment_code(code: str) -> str:
    """
    Function to read code line-by-line and add appropriate comments.
    """
    commented_code = []
    code_io = io.StringIO(code)  # Simulate a file-like object from the code string

    # Read code line by line
    while True:
        line = code_io.readline()
        if not line:  # End of the file
            break

        stripped_line = line.strip()

        # Simple comment logic based on common Python constructs
        if not stripped_line:  # Empty line
            commented_code.append("# Empty line")
        elif stripped_line.startswith("def "):  # Function definition
            commented_code.append(f"# This is a function: {stripped_line}")
        elif stripped_line.startswith("class "):  # Class definition
            commented_code.append(f"# This is a class: {stripped_line}")
        elif "import " in stripped_line:  # Import statements
            commented_code.append(f"# Importing a module: {stripped_line}")
        elif "print(" in stripped_line:  # Print statement
            commented_code.append(f"# Print statement: {stripped_line}")
        else:  # Default comment for general code lines
            commented_code.append(f"#{stripped_line}")

        # Append the original line as well
        commented_code.append(line.strip())

    return "\n".join(commented_code)

def handle_client(client_socket):
    """
    Handles the communication with the client.
    """
    try:
        # Receive the code from the client
        data = client_socket.recv(4096).decode('utf-8')
        print(f"Received data from client: {data}")  # Debug log

        request_data = json.loads(data)
        code = request_data.get("code", "")
        print(f"Code received from client: {code}")  # Debug log

        # Process the code and get the commented version
        commented_code = comment_code(code)
        print(f"Commented code: {commented_code}")  # Debug log

        # Send the commented code back to the client
        response = json.dumps({"commented_code": commented_code})
        client_socket.sendall(response.encode('utf-8'))
        print("Sent response to client.")

    except Exception as e:
        print(f"Error handling client: {e}")
    finally:
        client_socket.close()

def run_server():
    """
    Run the server to listen for incoming connections.
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((SERVER_HOST, SERVER_PORT))
        server_socket.listen(5)
        print(f"Server listening on {SERVER_HOST}:{SERVER_PORT}...")

        while True:
            client_socket, addr = server_socket.accept()
            print(f"Connection from {addr}")
            handle_client(client_socket)

if __name__ == "__main__":
    run_server()
