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

A variable's type can be specified explicitly:

```cent
mut score: i32 = 0;
```

Variables are zero-initialized if no value is given.

```cent
mut score: i32;
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

### Strings?

"What about the string type?" you may ask. In Cent, strings are actually just
arrays of bytes. We'll talk about them later.

## Functions

Functions are defined by using the `fn` keyword. The `main` function is the
entry point of the program. Functions can be used _before_ they're defined.

```cent
with std::io;

fn main() {
    hello_world();
}

fn hello_world() {
    io::println("Hello, world!");
}
```

You can specify the return type after the parentheses. If no return type is
specified, the function is assumed to return nothing. To return a value from a
function, use the `return` statement:

```cent
fn get_magic_number() i32 {
    return 42;
}
```

Functions can take parameters.

```cent
fn main() {
    let a = add(3, 4); // a = 7
}

fn add(a: i32, b: i32) i32 {
    return a + b;
}
```

### Default parameters

You can define _default_ parameters. If arguments aren't provided, the default
values are used.

```cent
fn main() {
    let ten = add(3, 7);
    let nine = add(3, 3, 3);
    let one = add(1, -1, 1, 0);
}

fn add(a: i32, b: i32, c: i32 = 0, d: i32 = 0) i32 {
    return a + b + c + d;
}
```

### Inner functions

Functions can be defined inside other functions. Inner functions are only
visible within the function where they are defined.

```cent
fn main() {
    fn square(x: i32) i32 {
        return x * x;
    }

    let a = square(7); // a = 49
}
```

## Control flow

### `if` statements

Use the `if` statement to branch your code depending on a condition.

```cent
with std::io;

fn main() {
    print_is_even(3); // x is odd
    print_is_even(4); // x is even
}

fn print_is_even(x: i32) {
    if x % 2 == 0 {
        io::println("x is even!");
    } else {
        io::println("x is odd!");
    }
}
```

You can use `else if` to check additional conditions.

```cent
with std::io;

fn greet(hour: u8) {
    if hour < 12 {
        io::println("Good morning!");
    } else if hour < 18 {
        io::println("Hello!");
    } else {
        io::println("Good evening!");
    }
}
```

### `switch` statements

The `switch` statement allows you to compare a value against several possible
cases:

```cent
with std::io;

fn day_of_week(day: u8) {
    switch day {
        1 { io::println("Monday"); }
        2 { io::println("Tuesday"); }
        3 { io::println("Wednesday"); }
        4 { io::println("Thursday"); }
        5 { io::println("Friday"); }
        6 { io::println("Saturday"); }
        7 { io::println("Sunday"); }
        else { io::println("Invalid day of week!"); }
    }
}
```

You can match multiple values in a single case.

```cent
with std::io;

fn is_weekend(day: u8) {
    switch day {
        1, 2, 3, 4, 5 { io::println("Weekday"); }
        6, 7 { io::println("Weekend!"); }
    }
}
```
