# Import socket module
from socket import *
import sys  # In order to terminate the program

# Create a TCP server socket
# (AF_INET is used for IPv4 protocols)
# (SOCK_STREAM is used for TCP)
serverSocket = socket(AF_INET, SOCK_STREAM)

# Assign a port number
serverPort = 6789

# Bind the socket to server address and server port
serverSocket.bind(("", serverPort))
# Listen to at most 1 connection at a time
serverSocket.listen(1)


def color(request_path):
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
        # If the request path does not contain "red" or "green," return 404 Not Found
        return (
            "HTTP/1.1 404 Not Found\r\n"
            "Content-Type: text/html\r\n\r\n"
            "<html><head><title>404 Not Found</title></head>"
            "<body><h1>404 Not Found</h1></body></html>"
        )


# Server should be up and running and listening to the incoming connections
while True:
    print('The server is ready to receive')
    # Set up a new connection from the client
    connectionSocket, addr = serverSocket.accept()

    try:
        # Receives the request message from the client
        message = connectionSocket.recv(1024).decode()
        # Extract the path of the requested object from the message
        # The path is the second part of HTTP header, identified by [1]
        request_path = message.split()[1]
        # print(request_path, " request path")

        # If the URL is "/", display the form for selecting colors
        if request_path == "/":
            response = (
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

            # Send the HTTP response header line to the connection socket
            connectionSocket.send(response.encode())
        else:
            response = color(request_path)
            connectionSocket.send(response.encode())

        # Close the client connection socket
        connectionSocket.close()

    except IOError:
        # Send HTTP response message for file not found
        connectionSocket.send("HTTP/1.1 404 Not Found\r\n\r\n".encode())
        connectionSocket.send("<html><head></head><body><h1>404 Not Found</h1></body></html>\r\n".encode())
        # Close the client connection socket
        connectionSocket.close()

serverSocket.close()
sys.exit()  # Terminate the program after sending the corresponding data
