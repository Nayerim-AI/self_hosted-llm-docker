import os
import re
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS
from pipeline.agent_chain import run_pipeline, run_wiki_pipeline
from llama_cpp import Llama
import logging

logging.basicConfig(level=logging.INFO)

app = Flask(__name__)
CORS(app)

MODELS_DIR = os.getenv("MODELS_DIR", "/models")
DEFAULT_MODEL_PATH = os.getenv("DEFAULT_MODEL_PATH", "/models/qwen/qwen1_5-0_5b-chat-q8_0.gguf")
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY", "***")

# Load model ONCE using llama_cpp
llm = Llama(model_path=DEFAULT_MODEL_PATH, n_ctx=1024, n_threads=4)

@app.route("/completion", methods=["POST"])
def run_model():
    data = request.json or {}
    user_input = data.get("prompt", "").strip()

    # === Flow 1: YouTube Deteksi ===
    youtube_match = re.search(r"(?:v=|youtu\.be/)([\w-]+)", user_input)
    if youtube_match:
        video_id = youtube_match.group(1)
        result = run_pipeline(video_id, YOUTUBE_API_KEY)

        if not result:
            return jsonify({"response": "Gagal memproses video YouTube."})

        judi_promosi = result.get("judi_promosi", [])
        normal = result.get("normal", [])
        total = len(judi_promosi) + len(normal)

        # Buat ringkasan sample komentar judi
        sample_output = []
        for i, item in enumerate(judi_promosi[:3], 1):  # tampilkan maksimal 3 contoh
            text = item.replace("\n", " ")[:100]  # <-- FIX di sini
            sample_output.append(f"{i}. {text}")

        sample_text = "\n".join(sample_output) if sample_output else "Tidak ada komentar yang bisa ditampilkan."

        response_text = (
            f"Dari {total} komentar, ditemukan {len(judi_promosi)} komentar promosi judi "
            f"dan {len(normal)} komentar normal.\n\n"
            f"Contoh komentar promosi judi:\n{sample_text}"
        )

        return jsonify({"response": response_text})

    # === Flow 2: Wikipedia Ringkasan ===

    if user_input.lower().startswith("wiki:"):
        topic = user_input[5:].strip()
        result = run_wiki_pipeline(topic)
        if not result or "summary" not in result:
            return jsonify({"response": "Gagal mengambil ringkasan Wikipedia."})

        # Kirim ke LLM untuk penyederhanaan atau klarifikasi
        wiki_summary = result["summary"]
        wiki_prompt = (
            "### System:\n"
            "Berikut ini adalah ringkasan Wikipedia dari suatu topik. "
            "Tuliskan ulang dengan bahasa yang mudah dipahami dalam maksimal 100 token.\n\n"
            f"### Ringkasan:\n{wiki_summary}\n\n### Penjelasan Sederhana:\n"
        )

        try:
            output = llm(wiki_prompt, max_tokens=100, stop=["</s>"])
            response = output["choices"][0]["text"].strip()
            if not response:
                response = "(Model tidak memberikan jawaban.)"
            return jsonify({"response": response})
        except Exception as e:
            logging.error(f"LLM error: {e}")
            return jsonify({"error": str(e)}), 500


    # === Flow 3: Chat Biasa ===
    if not user_input or len(user_input) < 5:
        user_input = "Apa yang bisa kamu bantu hari ini?"

    system_prompt = (
        "### System:\n"
        "You are a helpful and concise AI assistant. "
        "Answer the user's question in Indonesian using no more than 100 tokens.\n\n"
        "### User:\n"
    )
    final_prompt = f"{system_prompt}{user_input}\n\n### Assistant:\n"

    print("[DEBUG PROMPT]\n", final_prompt)

    try:
        output = llm(final_prompt, max_tokens=100, stop=["</s>"])
        response = output["choices"][0]["text"].strip()
        if not response:
            response = "(Model tidak memberikan jawaban.)"
        return jsonify({"response": response})
    except Exception as e:
        logging.error(f"LLM error: {e}")
        return jsonify({"error": str(e)}), 500

@app.route("/completion", methods=["GET"])
def handle_get():
    return jsonify({"error": "Method not allowed. Use POST."}), 405

if __name__ == "__main__":
    logging.info("Running main.py with llama_cpp")
    app.run(host="0.0.0.0", port=5000)
