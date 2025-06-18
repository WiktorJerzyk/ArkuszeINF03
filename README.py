def generuj_podsumowanie_glowne():
    lata = sorted([
        d for d in os.listdir('.')
        if os.path.isdir(d) and d.isdigit()
    ], reverse=True)

    wszystkie_liczniki = defaultdict(int)
    linie_readme = []

    linie_readme.append("# 📝 Arkusze INF03 📝")
    linie_readme.append("### Repozytoirum katalogujące egzaminy z poprzednich lat: INF03, EE.09, E14\n")
    linie_readme.append("## 📁 Nawigacja po latach 📁")
    linie_readme.append("> Każdy rok poniżej to odnośnik do odpowiedniego katalogu w repozytorium")

    for rok in lata:
        sciezka_roku = os.path.join(rok)
        foldery = [
            f for f in os.listdir(sciezka_roku)
            if os.path.isdir(os.path.join(sciezka_roku, f)) and not f.startswith('.')
        ]

        liczniki = {kod: 0 for kod in KODY}

        print(f"\n🔍 Analiza roku {rok}:")

        for folder in foldery:
            kod = rozpoznaj_kod(folder)
            print(f"📁 {folder} ➜ Kod: {kod}", end=' ')
            if kod in liczniki:
                liczniki[kod] += 1
                wszystkie_liczniki[kod] += 1
                print("✅ (zliczono)")
            else:
                print("⛔ (pominięto)")

        linia = f"###  [📁 {rok}](./{rok})"
        opisy = [f"{kod} - {liczniki[kod]}" for kod in KODY if liczniki[kod] > 0]
        opis = " | ".join(opisy) if opisy else "Brak arkuszy"
        linia += f"\n> {opis}\n"
        linie_readme.append(linia)

    # Podsumowanie końcowe
    linie_readme.append("\n# Podsumowanie")
    for kod in KODY:
        linie_readme.append(f"- {kod}: {wszystkie_liczniki[kod]} arkuszy")

    with open("Readme.md", "w", encoding="utf-8") as f:
        f.write("\n".join(linie_readme))

    print("\n✅ Zakończono generowanie Readme.md\n")
