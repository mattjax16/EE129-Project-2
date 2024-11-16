# Import socket module
from socket import *
import sys  # In order to terminate the program

def handle_color_request(request_path):
    """Handle color-related requests and return appropriate HTTP response"""
    if "red" in request_path:
        return (
            "HTTP/1.1 200 OK\r\n"
            "Content-Type: text/html\r\n\r\n"
            "<html><head><title>Red Color</title></head>"
            "<body>"
            "<h1>Your color is <span style='color:red;'>red!</span></h1>"
            "</body></html>"
        )
    elif "green" in request_path:
        return (
            "HTTP/1.1 200 OK\r\n"
            "Content-Type: text/html\r\n\r\n"
            "<html><head><title>Green Color</title></head>"
            "<body>"
            "<h1>Your color is <span style='color:green;'>green!</span></h1>"
            "</body></html>"
        )
    else:
        return (
            "HTTP/1.1 404 Not Found\r\n"
            "Content-Type: text/html\r\n\r\n"
            "<html><head><title>404 Not Found</title></head>"
            "<body><h1>404 Not Found</h1></body></html>"
        )

def get_color_form():
    """Return the HTML form for color selection"""
    return (
        "HTTP/1.1 200 OK\r\n"
        "Content-Type: text/html\r\n\r\n"
        "<html><head><title>Color Form</title></head>"
        "<body>"
        "<h1>Please choose your color</h1>"
        "<form action='/color' method='get'>"
        "<select name='color'>"
        "<option value='red'>Red</option>"
        "<option value='green'>Green</option>"
        "</select>"
        "<input type='submit' value='Submit'>"
        "</form>"
        "</body></html>"
    )

def main():
    # Create a TCP server socket
    # (AF_INET is used for IPv4 protocols)
    # (SOCK_STREAM is used for TCP)
    serverSocket = socket(AF_INET, SOCK_STREAM)

    # Assign a port number
    serverPort = 6581

    # Bind the socket to server address and server port
    serverSocket.bind(("", serverPort))

    # Listen to at most 1 connection at a time
    serverSocket.listen(1)

    print('The server is ready to receive')

    # Server should be up and running and listening to the incoming connections
    while True:
        try:
            # Set up a new connection from the client
            connectionSocket, addr = serverSocket.accept()
            print(f"Received connection from {addr}")

            try:
                # Receives the request message from the client
                message = connectionSocket.recv(1024).decode()

                if not message:
                    connectionSocket.close()
                    continue

                # Extract the path of the requested object from the message
                request_path = message.split()[1]
                print(f"Requested path: {request_path}")

                try:
                    # Handle the root path
                    if request_path == "/":
                        response = get_color_form()
                    else:
                        response = handle_color_request(request_path)

                    # Send the response
                    connectionSocket.send(response.encode())

                except IOError:
                    # Send HTTP response message for file not found
                    connectionSocket.send("HTTP/1.1 404 Not Found\r\n\r\n".encode())
                    connectionSocket.send("<html><head></head><body><h1>404 Not Found</h1></body></html>\r\n".encode())

            finally:
                # Close the client connection socket
                connectionSocket.close()
                print("Connection closed")

        except KeyboardInterrupt:
            print("\nShutting down server...")
            serverSocket.close()
            sys.exit(0)
        except Exception as e:
            print(f"Error handling connection: {e}")
            continue

if __name__ == "__main__":
    main()