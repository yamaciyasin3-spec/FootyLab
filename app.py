# app.py - Reklamlı + Canlı Analiz
import streamlit as st
import plotly.express as px
import pandas as pd
from data_fetcher import takımı_bul, maclari_cek, df_olustur
import streamlit.components.v1 as components

# AdSense doğrulama (Render.com için kesin çalışır)
components.html('<meta name="google-adsense-account" content="ca-pub-3852960467508583">', height=0)
def reklam_goster():
    st.markdown("""
    <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-XXXXXXXXXXXXXXXX" crossorigin="anonymous"></script>
    <ins class="adsbygoogle" style="display:block" data-ad-client="ca-pub-XXXXXXXXXXXXXXXX" data-ad-slot="YYYYYYYYYY" data-ad-format="auto" data-full-width-responsive="true"></ins>
    <script>(adsbygoogle = window.adsbygoogle || []).push({});</script>
    """, unsafe_allow_html=True)
    st.info("Reklamı izle, analiz ücretsiz devam etsin! 😊")

takim1 = st.text_input("1. Takım", "Fenerbahce")
takim2 = st.text_input("2. Takım", "Galatasaray")

if st.button("ANALİZİ BAŞLAT"):
    reklam_goster()  # Her sorguda reklam
    with st.spinner("Canlı veriler çekiliyor..."):
        id1, isim1 = takımı_bul(takim1)
        id2, isim2 = takımı_bul(takim2)
        maclar1 = maclari_cek(id1, isim1)
        maclar2 = maclari_cek(id2, isim2)
        df1 = df_olustur(maclar1, isim1)
        df2 = df_olustur(maclar2, isim2)
        st.success(f"{isim1} vs {isim2} - Canlı Analiz Tamamlandı!")
    
    if not df1.empty and not df2.empty:
        col1, col2 = st.columns(2)
        with col1:
            st.subheader(isim1)
            fig1 = px.pie(df1['Sonuç'].value_counts(), names=df1['Sonuç'].value_counts().index, title="Sonuç Dağılımı")
            st.plotly_chart(fig1)
            st.metric("Toplam Maç", len(df1))
        with col2:
            st.subheader(isim2)
            fig2 = px.pie(df2['Sonuç'].value_counts(), names=df2['Sonuç'].value_counts().index, title="Sonuç Dağılımı")
            st.plotly_chart(fig2)
            st.metric("Toplam Maç", len(df2))
        
        # Derbi geçmişi
        karsilikli = df1[df1['Rakip'].str.contains(isim2, case=False, na=False)]
        if len(karsilikli) > 0:
            st.subheader("Derbi Geçmişi")
            st.dataframe(karsilikli)
    else:

        st.info("Veri yükleniyor, tekrar dene.")










