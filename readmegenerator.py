import os
import re

PRIORYTET_KODOW = {
    'INF.03': 1,
    'EE.09': 2,
    'E.14': 3
}

def rozpoznaj_kod(folder_nazwa):
    dopasowanie = re.match(r'([A-Z]+\.\d{2})', folder_nazwa)
    return dopasowanie.group(1) if dopasowanie else 'ZZZ.99'

def miesiac_egzaminu(folder_nazwa):
    dopasowanie = re.search(r'(\d{2})\.(\d{2})', folder_nazwa)
    if dopasowanie:
        return dopasowanie.group(2)
    return None

def sortuj_foldery(fold_nazwy):
    def klucz_sortowania(nazwa):
        kod = rozpoznaj_kod(nazwa)
        priorytet = PRIORYTET_KODOW.get(kod, 999)
        dopasowanie = re.search(r'-([0-9]{2})-', nazwa)
        numer = int(dopasowanie.group(1)) if dopasowanie else 999
        return (priorytet, numer)
    return sorted(fold_nazwy, key=klucz_sortowania)

def skrocony_kod(nazwa):
    kod = rozpoznaj_kod(nazwa)
    return kod.replace('.', '')  # INF.03 -> INF03

def numer_egzaminu(nazwa):
    dop = re.search(r'-([0-9]{2})-', nazwa)
    return dop.group(1) if dop else '??'

def generuj_readme_dla_roku(folder_rok):
    podfoldery = [
        f for f in os.listdir(folder_rok)
        if os.path.isdir(os.path.join(folder_rok, f)) and not f.startswith('.')
    ]

    styczen = []
    czerwiec = []

    liczniki = {
        'INF03': 0,
        'EE09': 0,
        'E14': 0
    }

    for folder in podfoldery:
        miesiac = miesiac_egzaminu(folder)
        kod = skrocony_kod(folder)

        if kod in liczniki:
            liczniki[kod] += 1

        if miesiac == '01':
            styczen.append(folder)
        elif miesiac == '06':
            czerwiec.append(folder)

    styczen = sortuj_foldery(styczen)
    czerwiec = sortuj_foldery(czerwiec)

    sciezka_readme = os.path.join(folder_rok, 'Readme.md')
    with open(sciezka_readme, 'w', encoding='utf-8') as f:
        f.write("### [⬅️ Powrót](../)\n\n")
        f.write(f"# 📝Arkusze z {folder_rok} roku 📝\n\n")

        # Podsumowanie
        f.write("**Podsumowanie arkuszy:**\n\n")
        f.write(f"- INF03: {liczniki['INF03']} arkuszy\n")
        f.write(f"- EE09: {liczniki['EE09']} arkuszy\n")
        f.write(f"- E14: {liczniki['E14']} arkuszy\n\n")

        if styczen:
            f.write("## Styczeń\n")
            for folder in styczen:
                kod = skrocony_kod(folder)
                nr = numer_egzaminu(folder)
                f.write(f"- 📚 {kod}-**{nr}** [{folder}](./{folder})\n")
            f.write("\n")

        if czerwiec:
            f.write("## Czerwiec\n")
            for folder in czerwiec:
                kod = skrocony_kod(folder)
                nr = numer_egzaminu(folder)
                f.write(f"- 📚 {kod}-**{nr}** [{folder}](./{folder})\n")
            f.write("\n")

    print(f"✅ Utworzono: {sciezka_readme}")

def main():
    for rok in range(2025, 2018, -1):
        folder_rok = str(rok)
        if os.path.isdir(folder_rok):
            generuj_readme_dla_roku(folder_rok)
        else:
            print(f"  Pominięto: {folder_rok} (nie istnieje)")

if __name__ == "__main__":
    main()
