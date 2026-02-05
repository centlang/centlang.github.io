{% extends docs %}

# Installation Guide

<div class="note">
    If you want to install Cent from source, go to
    <a href="/docs/install/source/">Installing from Source</a>.
</div>

## Linux

### 1. Download

Download the latest Cent release for your architecture:

- [x86_64](https://github.com/centlang/cent/releases/latest/download/cent-linux-x86_64.tar.xz)
- [aarch64](https://github.com/centlang/cent/releases/latest/download/cent-linux-aarch64.tar.xz)
- [riscv64](https://github.com/centlang/cent/releases/latest/download/cent-linux-riscv64.tar.xz)

### 2. Install

Extract the archive to `~/cent`:

```sh
$ mkdir -p ~/cent
$ tar -xJf cent-linux-x86_64.tar.xz -C ~/cent
```

Add `~/cent/bin` to your `$PATH` by adding this line to your `~/.bashrc` (for Bash):

```sh
export PATH="$PATH:$HOME/cent/bin"
```

Apply the changes:

```sh
$ source ~/.bashrc
```

### 3. Verify

Verify the installation:

```sh
$ centc --version
Cent v0.1
```

---

## Windows

<div class="warning">
    Windows is NOT supported, yet. Bugs WILL happen. Windows version of the
    compiler is only able to produce object files.
</div>

### 1. Download

Download the latest Cent release:

- [x86_64](https://github.com/centlang/cent/releases/latest/download/cent-windows-x86_64.zip)

### 2. Install

Extract the archive to `C:\cent`, then add `C:\cent\bin` to your `PATH`:

```bat
$ setx /M PATH "%PATH%;C:\cent\bin"
```

### 3. Verify

Open a new terminal and verify the installation:

```bat
$ centc --version
Cent v0.1
```

## Next steps

When you're ready, go to the [Language Overview](/docs/overview/) to learn more
about Cent.
