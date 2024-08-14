from dotenv import load_dotenv
import os

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# Obtém a chave da API do VirusTotal
API_KEY = os.getenv("VIRUSTOTAL_API_KEY")

print(f"API_KEY: {API_KEY}")
