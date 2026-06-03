"""Widget pour le chiffrement de Porta"""
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                               QTextEdit, QPushButton, QLineEdit, QGroupBox,
                               QMessageBox, QTableWidget, QTableWidgetItem,
                               QAbstractItemView, QScrollArea)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QColor
from algorithms import porta


class PortaWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        """Initialise l'interface utilisateur"""
        # ✅ ScrollArea principale pour tout le widget
        main_scroll = QScrollArea()
        main_scroll.setWidgetResizable(True)
        main_scroll.setStyleSheet("QScrollArea { border: none; }")

        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setSpacing(10)
        layout.setContentsMargins(15, 15, 15, 15)

        # En-tête avec titre
        title = QLabel("<h1>🚪 Chiffrement de Porta</h1>")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        # Description de l'algorithme
        description = QLabel(
            "<p style='font-size: 11pt;'>"
            "Le <b>chiffrement de Porta</b> est un chiffrement polyalphabétique "
            "créé par Giovanni Battista della Porta au XVIe siècle.<br><br>"
            "<b>🔑 Caractéristiques :</b><br>"
            "• Utilise un tableau de 13 lignes (paires de lettres AB, CD, EF...)<br>"
            "• Chaque ligne contient un alphabet mélangé<br>"
            "• <b>Particularité : C'est un chiffrement réciproque</b> "
            "(chiffrer = déchiffrer)<br>"
            "• La clé détermine quelle ligne du tableau utiliser pour chaque lettre<br><br>"
            "<b>💡 Avantage :</b> Plus sécurisé que César, mais plus simple que Vigenère"
            "</p>"
        )
        description.setWordWrap(True)
        description.setStyleSheet("""
            background-color: #e3f2fd;
            padding: 15px;
            border-radius: 8px;
            border-left: 4px solid #2196F3;
        """)
        layout.addWidget(description)

        # Affichage du tableau de Porta
        self.create_porta_table(layout)

        # Groupe de paramètres
        params_group = QGroupBox("⚙️ Paramètres")
        params_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                font-size: 12pt;
                border: 2px solid #cccccc;
                border-radius: 6px;
                margin-top: 10px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
            }
        """)
        params_layout = QHBoxLayout()

        key_label = QLabel("Clé alphabétique :")
        key_label.setStyleSheet("font-size: 11pt;")
        params_layout.addWidget(key_label)

        self.key_input = QLineEdit()
        self.key_input.setPlaceholderText("Ex: SECRET, CRYPTO, PORTA")
        self.key_input.setStyleSheet("""
            QLineEdit {
                padding: 8px;
                font-size: 11pt;
                border: 2px solid #9C27B0;
                border-radius: 4px;
            }
            QLineEdit:focus {
                border: 2px solid #7B1FA2;
            }
        """)
        params_layout.addWidget(self.key_input)
        params_layout.addStretch()
        params_group.setLayout(params_layout)
        layout.addWidget(params_group)

        # Zone de texte d'entrée
        input_group = QGroupBox("📝 Texte à traiter")
        input_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                font-size: 12pt;
                border: 2px solid #cccccc;
                border-radius: 6px;
                margin-top: 10px;
                padding-top: 10px;
            }
        """)
        input_layout = QVBoxLayout()

        self.input_text = QTextEdit()
        self.input_text.setPlaceholderText("Entrez votre texte ici...\n\nExemple : HELLO WORLD")
        self.input_text.setStyleSheet("""
            QTextEdit {
                font-size: 11pt;
                padding: 10px;
                border: 2px solid #ddd;
                border-radius: 4px;
                background-color: white;
            }
            QTextEdit:focus {
                border: 2px solid #9C27B0;
            }
        """)
        self.input_text.setFixedHeight(100)
        input_layout.addWidget(self.input_text)
        input_group.setLayout(input_layout)
        layout.addWidget(input_group)

        # Boutons d'action
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(10)

        process_btn = QPushButton("🔄 Chiffrer / Déchiffrer")
        process_btn.clicked.connect(self.process_text)
        process_btn.setCursor(Qt.PointingHandCursor)
        process_btn.setStyleSheet("""
            QPushButton {
                background-color: #9C27B0;
                color: white;
                padding: 12px 24px;
                font-size: 13pt;
                font-weight: bold;
                border: none;
                border-radius: 6px;
            }
            QPushButton:hover { background-color: #7B1FA2; }
            QPushButton:pressed { background-color: #6A1B9A; }
        """)
        buttons_layout.addWidget(process_btn)

        clear_btn = QPushButton("🗑️ Effacer tout")
        clear_btn.clicked.connect(self.clear_all)
        clear_btn.setCursor(Qt.PointingHandCursor)
        clear_btn.setStyleSheet("""
            QPushButton {
                background-color: #f44336;
                color: white;
                padding: 12px 24px;
                font-size: 13pt;
                font-weight: bold;
                border: none;
                border-radius: 6px;
            }
            QPushButton:hover { background-color: #d32f2f; }
            QPushButton:pressed { background-color: #c62828; }
        """)
        buttons_layout.addWidget(clear_btn)

        example_btn = QPushButton("💡 Charger un exemple")
        example_btn.clicked.connect(self.load_example)
        example_btn.setCursor(Qt.PointingHandCursor)
        example_btn.setStyleSheet("""
            QPushButton {
                background-color: #FF9800;
                color: white;
                padding: 12px 24px;
                font-size: 13pt;
                font-weight: bold;
                border: none;
                border-radius: 6px;
            }
            QPushButton:hover { background-color: #F57C00; }
            QPushButton:pressed { background-color: #E65100; }
        """)
        buttons_layout.addWidget(example_btn)
        layout.addLayout(buttons_layout)

        # Zone de résultat
        output_group = QGroupBox("✅ Résultat")
        output_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                font-size: 12pt;
                border: 2px solid #4CAF50;
                border-radius: 6px;
                margin-top: 10px;
                padding-top: 10px;
            }
        """)
        output_layout = QVBoxLayout()

        self.output_text = QTextEdit()
        self.output_text.setReadOnly(True)
        self.output_text.setPlaceholderText("Le résultat apparaîtra ici...")
        self.output_text.setStyleSheet("""
            QTextEdit {
                font-size: 11pt;
                padding: 10px;
                border: 2px solid #ddd;
                border-radius: 4px;
                background-color: #f9f9f9;
                font-family: 'Courier New', monospace;
            }
        """)
        self.output_text.setFixedHeight(180)
        output_layout.addWidget(self.output_text)

        copy_btn = QPushButton("📋 Copier le résultat")
        copy_btn.clicked.connect(self.copy_result)
        copy_btn.setCursor(Qt.PointingHandCursor)
        copy_btn.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                padding: 8px 16px;
                font-size: 11pt;
                border: none;
                border-radius: 4px;
            }
            QPushButton:hover { background-color: #1976D2; }
        """)
        output_layout.addWidget(copy_btn)
        output_group.setLayout(output_layout)
        layout.addWidget(output_group)

        # ✅ Appliquer le container dans le scroll
        main_scroll.setWidget(container)

        outer_layout = QVBoxLayout()
        outer_layout.setContentsMargins(0, 0, 0, 0)
        outer_layout.addWidget(main_scroll)
        self.setLayout(outer_layout)

    def create_porta_table(self, parent_layout):
        """Crée et affiche le tableau de Porta"""
        table_group = QGroupBox("📊 Tableau de Porta (pour référence)")
        table_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                font-size: 11pt;
                border: 2px solid #9C27B0;
                border-radius: 6px;
                margin-top: 10px;
                padding-top: 10px;
            }
        """)
        table_layout = QVBoxLayout()

        # ✅ Tableau bien configuré
        self.porta_table = QTableWidget()
        self.porta_table.setFixedHeight(320)
        self.porta_table.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.porta_table.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.porta_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.porta_table.setSelectionMode(QAbstractItemView.NoSelection)

        rows = list(porta.PORTA_TABLE.keys())
        self.porta_table.setRowCount(len(rows))
        self.porta_table.setColumnCount(27)

        headers = ["Clé"] + list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
        self.porta_table.setHorizontalHeaderLabels(headers)

        # Remplir le tableau
        for i, key in enumerate(rows):
            key_item = QTableWidgetItem(key)
            key_item.setFont(QFont("Arial", 9, QFont.Bold))
            key_item.setBackground(QColor("#E1BEE7"))
            key_item.setTextAlignment(Qt.AlignCenter)
            self.porta_table.setItem(i, 0, key_item)

            alphabet_row = porta.PORTA_TABLE[key]
            for j, char in enumerate(alphabet_row):
                item = QTableWidgetItem(char)
                item.setTextAlignment(Qt.AlignCenter)
                item.setFont(QFont("Courier New", 9))
                # ✅ Alternance de couleurs par ligne
                if i % 2 == 0:
                    item.setBackground(QColor("#F3E5F5"))
                self.porta_table.setItem(i, j + 1, item)

        # Style
        self.porta_table.setStyleSheet("""
            QTableWidget {
                gridline-color: #9C27B0;
                border: 1px solid #9C27B0;
                font-size: 9pt;
            }
            QTableWidget::item {
                padding: 2px;
            }
            QHeaderView::section {
                background-color: #9C27B0;
                color: white;
                font-weight: bold;
                padding: 4px;
                border: 1px solid #7B1FA2;
                font-size: 9pt;
            }
        """)

        # ✅ Tailles fixes pour éviter le chevauchement
        self.porta_table.setColumnWidth(0, 45)
        for col in range(1, 27):
            self.porta_table.setColumnWidth(col, 28)
        for row in range(self.porta_table.rowCount()):
            self.porta_table.setRowHeight(row, 26)

        # Explication
        explanation = QLabel(
            "<i>📖 Comment utiliser ce tableau :</i><br>"
            "1. La <b>clé</b> détermine quelle ligne utiliser<br>"
            "2. Trouvez votre lettre en clair dans les colonnes (A-Z)<br>"
            "3. La lettre à l'intersection est la lettre chiffrée<br>"
            "4. Pour déchiffrer, utilisez exactement le même processus !"
        )
        explanation.setWordWrap(True)
        explanation.setStyleSheet("padding: 8px; font-size: 10pt; color: #555;")

        table_layout.addWidget(self.porta_table)
        table_layout.addWidget(explanation)
        table_group.setLayout(table_layout)
        parent_layout.addWidget(table_group)

    def process_text(self):
        """Chiffre ou déchiffre le texte"""
        text = self.input_text.toPlainText()
        key = self.key_input.text()

        if not text:
            QMessageBox.warning(self, "⚠️ Attention", "Veuillez entrer un texte à traiter!")
            return
        if not key:
            QMessageBox.warning(self, "⚠️ Attention", "Veuillez entrer une clé!\n\nExemple : SECRET")
            return
        if not key.isalpha():
            QMessageBox.warning(self, "⚠️ Attention", "La clé doit contenir uniquement des lettres!")
            return

        try:
            result = porta.encrypt(text, key)
            output = f"""╔══════════════════════════════════════════════╗
