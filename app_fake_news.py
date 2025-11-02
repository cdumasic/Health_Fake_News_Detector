import streamlit as st
from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline
import torch

# ==============================
# 1. Configuración inicial
# ==============================
st.set_page_config(
    page_title="Detector de Desinformación en Salud",
    layout="centered"
)

st.title("Detector de Desinformación sobre Salud")
st.markdown("Escribe una noticia o párrafo, y el sistema BETO analizará si parece **Real** o **Falsa**.")

# ==============================
# 2. Cargar el modelo entrenado
# ==============================
@st.cache_resource
def load_model():
    model_path = "./beto-fakenews-model"
    tokenizer = AutoTokenizer.from_pretrained(model_path)
    model = AutoModelForSequenceClassification.from_pretrained(model_path)
    return pipeline("text-classification", model=model, tokenizer=tokenizer, return_all_scores=True)

clf = load_model()

# ==============================
# 3. Entrada de texto
# ==============================
texto = st.text_area("✍️ Ingresa una noticia:", height=200)

if st.button("Analizar noticia"):
    if not texto.strip():
        st.warning("Por favor ingresa una noticia antes de analizar.")
    else:
        with st.spinner("Analizando..."):
            resultados = clf(texto)[0]

            # Obtener puntuaciones
            label0 = resultados[0]
            label1 = resultados[1]

            fake_prob = round(label0["score"] * 100, 2)
            real_prob = round(label1["score"] * 100, 2)
            prediccion = "Falsa" if fake_prob > real_prob else "Real"

        # ==============================
        # 4. Mostrar resultados
        # ==============================
        st.subheader("Resultado de la inferencia:")
        st.markdown(f"**Predicción:** {prediccion}")
        st.progress(int(max(fake_prob, real_prob)))
        st.write(f"**Probabilidad Real:** {real_prob}%")
        st.write(f"**Probabilidad Falsa:** {fake_prob}%")

        if abs(fake_prob - real_prob) < 10:
            st.info("El modelo no está completamente seguro, puede requerir revisión humana.")

st.markdown("---")
st.caption("Modelo basado en BETO - Finetuning con dataset de noticias de salud.")