async function analyze() {
    const url = document.getElementById("url").value;

    const res = await fetch("/analyze", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({url})
    });

    const data = await res.json();
    if (data.error) return alert("Invalid URL");

    document.getElementById("thumb").src = data.thumbnail;
    document.getElementById("thumb").hidden = false;
    document.getElementById("title").innerText = data.title;

    const q = document.getElementById("quality");
    q.innerHTML = "";
    data.formats.forEach(f => {
        q.innerHTML += `<option>${f}</option>`;
    });
}

async function download() {
    const payload = {
        url: url.value,
        mode: audio.checked ? "audio" : "video",
        quality: quality.value,
        audio_format: audioFormat.value
    };

    document.getElementById("status").innerText = "Downloading...";

    await fetch("/download", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(payload)
    });

    document.getElementById("status").innerText = "Download Complete!";
}
