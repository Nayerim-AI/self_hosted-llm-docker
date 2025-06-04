import os

def summarize_findings(findings, total_komentar):
    if not findings:
        return "Tidak ditemukan komentar yang terindikasi promosi judi online."

    output = []
    output.append(f"Komentar yang dianalisis: {total_komentar}")
    output.append(f"Jumlah terindikasi promosi judi: {len(findings)}")
    output.append("\nSample Komentar Terindikasi Promosi Judi:")
    
    for i, item in enumerate(findings, 1):
        if isinstance(item, dict):
            text = item.get("text", "")[:100].replace("\n", " ")
            label = item.get("label", True)
        else:  # asumsi item adalah string
            text = item[:100].replace("\n", " ")
            label = True
        output.append(f"{i}. [Label: {label}] {text}")
    
    return "\n".join(output)
