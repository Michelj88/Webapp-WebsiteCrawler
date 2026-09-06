# Website URL Crawler (Streamlit webapp)

Deze app crawlt een website binnen hetzelfde domein, verzamelt alle gevonden URL's,
en maakt een Excel-overzicht met:
- Kolom 1: volledige URL
- Kolom 2: hoofddomein
- Kolom 3+: elk pad-niveau na het hoofddomein

## Lokaal testen (optioneel)
```
pip install -r requirements.txt
streamlit run app.py
```
Opent automatisch in je browser op http://localhost:8501

## Gratis online zetten (geen .exe, werkt op elke pc met een browser)

**Optie A — Streamlit Community Cloud (aanbevolen, gratis)**
1. Maak een gratis account op https://share.streamlit.io (inloggen met GitHub)
2. Zet deze 2 bestanden (app.py + requirements.txt) in een nieuwe GitHub-repository
3. Klik in Streamlit Cloud op "New app", kies je repository en `app.py`
4. Klaar — je krijgt een link zoals `https://jouwnaam-crawler.streamlit.app`
   die je overal kunt openen, ook op je werk-pc, zonder installatie

**Optie B — Replit (ook gratis, geen GitHub nodig)**
1. Ga naar https://replit.com en maak een gratis account
2. Maak een nieuwe "Python Repl"
3. Upload app.py en requirements.txt
4. Draai `pip install -r requirements.txt` in de shell, klik daarna op "Run"
5. Replit geeft je een publieke link naar de draaiende app

Beide opties vereisen geen .exe en dus geen Windows Defender-gedoe —
je opent gewoon een link in de browser.
