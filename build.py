import tempfile
import os
import re
import shutil
import markdown
import html
import pynvim

SRC_DIRS = ["docs/"]
TEMPLATES_DIR = "templates/"
BUILD_DIR = "build/"

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
    code = re.sub(
        r"{{\s*(\w+)\s*}}", lambda m: context.get(m.group(1), ""), code
    )

    match = re.match(r"{%\s*extends (\w+)\s*%}", code)

    if match:
        path = os.path.join(TEMPLATES_DIR, f"{match.group(1)}.html")
        context = context | {"content": re.sub(r"{%.*?%}", "", code)}

        return render_template(open(path).read(), context)

    return code

def render_page(code: str, md: bool = False) -> str:
    if md:
        match = re.match(r"{%\s*extends (\w+)\s*%}", code)

        if match:
            path = os.path.join(TEMPLATES_DIR, f"{match.group(1)}.html")

            content = markdown.Markdown(extensions=["toc", "fenced_code"])

            content_html = highlight_html(
                content.convert(re.sub(r"{%.*?%}", "", code))
            )

            return render_template(
                open(path).read(), {"content": content_html, "toc": content.toc}
            )

    return render_template(code, {})

def main():
    shutil.rmtree(BUILD_DIR, ignore_errors=True)
    os.makedirs(BUILD_DIR)

    shutil.copytree("static", os.path.join(BUILD_DIR, "static"))

    with open(os.path.join(BUILD_DIR, "index.html"), "w") as file:
        file.write(render_page(open("index.html").read()))

    for dir in SRC_DIRS:
        output_dir = BUILD_DIR + dir
        os.makedirs(output_dir)

        for root, _, files in os.walk(dir):
            for file in files:
                md = file.endswith(".md")

                if not md and not file.endswith(".html"):
                    continue

                input = os.path.join(root, file)
                relative = os.path.relpath(input, dir)

                if md:
                    output = os.path.join(
                        output_dir, relative.replace(".md", ""), "index.html"
                    )
                else:
                    output = os.path.join(output_dir, relative)

                os.makedirs(os.path.dirname(output), exist_ok=True)

                print(f"{input} -> {output}")

                with open(output, "w") as output_file:
                    output_file.write(render_page(open(input).read(), md))

if __name__ == "__main__":
    main()
