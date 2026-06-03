"""Widget pour la transposition"""
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                               QTextEdit, QPushButton, QLineEdit, QGroupBox,
                               QMessageBox, QRadioButton, QButtonGroup, QSpinBox)
from PySide6.QtCore import Qt
from algorithms import transposition


class TranspositionWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # En-tête
        title = QLabel("<h1>Chiffrement par Transposition</h1>")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        description = QLabel(
            "La transposition réarrange les lettres du message sans les remplacer.<br>"
            "• <b>Columaire:</b> Écriture horizontale, lecture verticale par colonnes<br>"
            "• <b>Rail Fence:</b> Écriture en zigzag"
        )
        description.setWordWrap(True)
        description.setStyleSheet("color: #555; padding: 10px; background-color: #fce4ec; border-radius: 5px;")
        layout.addWidget(description)

        # Type de transposition
        type_group = QGroupBox("Type de transposition")
        type_layout = QVBoxLayout()

        self.radio_group = QButtonGroup()
        self.radio_columnar = QRadioButton("Transposition columaire")
        self.radio_rail = QRadioButton("Rail Fence (Zigzag)")

        self.radio_columnar.setChecked(True)
        self.radio_columnar.toggled.connect(self.update_params_visibility)

        self.radio_group.addButton(self.radio_columnar, 1)
        self.radio_group.addButton(self.radio_rail, 2)

        type_layout.addWidget(self.radio_columnar)
        type_layout.addWidget(self.radio_rail)

        type_group.setLayout(type_layout)
        layout.addWidget(type_group)

        # Paramètres columaire
        self.columnar_group = QGroupBox("Paramètres (Transposition columaire)")
        columnar_layout = QHBoxLayout()
        columnar_layout.addWidget(QLabel("Clé:"))
        self.key_input = QLineEdit()
        self.key_input.setPlaceholderText("Ex: CRYPTO")
        columnar_layout.addWidget(self.key_input)
        self.columnar_group.setLayout(columnar_layout)
        layout.addWidget(self.columnar_group)

        # Paramètres rail fence
        self.rail_group = QGroupBox("Paramètres (Rail Fence)")
        rail_layout = QHBoxLayout()
        rail_layout.addWidget(QLabel("Nombre de rails:"))
        self.rails_spin = QSpinBox()
        self.rails_spin.setRange(2, 10)
        self.rails_spin.setValue(3)
        rail_layout.addWidget(self.rails_spin)
        rail_layout.addStretch()
        self.rail_group.setLayout(rail_layout)
        self.rail_group.setVisible(False)
        layout.addWidget(self.rail_group)

        # Texte d'entrée
        input_group = QGroupBox("Texte")
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

    def update_params_visibility(self):
        """Met à jour la visibilité des paramètres"""
        is_columnar = self.radio_columnar.isChecked()
        self.columnar_group.setVisible(is_columnar)
        self.rail_group.setVisible(not is_columnar)

    def encrypt_text(self):
        text = self.input_text.toPlainText()

        if not text:
            QMessageBox.warning(self, "Attention", "Veuillez entrer un texte!")
            return

        try:
            if self.radio_columnar.isChecked():
                key = self.key_input.text()
                if not key:
                    QMessageBox.warning(self, "Attention", "Veuillez entrer une clé!")
                    return
                encrypted = transposition.encrypt_columnar(text, key)
            else:
                rails = self.rails_spin.value()
                encrypted = transposition.encrypt_rail_fence(text, rails)

            self.output_text.setPlainText(encrypted)
        except Exception as e:
            QMessageBox.critical(self, "Erreur", str(e))

    def decrypt_text(self):
        text = self.input_text.toPlainText()

        if not text:
            QMessageBox.warning(self, "Attention", "Veuillez entrer un texte!")
            return

        try:
            if self.radio_columnar.isChecked():
                key = self.key_input.text()
                if not key:
                    QMessageBox.warning(self, "Attention", "Veuillez entrer une clé!")
                    return
                decrypted = transposition.decrypt_columnar(text, key)
            else:
                rails = self.rails_spin.value()
                decrypted = transposition.decrypt_rail_fence(text, rails)

            self.output_text.setPlainText(decrypted)
        except Exception as e:
            QMessageBox.critical(self, "Erreur", str(e))

    def clear_all(self):
        self.input_text.clear()
        self.output_text.clear()