#test_ingest.py
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
import os

# -- Configuration --
NAMA_FILE_PDF = "sample.pdf"
PERSIST_DIRECTORY = "db_context" # folder simpan database vector

# check apakah file ada atau tidak (jika tidak tampilkan ERROR)
if not os.path.exists(NAMA_FILE_PDF):
    print(f"ERROR: File '{NAMA_FILE_PDF}' tidak ditemukan! pastikan nama file benar.")
    exit()
print(f"--- 1. Memulai Proses Loading: {NAMA_FILE_PDF} ---")

# Load PDF
# PyPDFLoader bertugas membaca file dan mengambil teksnya halaman per halaman
print(f"-- Memproses PDF: {NAMA_FILE_PDF} ---")
loader = PyPDFLoader(NAMA_FILE_PDF)
raw_documents = loader.load()

print(f"✅ Berhasil membaca PDF! Total Halaman: {len(raw_documents)}")

# -- Chunking ( Memecah Teks ) --
print("\n--- 2. Memulai Proses Chunking ---")

# RecursiveCharacterTextSplitter adalah teknik pemotongan cerdas.
# Dia berusaha memotong di akhir kalimat/paragraf, bukan memotong kata di tengah jalan.
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size =1000,       # Satu potongan maksimal 1000 karakter
    chunk_overlap=200       # Disisakan 200 karakter dari potongan sebelumnya (biar konteks nyambung)
)

chunks = text_splitter.split_documents(raw_documents)

print(f"✅ Selesai! Dokumen dipecah menjadi {len(chunks)} chunks.")

# INITIALIZE EMBEDDINGS & VECTOR DB
print("\n --- Membuat Vector Database ---")
# Kita pakai model 'all-MiniLM-L6-v2'. Ini model kecil, gratis, dan cepat.
# Saat pertama dijalankan, dia akan download modelnya dulu (sekitar 80MB).
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# Simpan chunks ke ChromaDB
# 'persist_directory' artinya datanya disimpan di harddisk, jadi gak hilang pas komputer mati.
vector_db = Chroma.from_documents(
    documents=chunks,
    embedding=embeddings,
    persist_directory=PERSIST_DIRECTORY
)

print(f"✅ Database berhasil disimpan di folder: {PERSIST_DIRECTORY}")

# --- 3. TEST PENCARIAN (SIMILARITY SEARCH) ---
# Mari kita buktikan sistemnya jalan. Kita cari topik spesifik.
query = "Apa keahlian atau skill utama yang disebutkan?" # Ganti pertanyaan ini sesuai isi PDF kamu!
print(f"\n--- 3. Testing Pencarian: '{query}' ---")

# Cari 3 chunk paling relevan dengan pertanyaan di atas
results = vector_db.similarity_search(query, k=3)

if results:
    print("\n[DITEMUKAN JAWABAN RELEVAN]:")
    for i, doc in enumerate(results):
        print(f"\n--- Hasil #{i+1} ---")
        print(doc.page_content[:300] + "...") # Tampilkan 300 huruf pertama saja biar gak kepanjangan
else:
    print("Tidak ditemukan hasil yang relevan.")