import wikipedia

def fetch_summary(topic):
    try:
        summary = wikipedia.summary(topic, sentences=3, auto_suggest=True)

        # Hilangkan newline ganda dan whitespace berlebihan
        summary = " ".join(summary.split())

        # Batasi panjang agar ramah LLM kecil
        if len(summary) > 400:
            summary = summary[:400].rsplit(".", 1)[0] + "..."

        return summary

    except wikipedia.exceptions.DisambiguationError as e:
        return f"Topik '{topic}' terlalu umum. Beberapa kemungkinan: {', '.join(e.options[:5])}..."
    except wikipedia.exceptions.PageError:
        return f"Topik '{topic}' tidak ditemukan di Wikipedia."
    except Exception as e:
        return f"[Wikipedia Error] {str(e)}"
