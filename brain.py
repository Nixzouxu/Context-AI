import os
from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_groq import ChatGroq
from langchain_classic.chains import RetrievalQA

# --- 1. SETUP AWAL ---
# Load API Key dari file .env
load_dotenv()

# Cek apakah API Key terbaca
groq_api_key = os.getenv("GROQ_API_KEY")
if not groq_api_key:
    print("❌ Error: API Key tidak ditemukan. Pastikan file .env sudah dibuat!")
    exit()

print("✅ Otak siap! Menghubungkan ke Database Ingatan...")

# --- 2. LOAD DATABASE (MEMORI) ---
# Kita panggil lagi embedding yang sama persis dengan Phase 2
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# Load database yang sudah ada (bukan bikin baru)
vector_db = Chroma(
    persist_directory="db_context", # Harus sama dengan folder di Phase 2
    embedding_function=embeddings
)

# --- 3. SETUP OTAK (LLM - LLAMA 3) ---
# Kita pakai Llama 3 (8B parameters) yang cepat dan gratis di Groq
llm = ChatGroq(
    groq_api_key=groq_api_key,
    model_name="llama-3.1-8b-instant",
    temperature=0
)

# --- 4. MEMBUAT RAG CHAIN (JEMBATAN) ---
# Chain ini menggabungkan: Retrieval (Cari data) -> Prompt -> LLM (Jawab)
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff", # "stuff" artinya semua teks relevan dimasukkan sekaligus ke prompt
    retriever=vector_db.as_retriever(search_kwargs={"k": 3}), # Ambil 3 chunk teratas
    return_source_documents=True # Agar kita tahu AI baca dari halaman mana
)

# --- 5. INTERAKSI (LOOP TANYA JAWAB) ---
print("\n🤖 Context AI Siap! (Ketik 'exit' untuk keluar)")
print("--------------------------------------------------")

while True:
    query = input("\nKamu: ")
    if query.lower() == "exit":
        break
    
    # Jalankan Chain
    print("⏳ Sedang berpikir...")
    response = qa_chain.invoke({"query": query})
    
    # Tampilkan Jawaban
    print(f"\n🤖 Context AI: {response['result']}")
    
    # (Opsional) Tampilkan Sumber
    print("\n[Sumber Referensi]:")
    for doc in response['source_documents']:
        print(f"- {doc.page_content[:100]}...") # Tampilkan 100 huruf awal sumbernya