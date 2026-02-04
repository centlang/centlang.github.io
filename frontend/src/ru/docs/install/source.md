{% extends docs %}

# Установка из исходников

## Linux

### 1. Установка зависимостей для сборки

Debian/Ubuntu:

```sh
$ sudo apt-get install -y build-essential cmake ninja-build git
```

Arch Linux:

```sh
$ sudo pacman -Syu cmake ninja gcc git
```

Void Linux:

```sh
$ sudo xbps-install -Syu cmake ninja gcc git
```

### 2. Клонирование

Клонируйте репозиторий:

```sh
$ git clone https://github.com/centlang/cent && cd cent
```

### 3. Сборка и установка

Соберите:

```sh
$ mkdir build && cd build
$ cmake .. -DCMAKE_BUILD_TYPE=Release -GNinja
$ ninja
```

Установите:

```sh
$ sudo ninja install
```

### 4. Проверка

Проверьте установку:

```sh
$ centc --version
Cent v0.1
```
