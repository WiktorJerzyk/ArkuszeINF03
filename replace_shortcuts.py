import os
import requests

def is_internet_shortcut(file_path):
    """Sprawdza, czy plik zawiera [InternetShortcut] i URL"""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
        return lines and lines[0].strip() == '[InternetShortcut]'
    except:
        return False

def extract_url(file_path):
    """Wydobywa URL=... z pliku .url"""
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            if line.startswith('URL='):
                return line.strip().split('=', 1)[1]
    return None

def replace_with_pdf(url, shortcut_path):
    """Pobiera PDF i zastępuje nim plik .url"""
    pdf_path = os.path.splitext(shortcut_path)[0] + '.pdf'
    try:
        print(f"Pobieram: {url}")
        response = requests.get(url)
        response.raise_for_status()
        with open(pdf_path, 'wb') as pdf_file:
            pdf_file.write(response.content)
        os.remove(shortcut_path)
        print(f"Zastąpiono {shortcut_path} -> {pdf_path}")
    except Exception as e:
        print(f"Błąd przy pobieraniu {url}: {e}")

def scan_repo_and_replace(start_dir='.'):
    """Rekursyjne przeszukiwanie repozytorium"""
    for root, _, files in os.walk(start_dir):
        for name in files:
            if name.endswith('.url'):
                file_path = os.path.join(root, name)
                if is_internet_shortcut(file_path):
                    url = extract_url(file_path)
                    if url and url.lower().endswith('.pdf'):
                        replace_with_pdf(url, file_path)

if __name__ == "__main__":
    scan_repo_and_replace('.')
