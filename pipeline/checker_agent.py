# pipeline/checker_agent.py

from checker.predict import tokenizer, model, device
import torch

def detect_judi_promosi(texts):
    valid_texts = [t[:200] for t in texts if isinstance(t, str) and t.strip()]  # Pangkas teks

    if not valid_texts:
        return []

    # Batching bisa ditambah kalau komentar > 50
    inputs = tokenizer(valid_texts, return_tensors="pt", truncation=True, padding=True, max_length=512)
    inputs = {k: v.to(device) for k, v in inputs.items()}

    model.eval()
    with torch.no_grad():
        outputs = model(**inputs)
    probs = torch.softmax(outputs.logits, dim=1)
    labels = torch.argmax(probs, dim=1)

    results = []
    for i, (label_id, prob) in enumerate(zip(labels, probs)):
        label = label_id.item()
        confidence = prob[label].item()
        if label == 1:  # "judi_promosi"
            results.append({
                "text": valid_texts[i],
                "label_id": label,
                "label_name": "judi_promosi",
                "confidence": round(confidence, 4)
            })
    return results

