"""Widget pour le chiffrement César"""
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                               QTextEdit, QPushButton, QSpinBox, QGroupBox,
                               QMessageBox)
from PySide6.QtCore import Qt
from algorithms import caesar


class CaesarWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        """Initialise l'interface"""
        layout = QVBoxLayout()

        # En-tête
        title = QLabel("<h1>Chiffrement de César</h1>")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        description = QLabel(
            "Le chiffrement de César consiste à décaler chaque lettre "
            "de l'alphabet d'un nombre fixe de positions."
        )
        description.setWordWrap(True)
        description.setStyleSheet("color: #666; padding: 10px;")
        layout.addWidget(description)

        # Groupe de paramètres
        params_group = QGroupBox("Paramètres")
        params_layout = QHBoxLayout()

        params_layout.addWidget(QLabel("Décalage:"))
        self.shift_spin = QSpinBox()
        self.shift_spin.setRange(0, 25)
        self.shift_spin.setValue(3)
        self.shift_spin.setMinimumWidth(100)
        params_layout.addWidget(self.shift_spin)
        params_layout.addStretch()

        params_group.setLayout(params_layout)
        layout.addWidget(params_group)

        # Zone de texte d'entrée
        input_group = QGroupBox("Texte à chiffrer")
        input_layout = QVBoxLayout()
        self.input_text = QTextEdit()
        self.input_text.setPlaceholderText("Entrez votre texte ici...")
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

    def encrypt_text(self):
        """Chiffre le texte"""
        text = self.input_text.toPlainText()
        if not text:
            QMessageBox.warning(self, "Attention", "Veuillez entrer un texte!")
            return

        shift = self.shift_spin.value()
        encrypted = caesar.encrypt(text, shift)
        self.output_text.setPlainText(encrypted)

    def decrypt_text(self):
        """Déchiffre le texte"""
        text = self.input_text.toPlainText()
        if not text:
            QMessageBox.warning(self, "Attention", "Veuillez entrer un texte!")
            return

        shift = self.shift_spin.value()
        decrypted = caesar.decrypt(text, shift)
        self.output_text.setPlainText(decrypted)

    def clear_all(self):
        """Efface tous les champs"""
        self.input_text.clear()
        self.output_text.clear()