const droparea = document.querySelector(".drop")
const input = document.querySelector("#uploadimage")

state = {
    isDragging: false,
    wrongFile: false,
    file: null
}

input.addEventListener("change", () => {
    const files = input.files
    onDrop(files[0]);
})

const dragOver = () => {
    state.isDragging = true;
};
const dragLeave = () => {
    state.isDragging = false;
};

const displayImage = () => {
  document.querySelector("#ocr-img").src=URL.createObjectURL(state.file);
}

const onDrop = (file) => {
    // allows image only
    if (file.type.indexOf("image/") >= 0) {
        state.file=file
        displayImage()
    }
}

droparea.addEventListener("drop", (e) => {
    e.preventDefault()
    const files = e.dataTransfer.files;
    onDrop(files[0])
})

document.querySelector("#ocr-img").addEventListener("drop", (e) => {
    e.preventDefault()
    const files = e.dataTransfer.files;
    onDrop(files[0])
})

droparea.addEventListener("dragover", (event) => {
    // prevent default to allow drop
    event.preventDefault();
  });

document.onpaste = (event) => {
    event.preventDefault();
    var items = event.clipboardData?.items;
    for (let index in items) {
        var item = items[index];
        if (item.kind === 'file') {
            const blob = item.getAsFile();
            const reader = new FileReader();
            reader.onload = (pasteEvent) => {
                state.imageSource = pasteEvent.target?.result;
            };
            reader.readAsDataURL(blob);
            onDrop(blob);
        }
    }
};

function doOCR(){
    var data = new FormData()
    const language = document.getElementById('source_lang').value;
    data.append('file', state.file)
    data.append('language',language)
    fetch('/api/ocr', {
      method: 'POST',
      body: data
    })
    .then(response => response.json())
    .then(result => {
        document.querySelector("#resulttext").value=result.text
    })
    .catch(() => { /* Error. Inform the user */ })
}