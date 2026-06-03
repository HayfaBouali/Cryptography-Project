"""Widget pour la substitution avec alphabets désordonnés"""
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                               QTextEdit, QPushButton, QLineEdit, QGroupBox,
                               QMessageBox, QRadioButton, QButtonGroup)
from PySide6.QtCore import Qt
from algorithms import substitution


class SubstitutionWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # En-tête
        title = QLabel("<h1>Substitution - Alphabets Désordonnés</h1>")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        description = QLabel(
            "Construction d'alphabets de substitution:<br>"
            "• <b>Horizontal:</b> Mot-clé + reste de l'alphabet<br>"
            "• <b>Vertical:</b> Mot-clé placé verticalement dans une grille"
        )
        description.setWordWrap(True)
        description.setStyleSheet("color: #555; padding: 10px; background-color: #fff3e0; border-radius: 5px;")
        layout.addWidget(description)

        # Type de construction
        construction_group = QGroupBox("Type de construction")
        construction_layout = QVBoxLayout()

        self.radio_group = QButtonGroup()

        self.radio_random = QRadioButton("Aléatoire")
        self.radio_horizontal = QRadioButton("Horizontal (mot-clé)")
        self.radio_vertical = QRadioButton("Vertical (mot-clé)")

        self.radio_horizontal.setChecked(True)

        self.radio_group.addButton(self.radio_random, 1)
        self.radio_group.addButton(self.radio_horizontal, 2)
        self.radio_group.addButton(self.radio_vertical, 3)

        construction_layout.addWidget(self.radio_random)
        construction_layout.addWidget(self.radio_horizontal)
        construction_layout.addWidget(self.radio_vertical)

        construction_group.setLayout(construction_layout)
        layout.addWidget(construction_group)

        # Mot-clé
        key_group = QGroupBox("Mot-clé (pour construction horizontal/vertical)")
        key_layout = QHBoxLayout()

        self.keyword_input = QLineEdit()
        self.keyword_input.setPlaceholderText("Ex: CRYPTOGRAPHIE")
        key_layout.addWidget(self.keyword_input)

        gen_btn = QPushButton("🔑 Générer l'alphabet")
        gen_btn.clicked.connect(self.generate_alphabet)
        gen_btn.setStyleSheet("""
            QPushButton {
                background-color: #FF9800;
                color: white;
                padding: 8px;
                border-radius: 4px;
            }
            QPushButton:hover { background-color: #F57C00; }
        """)
        key_layout.addWidget(gen_btn)

        key_group.setLayout(key_layout)
        layout.addWidget(key_group)

        # Alphabet de substitution
        alphabet_group = QGroupBox("Alphabet de substitution généré")
        alphabet_layout = QVBoxLayout()

        self.alphabet_display = QTextEdit()
        self.alphabet_display.setMaximumHeight(80)
        self.alphabet_display.setReadOnly(True)
        self.alphabet_display.setStyleSheet("background-color: #e8f5e9; font-family: monospace; font-size: 14px;")
        alphabet_layout.addWidget(self.alphabet_display)

        alphabet_group.setLayout(alphabet_layout)
        layout.addWidget(alphabet_group)

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

    def generate_alphabet(self):
        """Génère l'alphabet de substitution"""
        method_id = self.radio_group.checkedId()

        try:
            if method_id == 1:  # Aléatoire
                alphabet = substitution.generate_random_alphabet()
            elif method_id == 2:  # Horizontal
                keyword = self.keyword_input.text()
                if not keyword:
                    QMessageBox.warning(self, "Attention", "Veuillez entrer un mot-clé!")
                    return
                alphabet = substitution.generate_keyword_alphabet(keyword)
            elif method_id == 3:  # Vertical
                keyword = self.keyword_input.text()
                if not keyword:
                    QMessageBox.warning(self, "Attention", "Veuillez entrer un mot-clé!")
                    return
                alphabet = substitution.generate_vertical_alphabet(keyword)

            # Afficher l'alphabet normal et de substitution
            normal = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
            display = f"Normal:       {normal}\nSubstitution: {alphabet}"
            self.alphabet_display.setPlainText(display)

        except Exception as e:
            QMessageBox.critical(self, "Erreur", str(e))

    def encrypt_text(self):
        text = self.input_text.toPlainText()
        alphabet = self.alphabet_display.toPlainText()

        if not text:
            QMessageBox.warning(self, "Attention", "Veuillez entrer un texte!")
            return

        if not alphabet or "Substitution:" not in alphabet:
            QMessageBox.warning(self, "Attention", "Veuillez générer un alphabet de substitution!")
            return

        try:
            # Extraire l'alphabet de substitution
            sub_alphabet = alphabet.split("Substitution:")[1].strip()
            encrypted = substitution.encrypt(text, sub_alphabet)
            self.output_text.setPlainText(encrypted)
        except Exception as e:
            QMessageBox.critical(self, "Erreur", str(e))

    def decrypt_text(self):
        text = self.input_text.toPlainText()
        alphabet = self.alphabet_display.toPlainText()

        if not text:
            QMessageBox.warning(self, "Attention", "Veuillez entrer un texte!")
            return

        if not alphabet or "Substitution:" not in alphabet:
            QMessageBox.warning(self, "Attention", "Veuillez générer un alphabet de substitution!")
            return

        try:
            sub_alphabet = alphabet.split("Substitution:")[1].strip()
            decrypted = substitution.decrypt(text, sub_alphabet)
            self.output_text.setPlainText(decrypted)
        except Exception as e:
            QMessageBox.critical(self, "Erreur", str(e))

    def clear_all(self):
        self.input_text.clear()
        self.output_text.clear()