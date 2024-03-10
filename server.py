import socket

import threading

import ssl



# Define your questions and answers here

questions = [

    ("1) What is the capital of France?", ["A) Paris", "B) London", "C) Berlin", "D) Washington D.C."], "A"),

    ("2) Who is the Prime Minister of India?", ["A) Narendra Modi", "B) Vladimir Putin", "C) Barack Obama", "D) Emmanuel Macron"], "A"),

    ("3) What is the largest planet in our solar system?", ["A) Jupiter", "B) Saturn", "C) Uranus", "D) Neptune"], "A"),

    ("4) Who invented the telephone?", ["A) Alexander Graham Bell", "B) Thomas Edison", "C) Nikola Tesla", "D) Marie Curie"], "A"),

    ("5) What is the capital of Australia?", ["A) Canberra", "B) Sydney", "C) Melbourne", "D) Brisbane"], "A")

]



def handle_client(client_socket, addr):

    print(f"Connected to {addr}")



    score = 0

    try:

        for question, options, answer in questions:

            print(f"Sending question: {question}")

            # Send the question and the options in one message, separated by a newline

            message = question + '\n' + '\n'.join(options) + '\n'

            client_socket.sendall(message.encode())

            client_response = client_socket.recv(1024).decode().strip()

            print(f"Received response: {client_response}")

            if client_response.lower() == answer.lower():

                score += 1

                client_socket.sendall(f"Correct! Your score is {score}\n".encode())

            else:

                client_socket.sendall(f"Incorrect. The correct answer is {answer}\n".encode())

    except ConnectionResetError:

        print(f"Connection with {addr} reset.")

    client_socket.sendall(f"Game over! Your final score is {score}\n".encode())

    client_socket.close()



# Server setup with SSL/TLS implementation

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_socket.bind(('localhost', 12345))

server_socket.listen(5)



context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)

context.load_cert_chain(certfile="cert.pem", keyfile="key.pem")



while True:

    client_socket, addr = server_socket.accept()

    secure_client_socket = context.wrap_socket(client_socket, server_side=True)

    client_thread = threading.Thread(target=handle_client, args=(secure_client_socket, addr))

    client_thread.start()