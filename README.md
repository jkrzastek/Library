# Biblioteka - Aplikacja do zarządzania rekordami książek

Biblioteka to aplikacja desktopowa, która pozwala na zarządzanie rekordami książek. Umożliwia dodawanie, usuwanie oraz edytowanie danych o książkach, takich jak tytuł, autorzy, rok wydania, ISBN, liczba stron i inne. Aplikacja umożliwia również wyszukiwanie książek w oparciu o różne pola.

## Funkcjonalności

- **Dodawanie rekordów**: Możliwość dodania nowego rekordu książki poprzez formularz zawierający pola takie jak tytuł, autor, rok wydania, ISBN, liczba stron itp.
- **Usuwanie rekordów**: Możliwość usuwania zaznaczonych rekordów z tabeli.
- **Edycja rekordów**: Użytkownik może edytować dane książek bezpośrednio w tabeli.
- **Wyszukiwanie**: Pole wyszukiwania umożliwia szybkie filtrowanie rekordów na podstawie wpisanego tekstu. Wyszukiwanie odbywa się we wszystkich kolumnach.
- **Sortowanie**: Możliwość sortowania danych po każdej z kolumn w tabeli.
- **Zapis danych**: Wszystkie zmiany są automatycznie zapisywane do pliku CSV.

## Instalacja

Aby uruchomić aplikację, musisz mieć zainstalowane następujące biblioteki:

1. PyQt5
2. pandas

Możesz zainstalować je za pomocą pip:

```bash
pip install PyQt5 pandas
