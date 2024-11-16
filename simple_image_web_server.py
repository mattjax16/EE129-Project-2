"""
simple_image_web_server.py
This server listens for incoming TCP connections on a specified port.
When a client connects, it spawns a new thread to handle the request.
The server responds with an image file (rick_roll.jpg) if it exists,
or a 404 Not Found error if the file is not found.
"""

# Import required modules
from socket import *
import sys
import threading
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(threadName)s] %(message)s'
)

class ClientHandler(threading.Thread):
    def __init__(self, connection_socket, client_address):
        threading.Thread.__init__(self)
        self.connection_socket = connection_socket
        self.client_address = client_address

    def run(self):
        """
        Handle the client connection.
        Receives the request message from the client, attempts to read and send
        the 'rick_roll.jpg' file. If the file is not found, sends a 404 Not Found
        response. Closes the client connection after processing the request.
        """
        try:
            # Receives the request message from the client
            message = self.connection_socket.recv(1024).decode()
            if not message:
                return
            logging.info(f"Received message from {self.client_address}")
            # No matter what we will send rick_roll.jpg back to the client
            filename = "rick_roll.jpg"
            try:
                # Open the file and store the entire content in a temporary buffer
                with open(filename, "rb") as f:
                    outputdata = f.read()
                # Send HTTP response headers
                self.connection_socket.send("HTTP/1.1 200 OK\r\nContent-Type: image/jpeg\r\n\r\n".encode())
                # Send the content of the requested file
                self.connection_socket.sendall(outputdata)
                logging.info(f"Sent file to {self.client_address}")
            except IOError:
                # Send HTTP response message for file not found
                self.connection_socket.send("HTTP/1.1 404 Not Found\r\n\r\n".encode())
                self.connection_socket.send(
                    "<html><head></head><body><h1>404 Not Found</h1></body></html>\r\n".encode())
                logging.info(f"File not found error for {self.client_address}")
        except Exception as e:
            logging.error(f"Error handling client {self.client_address}: {e}")
        finally:
            # Close the client connection socket
            self.connection_socket.close()
            logging.info(f"Closed connection with {self.client_address}")

def main():
    # Create a TCP server socket
    server_socket = socket(AF_INET, SOCK_STREAM)
    # Enable address reuse
    server_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    # Assign a port number
    server_port = 6581
    try:
        # Bind the socket to server address and server port
        server_socket.bind(("", server_port))
        # Listen for incoming connections
        server_socket.listen(10)
        logging.info(f"Server started on port {server_port}")
        logging.info("The server is ready to receive connections")
        # Server should be up and running and listening to the incoming connections
        while True:
            try:
                # Set up a new connection from the client
                connection_socket, client_address = server_socket.accept()
                logging.info(f"Accepted connection from {client_address}")
                # Create a new thread to handle the client connection
                client_thread = ClientHandler(connection_socket, client_address)
                client_thread.daemon = True  # Set as daemon thread
                client_thread.start()
            except Exception as e:
                logging.error(f"Error accepting connection: {e}")
                continue
    except KeyboardInterrupt:
        logging.info("\nShutting down server...")
    except Exception as e:
        logging.error(f"Server error: {e}")
    finally:
        server_socket.close()
        sys.exit(0)

if __name__ == "__main__":
    main()