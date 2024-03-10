import socket

import ssl



# Create SSL context

context = ssl.create_default_context()

context.check_hostname = False

context.verify_mode = ssl.CERT_NONE



# Create a regular TCP socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)



# Wrap the socket with SSL/TLS

secure_client_socket = context.wrap_socket(client_socket, server_hostname='localhost')



try:

    # Connect to the server

    secure_client_socket.connect(('localhost', 12345))  # Replace '127.0.0.1' with the server's IP address

    print("Connected to the server.")



    while True:

        # Receive question data from the server

        question_data = secure_client_socket.recv(4096).decode().strip()

        if not question_data:

            break



        # Process the received question data

        questions = question_data.split('\n')

        question = questions[0]

        options = questions[1:-1]



        # Check if the game is over

        if question.startswith("Game over! Your final score is"):

            print(question)

            break



        # Display the question and options

        print(question)

        for option in options:

            print(option)



        # Send user's answer to the server

        answer = input("Your answer: ")

        secure_client_socket.send(answer.encode())



except ConnectionRefusedError:

    print("Connection to the server was refused. Please make sure the server is running.")

except Exception as e:

    print(f"An error occurred: {e}")



finally:

    secure_client_socket.close()