Saya membuat setup lengkap yang menggabungkan backend Flask, frontend interaktif dengan Streamlit, dan Cloudflare Tunnel (cloudflared) untuk membuat demonya bisa diakses publik langsung dari laptop saya. Model yang saya gunakan adalah Qwen dan Phi dari Hugging Face.

Sebagai fitur utamanya, saya melatih model ini untuk bisa melakukan deteksi komentar judi online dalam Bahasa Indonesia.

Demo bisa dicoba di: llm.capjumbo.my.id

Fitur & Keahlian yang Ditampilkan:
Containerization dengan Docker: Berhasil membungkus aplikasi Python (Flask & Streamlit) beserta model LLM ke dalam satu image Docker agar mudah dijalankan di mana saja.
Integrasi Model LLM: Mengimplementasikan model open-source dari Hugging Face (Qwen & Phi-3) ke dalam aplikasi.
Fitur AI Khusus: Membuat fungsi spesifik untuk mendeteksi konten judi online pada teks berbahasa Indonesia, menunjukkan kemampuan untuk fine-tuning atau prompt engineering pada kasus nyata.
Full-Stack Sederhana: Membangun backend API menggunakan Flask untuk menangani logika, dan UI interaktif dengan Streamlit untuk memudahkan interaksi dengan model.
Secure Tunneling: Menggunakan Cloudflare Tunnel untuk mengekspos service yang berjalan lokal (localhost) ke internet dengan aman, tanpa perlu konfigurasi port forwarding di router.
