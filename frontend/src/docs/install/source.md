{% extends docs %}

# Installing from Source

## Linux

### 1. Install build dependencies

Void Linux:

```sh
$ sudo xbps-install -Syu cmake ninja gcc git
```

Debian/Ubuntu:

```sh
$ sudo apt-get install -y build-essential cmake ninja-build git
```

Arch Linux:

```sh
$ sudo pacman -Syu cmake ninja gcc git
```

### 2. Clone

Clone the repository:

```sh
$ git clone https://github.com/centlang/cent && cd cent
```

### 3. Build and install

Build:

```sh
$ mkdir build && cd build
$ cmake .. -DCMAKE_BUILD_TYPE=Release -GNinja
$ ninja
```

Install:

```sh
$ sudo ninja install
```

### 4. Verify

Verify the installation:

```sh
$ centc --version
Cent v0.1
```
