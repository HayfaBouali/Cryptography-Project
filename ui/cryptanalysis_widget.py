"""Widget pour la cryptanalyse"""
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                               QTextEdit, QPushButton, QGroupBox, QTableWidget,
                               QTableWidgetItem, QMessageBox, QComboBox)
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor
from cryptanalysis import frequency_analysis
from algorithms import caesar
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas


class CryptanalysisWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        """Initialise l'interface"""
        layout = QVBoxLayout()

        # En-tête
        title = QLabel("<h1>Cryptanalyse</h1>")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        description = QLabel(
            "Outils d'analyse pour casser les chiffrements classiques "
            "par analyse de fréquence et force brute."
        )
        description.setWordWrap(True)
        description.setStyleSheet("color: #666; padding: 10px;")
        layout.addWidget(description)

        # Choix de l'analyse
        analysis_group = QGroupBox("Type d'analyse")
        analysis_layout = QHBoxLayout()

        analysis_layout.addWidget(QLabel("Méthode:"))
        self.analysis_combo = QComboBox()
        self.analysis_combo.addItems([
            "Analyse de fréquence",
            "Force brute (César)",
            "Test du Chi²"
        ])
        analysis_layout.addWidget(self.analysis_combo)
        analysis_layout.addStretch()

        analysis_group.setLayout(analysis_layout)
        layout.addWidget(analysis_group)

        # Zone de texte chiffré
        input_group = QGroupBox("Texte chiffré")
        input_layout = QVBoxLayout()
        self.input_text = QTextEdit()
        self.input_text.setPlaceholderText("Entrez le texte chiffré à analyser...")
        self.input_text.setMaximumHeight(100)
        input_layout.addWidget(self.input_text)
        input_group.setLayout(input_layout)
        layout.addWidget(input_group)

        # Bouton d'analyse
        analyze_btn = QPushButton("🔍 Analyser")
        analyze_btn.clicked.connect(self.analyze)
        analyze_btn.setStyleSheet("""
            QPushButton {
                background-color: #9C27B0;
                color: white;
                padding: 10px;
                font-size: 14px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #7B1FA2;
            }
        """)
        layout.addWidget(analyze_btn)

        # Résultats
        results_group = QGroupBox("Résultats")
        results_layout = QVBoxLayout()

        self.results_table = QTableWidget()
        self.results_table.setMaximumHeight(200)
        results_layout.addWidget(self.results_table)

        self.results_text = QTextEdit()
        self.results_text.setReadOnly(True)
        self.results_text.setStyleSheet("background-color: #f9f9f9;")
        results_layout.addWidget(self.results_text)

        results_group.setLayout(results_layout)
        layout.addWidget(results_group)

        self.setLayout(layout)

    def analyze(self):
        """Lance l'analyse"""
        text = self.input_text.toPlainText()

        if not text:
            QMessageBox.warning(self, "Attention", "Veuillez entrer un texte!")
            return

        method = self.analysis_combo.currentText()

        if method == "Analyse de fréquence":
            self.frequency_analysis(text)
        elif method == "Force brute (César)":
            self.brute_force_caesar(text)
        elif method == "Test du Chi²":
            self.chi_squared_analysis(text)

    def frequency_analysis(self, text):
        """Analyse de fréquence"""
        freq = frequency_analysis.analyze_frequency(text)
        most_common = frequency_analysis.get_most_common(text, 10)

        # Afficher dans le tableau
        self.results_table.setColumnCount(2)
        self.results_table.setHorizontalHeaderLabels(["Lettre", "Fréquence (%)"])
        self.results_table.setRowCount(len(most_common))

        for i, (letter, frequency) in enumerate(most_common):
            self.results_table.setItem(i, 0, QTableWidgetItem(letter))
            freq_item = QTableWidgetItem(f"{frequency:.2f}%")
            self.results_table.setItem(i, 1, freq_item)

        self.results_table.resizeColumnsToContents()

        # Texte d'analyse
        analysis_text = f"""=== ANALYSE DE FRÉQUENCE ===

📊 Les 5 lettres les plus fréquentes:
"""
        for i, (letter, freq) in enumerate(most_common[:5], 1):
            analysis_text += f"{i}. {letter}: {freq:.2f}%\n"

        analysis_text += f"""
💡 En français, les lettres les plus fréquentes sont: E, A, S, I, N, T, R

🔍 Suggestions:
- Si '{most_common[0][0]}' apparaît le plus, il pourrait représenter 'E'
- Cherchez des motifs courts qui pourraient être des articles (LE, LA, UN, DE)
"""

        self.results_text.setPlainText(analysis_text)

    def brute_force_caesar(self, text):
        """Force brute sur César"""
        results = caesar.brute_force(text)

        # Afficher dans le tableau
        self.results_table.setColumnCount(2)
        self.results_table.setHorizontalHeaderLabels(["Décalage", "Texte déchiffré"])
        self.results_table.setRowCount(len(results))

        for i, (shift, decrypted) in enumerate(results):
            self.results_table.setItem(i, 0, QTableWidgetItem(str(shift)))
            preview = decrypted[:80] + "..." if len(decrypted) > 80 else decrypted
            self.results_table.setItem(i, 1, QTableWidgetItem(preview))

        self.results_table.resizeColumnsToContents()

        analysis_text = """=== FORCE BRUTE (CÉSAR) ===

🔓 Tous les déchiffrements possibles sont affichés ci-dessus.

💡 Pour identifier le bon texte:
1. Cherchez un texte qui a du sens
2. Vérifiez la présence de mots français courants
3. La structure grammaticale doit être correcte
"""

        self.results_text.setPlainText(analysis_text)

    def chi_squared_analysis(self, text):
        """Test du Chi²"""
        best_shift, chi_value = frequency_analysis.chi_squared_test(text)
        decrypted = caesar.decrypt(text, best_shift)

        # Afficher le résultat
        self.results_table.setColumnCount(2)
        self.results_table.setHorizontalHeaderLabels(["Paramètre", "Valeur"])
        self.results_table.setRowCount(2)

        self.results_table.setItem(0, 0, QTableWidgetItem("Décalage trouvé"))
        self.results_table.setItem(0, 1, QTableWidgetItem(str(best_shift)))

        self.results_table.setItem(1, 0, QTableWidgetItem("Chi² score"))
        self.results_table.setItem(1, 1, QTableWidgetItem(f"{chi_value:.2f}"))

        self.results_table.resizeColumnsToContents()

        analysis_text = f"""=== TEST DU CHI² ===

✅ Meilleur décalage trouvé: {best_shift}
📊 Score Chi²: {chi_value:.2f}

📝 Texte déchiffré:
{decrypted}

💡 Le test du Chi² compare la distribution des lettres du texte
   avec la distribution attendue en français.
   Plus le score est bas, meilleur est le déchiffrement.
"""

        self.results_text.setPlainText(analysis_text)