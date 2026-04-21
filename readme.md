# centlang.org

Website for Cent programming language, built completely from scratch.

![Preview](assets/preview.png)

## Running locally

Requirements:

- Python 3
- Docker (for language playground)
- Neovim (for syntax highlighting)
- cent.vim (for Cent syntax highlighting)

Clone the repository:

```sh
$ git clone https://github.com/centlang/centlang.org
$ cd centlang.org
```

Build the website:

```sh
$ cd frontend
$ pip install -r requirements.txt
$ python build.py
$ cd ..
```

Prepare the backend:

```sh
$ cd backend
$ docker build -t centc .
$ pip install -r requirements.txt
$ cd ..
```

Run the backend:

```sh
$ CF_TURNSTILE_KEY=YOUR_KEY uvicorn api:app --app-dir backend
```

Serve the frontend:

```sh
$ python -m http.server -d frontend/build 8000
```
