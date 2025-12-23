🧠 Context AI

<div align="center">

Your Intelligent Document Assistant. Goodbye Ctrl+F, Hello Semantic Search.

Demo · Report Bug · Request Feature

</div>

🧐 About The Project

Dalam dunia yang dibanjiri informasi, mencari jarum dalam tumpukan jerami (baca: mencari info spesifik dalam PDF 100 halaman) adalah pekerjaan yang melelahkan. Pencarian keyword tradisional sering gagal memahami konteks.

Context AI hadir untuk memecahkan masalah tersebut. Ini adalah aplikasi RAG (Retrieval-Augmented Generation) Hybrid yang memungkinkan Anda untuk:

Berdiskusi dengan Dokumen: Upload PDF, lalu tanya apa saja. AI akan menjawab berdasarkan fakta di dokumen.

General Chatting: Butuh brainstorming atau bantuan coding? Switch ke mode General Chat.

Dibangun dengan Llama 3.1 (via Groq), aplikasi ini menawarkan kecepatan inferensi yang blazing fast (hampir instan), menghilangkan rasa frustrasi menunggu jawaban AI.

🏗️ Architecture & How It Works

Aplikasi ini tidak sekadar "membaca" PDF. Ia memahaminya. Berikut adalah pipeline di balik layar:

graph LR
    A[User Upload PDF] --> B(Chunking & Splitting)
    B --> C{Embedding Process}
    C --> D[(ChromaDB Vector Store)]
    E[User Question] --> F(Semantic Search)
    D --> F
    F --> G[Context Retrieval]
    G --> H[LLM Llama 3.1]
    H --> I[Final Answer]


Engineering Decisions:

Vector Database (ChromaDB): Dipilih karena sifatnya yang embedded (lokal), ringan, dan tidak memerlukan setup server terpisah. Cocok untuk deployment cepat.

LLM (Groq API): Menggunakan LPU (Language Processing Unit) yang membuat inferensi Llama 3 menjadi sangat cepat dibandingkan GPU standar.

Framework (LangChain): Memudahkan orkestrasi antara Retriever, Prompt Templates, dan LLM.

✨ Key Features

⚡ Hybrid Intelligence: Mode ganda untuk fleksibilitas maksimal (Chat Umum & Analisis Dokumen).

🔄 Dynamic Knowledge Base (CRUD):

Create: Upload multiple PDF sekaligus.

Read: Status indikator visual database.

Delete: Tombol reset instan untuk membersihkan memori AI.

🛡️ Anti-Hallucination: System Prompt yang dirancang ketat agar AI berani berkata "Tidak tahu" jika informasi tidak ada di dokumen.

📍 Source Citation: Transparansi penuh. AI menunjukkan dari halaman mana jawaban diambil.

🎨 Modern UI: Interface bersih dengan Typing Effect, Toast Notifications, dan Responsive Sidebar.

📂 Project Structure

Struktur direktori yang rapi memudahkan pengembangan dan maintenance.

Context-AI/
├── 📄 app.py               # Entry point aplikasi (Streamlit Frontend + Logic)
├── 📄 requirements.txt     # Daftar dependensi produksi
├── 📄 .env.example         # Template konfigurasi environment
├── 📄 .gitignore           # Aturan pengabaian file Git
├── 📁 db_veritas/          # (Auto-generated) Penyimpanan vektor lokal
└── 📁 temp_files/          # (Auto-generated) Buffer pemrosesan file


🚀 Getting Started

Ingin menjalankan ini di mesin lokal Anda? Ikuti langkah mudah ini.

Prerequisites

Python 3.10 atau lebih baru.

API Key dari Groq Cloud (Gratis untuk tier developer).

Installation

Clone Repository

git clone [https://github.com/USERNAME_ANDA/Context-AI.git](https://github.com/USERNAME_ANDA/Context-AI.git)
cd Context-AI


Set Up Virtual Environment (Recommended)

python -m venv venv
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate


Install Dependencies

pip install -r requirements.txt


Configure Environment
Buat file .env di root folder dan masukkan API Key Anda:

GROQ_API_KEY=gsk_your_secret_key_here


Run Application

streamlit run app.py


🚧 Version 1.0 Disclaimer (Beta)

Catatan Pengembang:

Proyek ini saat ini berada di fase Versi 1.0 (MVP - Minimum Viable Product). Meskipun fitur inti telah berjalan dengan baik, sebagai sesama developer, saya ingin transparan mengenai area yang masih bisa ditingkatkan:

Keterbatasan Memori: Dokumen yang sangat besar (>200 halaman) mungkin memakan waktu lama saat proses chunking di mesin lokal.

Kompleksitas PDF: Tabel yang rumit atau PDF hasil scan (gambar) belum dapat dibaca dengan sempurna oleh PyPDFLoader.

Session Persistence: Saat ini, jika browser di-refresh, riwayat chat akan hilang (Stateless).

Roadmap Masa Depan:

[ ] Implementasi Conversation Memory (LangChain Memory).

[ ] Dukungan OCR untuk PDF hasil scan.

[ ] Integrasi Docker untuk deployment yang lebih mudah.

🤝 Contributing

Kontribusi adalah apa yang membuat komunitas open source menjadi tempat yang luar biasa untuk belajar. Segala bentuk kontribusi (Bug fix, Feature request, Documentation) sangat diapresiasi.

Fork Project ini

Create Feature Branch (git checkout -b feature/AmazingFeature)

Commit Changes (git commit -m 'Add some AmazingFeature')

Push to Branch (git push origin feature/AmazingFeature)

Open Pull Request

📜 License

Didistribusikan di bawah Lisensi MIT. Lihat LICENSE untuk informasi lebih lanjut.

<div align="center">
Made with ❤️ and lots of ☕ by <b>[Nama Kamu]</b>
</div>
