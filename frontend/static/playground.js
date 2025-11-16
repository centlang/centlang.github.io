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
    editorWrapper.style.height = `${editor.offsetHeight}px`;
    lines.style.height = `${editor.offsetHeight}px`;
}).observe(editor);

editor.addEventListener("scroll", () => {
    lines.scrollTop = editor.scrollTop;
});

editor.addEventListener("keydown", function (e) {
    if (e.key === "Tab") {
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

function escapeHtml(input) {
    return input
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&apos;");
}

function ansiStateToStyle(state) {
    const fg = {
        30: "var(--ansi-black)",
        31: "var(--ansi-red)",
        32: "var(--ansi-green)",
        33: "var(--ansi-yellow)",
        34: "var(--ansi-blue)",
        35: "var(--ansi-magenta)",
        36: "var(--ansi-cyan)",
        37: "var(--ansi-white)",
    };

    const bg = {
        40: "var(--ansi-black)",
        41: "var(--ansi-red)",
        42: "var(--ansi-green)",
        43: "var(--ansi-yellow)",
        44: "var(--ansi-blue)",
        45: "var(--ansi-magenta)",
        46: "var(--ansi-cyan)",
        47: "var(--ansi-white)",
    };

    let result = "";

    if (state.fg) {
        result += `color:${fg[state.fg]};`;
    }

    if (state.bg) {
        result += `background-color:${bg[state.bg]};`;
    }

    if (state.bold) {
        result += "font-weight:700;";
    }

    if (state.italic) {
        result += "font-style:italic;";
    }

    if (state.underline && state.strikethrough) {
        result += "text-decoration:underline line-through;";
    } else if (state.underline) {
        result += "text-decoration:underline;";
    } else if (state.strikethrough) {
        result += "text-decoration:line-through;";
    }

    return result;
}

function ansiToHtml(input) {
    const ANSI_CSI = /\x1b\[([0-9;]*)m/g;

    const RESET_STATE = {
        bold: false,
        italic: false,
        underline: false,
        strikethrough: false,
        fg: null,
        bg: null,
    };

    let match = ANSI_CSI.exec(input);
    let lastIndex = 0;

    let state = Object.assign({}, RESET_STATE);
    let result = "";

    while (match !== null) {
        result += `<span style="${ansiStateToStyle(state)}">${escapeHtml(input.substring(lastIndex, match.index))}</span>`;

        for (let c of match[1].split(";").map(Number)) {
            switch (c) {
                case 0:
                    state = Object.assign({}, RESET_STATE);
                    continue;
                case 1:
                    state.bold = true;
                    continue;
                case 3:
                    state.italic = true;
                    continue;
                case 4:
                    state.underline = true;
                    continue;
                case 9:
                    state.strikethrough = true;
                    continue;
                case 22:
                    state.bold = false;
                    continue;
                case 23:
                    state.italic = false;
                    continue;
                case 24:
                    state.underline = false;
                    continue;
                case 29:
                    state.strikethrough = false;
                    continue;
            }

            if (c >= 30 && c <= 37) {
                state.fg = c;
            } else if (c >= 40 && c <= 47) {
                state.bg = c;
            }
        }

        lastIndex = ANSI_CSI.lastIndex;
        match = ANSI_CSI.exec(input);
    }

    return result + input.substring(lastIndex);
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

        stderr.innerHTML = ansiToHtml(result.stderr).trim();
        stdout.innerHTML = ansiToHtml(result.stdout).trim();
        system.textContent = `Program returned ${result.exit}`;
    } catch (error) {
        stderr.innerHTML = "";
        stdout.innerHTML = "";
        system.textContent = `Failed to run code: ${error.message}`;
    }
}

editor.value =
    new URL(document.URL).searchParams.get("code") ??
    localStorage.getItem("code") ??
    DEFAULT_CODE;

updateLineNumbers();
