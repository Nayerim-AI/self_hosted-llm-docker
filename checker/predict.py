# checker/predict.py

import torch
from transformers import BertTokenizer, BertForSequenceClassification

# Load sekali saja
MODEL_PATH = "./checker/model"
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

tokenizer = BertTokenizer.from_pretrained(MODEL_PATH)
model = BertForSequenceClassification.from_pretrained(MODEL_PATH)
model.to(device)
model.eval()

def classify_comment(text: str):
    if not text or not isinstance(text, str):
        return {"label_id": -1, "label_name": "invalid", "confidence": 0.0}

    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True, max_length=512)
    inputs = {k: v.to(device) for k, v in inputs.items()}

    with torch.no_grad():
        outputs = model(**inputs)
    logits = outputs.logits
    probs = torch.softmax(logits, dim=1)
    label = torch.argmax(probs, dim=1).item()
    confidence = probs[0][label].item()

    label_map = {
        0: "normal",
        1: "judi_promosi"
    }

    return {
        "label_id": label,
        "label_name": label_map.get(label, "unknown"),
        "confidence": round(confidence, 4)
    }
