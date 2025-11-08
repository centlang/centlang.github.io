const editor = document.getElementById("editor");
const lines = document.getElementById("lines");

editor.addEventListener("input", updateLineNumbers);

editor.addEventListener("scroll", () => {
    lines.scrollTop = editor.scrollTop;
});

editor.addEventListener("keydown", function (e) {
    if (e.key == "Tab") {
        e.preventDefault();

        const start = this.selectionStart;
        const end = this.selectionEnd;

        this.value =
            this.value.substring(0, start) + "    " + this.value.substring(end);

        this.selectionEnd = start + 4;
        this.selectionStart = this.selectionEnd;
    }
});

function updateLineNumbers() {
    const length = editor.value.split("\n").length;
    let numbers = "";

    for (let i = 1; i <= length; ++i) {
        numbers += i + "\n";
    }

    lines.textContent = numbers;
}

updateLineNumbers();
