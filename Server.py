import sys
import socket
from threading import Thread
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QPushButton, QLabel, QLineEdit, QTextEdit, QWidget

class ServerInterface(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Le serveur de tchat")
        self.setGeometry(100, 100, 500, 400)
        widget = QWidget()
        layout = QVBoxLayout()
        self.ip_label = QLabel("Serveur")
        self.ip_input = QLineEdit("0.0.0.0")
        self.port_label = QLabel("Port")
        self.port_input = QLineEdit("4200")
        self.clients_max_label = QLabel("Nombre de clients maximum")
        self.clients_max_input = QLineEdit("5")
        self.clients_display = QTextEdit()
        self.clients_display.setReadOnly(True)
        self.toggle_button = QPushButton("Démarrage du serveur")

        layout.addWidget(self.ip_label)
        layout.addWidget(self.ip_input)
        layout.addWidget(self.port_label)
        layout.addWidget(self.port_input)
        layout.addWidget(self.clients_max_label)
        layout.addWidget(self.clients_max_input)
        layout.addWidget(self.clients_display)
        layout.addWidget(self.toggle_button)
        widget.setLayout(layout)
        self.setCentralWidget(widget)
        self.toggle_button.clicked.connect(self.__demarrage)
        self.server_socket = None
        self.is_running = False
        self.accept_thread = None
        self.client_conn = None
        self.client_addr = None

    def __demarrage(self):
        if not self.is_running:
            try:
                host = self.ip_input.text()
                port = int(self.port_input.text())
                max_clients = int(self.clients_max_input.text())
                self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.server_socket.bind((host, port))
                self.server_socket.listen(max_clients)
                self.is_running = True
                self.toggle_button.setText("Arrêt du serveur")
                self.clients_display.append(f"Serveur démarré :  {host}:{port}\n")
                self.accept_thread = Thread(target=self.__accept)
                self.accept_thread.start()
            except ValueError:
                self.clients_display.append("erreur le port et le nombr de clients doivent etre des nombres entier\n")
            except Exception as e:
                self.clients_display.append(f"erreur lors du demarrage : {e}\n")
        else:
            self.__stop()

    def __stop(self):
        self.is_running = False
        if self.client_conn:
            try:
                self.client_conn.close()
            except Exception as e:
                self.clients_display.append(f"erreur de la fermeture du client : {e}\n")
        if self.server_socket:
            try:
                self.server_socket.close()
            except Exception as e:
                self.clients_display.append(f"erreur de l'arret du serveur : {e}\n")
        self.toggle_button.setText("Démarrage du serveur")
        self.clients_display.append("Serveur arrêté.\n")

    def __accept(self):
        try:
            self.clients_display.append("En attente d'un client...\n")
            conn, addr = self.server_socket.accept()
            self.client_conn = conn
            self.client_addr = addr
            self.clients_display.append(f"Client connecté : {addr}\n")
            self.__reception()
        except Exception as e:
            self.clients_display.append(f"erreur d'acceptation : {e}\n")

    def __reception(self):
        try:
            while self.is_running:
                message = self.client_conn.recv(1024).decode()
                if not message or message == "deco-server":
                    self.clients_display.append(f"Client déconnecté : {self.client_addr}\n")
                    break
                self.clients_display.append(f"Message reçu de {self.client_addr} : {message}\n")
                self.client_conn.send(f"Message reçu : {message}".encode())
        except Exception as e:
            self.clients_display.append(f"erreur de la réception de message : {e}\n")
        finally:
            self.client_conn.close()

    # Partie 8 : comment accepter plusieurs clients ?
    # Question 1 :
    # Le client doit envoyer un message deco-server pour qu'il s'arrete.

    #Lien Github
    #https://github.com/ochf21/ExamenR309

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ServerInterface()
    window.show()
    sys.exit(app.exec())
