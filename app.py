import streamlit as st
import os
import time
import shutil
from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_groq import ChatGroq
from langchain_classic.chains import RetrievalQA
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.prompts import PromptTemplate

# --- 1. CONFIG & SETUP ---
st.set_page_config(page_title="Context AI Pro", page_icon="⚡", layout="wide")

# Folder untuk Database & File Sementara
DB_PATH = "db_context"
TEMP_FOLDER = "temp_files"

# Pastikan folder temp ada
if not os.path.exists(TEMP_FOLDER):
    os.makedirs(TEMP_FOLDER)

# Load API Key
load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")

# --- 2. CUSTOM CSS (MODERN UI) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    
    /* Judul Gradient */
    .gradient-text {
        background: linear-gradient(90deg, #4b6cb7 0%, #182848 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: bold;
        font-size: 2.5em;
    }

    /* Card Stats di Sidebar */
    .metric-card {
        background-color: #f8f9fa;
        border: 1px solid #e9ecef;
        padding: 10px;
        border-radius: 8px;
        text-align: center;
        margin-bottom: 10px;
    }

    /* Chat Bubbles Clean */
    div[data-testid="stChatMessage"] {
        background-color: #ffffff !important;
        border: 1px solid #e0e0e0;
        border-radius: 12px;
        padding: 15px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    div[data-testid="stChatMessage"] * { color: #1f1f1f !important; }
    div[data-testid="stChatMessage"][data-testid="user"] { background-color: #eef2ff !important; }
    
    #MainMenu, footer, header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- 3. FUNGSI BACKEND (CORE LOGIC) ---

def get_llm():
    """Mengambil model LLM Llama 3.1"""
    if not groq_api_key:
        st.error("❌ API Key tidak ditemukan!")
        st.stop()
    return ChatGroq(groq_api_key=groq_api_key, model_name="llama-3.1-8b-instant", temperature=0)

def get_embeddings():
    """Mengambil model Embedding"""
    return HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

def reset_database():
    """Menghapus total database (DELETE)"""
    if os.path.exists(DB_PATH):
        shutil.rmtree(DB_PATH) # Hapus folder db
    st.session_state.db_initialized = False
    st.toast("Database berhasil di-reset!", icon="🗑️")

def process_documents(uploaded_files):
    """Memproses file PDF baru (CREATE/UPDATE)"""
    if not uploaded_files:
        return
    
    total_chunks = 0
    documents = []
    
    progress_text = st.empty()
    progress_bar = st.progress(0)

    # 1. Simpan & Load PDF
    for i, file in enumerate(uploaded_files):
        progress_text.text(f"⏳ Membaca file: {file.name}...")
        temp_path = os.path.join(TEMP_FOLDER, file.name)
        
        with open(temp_path, "wb") as f:
            f.write(file.getbuffer())
            
        loader = PyPDFLoader(temp_path)
        docs = loader.load()
        documents.extend(docs)
        
        # Hapus file temp biar hemat storage
        os.remove(temp_path)
        progress_bar.progress((i + 1) / len(uploaded_files))

    # 2. Chunking
    progress_text.text("✂️ Memecah dokumen menjadi potongan kecil...")
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = text_splitter.split_documents(documents)
    total_chunks = len(chunks)

    # 3. Embedding & Storing
    progress_text.text(f"💾 Menyimpan {total_chunks} memori baru ke otak AI...")
    
    if chunks:
        vector_db = Chroma.from_documents(
            documents=chunks,
            embedding=get_embeddings(),
            persist_directory=DB_PATH
        )
        st.session_state.db_initialized = True
        st.toast(f"Sukses! {len(uploaded_files)} dokumen dipelajari ({total_chunks} chunks).", icon="✅")
    
    progress_text.empty()
    progress_bar.empty()

# --- 4. SIDEBAR CONTROLS ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2585/2585589.png", width=50)
    st.markdown("### **Control Panel**")
    
    # MODE SELECTION
    mode = st.radio("Pilih Mode AI:", ["💬 General Chat", "📄 Tanya Dokumen"], index=1)
    
    st.divider()

    # DOCUMENT MANAGER (Hanya aktif di mode Tanya Dokumen)
    if mode == "📄 Tanya Dokumen":
        st.markdown("**📂 Manajemen Dokumen**")
        uploaded_files = st.file_uploader("Upload PDF Baru", type="pdf", accept_multiple_files=True)
        
        if st.button("Proses Dokumen", type="primary"):
            with st.spinner("Sedang melatih AI..."):
                process_documents(uploaded_files)
        
        st.divider()
        
        # CRUD: DELETE (Reset DB)
        col_del1, col_del2 = st.columns([3, 1])
        with col_del1:
            st.caption("Hapus semua ingatan dokumen?")
        with col_del2:
            if st.button("🗑️", help="Reset Database"):
                reset_database()
                st.rerun()

    st.markdown("---")
    # STATUS DATABASE
    db_exists = os.path.exists(DB_PATH) and os.listdir(DB_PATH)
    status_color = "green" if db_exists else "red"
    status_text = "Aktif" if db_exists else "Kosong"
    
    st.markdown(f"""
    <div class='metric-card'>
        <small>Status Database</small><br>
        <b style='color:{status_color}'>● {status_text}</b>
    </div>
    """, unsafe_allow_html=True)

# --- 5. MAIN INTERFACE ---
st.markdown('<p class="gradient-text">Context AI Pro</p>', unsafe_allow_html=True)

if mode == "💬 General Chat":
    st.caption("🤖 Mode: Asisten Pintar (Seperti ChatGPT)")
else:
    st.caption("📄 Mode: Analisis Dokumen (RAG)")

# Inisialisasi History Chat
if "messages" not in st.session_state:
    st.session_state.messages = []

# Tampilkan Chat
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- 6. LOGIKA JAWABAN (THE BRAIN) ---
if prompt := st.chat_input("Ketik pesan kamu..."):
    # Tampilkan pesan user
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Proses Jawaban
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        try:
            llm = get_llm()
            
            # --- JALUR 1: GENERAL CHAT ---
            if mode == "💬 General Chat":
                # Langsung tanya ke LLM tanpa cari dokumen
                response_stream = llm.stream(prompt) # Pakai stream biar ngetik
                
                for chunk in response_stream:
                    if chunk.content:
                        full_response += chunk.content
                        message_placeholder.markdown(full_response + "▌")
                message_placeholder.markdown(full_response)

            # --- JALUR 2: RAG (DOKUMEN) ---
            else:
                # Cek dulu databasenya ada isinya gak?
                if not (os.path.exists(DB_PATH) and os.listdir(DB_PATH)):
                    st.warning("⚠️ Database dokumen kosong! Silakan upload PDF dulu di sidebar.")
                    full_response = "Saya belum punya dokumen untuk dibaca. Upload dulu ya!"
                    message_placeholder.markdown(full_response)
                else:
                    embeddings = get_embeddings()
                    vector_db = Chroma(persist_directory=DB_PATH, embedding_function=embeddings)
                    
                    # Prompt Khusus agar AI tidak halusinasi
                    qa_prompt = PromptTemplate(
                        template="""Anda adalah asisten analisis dokumen.
                        Gunakan potongan konteks berikut untuk menjawab pertanyaan.
                        Jika jawaban tidak ada di konteks, katakan "Maaf, informasi tidak ditemukan di dokumen."
                        
                        Konteks: {context}
                        
                        Pertanyaan: {question}
                        
                        Jawaban:""",
                        input_variables=["context", "question"]
                    )
                    
                    chain = RetrievalQA.from_chain_type(
                        llm=llm,
                        chain_type="stuff",
                        retriever=vector_db.as_retriever(search_kwargs={"k": 3}),
                        return_source_documents=True,
                        chain_type_kwargs={"prompt": qa_prompt}
                    )
                    
                    with st.spinner("🔍 Mencari di dokumen..."):
                        response = chain.invoke({"query": prompt})
                        answer = response['result']
                        sources = response['source_documents']
                        
                        # Efek ngetik manual untuk RAG (karena chain tidak selalu stream)
                        for word in answer.split():
                            full_response += word + " "
                            time.sleep(0.05)
                            message_placeholder.markdown(full_response + "▌")
                        message_placeholder.markdown(full_response)
                        
                        # Tampilkan Sumber
                        with st.expander("📚 Sumber Referensi"):
                            for i, doc in enumerate(sources):
                                st.markdown(f"**Sumber {i+1} (Hal {doc.metadata.get('page', '?') + 1}):**")
                                st.info(doc.page_content[:200] + "...")

        except Exception as e:
            st.error(f"Error: {e}")
            full_response = "Maaf, terjadi kesalahan sistem."

    st.session_state.messages.append({"role": "assistant", "content": full_response})