const DEFAULT_CODE = `with std::io;

fn main() {
    io::println("Hello, world!");
}`;

const API_URL = "/api";

const editor = document.getElementById("editor");
const editorWrapper = document.getElementById("editor-wrapper");
const lines = document.getElementById("lines");

const stdout = document.getElementById("stdout");
const stderr = document.getElementById("stderr");
const system = document.getElementById("system");

const compilationMode = document.getElementById("compilation-mode");

editor.addEventListener("input", () => {
    updateLineNumbers();
    localStorage.setItem("code", editor.value);
});

new ResizeObserver(() => {
    editorWrapper.style.height = editor.style.height;
    lines.style.height = editor.style.height;
}).observe(editor);

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

async function runCode() {
    try {
        stderr.textContent = "";
        stdout.textContent = "Running...";
        system.textContent = "";

        const response = await fetch(`${API_URL}/run`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                code: editor.value,
                mode: compilationMode.value,
            }),
        });

        const result = await response.json();

        if (!response.ok) {
            throw new Error(result.detail);
        }

        stderr.textContent = result.stderr;
        stdout.textContent = result.stdout;
        system.textContent = `Program returned ${result.exit}`;
    } catch (error) {
        stderr.textContent = "";
        stdout.textContent = "";
        system.textContent = `Failed to run code: ${error.message}`;
    }
}

editor.value =
    new URL(document.URL).searchParams.get("code") ??
    localStorage.getItem("code") ??
    DEFAULT_CODE;

updateLineNumbers();
