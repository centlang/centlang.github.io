const codeSnippet = document.getElementById("code-snippet");
const runInPlayground = document.getElementById("run-in-playground");

function updateRunInPlayground() {
    let code = encodeURIComponent(codeSnippet.innerText);
    runInPlayground.href = `${runInPlayground.dataset.base}/play/?code=${code}`;
}

updateRunInPlayground();
