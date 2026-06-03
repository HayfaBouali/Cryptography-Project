"""Widget pour RSA"""
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                               QTextEdit, QPushButton, QGroupBox, QMessageBox,
                               QComboBox)
from PySide6.QtCore import Qt
from algorithms import rsa


class RSAWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.keys = None
        self.init_ui()

    def init_ui(self):
        """Initialise l'interface"""
        layout = QVBoxLayout()

        # En-tête
        title = QLabel("<h1>Chiffrement RSA</h1>")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        description = QLabel(
            "RSA est un algorithme de cryptographie asymétrique qui utilise "
            "une paire de clés (publique et privée)."
        )
        description.setWordWrap(True)
        description.setStyleSheet("color: #666; padding: 10px;")
        layout.addWidget(description)

        # Génération de clés
        key_group = QGroupBox("Génération de clés")
        key_layout = QVBoxLayout()

        gen_layout = QHBoxLayout()
        gen_layout.addWidget(QLabel("Taille de clé:"))

        self.key_size_combo = QComboBox()
        self.key_size_combo.addItems(["1024 bits", "2048 bits", "4096 bits"])
        self.key_size_combo.setCurrentIndex(1)
        gen_layout.addWidget(self.key_size_combo)

        gen_btn = QPushButton("🔑 Générer les clés")
        gen_btn.clicked.connect(self.generate_keys)
        gen_btn.setStyleSheet("""
            QPushButton {
                background-color: #FF9800;
                color: white;
                padding: 8px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #F57C00;
            }
        """)
        gen_layout.addWidget(gen_btn)
        gen_layout.addStretch()

        key_layout.addLayout(gen_layout)

        # Affichage des clés
        self.keys_display = QTextEdit()
        self.keys_display.setReadOnly(True)
        self.keys_display.setMaximumHeight(150)
        self.keys_display.setPlaceholderText("Cliquez sur 'Générer les clés' pour créer une paire de clés RSA")
        key_layout.addWidget(self.keys_display)

        key_group.setLayout(key_layout)
        layout.addWidget(key_group)

        # Zone de texte d'entrée
        input_group = QGroupBox("Message")
        input_layout = QVBoxLayout()
        self.input_text = QTextEdit()
        self.input_text.setPlaceholderText("Entrez votre message ici...")
        self.input_text.setMaximumHeight(100)
        input_layout.addWidget(self.input_text)
        input_group.setLayout(input_layout)
        layout.addWidget(input_group)

        # Boutons d'action
        buttons_layout = QHBoxLayout()

        encrypt_btn = QPushButton("🔒 Chiffrer")
        encrypt_btn.clicked.connect(self.encrypt_text)
        encrypt_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                padding: 10px;
                font-size: 14px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        buttons_layout.addWidget(encrypt_btn)

        decrypt_btn = QPushButton("🔓 Déchiffrer")
        decrypt_btn.clicked.connect(self.decrypt_text)
        decrypt_btn.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                padding: 10px;
                font-size: 14px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #0b7dda;
            }
        """)
        buttons_layout.addWidget(decrypt_btn)

        clear_btn = QPushButton("🗑️ Effacer")
        clear_btn.clicked.connect(self.clear_all)
        clear_btn.setStyleSheet("""
            QPushButton {
                background-color: #f44336;
                color: white;
                padding: 10px;
                font-size: 14px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #da190b;
            }
        """)
        buttons_layout.addWidget(clear_btn)

        layout.addLayout(buttons_layout)

        # Zone de résultat
        output_group = QGroupBox("Résultat")
        output_layout = QVBoxLayout()
        self.output_text = QTextEdit()
        self.output_text.setReadOnly(True)
        self.output_text.setMinimumHeight(150)
        self.output_text.setStyleSheet("background-color: #f9f9f9;")
        output_layout.addWidget(self.output_text)
        output_group.setLayout(output_layout)
        layout.addWidget(output_group)

        self.setLayout(layout)

    def generate_keys(self):
        """Génère une paire de clés RSA"""
        key_size_text = self.key_size_combo.currentText()
        bits = int(key_size_text.split()[0])

        QMessageBox.information(self, "Génération",
                                f"Génération de clés {bits} bits en cours...\nCela peut prendre quelques secondes.")

        try:
            self.keys = rsa.generate_keys(bits)

            display_text = f"""=== CLÉS RSA GÉNÉRÉES ===

📊 Paramètres:
  • n (module) = {self.keys['n']}
  • e (exposant public) = {self.keys['e']}
  • d (exposant privé) = {self.keys['d']}

🔓 Clé publique:
{self.keys['public_key'][:100]}...

🔒 Clé privée:
{self.keys['private_key'][:100]}...
"""
            self.keys_display.setPlainText(display_text)

        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Erreur lors de la génération: {str(e)}")

    def encrypt_text(self):
        """Chiffre le texte"""
        if not self.keys:
            QMessageBox.warning(self, "Attention", "Veuillez d'abord générer les clés!")
            return

        text = self.input_text.toPlainText()
        if not text:
            QMessageBox.warning(self, "Attention", "Veuillez entrer un message!")
            return

        try:
            encrypted = rsa.encrypt(text, self.keys['public_key'])
            self.output_text.setPlainText(encrypted)
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Erreur de chiffrement: {str(e)}")

    def decrypt_text(self):
        """Déchiffre le texte"""
        if not self.keys:
            QMessageBox.warning(self, "Attention", "Veuillez d'abord générer les clés!")
            return

        text = self.input_text.toPlainText()
        if not text:
            QMessageBox.warning(self, "Attention", "Veuillez entrer un message chiffré!")
            return

        try:
            decrypted = rsa.decrypt(text, self.keys['private_key'])
            self.output_text.setPlainText(decrypted)
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Erreur de déchiffrement: {str(e)}")

    def clear_all(self):
        """Efface tous les champs"""
        self.input_text.clear()
        self.output_text.clear()