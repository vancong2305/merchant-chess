import threading
import json
import socket

HOST = '127.0.0.1'  # Server's IP address
PORT = 9999         # Server's port

def handle_client(client_socket):
    try:
        print('Connected by', client_socket.getpeername())
        while True:
            data = client_socket.recv(1024)

            if not data:
                print("Client disconnected")
                break

            json_data = data.decode("utf8")
            print(json_data)
            # Validate and process the received JSON data
            try:
                received_data = json.loads(json_data)
                name = received_data['object']
                age = received_data['create']
                city = received_data['city']

                # Process the data (e.g., store in a database)
                # ... (your data processing logic here)

                # Send a success response or additional data as needed
                msg = f"Received JSON object successfully: Name: {name}, Age: {age}, City: {city}"
                client_socket.sendall(bytes(msg, "utf8"))
            except (json.JSONDecodeError, KeyError) as e:
                # Handle invalid JSON or missing keys gracefully
                print(f"Error processing JSON: {e}")
                msg = "Invalid JSON object"
                client_socket.sendall(bytes(msg, "utf8"))

    finally:
        # Ensure the client socket is closed even in case of exceptions
        client_socket.close()

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen(8)

    print('Server listening on port', PORT)
    while True:
        client, addr = s.accept()
        # Create a new thread or use an asynchronous framework to handle concurrent clients
        threading.Thread(target=handle_client, args=(client,)).start()

print('Server shutting down')