"""Widget pour ADFGVX"""
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                               QTextEdit, QPushButton, QLineEdit, QGroupBox,
                               QMessageBox)
from PySide6.QtCore import Qt
from algorithms import adfgvx


class ADFGVXWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # En-tête
        title = QLabel("<h1>Chiffrement ADFGVX</h1>")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        description = QLabel(
            "ADFGVX combine substitution (carré de Polybe 6×6) et transposition.<br>"
            "<b>Étape 1:</b> Substitution avec carré de Polybe (mot-clé 1)<br>"
            "<b>Étape 2:</b> Transposition columaire (mot-clé 2)<br>"
            "<b>Utilisé pendant la Première Guerre mondiale</b>"
        )
        description.setWordWrap(True)
        description.setStyleSheet("color: #555; padding: 10px; background-color: #ffebee; border-radius: 5px;")
        layout.addWidget(description)

        # Paramètres
        params_group = QGroupBox("Mots-clés")
        params_layout = QVBoxLayout()

        key1_layout = QHBoxLayout()
        key1_layout.addWidget(QLabel("Clé 1 (Polybe):"))
        self.key1_input = QLineEdit()
        self.key1_input.setPlaceholderText("Ex: CRYPTOGRAPHIE")
        key1_layout.addWidget(self.key1_input)
        params_layout.addLayout(key1_layout)

        key2_layout = QHBoxLayout()
        key2_layout.addWidget(QLabel("Clé 2 (Transposition):"))
        self.key2_input = QLineEdit()
        self.key2_input.setPlaceholderText("Ex: GUERRE")
        key2_layout.addWidget(self.key2_input)
        params_layout.addLayout(key2_layout)

        params_group.setLayout(params_layout)
        layout.addWidget(params_group)

        # Texte d'entrée
        input_group = QGroupBox("Texte")
        input_layout = QVBoxLayout()
        self.input_text = QTextEdit()
        self.input_text.setPlaceholderText("Entrez votre texte...")
        self.input_text.setMinimumHeight(100)
        input_layout.addWidget(self.input_text)
        input_group.setLayout(input_layout)
        layout.addWidget(input_group)

        # Boutons
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
            QPushButton:hover { background-color: #45a049; }
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
            QPushButton:hover { background-color: #0b7dda; }
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
            QPushButton:hover { background-color: #da190b; }
        """)
        buttons_layout.addWidget(clear_btn)

        layout.addLayout(buttons_layout)

        # Résultat
        output_group = QGroupBox("Résultat")
        output_layout = QVBoxLayout()
        self.output_text = QTextEdit()
        self.output_text.setReadOnly(True)
        self.output_text.setMinimumHeight(100)
        self.output_text.setStyleSheet("background-color: #f9f9f9;")
        output_layout.addWidget(self.output_text)
        output_group.setLayout(output_layout)
        layout.addWidget(output_group)

        self.setLayout(layout)

    def encrypt_text(self):
        text = self.input_text.toPlainText()
        key1 = self.key1_input.text()
        key2 = self.key2_input.text()

        if not text:
            QMessageBox.warning(self, "Attention", "Veuillez entrer un texte!")
            return

        if not key1 or not key2:
            QMessageBox.warning(self, "Attention", "Veuillez entrer les deux mots-clés!")
            return

        try:
            encrypted = adfgvx.encrypt(text, key1, key2)
            self.output_text.setPlainText(encrypted)
        except Exception as e:
            QMessageBox.critical(self, "Erreur", str(e))

    def decrypt_text(self):
        text = self.input_text.toPlainText()
        key1 = self.key1_input.text()
        key2 = self.key2_input.text()

        if not text:
            QMessageBox.warning(self, "Attention", "Veuillez entrer un texte!")
            return

        if not key1 or not key2:
            QMessageBox.warning(self, "Attention", "Veuillez entrer les deux mots-clés!")
            return

        try:
            decrypted = adfgvx.decrypt(text, key1, key2)
            self.output_text.setPlainText(decrypted)
        except Exception as e:
            QMessageBox.critical(self, "Erreur", str(e))

    def clear_all(self):
        self.input_text.clear()
        self.output_text.clear()