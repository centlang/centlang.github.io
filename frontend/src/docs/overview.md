{% extends docs %}

# Language Overview

<div class="note">
    If you haven't installed Cent yet, refer to the
    <a href="/docs/install/">Installation Guide</a> or use
    <a href="/play/">Cent Playground</a> to run code right in your browser.
</div>

## Introduction

This tutorial assumes you are familiar with basic programming concepts and have
used another programming language before.

## Hello, world!

We'll write a simple program that prints `Hello, world!` to the screen. Create a
new file named `main.cn` with the following content:

```cent
with std::io;

fn main() {
    io::println("Hello, world!");
}
```

Now, run these commands to compile and execute the program:

```sh
$ centc main.cn
$ ./main
Hello, world!
```

You can also use the `--run` option to automatically run the compiled
executable:

```sh
$ centc main.cn --run
Hello, world!
```

## Variables

The `let` statement creates an _immutable_ variable.

```cent
let language = "Cent";
```

To create a _mutable_ variable, use the `mut` keyword.

```cent
mut score = 0;
score = 10;
```

Cent is statically typed, so you cannot change the type of a variable.

```cent
mut score = 10;
score = 4.5; // invalid!
```

## Comments

You can use comments to explain certain parts of your code. Comments start with
`//`.

```cent
let variable = 10; // this is a variable
```

## Constants

To create a constant, use the `const` keyword. Constants are computed at compile
time.

```cent
const PI = 3.14;
const GOLDEN_RATIO = 1.618;
const SECONDS_IN_A_DAY = 60 * 60 * 24;
```

It is a convention to name constants all uppercase with underscores between
words.

## Primitive types

### Integer types

Integer types start with either `i` or `u`. Integer types starting with `u` are
_unsigned_, meaning they can't be negative. After that, the size in bits is
specified:

```cent
i8 i16 i32 i64 // signed
u8 u16 u32 u64 // unsigned
```

Unsigned integer types can represent larger positive values than their signed
counterparts.

### Size types

You can use `usize` and `isize`. They have the size of the pointer type on the
current architecture and are commonly used for indexing.

### Floating-point types

Floating-point types are used to store numbers with decimal points. In Cent,
there are two such types: `f32` and `f64`.

### The `bool` type

A `bool` value is either `true` or `false`.

### The `rune` type

The `rune` type represents a Unicode code point.

### Strings

"What about the string type?" you may ask. In Cent, strings are actually just
arrays of bytes. We'll talk about them later.
