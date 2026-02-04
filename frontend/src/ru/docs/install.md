{% extends docs %}

# Руководство по установке

<div class="note">
    Если вы хотите установить Cent из исходников, перейдите в раздел
    <a href="/ru/docs/install/source/">Установка из исходников</a>.
</div>

## Linux

### 1. Загрузка

Скачайте последнюю версию Cent для вашей архитектуры:

- [x86_64](https://github.com/centlang/cent/releases/latest/download/cent-linux-x86_64.tar.xz)
- [aarch64](https://github.com/centlang/cent/releases/latest/download/cent-linux-aarch64.tar.xz)
- [riscv64](https://github.com/centlang/cent/releases/latest/download/cent-linux-riscv64.tar.xz)

### 2. Установка

Распакуйте архив в `~/cent`:

```sh
$ mkdir -p ~/cent
$ tar -xJf cent-linux-x86_64.tar.xz -C ~/cent
```

Добавьте `~/cent/bin` в ваш `$PATH`, добавив эту строку в `~/.bashrc` (для
Bash):

```sh
export PATH="$PATH:$HOME/cent/bin"
```

Примените изменения:

```sh
$ source ~/.bashrc
```

### 3. Проверка

Проверьте установку:

```sh
$ centc --version
Cent v0.1
```

## Windows

<div class="warning">
    Поддержка Windows ещё НЕ реализована. Будут ошибки. Версия компилятора для
    Windows может только создавать объектные файлы.
</div>

### 1. Загрузка

Скачайте последнюю версию Cent:

- [x86_64](https://github.com/centlang/cent/releases/latest/download/cent-windows-x86_64.zip)

### 2. Установка

Распакуйте архив в `C:\cent`, затем добавьте `C:\cent\bin` в переменную
окружения `PATH`:

```bat
$ setx /M PATH "%PATH%;C:\cent\bin"
```

### 3. Проверка

Откройте новый терминал и проверьте установку:

```bat
$ centc --version
Cent v0.1
```

## Следующие шаги

Когда будете готовы, перейдите в раздел [Обзор языка](/docs/overview/), чтобы
узнать больше о Cent.
