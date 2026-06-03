"""Widget pour AES"""
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                               QTextEdit, QPushButton, QGroupBox, QMessageBox,
                               QComboBox, QLineEdit)
from PySide6.QtCore import Qt
from algorithms import aes


class AESWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        """Initialise l'interface"""
        layout = QVBoxLayout()

        # En-tête
        title = QLabel("<h1>Chiffrement AES</h1>")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        description = QLabel(
            "AES (Advanced Encryption Standard) est un algorithme de chiffrement "
            "symétrique par blocs utilisé dans le monde entier."
        )
        description.setWordWrap(True)
        description.setStyleSheet("color: #666; padding: 10px;")
        layout.addWidget(description)

        # Génération de clé
        key_group = QGroupBox("Clé de chiffrement")
        key_layout = QVBoxLayout()

        gen_layout = QHBoxLayout()
        gen_layout.addWidget(QLabel("Taille:"))

        self.key_size_combo = QComboBox()
        self.key_size_combo.addItems(["128 bits", "192 bits", "256 bits"])
        self.key_size_combo.setCurrentIndex(2)
        gen_layout.addWidget(self.key_size_combo)

        gen_btn = QPushButton("🔑 Générer une clé")
        gen_btn.clicked.connect(self.generate_key)
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

        self.key_input = QLineEdit()
        self.key_input.setPlaceholderText("Clé (générée automatiquement ou saisie manuellement)")
        key_layout.addWidget(self.key_input)

        key_group.setLayout(key_layout)
        layout.addWidget(key_group)

        # Zone de texte d'entrée
        input_group = QGroupBox("Message")
        input_layout = QVBoxLayout()
        self.input_text = QTextEdit()
        self.input_text.setPlaceholderText("Entrez votre message ici...")
        self.input_text.setMinimumHeight(150)
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

    def generate_key(self):
        """Génère une clé AES"""
        key_size_text = self.key_size_combo.currentText()
        size = int(key_size_text.split()[0])

        try:
            key = aes.generate_key(size)
            self.key_input.setText(key)
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Erreur lors de la génération: {str(e)}")

    def encrypt_text(self):
        """Chiffre le texte"""
        text = self.input_text.toPlainText()
        key = self.key_input.text()

        if not text:
            QMessageBox.warning(self, "Attention", "Veuillez entrer un message!")
            return

        if not key:
            QMessageBox.warning(self, "Attention", "Veuillez générer ou entrer une clé!")
            return

        try:
            encrypted = aes.encrypt(text, key)
            self.output_text.setPlainText(encrypted)
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Erreur de chiffrement: {str(e)}")

    def decrypt_text(self):
        """Déchiffre le texte"""
        text = self.input_text.toPlainText()
        key = self.key_input.text()

        if not text:
            QMessageBox.warning(self, "Attention", "Veuillez entrer un message chiffré!")
            return

        if not key:
            QMessageBox.warning(self, "Attention", "Veuillez entrer la clé!")
            return

        try:
            decrypted = aes.decrypt(text, key)
            self.output_text.setPlainText(decrypted)
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Erreur de déchiffrement: {str(e)}")

    def clear_all(self):
        """Efface tous les champs"""
        self.input_text.clear()
        self.output_text.clear()