import sys
import os

print("--- DIAGNOSA CONTEX AI ---")

# 1. Cek Python yang dipakai
print(f"1. Python Executable: {sys.executable}")

# 2. Cek File .env
env_path = os.path.join(os.getcwd(), '.env')
if os.path.exists(env_path):
    print("2. File .env ditemukan: ✅ ADA")
else:
    print(f"2. File .env ditemukan: ❌ TIDAK ADA (Cari di: {env_path})")

# 3. Cek Library
print("3. Cek Import Library...")
try:
    from langchain_chroma import Chroma
    print("   - langchain_chroma: ✅ OK")
except ImportError as e:
    print(f"   - langchain_chroma: ❌ ERROR ({e})")

try:
    from langchain_huggingface import HuggingFaceEmbeddings
    print("   - langchain_huggingface: ✅ OK")
except ImportError as e:
    print(f"   - langchain_huggingface: ❌ ERROR ({e})")

try:
    from dotenv import load_dotenv
    load_dotenv()
    key = os.getenv("GROQ_API_KEY")
    if key:
        print(f"4. API Key Terbaca: ✅ (Depan: {key[:5]}...)")
    else:
        print("4. API Key Terbaca: ❌ KOSONG (Cek isi file .env)")
except Exception as e:
    print(f"4. Error baca .env: {e}")

print("---------------------------")