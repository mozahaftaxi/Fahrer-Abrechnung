import streamlit as st
import pandas as pd
from datetime import date
import os

# Konfiguration der Seite
st.set_page_config(page_title="Fahrer-Abrechnung", layout="wide", page_icon="🚖")

st.title("🚖 Fahrer-Abrechnung Digital")

# --- KOPFDATEN ---
col1, col2, col3 = st.columns(3)
with col1:
    datum = st.date_input("Datum", date.today())
with col2:
    fahrer = st.text_input("Fahrer Name", "Zahaf")
with col3:
    wagen_nr = st.text_input("Wagen Nr.", "Wg. 7")

st.divider()

# --- TABELLE FÜR EINTRÄGE ---
st.subheader("Fahrten / Buchungen")

# Initialisierung des Session States für die Daten, falls noch nicht vorhanden
if 'rows' not in st.session_state:
    st.session_state.rows = [
        {"Bemerkung": "", "Name": "", "Start": "", "Ziel": "", "Uhr": "", "Netto": 0.0, "Differenz": 0.0}
    ]

# Der data_editor erlaubt das direkte Bearbeiten der Tabelle
df_input = st.data_editor(st.session_state.rows, num_rows="dynamic", use_container_width=True)

# --- BERECHNUNG ---
# Wir wandeln die Eingabe in ein DataFrame um, um leichter rechnen zu können
df = pd.DataFrame(df_input)

# Sicherstellen, dass numerische Spalten auch Zahlen sind (ersetzt None durch 0)
total_netto = df["Netto"].fillna(0).sum()
total_diff = df["Differenz"].fillna(0).sum()
brutto_minus_diff = total_netto - total_diff

# --- ZUSAMMENFASSUNG ---
st.divider()
c1, c2 = st.columns(2)
with c1:
    st.metric("Gesamt Netto", f"{total_netto:,.22f} €".replace(",", "X").replace(".", ",").replace("X", "."))
with c2:
    st.metric("Netto - Differenz", f"{brutto_minus_diff:,.2f} €".replace(",", "X").replace(".", ",").replace("X", "."))

# --- SPEICHERN FUNKTION ---
if st.button("Abrechnung Speichern", type="primary"):
    # Erstellen eines DataFrames für den Export mit Kopfdaten
    export_df = df.copy()
    export_df["Datum"] = datum
    export_df["Fahrer"] = fahrer
    export_df["Wagen"] = wagen_nr
    
    # Speichern als CSV (lokal im Projektordner)
    file_exists = os.path.isfile("abrechnungen_archiv.csv")
    export_df.to_csv("abrechnungen_archiv.csv", mode='a', index=False, header=not file_exists, sep=";")
    
    st.success(f"Daten für {fahrer} am {datum} wurden erfolgreich archiviert!")
    st.balloons()
import streamlit as st
import pandas as pd
from datetime import date

# Seite konfigurieren
st.set_page_config(page_title="Fahrer-Abrechnung", layout="wide")

st.title("🚖 Fahrer-Abrechnung Digital")

# Kopfdaten Eingabe
col1, col2, col3 = st.columns(3)
with col1:
    datum = st.date_input("Datum", date.today())
with col2:
    fahrer = st.text_input("Fahrer Name", "Zahaf")
with col3:
    wagen_nr = st.text_input("Wagen Nr.", "Wg. 7")

st.divider()

# Tabelle für Fahrten
st.subheader("Fahrten / Buchungen")

# Startdaten für die Tabelle
if 'rows' not in st.session_state:
    st.session_state.rows = [
        {"Bemerkung": "", "Name": "", "Start": "", "Ziel": "", "Uhr": "", "Netto": 0.0, "Differenz": 0.0}
    ]

# Editor anzeigen
df_input = st.data_editor(st.session_state.rows, num_rows="dynamic", use_container_width=True)

# Berechnungen
df = pd.DataFrame(df_input)
total_netto = df["Netto"].fillna(0).sum()
total_diff = df["Differenz"].fillna(0).sum()
ergebnis = total_netto - total_diff

# Zusammenfassung anzeigen
st.divider()
c1, c2 = st.columns(2)
c1.metric("Gesamt Netto", f"{total_netto:.2f} €")
c2.metric("Netto - Differenz", f"{ergebnis:.2f} €")

if st.button("Abrechnung Speichern"):
    st.success("Daten wurden verarbeitet! (Speicherung in Google Sheets folgt im nächsten Schritt)")
