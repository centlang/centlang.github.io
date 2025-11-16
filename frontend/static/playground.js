const DEFAULT_CODE = `with std::io;

fn main() {
    io::println("Hello, world!");
}`;

const API_URL = "/api";

const editorTextarea = document.getElementById("editor-textarea");
const editorPre = document.getElementById("editor-pre");

const lines = document.getElementById("lines");

const stdout = document.getElementById("stdout");
const stderr = document.getElementById("stderr");
const system = document.getElementById("system");

const compilationMode = document.getElementById("compilation-mode");

editorTextarea.addEventListener("input", () => {
    updateLineNumbers();
    updateHighlight();
    localStorage.setItem("code", editorTextarea.value);
});

editorTextarea.addEventListener("scroll", () => {
    lines.scrollTop = editorTextarea.scrollTop;
    editorPre.scrollTop = editorTextarea.scrollTop;
    editorPre.scrollLeft = editorTextarea.scrollLeft;
});

editorTextarea.addEventListener("keydown", function (e) {
    if (e.key === "Tab") {
        e.preventDefault();

        const start = this.selectionStart;
        const end = this.selectionEnd;

        this.value =
            this.value.substring(0, start) + "    " + this.value.substring(end);

        this.selectionEnd = start + 4;
        this.selectionStart = this.selectionEnd;

        updateHighlight();
    }
});

function updateLineNumbers() {
    const length = editorTextarea.value.split("\n").length;
    let numbers = "";

    for (let i = 1; i <= length; ++i) {
        numbers += i + "\n";
    }

    lines.textContent = numbers;
}

function updateHighlight() {
    editorPre.innerHTML = highlightCent(editorTextarea.value);
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

        for (const c of match[1].split(";").map(Number)) {
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
                code: editorTextarea.value,
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

function highlightCent(input) {
    const TOKENS = [
        { className: "Comment", regex: /\/\/.*/y },
        { className: "String", regex: /"(?:\\.|[^"\\])*"/y },
        { className: "Number", regex: /\b[0-9][0-9_]*\b/y },
        { className: "Number", regex: /\b0x[0-9a-fA-F_]*\b/y },
        { className: "Number", regex: /\b0b[01_]*\b/y },
        { className: "Number", regex: /\b0o[0-7_]*\b/y },
        { className: "Number", regex: /\b[0-9][0-9_]*\.[0-9_]\+\b/y },
        {
            className: "Keyword",
            regex: /\b(pub|fn|type|union|enum|in|let|mut|const)\b/y,
        },
        { className: "Keyword", regex: /\b(extern|distinct|untagged)\b/y },
        {
            className: "Statement",
            regex: /\b(if|else|switch|return|break|continue|unreachable|while|for)\b/y,
        },
        { className: "Statement", regex: /\bwith\b/y },
        { className: "Boolean", regex: /\b(true|false)\b/y },
        { className: "Constant", regex: /\b(null|undefined)\b/y },
        {
            className: "Type",
            regex: /\b(i8|i16|i32|i64|isize|u8|u16|u32|u64|usize|f32|f64|bool|never)\b/y,
        },
        {
            className: "Operator",
            regex: /(?:\+|-|\*|\/|%|!|&|\||\^|<|>|=)=?|\|\||&&/y,
        },
    ];

    let result = "";
    let index = 0;

    while (index < input.length) {
        let matched = false;

        for (const t of TOKENS) {
            t.regex.lastIndex = index;
            const match = t.regex.exec(input);

            if (match !== null) {
                result += `<span class="${t.className}">${escapeHtml(match[0])}</span>`;
                index = t.regex.lastIndex;
                matched = true;
                break;
            }
        }

        if (!matched) {
            result += escapeHtml(input[index]);
            ++index;
        }
    }

    return result;
}

editorTextarea.value =
    new URL(document.URL).searchParams.get("code") ??
    localStorage.getItem("code") ??
    DEFAULT_CODE;

updateHighlight();
updateLineNumbers();
