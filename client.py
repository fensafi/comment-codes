import socket
import json

# Server constants
SERVER_HOST = "server"  # Use "server" if using Docker Compose
SERVER_PORT = 17000

def main():
    """
    Connects to the server, sends a code snippet, and prints the commented response.
    """
    # Example code snippet to send to the server
    example_code = """
def hello_world():
    print("Hello, World!")

hello_world()
    """

    try:
        # Establish connection to the server
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.connect((SERVER_HOST, SERVER_PORT))
            print("Connected to server.")

            # Send the code to the server
            request = json.dumps({"code": example_code})
            client_socket.sendall(request.encode('utf-8'))
            print("Sent code to server.")

            # Receive the commented code from the server
            response = client_socket.recv(4096).decode('utf-8')
            
            # Debug: print the raw response from the server
            print(f"Raw response: {response}")
            
            if response:
                try:
                    response_data = json.loads(response)
                    commented_code = response_data.get("commented_code", "")
                    
                    print("\n--- Commented Code ---")
                    print(commented_code)
                except json.JSONDecodeError:
                    print("Failed to decode JSON response")
            else:
                print("Received empty response from server.")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
