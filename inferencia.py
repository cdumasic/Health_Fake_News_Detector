from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline

# Ruta del modelo entrenado
model_path = "./beto-fakenews-model"

# Carga el modelo y el tokenizer
tokenizer = AutoTokenizer.from_pretrained(model_path)
model = AutoModelForSequenceClassification.from_pretrained(model_path)

# Crea el pipeline de clasificación
fake_news_clf = pipeline("text-classification", model=model, tokenizer=tokenizer)

# Ejemplo de prueba
texto = "supuesta votación que dará lugar a que los hombres tengan que esperar diez años más que las mujeres para recibir su pensión por jubilación ―hasta los 75 ellos, hasta los 65 ellas"
resultado = fake_news_clf(texto)
print(resultado)