document.addEventListener("click", e => {
    const button = e.target.closest(".copy-button");

    if (!button) {
        return;
    }

    const code = button.parentElement.querySelector("pre");

    if (!code) {
        return;
    }

    navigator.clipboard.writeText(code.innerText);
});
