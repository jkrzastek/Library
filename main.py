import sys
import pandas as pd
from PyQt5.QtWidgets import (QApplication, QMainWindow, QTableWidget, QTableWidgetItem,
                             QVBoxLayout, QWidget, QPushButton, QHBoxLayout, QLineEdit, QDialog,
                             QFormLayout, QDialogButtonBox, QMessageBox)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
import csv

class AddRecordDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Dodaj Rekord")
        self.setGeometry(150, 150, 400, 300)

        form_layout = QFormLayout()

        self.title_input = QLineEdit()
        self.author_second_input = QLineEdit()
        self.author_first_input = QLineEdit()
        self.year_input = QLineEdit()
        self.publisher_input = QLineEdit()
        self.type_input = QLineEdit()
        self.isbn_input = QLineEdit()
        self.pages_input = QLineEdit()
        self.color_input = QLineEdit()
        self.place_input = QLineEdit()

        form_layout.addRow("Tytuł:", self.title_input)
        form_layout.addRow("Autor nazwisko:", self.author_second_input)
        form_layout.addRow("Autor imię:", self.author_first_input)
        form_layout.addRow("Rok:", self.year_input)
        form_layout.addRow("Wydawnictwo:", self.publisher_input)
        form_layout.addRow("Rodzaj:", self.type_input)
        form_layout.addRow("ISBN:", self.isbn_input)
        form_layout.addRow("Liczba stron:", self.pages_input)
        form_layout.addRow("Kolor:", self.color_input)
        form_layout.addRow("IDMiejsca:", self.place_input)

        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)

        layout = QVBoxLayout()
        layout.addLayout(form_layout)
        layout.addWidget(button_box)
        self.setLayout(layout)


class LibraryApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Biblioteka")
        self.setGeometry(100, 100, 1650, 400)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        # Layout do wyszukiwania
        search_layout = QHBoxLayout()

        # Ikona lupy
        self.search_icon = QPushButton()
        self.search_icon.setIcon(QIcon('obraz/lupa.png'))  # Upewnij się, że masz ikonę w odpowiednim katalogu
        self.search_icon.setStyleSheet("background: transparent; border: none;")

        # Pole wyszukiwania
        self.search_input = QLineEdit(self)
        self.search_input.setPlaceholderText("Szukaj...")
        self.search_input.setFixedWidth(200)  # Skracamy szerokość
        self.search_input.textChanged.connect(self.search_data)

        # Dodajemy ikonę i pole do layoutu
        search_layout.addWidget(self.search_icon)
        search_layout.addWidget(self.search_input)

        # Ustawienie wyrównania na lewą stronę
        search_layout.setAlignment(Qt.AlignLeft)

        # Dodajemy pustą przestrzeń, aby wymusić wyrównanie
        search_layout.addStretch(1)  # Stretch wymusza, by wszystkie elementy były po lewej stronie

        # Ustawienie marginesów na 0, by lepiej dopasować elementy
        search_layout.setContentsMargins(0, 0, 0, 0)

        # Dodajemy layout wyszukiwania do głównego layoutu
        self.layout.addLayout(search_layout)

        self.table = QTableWidget()
        self.table.setSortingEnabled(True)
        self.layout.addWidget(self.table)

        # Przyciski "Dodaj" i "Usuń"
        buttons_layout = QHBoxLayout()
        self.add_button = QPushButton("Dodaj")
        self.add_button.clicked.connect(self.open_add_record_dialog)
        self.delete_button = QPushButton("Usuń")
        self.delete_button.clicked.connect(self.delete_record)

        buttons_layout.addWidget(self.add_button)
        buttons_layout.addWidget(self.delete_button)
        self.layout.addLayout(buttons_layout)

        self.load_data("data.csv")

        # Podłączamy metodę do śledzenia edycji komórek
        self.table.cellChanged.connect(self.handle_cell_edit)

        self.setStyleSheet("""
            QMainWindow {
                background-color: #1f1f2e;
                color: #f0f0f0;
            }
            QTableWidget {
                background-color: #2b2b38;
                color: #f0f0f0;
                border: 1px solid #444;
            }
            QHeaderView::section {
                background-color: #c7c7d1;
                padding: 5px;
                border: 1px solid #444;
            }
            QPushButton {
                background-color: #5a5a75;
                color: white;
                border: 1px solid #444;
                padding: 10px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #70707f;
            }
            QLineEdit {
                background-color: #3b3b47;
                color: white;
                border: 1px solid #444;
                padding: 5px;
            }
            QLineEdit:focus {
                border-color: #5a5a75;
            }
        """)

    def handle_cell_edit(self, row, col):
        """
        Obsługuje edytowanie komórki w tabeli i zapisuje zmiany w DataFrame.
        """
        new_value = self.table.item(row, col).text()

        # Zaktualizuj wartość w DataFrame
        self.df.iat[row, col] = new_value

        # Zapisz zaktualizowane dane w pliku CSV
        self.save_data()

    def load_data(self, file_path):
        try:
            self.file_path = file_path
            self.df = pd.read_csv(file_path, quotechar='"')

            if "Liczba stron" in self.df.columns:
                self.df["Liczba stron"] = self.df["Liczba stron"].apply(lambda x: int(float(x)) if pd.notna(x) else x)

            self.original_df = self.df.copy()  # Zapisujemy oryginalne dane
            self.refresh_table()


        except FileNotFoundError:
            print("Plik CSV nie został znaleziony.")
            self.df = pd.DataFrame(
                columns=["Tytuł", "Autor nazwisko", "Autor imię", "Rok", "Wydawnictwo", "Rodzaj", "ISBN",
                         "Liczba stron", "Kolor", "IDMiejsca"])
            self.original_df = self.df.copy()  # Zapisujemy pusty DataFrame jako oryginalne dane

        except Exception as e:
            print(f"Błąd podczas wczytywania danych: {e}")
            self.df = pd.DataFrame(
                columns=["Tytuł", "Autor nazwisko", "Autor imię", "Rok", "Wydawnictwo", "Rodzaj", "ISBN",
                         "Liczba stron", "Kolor", "IDMiejsca"])
            self.original_df = self.df.copy()  # Zapisujemy pusty DataFrame jako oryginalne dane

    def refresh_table(self, df_to_display=None):
        if df_to_display is None:
            df_to_display = self.df

        self.table.setRowCount(df_to_display.shape[0])
        self.table.setColumnCount(df_to_display.shape[1])
        self.table.setHorizontalHeaderLabels(list(df_to_display.columns))

        for row in range(df_to_display.shape[0]):
            for col in range(df_to_display.shape[1]):
                value = df_to_display.iat[row, col]
                item = QTableWidgetItem(str(value))
                self.table.setItem(row, col, item)

            # Dodaj przycisk "Usuń" tylko do ostatniego wiersza
            if row == df_to_display.shape[0] - 1:
                delete_button = QPushButton("Usuń")
                delete_button.clicked.connect(lambda _, r=row: self.delete_row(r))
                self.table.setCellWidget(row, df_to_display.shape[1], delete_button)


    def save_data(self):
        #self.df.to_csv(self.file_path, index=False)
        self.df.to_csv(self.file_path, index=False, quoting=csv.QUOTE_ALL)

    def search_data(self):
        search_text = self.search_input.text().lower()

        if search_text == "":
            self.df = self.original_df.copy()  # Przywracamy pełne dane
        else:
            # Filtrowanie wierszy, które zawierają szukany tekst w którejkolwiek z kolumn
            filtered_df = self.original_df[
                self.original_df.apply(lambda row: row.astype(str).str.contains(search_text, case=False).any(), axis=1)
            ]

            # Usunięcie duplikatów
            filtered_df = filtered_df.drop_duplicates().reset_index(drop=True)

            self.df = filtered_df  # Przypisujemy wynik do self.df

        self.refresh_table()  # Odświeżamy tabelę TYLKO RAZ

    def open_add_record_dialog(self):
        dialog = AddRecordDialog(self)
        self.dialog = AddRecordDialog(self)

        if dialog.exec_() == QDialog.Accepted:
            # Odczytanie danych z pól i dodanie nowego rekordu do DataFrame
            new_record = {
                "Tytuł": dialog.title_input.text(),
                "Autor nazwisko": dialog.author_second_input.text(),
                "Autor imię": dialog.author_first_input.text(),
                "Rok": dialog.year_input.text(),
                "Wydawnictwo": dialog.publisher_input.text(),
                "Rodzaj": dialog.type_input.text(),
                "ISBN": dialog.isbn_input.text(),
                "Liczba stron": dialog.pages_input.text(),
                "Kolor": dialog.color_input.text(),
                "IDMiejsca": dialog.place_input.text()
            }


            # Sprawdzenie, czy wszystkie wymagane pola zostały wypełnione
            if any(value == "" for value in new_record.values()):
                QMessageBox.warning(self, "Błąd", "Wszystkie pola muszą być wypełnione!")
                return

            # Konwersja pól na odpowiednie typy (np. liczba stron na int)
            try:
                new_record["Liczba stron"] = int(new_record["Liczba stron"]) if new_record[
                    "Liczba stron"].isdigit() else 0
            except ValueError:
                new_record["Liczba stron"] = 0

            #print(f"Converted Record: {new_record}")  # Zobaczymy, jak wyglądają dane po konwersji


            new_df = pd.DataFrame([new_record], columns=self.df.columns)  # Używamy dokładnie tych samych kolumn!
            self.df = pd.concat([self.df, new_df], ignore_index=True)
            #print(f"DataFrame after adding record:\n{self.df.tail()}")

            # Odświeżenie tabeli i zapisanie danych
            self.refresh_table()
            self.save_data()


    def delete_record(self):
        selected_rows = sorted(set(index.row() for index in self.table.selectedIndexes()), reverse=True)

        if not selected_rows:
            return  # Nic nie zaznaczono

        reply = QMessageBox.question(self, "Potwierdzenie", "Czy na pewno chcesz usunąć zaznaczone rekordy?",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            self.df.drop(selected_rows, inplace=True)
            self.df.reset_index(drop=True, inplace=True)
            self.refresh_table()
            self.save_data()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LibraryApp()
    window.show()
    sys.exit(app.exec_())
