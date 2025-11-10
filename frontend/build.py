import tempfile
import os
import re
import shutil
import json
import markdown
import html
import pynvim

SRC_DIR = "src/"
STATIC_DIR = "static/"
TEMPLATES_DIR = "templates/"
BUILD_DIR = "build/"

TRANSLATIONS = json.load(open("translations.json"))

nvim = pynvim.attach(
    "child", argv=["nvim", "--embed", "--headless", "-u", "NONE"]
)

nvim.command("syntax on")
nvim.command("runtime! plugin/tohtml.lua")

def nvim_to_html(code: str, lang: str) -> str:
    with tempfile.NamedTemporaryFile("w", delete=False) as tmp_input:
        tmp_input_path = tmp_input.name
        tmp_input.write(code)
        tmp_input.flush()

    with tempfile.NamedTemporaryFile(delete=False) as tmp_output:
        tmp_output_path = tmp_output.name

    nvim.command(f"e {tmp_input_path}")
    nvim.command(f"set ft={lang}")
    nvim.command("TOhtml")
    nvim.command(f"w! {tmp_output_path}")
    nvim.command("%bd!")

    html = open(tmp_output_path).read()
    match = re.search(r"<pre>(.*?)</pre>", html, flags=re.DOTALL)

    os.remove(tmp_input_path)
    os.remove(tmp_output_path)

    return f"<pre>{(match.group(1) if match else code).strip()}</pre>"

def highlight_html(code: str) -> str:
    return re.sub(
        r'<pre><code(?:\s+class="language-(\w+)")?>(.*?)</code></pre>',
        lambda m: nvim_to_html(html.unescape(m.group(2)), m.group(1)),
        code,
        flags=re.DOTALL,
    )

def render_template(code: str, context: dict) -> str:
    def get_var(match):
        result = context

        for value in match.group(1).split("."):
            result = result[value]

        return str(result)

    code = re.sub(r"{{\s*([\w.-]+)\s*}}", get_var, code)

    match = re.match(r"{%\s*extends (\w+)\s*%}", code)

    if match:
        path = os.path.join(TEMPLATES_DIR, f"{match.group(1)}.html")
        context = context | {"content": re.sub(r"{%.*?%}", "", code)}

        return render_template(open(path).read(), context)

    return code

def render_page(
    code: str, context: dict | None = None, md: bool = False
) -> str:
    if context is None:
        context = {}

    if md:
        match = re.match(r"{%\s*extends (\w+)\s*%}", code)

        if match:
            path = os.path.join(TEMPLATES_DIR, f"{match.group(1)}.html")

            content = markdown.Markdown(extensions=["toc", "fenced_code"])

            content_html = highlight_html(
                content.convert(re.sub(r"{%.*?%}", "", code))
            )

            return render_template(
                open(path).read(),
                context | {"content": content_html, "toc": content.toc},
            )

    return render_template(code, context)

def build_files(src_dir: str, build_dir: str, language: str):
    for root, dirs, files in os.walk(src_dir):
        dirs[:] = [d for d in dirs if d not in TRANSLATIONS]

        for file in files:
            md = file.endswith(".md")

            if not md and not file.endswith(".html"):
                continue

            input = os.path.join(root, file)
            relative = os.path.relpath(input, src_dir)

            if md:
                output = os.path.join(
                    build_dir, relative.replace(".md", ""), "index.html"
                )
            else:
                output = os.path.join(build_dir, relative)

            if os.path.exists(output):
                continue

            os.makedirs(os.path.dirname(output), exist_ok=True)

            if language != "default":
                print(f"[{language}]", end=" ")

            print(f"{input} -> {output}")

            with open(output, "w") as output_file:
                output_file.write(
                    render_page(
                        open(input).read(),
                        context={
                            "t": TRANSLATIONS[language],
                            "page": {
                                "base": (
                                    f"/{language}"
                                    if language != "default"
                                    else ""
                                )
                            },
                        },
                        md=md,
                    )
                )

def main():
    shutil.rmtree(BUILD_DIR, ignore_errors=True)
    os.makedirs(BUILD_DIR)

    shutil.copytree(STATIC_DIR, os.path.join(BUILD_DIR, "static"))

    for language in TRANSLATIONS:
        if language == "default":
            build_files(SRC_DIR, BUILD_DIR, language)
        else:
            build_files(
                os.path.join(SRC_DIR, language),
                os.path.join(BUILD_DIR, language),
                language,
            )

            build_files(SRC_DIR, os.path.join(BUILD_DIR, language), language)

if __name__ == "__main__":
    main()
