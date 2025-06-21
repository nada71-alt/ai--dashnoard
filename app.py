import streamlit as st
import pandas as pd
import requests
import os
from dotenv import load_dotenv

# Charger les variables d'environnement (clé API)
load_dotenv()
API_KEY = os.getenv("DEEPSEEK_API_KEY")  # Assure-toi que la clé est bien dans .env avec ce nom

# Fonction pour charger les données produits
@st.cache_data
def load_data():
    return pd.read_csv("produits.csv")

# Fonction pour appeler l’API DeepSeek
def call_deepseek(prompt):
    url = "https://api.deepseek.com/v1/chat/completions"  # ✅ URL CORRIGÉE
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    body = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "system", "content": "Tu es un expert e-commerce, tu réponds de manière claire."},
            {"role": "user", "content": prompt}
        ]
    }

    try:
        response = requests.post(url, headers=headers, json=body)
        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"]
        else:
            return f"Erreur API : {response.status_code} - {response.text}"
    except requests.exceptions.RequestException as e:
        return f"Erreur de connexion : {e}"

# Interface utilisateur
st.set_page_config(page_title="Dashboard IA - Shopify", layout="centered")
st.title("🧠 Tableau de bord IA - Produits Shopify")

# Chargement des données
df = load_data()

# Affichage des produits
st.subheader("📦 Aperçu des produits")
st.dataframe(df[["Handle", "Title", "Body (HTML)"]])

# Statistiques de base
st.subheader("📊 Statistiques")
st.markdown(f"*Nombre total de produits :* {len(df)}")
if "Prix" in df.columns:
    st.markdown(f"*Prix moyen :* {df['Prix'].mean():.2f} MAD")

# Section d'analyse IA
st.subheader("💬 Analyse IA")
question = st.text_input("Pose une question sur tes produits (ex : Quel produit est le plus rentable ?)")

if st.button("Analyser avec GPT"):
    if question:
        with st.spinner("Analyse en cours..."):
            resultat = call_deepseek(question)
            st.success("✅ Résultat :")
            st.write(resultat)
    else:
        st.warning("❗ Merci de poser une question avant d’analyser.")