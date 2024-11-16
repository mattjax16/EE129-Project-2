# Import socket module
from socket import *
import sys  # In order to terminate the program

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

                # No matter what we will send rick_roll.jpg back to the client
                filename = "rick_roll.jpg"

                try:
                    # Open the file and store the entire content in a temporary buffer
                    with open(filename, "rb") as f:
                        outputdata = f.read()

                    # Send the HTTP response header line to the connection socket
                    # Send the Content-Type header to specify the type of content being sent
                    connectionSocket.send("HTTP/1.1 200 OK\r\nContent-Type: image/jpeg\r\n\r\n".encode())

                    # Send the content of the requested file to the connection socket
                    connectionSocket.sendall(outputdata)

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