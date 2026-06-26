Processador	12th Gen Intel(R) Core(TM) i5-12450H (2.00 GHz)
RAM instalada	16,0 GB (utilizável: 15,7 GB)
Placa gráfica	NVIDIA GeForce RTX 2050 (4 GB)
Intel(R) UHD Graphics (128 MB)
Armazenamento	224 GB de 477 GB usados
Tipo de sistema	Sistema operacional de 64 bits, processador baseado em x64
Caneta e toque	Nenhuma entrada à caneta ou por toque disponível para este vídeo



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