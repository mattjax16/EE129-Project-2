"""
simple_image_web_server.py
This server listens for incoming TCP connections with a configurable backlog.
Uses ThreadPoolExecutor to handle client connections efficiently.
"""
from socket import *
import sys
import logging
from concurrent.futures import ThreadPoolExecutor
import multiprocessing

PORT_NUMBER = 6420  # Port to listen on
MAX_WORKERS = multiprocessing.cpu_count()  # Number of worker threads in the pool (I have 8 cores os I chose 8)
LISTEN_BACKLOG = 100  # Number of connections to queue
IMAGE_FILE = "rick_roll.jpg" # File to serve

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(threadName)s] %(message)s'
)

def handle_client(connection_socket, client_address):
    """
    Handle the client connection.
    """
    try:
        message = connection_socket.recv(1024).decode()
        if not message:
            return
        logging.info(f"Processing request from {client_address}")

        filename = "rick_roll.jpg"
        try:
            with open(filename, "rb") as f:
                outputdata = f.read()
            connection_socket.send("HTTP/1.1 200 OK\r\nContent-Type: image/jpeg\r\n\r\n".encode())
            connection_socket.sendall(outputdata)
            logging.info(f"Sent file to {client_address}")

        except IOError:
            connection_socket.send("HTTP/1.1 404 Not Found\r\n\r\n".encode())
            connection_socket.send(
                "<html><head></head><body><h1>404 Image Not Found</h1></body></html>\r\n".encode())
            logging.info(f"File not found error for {client_address}")

    except Exception as e:
        logging.error(f"Error handling client {client_address}: {e}")
    finally:
        connection_socket.close()
        logging.info(f"Closed connection with {client_address}")

def main():
    server_socket = socket(AF_INET, SOCK_STREAM)
    server_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

    try:
        server_socket.bind(("", PORT_NUMBER))
        server_socket.listen(LISTEN_BACKLOG)
        logging.info(f"Server started on port {PORT_NUMBER}")
        logging.info(f"Configured with:")
        logging.info(f"- Max worker threads: {MAX_WORKERS}")
        logging.info(f"- Connection backlog: {LISTEN_BACKLOG}")
        logging.info("Server ready to accept connections")

        with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
            while True:
                try:
                    # Accept will pull from the backlog queue
                    connection_socket, client_address = server_socket.accept()
                    logging.info(f"Accepted connection from {client_address}")

                    # Submit to thread pool - if pool is full, task will queue internally
                    executor.submit(handle_client, connection_socket, client_address)

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
