"""
simple_color_web_server.py
This server listens for incoming TCP connections and serves a color selection form.
Uses ThreadPoolExecutor to handle client connections efficiently.
"""
from socket import *
import sys
import logging
from concurrent.futures import ThreadPoolExecutor

PORT_NUMBER = 6421  # Port to listen on
MAX_WORKERS = 8  # Number of worker threads in the pool (I have 8 cores os I chose 8)
LISTEN_BACKLOG = 100  # Number of connections to queue
COLORS = {"red": "#FF0000", "green": "#00FF00", "blue": "#0000FF", "orange": "#FFA500", "pink": "#FFC0CB", "cyan": "#00FFFF", "magenta": "#FF00FF", "brown": "#7B3F00"}  # Available colors with their hex codes (by having red first it takes precedence)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(threadName)s] %(message)s'
)

def create_html(title, body, status="200 OK"):
    """
    Create HTML response with given title, body, and status.
    """
    return (
        f"HTTP/1.1 {status}\r\nContent-Type: text/html\r\n\r\n"
        f"<html><head><title>{title}</title></head><body>{body}</body></html>"
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
        path = message.split()[1]
        try:
            if path == "/":
                # Serve the color selection form
                form = ("<h1>Choose your color</h1><form action='/color'><select name='color'>"
                        + "".join([f"<option value='{color}'>{color.title()}</option>" for color in COLORS])
                        + "</select><input type='submit' value='Submit'></form>")
                response = create_html("Color Form", form)
            else:
                # Handle color selection
                for color in COLORS:
                    if color in path:
                        body = f"<h1>Your color is <span style='color:{COLORS[color]};'>{color}!</span></h1>"
                        response = create_html(f"{color.title()} Color", body)
                        break
                else:
                    response = create_html( title="404 Not Found",body="<h1>404 Not Found</h1>",status="404 Not Found")
            connection_socket.send(response.encode())
            logging.info(f"Sent response to {client_address}")
        except IOError:
            not_found = create_html(title="",body="<h1>Not Found</h1>",status="404 Not Found")
            connection_socket.send(not_found.encode())
            logging.info(f"Error response sent to {client_address}")
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
                    connection_socket, client_address = server_socket.accept() # Accept will pull from the backlog queue
                    logging.info(f"Accepted connection from {client_address}")
                    executor.submit(handle_client, connection_socket, client_address) # Submit to thread pool - if pool is full, task will queue internally
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