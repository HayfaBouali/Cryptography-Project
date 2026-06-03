"""Fenêtre principale avec TOUS les algorithmes"""
from PySide6.QtWidgets import (QMainWindow, QTabWidget, QMessageBox)
from PySide6.QtGui import QAction

from ui.caesar_widget import CaesarWidget
from ui.affine_widget import AffineWidget
from ui.vigenere_widget import VigenereWidget
from ui.porta_widget import PortaWidget
from ui.substitution_widget import SubstitutionWidget
from ui.transposition_widget import TranspositionWidget
from ui.adfgvx_widget import ADFGVXWidget
from ui.rsa_widget import RSAWidget
from ui.cryptanalysis_widget import CryptanalysisWidget


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Application de Cryptographie - Projet Complet")
        self.setGeometry(100, 100, 1400, 900)

        self.init_ui()
        self.create_menu()

    def init_ui(self):
        """Initialise l'interface utilisateur"""
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        # Tous les algorithmes vus en cours
        self.tabs.addTab(CaesarWidget(), "🔤 César")
        self.tabs.addTab(AffineWidget(), "🔢 Affine")
        self.tabs.addTab(VigenereWidget(), "🔑 Vigenère")
        self.tabs.addTab(PortaWidget(), "🚪 Porta")
        self.tabs.addTab(SubstitutionWidget(), "🔄 Substitution (Alphabets)")
        self.tabs.addTab(TranspositionWidget(), "↔️ Transposition")
        self.tabs.addTab(ADFGVXWidget(), "⚔️ ADFGVX")
        self.tabs.addTab(RSAWidget(), "🔐 RSA")
        self.tabs.addTab(CryptanalysisWidget(), "🔍 Cryptanalyse")

        # Style moderne
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f5f5f5;
            }
            QTabWidget::pane {
                border: 2px solid #cccccc;
                background-color: white;
                border-radius: 5px;
            }
            QTabBar::tab {
                background-color: #e0e0e0;
                padding: 12px 25px;
                margin: 2px;
                border-top-left-radius: 5px;
                border-top-right-radius: 5px;
                font-weight: bold;
            }
            QTabBar::tab:selected {
                background-color: white;
                border-bottom: 3px solid #2196F3;
            }
            QTabBar::tab:hover {
                background-color: #d0d0d0;
            }
        """)

    def create_menu(self):
        """Crée la barre de menu"""
        menubar = self.menuBar()

        # Menu Fichier
        file_menu = menubar.addMenu("&Fichier")

        quit_action = QAction("&Quitter", self)
        quit_action.setShortcut("Ctrl+Q")
        quit_action.triggered.connect(self.close)
        file_menu.addAction(quit_action)

        # Menu Aide
        help_menu = menubar.addMenu("&Aide")

        about_action = QAction("&À propos", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)

        algo_info_action = QAction("&Info Algorithmes", self)
        algo_info_action.triggered.connect(self.show_algo_info)
        help_menu.addAction(algo_info_action)

    def show_about(self):
        """Affiche À propos"""
        QMessageBox.about(self, "À propos",
                          """<h2>Application de Cryptographie</h2>
                          <p><b>Version 2.0 - Projet Complet</b></p>
                          <p>Tous les algorithmes vus en cours :</p>
                          <ul>
                              <li>✅ César</li>
                              <li>✅ Affine</li>
                              <li>✅ Vigenère</li>
                              <li>✅ Porta</li>
                              <li>✅ Substitution (Alphabets désordonnés)</li>
                              <li>✅ Transposition</li>
                              <li>✅ ADFGVX</li>
                              <li>✅ RSA</li>
                              <li>✅ Analyse de fréquence</li>
                          </ul>
                          <p>Développé avec Python et PySide6</p>
                          """)

    def show_algo_info(self):
        """Affiche les informations sur les algorithmes"""
        QMessageBox.information(self, "Informations sur les algorithmes",
                                """<h3>Guide des algorithmes</h3>
                    
                                <p><b>📌 César:</b> Décalage simple de l'alphabet</p>
                                <p><b>📌 Affine:</b> C = (a×P + b) mod 26</p>
                                <p><b>📌 Vigenère:</b> Chiffrement polyalphabétique</p>
                                <p><b>📌 Porta:</b> Tableau de substitution réciproque</p>
                                <p><b>📌 Substitution:</b> Alphabets désordonnés (horizontal/vertical)</p>
                                <p><b>📌 Transposition:</b> Réarrangement des lettres</p>
                                <p><b>📌 ADFGVX:</b> Substitution + Transposition</p>
                                <p><b>📌 RSA:</b> Cryptographie asymétrique</p>
                                <p><b>📌 Cryptanalyse:</b> Analyse de fréquence et force brute</p>
                                """)