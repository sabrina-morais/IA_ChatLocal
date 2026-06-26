console.log("APP.JS CARREGADO");

function setStatus(msg){

    document
        .getElementById("status-box")
        .innerText = msg;
}


async function sendMessage(){

    const input =
        document.getElementById("message");

    const chat =
        document.getElementById("chat-box");

    const msg =
        input.value.trim();

    if(!msg){
        return;
    }

    chat.innerHTML += `
        <div class="user-msg">
            <b>Você:</b><br>${msg}
        </div>
    `;

    input.value = "";

    const loading =
        document.createElement("div");

    loading.className = "bot-msg";

    loading.id = "loading";

    loading.innerHTML =
        "🤖 Qwen está pensando...";

    chat.appendChild(loading);

    setStatus(
        "Consultando modelo..."
    );

    try{

        const response =
            await fetch("/chat",{

                method:"POST",

                headers:{
                    "Content-Type":"application/json"
                },

                body:JSON.stringify({
                    message:msg
                })
            });

        const data =
            await response.json();

        loading.remove();

        chat.innerHTML += `
            <div class="bot-msg">
                <b>Qwen:</b><br>
                ${marked.parse(data.response)}
            </div>
        `;

        setStatus("Pronto");

    }
    catch(error){

        console.error(error);

        loading.remove();

        chat.innerHTML += `
            <div class="error-msg">
                Erro ao consultar modelo.
            </div>
        `;

        setStatus("Erro");
    }

    chat.scrollTop =
        chat.scrollHeight;
}


async function uploadPDF(){

    const file =
        document.getElementById("pdf-file")
        .files[0];

    if(!file){

        setStatus(
            "Selecione um PDF."
        );

        return;
    }

    setStatus(
        "Enviando PDF..."
    );

    const formData =
        new FormData();

    formData.append(
        "file",
        file
    );

    const response =
        await fetch(
            "/upload",
            {
                method:"POST",
                body:formData
            }
        );

    const data =
        await response.json();

    setStatus(data.message);
}


async function uploadAudio(){

    const file =
        document.getElementById("audio-file")
        .files[0];

    if(!file){

        setStatus(
            "Selecione um áudio."
        );

        return;
    }

    setStatus(
        "Enviando áudio..."
    );

    const formData =
        new FormData();

    formData.append(
        "file",
        file
    );

    const response =
        await fetch(
            "/upload-audio",
            {
                method:"POST",
                body:formData
            }
        );

    const data =
        await response.json();

    setStatus(data.message);
}


async function uploadVideo(){

    const file =
        document.getElementById("video-file")
        .files[0];

    if(!file){

        setStatus(
            "Selecione um vídeo."
        );

        return;
    }

    setStatus(
        "Enviando vídeo..."
    );

    const formData =
        new FormData();

    formData.append(
        "file",
        file
    );

    const response =
        await fetch(
            "/upload-video",
            {
                method:"POST",
                body:formData
            }
        );

    const data =
        await response.json();

    setStatus(data.message);
}


async function ingestDocuments(){

    setStatus(
        "Indexando documentos..."
    );

    const response =
        await fetch(
            "/ingest",
            {
                method:"POST"
            }
        );

    const data =
        await response.json();

    setStatus(data.message);
}

async function clearChat(){

    await fetch(
        "/clear",
        {
            method:"POST"
        }
    );

    document
        .getElementById(
            "chat-box"
        )
        .innerHTML = "";

    setStatus(
        "Nova conversa iniciada"
    );
}

document.addEventListener(
    "DOMContentLoaded",
    () => {

        document
            .getElementById("btn-send")
            .addEventListener(
                "click",
                sendMessage
            );

        document
            .getElementById("btn-pdf")
            .addEventListener(
                "click",
                uploadPDF
            );

        document
            .getElementById("btn-audio")
            .addEventListener(
                "click",
                uploadAudio
            );

        document
            .getElementById("btn-video")
            .addEventListener(
                "click",
                uploadVideo
            );

        document
            .getElementById("btn-ingest")
            .addEventListener(
                "click",
                ingestDocuments
            );

        document
            .getElementById("btn-clear")
            .addEventListener(
                "click",
                clearChat
            );

        document
            .getElementById("message")
            .addEventListener(
                "keydown",
                function(e){

                    if(
                        e.key === "Enter"
                        &&
                        !e.shiftKey
                    ){

                        e.preventDefault();

                        sendMessage();
                    }
                }
            );

    }
);