║           RÉSULTAT DU CHIFFREMENT            ║
╚══════════════════════════════════════════════╝

🔑 Clé utilisée : {key.upper()}
📊 Longueur du texte : {len(text)} caractères
📊 Longueur du résultat : {len(result)} caractères

📝 Texte original :
{text}

🔒 Résultat :
{result}

💡 Info : Le chiffre de Porta est RÉCIPROQUE.
   Pour déchiffrer, utilisez la même clé et cliquez à nouveau !
"""
            self.output_text.setPlainText(output)

        except Exception as e:
            QMessageBox.critical(self, "❌ Erreur", f"Une erreur s'est produite :\n\n{str(e)}")

    def clear_all(self):
        """Efface tous les champs"""
        self.input_text.clear()
        self.output_text.clear()
        self.key_input.clear()

    def load_example(self):
        """Charge un exemple de démonstration"""
        self.input_text.setPlainText("BONJOUR LE MONDE")
        self.key_input.setText("CRYPTOGRAPHIE")
        QMessageBox.information(
            self, "💡 Exemple chargé",
            "Un exemple a été chargé !\n\n"
            "• Texte : BONJOUR LE MONDE\n"
            "• Clé : CRYPTOGRAPHIE\n\n"
            "Cliquez sur 'Chiffrer / Déchiffrer' pour voir le résultat."
        )

    def copy_result(self):
        """Copie le résultat dans le presse-papier"""
        from PySide6.QtWidgets import QApplication
        result = self.output_text.toPlainText()
        if result and result != "Le résultat apparaîtra ici...":
            clipboard = QApplication.clipboard()
            clipboard.setText(result)
            QMessageBox.information(self, "✅ Copié", "Le résultat a été copié dans le presse-papier !")
        else:
            QMessageBox.warning(self, "⚠️ Attention", "Aucun résultat à copier !")