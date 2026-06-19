async function sendMessage(){

    const msg =
        document.getElementById("message")
        .value;

    if(!msg) return;

    const chat =
        document.getElementById("chat-box");

    chat.innerHTML +=
    `<div class="user-msg">
        ${msg}
    </div>`;

    document
    .getElementById("message")
    .value = "";

    document
    .getElementById("status-box")
    .innerHTML =
    "🤖 Qwen está pensando...";

    const response =
        await fetch("/chat",{
            method:"POST",
            headers:{
                "Content-Type":
                "application/json"
            },
            body:JSON.stringify({
                message:msg
            })
        });

    const data =
        await response.json();

    chat.innerHTML +=
    `<div class="bot-msg">
        ${data.response}
    </div>`;

    document
    .getElementById("status-box")
    .innerHTML =
    "Pronto";

    chat.scrollTop =
        chat.scrollHeight;
}


async function uploadPDF(){

    const file =
    document.getElementById(
        "pdf-file"
    ).files[0];

    if(!file){

        alert("Selecione PDF");
        return;
    }

    document
    .getElementById("status-box")
    .innerHTML =
    "📤 Enviando PDF...";

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

    document
    .getElementById("status-box")
    .innerHTML =
    data.message;
}


async function ingestPDFs(){

    document
    .getElementById("status-box")
    .innerHTML =
    "📚 Indexando PDF...";

    const response =
        await fetch(
            "/ingest",
            {
                method:"POST"
            }
        );

    const data =
        await response.json();

    document
    .getElementById("status-box")
    .innerHTML =
    data.message;
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
    ).innerHTML = "";
}