import os
import zipfile

# Ścieżka do folderu, gdzie znajduje się skrypt, czyli "Arkusze"
sciezka_glowna = os.path.dirname(os.path.abspath(__file__))

for nazwa_folderu in os.listdir(sciezka_glowna):
    sciezka_roku = os.path.join(sciezka_glowna, nazwa_folderu)

    # Sprawdź, czy to folder i czy jego nazwa to liczba (czyli np. 2025)
    if os.path.isdir(sciezka_roku) and nazwa_folderu.isdigit():
        for plik in os.listdir(sciezka_roku):
            sciezka_pliku = os.path.join(sciezka_roku, plik)

            if os.path.isfile(sciezka_pliku) and plik.lower().endswith('.zip'):
                # Nazwa folderu docelowego: ta sama co plik ZIP, ale bez rozszerzenia
                nazwa_folderu_docelowego = os.path.splitext(plik)[0]
                sciezka_docelowa = os.path.join(sciezka_roku, nazwa_folderu_docelowego)

                # Stwórz folder docelowy, jeśli nie istnieje
                os.makedirs(sciezka_docelowa, exist_ok=True)

                try:
                    with zipfile.ZipFile(sciezka_pliku, 'r') as zip_ref:
                        zip_ref.extractall(sciezka_docelowa)
                        print(f"Rozpakowano: {plik} → {nazwa_folderu_docelowego}/")
                except zipfile.BadZipFile:
                    print(f"Błąd: uszkodzony plik ZIP - {plik}")
