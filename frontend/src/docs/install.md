{% extends docs %}

# Installation Guide

<div class="note">
    If you want to install Cent from source, go to
    <a href="/docs/install/source">Installing from Source</a>.
</div>

## Linux

### 1. Download

Download the latest Cent release for your architecture:

- [Linux x86_64](https://github.com/centlang/cent/releases/latest/download/cent-linux-x86_64.tar.xz)

### 2. Install

Extract the archive you just downloaded to `/usr/local/`:

```sh
$ sudo tar -xJf cent-linux-x86_64.tar.xz -C /usr/local/
```

### 3. Verify

Verify the installation:

```sh
$ centc --version
Cent v0.1
```
