import os
import requests

ARCHIVE_EXTENSIONS = ('.zip', '.7z', '.rar', '.tar', '.tar.gz')

def is_internet_shortcut(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.readline().strip() == '[InternetShortcut]'
    except:
        return False

def extract_url(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            if line.startswith('URL='):
                return line.strip().split('=', 1)[1]
    return None

def download_archive(url, target_dir):
    filename = os.path.basename(url)
    target_path = os.path.join(target_dir, filename)

    try:
        print(f"⬇️ Pobieram: {url}")
        response = requests.get(url)
        response.raise_for_status()
        with open(target_path, 'wb') as f:
            f.write(response.content)
        print(f"✅ Zapisano do: {target_path}")
        return True
    except Exception as e:
        print(f"❌ Błąd przy pobieraniu {url}: {e}")
        return False

def scan_and_download(start_dir='.'):
    for root, _, files in os.walk(start_dir):
        for file in files:
            if file.endswith('.url'):
                full_path = os.path.join(root, file)
                if is_internet_shortcut(full_path):
                    url = extract_url(full_path)
                    if url and url.lower().endswith(ARCHIVE_EXTENSIONS):
                        success = download_archive(url, root)
                        if success:
                            os.remove(full_path)  # usuń .url po pobraniu
                            print(f"🗑️ Usunięto plik skrótu: {full_path}")

if __name__ == "__main__":
    scan_and_download()
