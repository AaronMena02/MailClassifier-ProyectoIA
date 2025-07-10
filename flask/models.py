from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import re

# Rutas a los modelos en Hugging Face
MODELS_PATHS = {
    "sentiment": "aaronmena02/sentiment-model-mailclassifier",
    "priority": "aaronmena02/priority-model-mailclassifier",
    "category": "aaronmena02/category-model-mailclassifier"
}

# Carga tokenizer, modelo, id2label y max_len
def load_model_components(model_path):
    tokenizer = AutoTokenizer.from_pretrained(model_path)
    model = AutoModelForSequenceClassification.from_pretrained(model_path)
    id2label = {int(k): v for k, v in model.config.id2label.items()}
    max_len = model.config.max_position_embeddings
    return tokenizer, model, id2label, max_len

# Cargar todos los modelos
tokenizer_sentiment, model_sentiment, sentiment_map, max_len_sentiment = load_model_components(MODELS_PATHS["sentiment"])
tokenizer_priority, model_priority, priority_map, max_len_priority = load_model_components(MODELS_PATHS["priority"])
tokenizer_category, model_category, category_map, max_len_category = load_model_components(MODELS_PATHS["category"])

# Preprocesamiento (asunto + cuerpo)
def preprocesar_texto(asunto, cuerpo):
    texto = f"{asunto.strip()}. {cuerpo.strip()}"
    texto = re.sub(r"\s+", " ", texto)
    texto = texto.encode("utf-8", "ignore").decode("utf-8", "ignore")
    return texto.strip()

# Predicción segura sin salirse del rango
def predict(text, tokenizer, model, max_len):
    inputs = tokenizer(
        text,
        return_tensors="pt",
        padding="max_length",
        truncation=True,
        max_length=max_len
    )

    # Corte manual para evitar índices fuera de rango en position_ids
    for key in inputs:
        inputs[key] = inputs[key][:, :max_len]

    # Regenerar position_ids válidos explícitamente
    inputs["position_ids"] = torch.arange(0, inputs["input_ids"].shape[1]).unsqueeze(0)

    with torch.no_grad():
        outputs = model(**inputs)

    probs = torch.nn.functional.softmax(outputs.logits, dim=-1)
    pred_idx = torch.argmax(probs, dim=1).item()
    confidence = probs[0][pred_idx].item()
    return pred_idx, confidence

# Clasificador completo
def classify_email(text):
    sentiment_idx, sentiment_prob = predict(text, tokenizer_sentiment, model_sentiment, max_len_sentiment)
    priority_idx, priority_prob = predict(text, tokenizer_priority, model_priority, max_len_priority)
    category_idx, category_prob = predict(text, tokenizer_category, model_category, max_len_category)

    return {
        "sentiment": sentiment_map.get(sentiment_idx, str(sentiment_idx)),
        "sentiment_prob": sentiment_prob,
        "priority": priority_map.get(priority_idx, str(priority_idx)),
        "priority_prob": priority_prob,
        "category": category_map.get(category_idx, str(category_idx)),
        "category_prob": category_prob
    }
