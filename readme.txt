Instalar Ollama
winget intall Ollama.Ollama

Baixar o modelo
ollama pull qwen3:14b

testar
ollama run qwen3:14b

Criar ambiente python
python -m venv venv
venv\Scripts\activate

//erro de segurança no powrshell 
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

intalar requerimets
pip install -r requirements.txt


ollama list

uvicorn app:app --reload