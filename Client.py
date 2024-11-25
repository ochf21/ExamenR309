import socket


class Client:
    def __init__(self, host="127.0.0.1", port=4200):
        self.host = host
        self.port = port
        self.client_socket = None

    def connect(self):
        try:
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect((self.host, self.port))
            print(f"Connecté au serveur sur {self.host}:{self.port}")
        except Exception as e:
            print(f"Erreur de connexion : {e}")
            self.client_socket = None

    def send_message(self, message):
        if not self.client_socket:
            print("Client non connecté au serveur.")
            return False

        try:
            self.client_socket.send(message.encode())
            if message == "deco-server":
                print("Déconnexion du serveur.")
                self.disconnect()
                return False

            response = self.client_socket.recv(1024).decode()
            print(f"Réponse du serveur : {response}")
            return True
        except socket.error as e:
            print(f"Erreur d'envoi ou réception : {e}")
            self.disconnect()
            return False

    def disconnect(self):
        if self.client_socket:
            try:
                self.client_socket.close()
                print("Déconnexion réussie.")
            except Exception as e:
                print(f"Erreur lors de la déconnexion : {e}")
            finally:
                self.client_socket = None


if __name__ == '__main__':
    client = Client()
    client.connect()

    while True:
        message = input("Votre message : ")
        if not client.send_message(message):
            break
