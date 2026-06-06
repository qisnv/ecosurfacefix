```python
# ==========================================
# EcoSurface - Monitoring Kualitas Air
# ==========================================
# Author : Bilqis Novalia
# Framework : Streamlit
#
# Aplikasi untuk:
# 1. Panduan Sampling Air Permukaan
# 2. Evaluasi Baku Mutu Air Permukaan
#
# ==========================================

import streamlit as st
import pandas as pd

# ==========================================
# KONFIGURASI HALAMAN
# ==========================================
st.set_page_config(
    page_title="EcoSurface",
    page_icon="💧",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# CUSTOM CSS
# ==========================================
st.markdown("""
<style>

.main {
    background-color: #f7fbfc;
}

.card {
    background-color: white;
    padding: 20px;
    border-radius: 15px;
    border-left: 6px solid #2E8B57;
    box-shadow: 0px 3px 10px rgba(0,0,0,0.08);
    margin-bottom: 15px;
}

.small-card {
    background-color: #ffffff;
    padding: 15px;
    border-radius: 12px;
    text-align: center;
    border: 1px solid #e0e0e0;
}

.title-center {
    text-align:center;
}

.result-success {
    background-color:#e8f5e9;
    padding:20px;
    border-radius:12px;
    border-left:6px solid #2e7d32;
}

.result-danger {
    background-color:#ffebee;
    padding:20px;
    border-radius:12px;
    border-left:6px solid #c62828;
}

</style>
""", unsafe_allow_html=True)

# ==========================================
# DATABASE PANDUAN SAMPLING
# ==========================================
SAMPLING_GUIDE = {

    "pH": {
        "wadah":"Botol Plastik (PE)",
        "volume":"100 mL",
        "pengawet":"Tidak ada",
        "penyimpanan":"4°C",
        "holding_time":"< 2 jam",
        "catatan":"Analisis dilakukan sesegera mungkin."
    },

    "Suhu": {
        "wadah":"Botol Kaca",
        "volume":"1 L",
        "pengawet":"Tidak ada",
        "penyimpanan":"In Situ",
        "holding_time":"Segera dibaca",
        "catatan":"Diukur langsung di lapangan."
    },

    "TSS": {
        "wadah":"Botol PE / Kaca",
        "volume":"1 L",
        "pengawet":"Tidak ada",
        "penyimpanan":"4°C",
        "holding_time":"7 hari",
        "catatan":"Hindari pengadukan berlebihan."
    },

    "TDS": {
        "wadah":"Botol PE",
        "volume":"500 mL",
        "pengawet":"Tidak ada",
        "penyimpanan":"4°C",
        "holding_time":"28 hari",
        "catatan":"Saring dengan filter 0,45 μm."
    },

    "DO": {
        "wadah":"Botol DO",
        "volume":"300 mL",
        "pengawet":"Reagen Winkler",
        "penyimpanan":"4°C",
        "holding_time":"8 jam",
        "catatan":"Hindari gelembung udara."
    },

    "BOD": {
        "wadah":"Botol Kaca Amber",
        "volume":"1 L",
        "pengawet":"H2SO4 pH < 2",
        "penyimpanan":"4°C",
        "holding_time":"48 jam",
        "catatan":"Ideal dianalisis < 6 jam."
    },

    "COD": {
        "wadah":"Botol Kaca",
        "volume":"500 mL",
        "pengawet":"H2SO4 pH < 2",
        "penyimpanan":"4°C",
        "holding_time":"28 hari",
        "catatan":"Segera didinginkan."
    },

    "Nitrat": {
        "wadah":"Botol PE",
        "volume":"250 mL",
        "pengawet":"H2SO4 pH < 2",
        "penyimpanan":"4°C",
        "holding_time":"28 hari",
        "catatan":"Hindari kontaminasi."
    },

    "Nitrit": {
        "wadah":"Botol PE",
        "volume":"250 mL",
        "pengawet":"Pendinginan",
        "penyimpanan":"4°C",
        "holding_time":"48 jam",
        "catatan":"Analisis sesegera mungkin."
    },

    "Amonia": {
        "wadah":"Botol PE",
        "volume":"500 mL",
        "pengawet":"H2SO4 pH < 2",
        "penyimpanan":"4°C",
        "holding_time":"28 hari",
        "catatan":"Jaga pH tetap asam."
    },

    "Fosfat": {
        "wadah":"Botol PE",
        "volume":"250 mL",
        "pengawet":"H2SO4 pH < 2",
        "penyimpanan":"4°C",
        "holding_time":"28 hari",
        "catatan":"Gunakan wadah bersih bebas fosfat."
    },

    "Sulfat": {
        "wadah":"Botol PE",
        "volume":"250 mL",
        "pengawet":"Tidak ada",
        "penyimpanan":"4°C",
        "holding_time":"28 hari",
        "catatan":"Hindari kontaminasi silang."
    },

    "Klorida": {
        "wadah":"Botol PE",
        "volume":"250 mL",
        "pengawet":"Tidak ada",
        "penyimpanan":"4°C",
        "holding_time":"28 hari",
        "catatan":"Simpan dalam kondisi dingin."
    },

    "Total Coliform": {
        "wadah":"Botol Steril",
        "volume":"100 mL",
        "pengawet":"Na2S2O3",
        "penyimpanan":"4°C",
        "holding_time":"24 jam",
        "catatan":"Jaga sterilitas wadah."
    },

    "Fecal Coliform": {
        "wadah":"Botol Steril",
        "volume":"100 mL",
        "pengawet":"Na2S2O3",
        "penyimpanan":"4°C",
        "holding_time":"24 jam",
        "catatan":"Analisis mikrobiologi secepatnya."
    },

    "Besi (Fe)": {
        "wadah":"Botol PE",
        "volume":"500 mL",
        "pengawet":"HNO3 pH < 2",
        "penyimpanan":"4°C",
        "holding_time":"6 bulan",
        "catatan":"Untuk logam terlarut lakukan filtrasi."
    },

    "Mangan (Mn)": {
        "wadah":"Botol PE",
        "volume":"500 mL",
        "pengawet":"HNO3 pH < 2",
        "penyimpanan":"4°C",
        "holding_time":"6 bulan",
        "catatan":"Simpan dalam kondisi asam."
    }
}

# ==========================================
# DATABASE BAKU MUTU
# ==========================================
WATER_STANDARDS = {

    "pH": {
        "min":6.0,
        "max":9.0,
        "tipe":"range"
    },

    "TSS":{
        "nilai":50,
        "tipe":"<="
    },

    "DO":{
        "nilai":4,
        "tipe":">="
    },

    "BOD":{
        "nilai":3,
        "tipe":"<="
    },

    "COD":{
        "nilai":25,
        "tipe":"<="
    },

    "Nitrat":{
        "nilai":0.5,
        "tipe":"<="
    },

    "Nitrit":{
        "nilai":0.06,
        "tipe":"<="
    },

    "Amonia":{
        "nilai":0.5,
        "tipe":"<="
    },

    "Fosfat":{
        "nilai":0.5,
        "tipe":"<="
    },

    "Total Coliform":{
        "nilai":100,
        "tipe":"<="
    }
}

# ==========================================
# FUNGSI CARD
# ==========================================
def info_card(title, content):

    st.markdown(
        f"""
        <div class="card">
            <h4>{title}</h4>
            {content}
        </div>
        """,
        unsafe_allow_html=True
    )

# ==========================================
# HALAMAN BERANDA
# ==========================================
def home_page():

    st.title("💧 EcoSurface")

    st.markdown("""
    ### Pemantauan Kualitas Air Permukaan

    EcoSurface membantu pengguna menentukan kebutuhan sampling
    dan mengevaluasi hasil analisis kualitas air terhadap baku mutu.
    """)

    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "📊 Parameter Sampling",
            len(SAMPLING_GUIDE)
        )

    with col2:
        st.metric(
            "⚖️ Parameter Baku Mutu",
            len(WATER_STANDARDS)
        )

    st.divider()

    st.subheader("🚀 Quick Start")

    c1, c2 = st.columns(2)

    with c1:
        st.info(
            """
            Gunakan menu **Panduan Sampling**
            untuk melihat wadah, pengawet,
            penyimpanan dan holding time.
            """
        )

    with c2:
        st.info(
            """
            Gunakan menu **Evaluasi Baku Mutu**
            untuk membandingkan hasil analisis
            dengan baku mutu.
            """
        )
```
