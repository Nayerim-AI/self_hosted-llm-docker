from pipeline.youtube_agent import get_comments
from pipeline.checker_agent import detect_judi_promosi
from pipeline.llm_agent import summarize_findings
from pipeline.wiki_agent import fetch_summary

from pipeline.youtube_agent import get_comments
from pipeline.checker_agent import detect_judi_promosi
from checker.predict import classify_comment  # <- kamu sudah punya ini

def run_pipeline(video_id, api_key):
    comments = get_comments(video_id, api_key)
    
    # Hasil klasifikasi semua komentar
    judi = []
    normal = []

    for c in comments:
        result = classify_comment(c)
        if result["label_name"] == "judi_promosi":
            judi.append(c)
        else:
            normal.append(c)

    return {
        "judi_promosi": judi,
        "normal": normal
    }



# === Wikipedia Ringkasan Sederhana ===
def run_wiki_pipeline(topic):
    summary = fetch_summary(topic)

    # Jika summary hasilnya error, return langsung
    if summary.startswith("Topik") or summary.startswith("[Wikipedia Error]"):
        return {"summary": summary}

    # Bersihkan dan pangkas agar ramah LLM
    summary = " ".join(summary.split())
    if len(summary) > 300:
        summary = summary[:300].rsplit(".", 1)[0] + "..."

    prompt = (
        f"Berikut adalah ringkasan Wikipedia tentang topik '{topic}':\n"
        f"{summary}\n\n"
        "Tulis ulang ringkasan ini agar lebih sederhana dan mudah dipahami oleh pelajar SMA. "
        "Gunakan maksimal 2 kalimat dan hindari istilah akademik:"
    )

    result = summarize_findings([{"text": prompt, "confidence": 0.99}])
    return {"summary": result}
