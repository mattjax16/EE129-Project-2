# Import socket module
from socket import *
import sys


def create_html(title, body, status="200 OK"):
    """Create HTML response with given title, body, and status"""
    return (
        f"HTTP/1.1 {status}\r\n"
        f"Content-Type: text/html\r\n\r\n"
        f"<html><head><title>{title}</title></head>"
        f"<body>{body}</body></html>"
    )


def handle_color(request_path):
    """Handle color requests"""
    colors = {
        "red": "#FF0000",
        "green": "#00FF00"
    }

    for color in colors:
        if color in request_path:
            body = f"<h1>Your color is <span style='color:{colors[color]};'>{color}!</span></h1>"
            return create_html(f"{color.title()} Color", body)

    return create_html(title="404 Not Found",body= "<h1>404 Not Found</h1>",status= "404 Not Found")


def main():
    server = socket(AF_INET, SOCK_STREAM)
    server.bind(("", 6581))
    server.listen(1)
    print('Server ready')

    while True:
        try:
            conn, addr = server.accept()
            print(f"Connected: {addr}")

            try:
                msg = conn.recv(1024).decode()
                if not msg:
                    continue

                path = msg.split()[1]
                print(f"Path: {path}")

                if path == "/":
                    form = (
                        "<h1>Choose your color</h1>"
                        "<form action='/color'>"
                        "<select name='color'>"
                        "<option value='red'>Red</option>"
                        "<option value='green'>Green</option>"
                        "</select>"
                        "<input type='submit' value='Submit'>"
                        "</form>"
                    )
                    response = create_html("Color Form", form)
                else:
                    response = handle_color(path)

                conn.send(response.encode())

            except IOError:
                not_found = create_html(title="404 Not Found", body= "<h1>404 Not Found</h1>", status= "404 Not Found")
                conn.send(not_found.encode())
            finally:
                conn.close()
                print("Closed")

        except KeyboardInterrupt:
            print("\nShutting down...")
            server.close()
            sys.exit(0)
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()