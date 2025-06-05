import os

def fix_pdf_names(start_dir='.'):
    """Zamienia nazwy plików .pdf.pdf na .pdf w całym katalogu"""
    for root, _, files in os.walk(start_dir):
        for name in files:
            if name.endswith('.pdf.pdf'):
                old_path = os.path.join(root, name)
                new_name = name[:-4]  # usuwa ostatnie ".pdf"
                new_path = os.path.join(root, new_name)
                
                # Sprawdzenie, czy nie nadpiszemy istniejącego pliku
                if not os.path.exists(new_path):
                    os.rename(old_path, new_path)
                    print(f"Zmieniono nazwę: {old_path} -> {new_path}")
                else:
                    print(f" Plik docelowy już istnieje, pominięto: {old_path}")

if __name__ == "__main__":
    fix_pdf_names('.')
