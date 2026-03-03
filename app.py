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
