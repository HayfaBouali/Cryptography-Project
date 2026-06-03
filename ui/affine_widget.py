"""Widget pour le chiffrement affine"""
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                               QTextEdit, QPushButton, QSpinBox, QGroupBox,
                               QMessageBox, QComboBox)
from PySide6.QtCore import Qt
from algorithms import affine


class AffineWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # En-tête
        title = QLabel("<h1>Chiffrement Affine</h1>")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        description = QLabel(
            "<b>Formule:</b> C = (a × P + b) mod 26<br>"
            "<b>Contrainte:</b> a doit être premier avec 26<br>"
            "<b>Valeurs valides pour a:</b> 1, 3, 5, 7, 9, 11, 15, 17, 19, 21, 23, 25"
        )
        description.setWordWrap(True)
        description.setStyleSheet("color: #555; padding: 10px; background-color: #ffffcc; border-radius: 5px;")
        layout.addWidget(description)

        # Paramètres
        params_group = QGroupBox("Paramètres (clés a et b)")
        params_layout = QHBoxLayout()

        params_layout.addWidget(QLabel("a (multiplicative):"))
        self.a_combo = QComboBox()
        valid_a = affine.get_valid_a_values()
        self.a_combo.addItems([str(a) for a in valid_a])
        self.a_combo.setCurrentText("5")
        params_layout.addWidget(self.a_combo)

        params_layout.addWidget(QLabel("b (additive):"))
        self.b_spin = QSpinBox()
        self.b_spin.setRange(0, 25)
        self.b_spin.setValue(8)
        params_layout.addWidget(self.b_spin)

        params_layout.addStretch()

        params_group.setLayout(params_layout)
        layout.addWidget(params_group)

        # Texte d'entrée
        input_group = QGroupBox("Texte à chiffrer")
        input_layout = QVBoxLayout()
        self.input_text = QTextEdit()
        self.input_text.setPlaceholderText("Entrez votre texte...")
        self.input_text.setMinimumHeight(120)
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
        self.output_text.setMinimumHeight(120)
        self.output_text.setStyleSheet("background-color: #f9f9f9;")
        output_layout.addWidget(self.output_text)
        output_group.setLayout(output_layout)
        layout.addWidget(output_group)

        self.setLayout(layout)

    def encrypt_text(self):
        text = self.input_text.toPlainText()
        if not text:
            QMessageBox.warning(self, "Attention", "Veuillez entrer un texte!")
            return

        try:
            a = int(self.a_combo.currentText())
            b = self.b_spin.value()
            encrypted = affine.encrypt(text, a, b)
            self.output_text.setPlainText(encrypted)
        except Exception as e:
            QMessageBox.critical(self, "Erreur", str(e))

    def decrypt_text(self):
        text = self.input_text.toPlainText()
        if not text:
            QMessageBox.warning(self, "Attention", "Veuillez entrer un texte!")
            return

        try:
            a = int(self.a_combo.currentText())
            b = self.b_spin.value()
            decrypted = affine.decrypt(text, a, b)
            self.output_text.setPlainText(decrypted)
        except Exception as e:
            QMessageBox.critical(self, "Erreur", str(e))

    def clear_all(self):
        self.input_text.clear()
        self.output_text.clear()