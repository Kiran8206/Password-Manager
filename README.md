# Password-Manager
A CLI application written in python which securely stores and retrieves website passwords of different users.
I have used fernet (Symmetric authenticated cryptography) to implement the password hashing as it guarantees that any message encrypted using it cannot be decrypted without using the secret key.
Please refer to the Image.png which shows the working output of this application. The output is self-explanatory and the program differentiates the users using the master password they supply when prompted.
