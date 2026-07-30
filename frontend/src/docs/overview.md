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

The `let` statement creates an immutable variable.

```cent
let language = "Cent";
```

To create a mutable variable, use the `mut` keyword.

```cent
mut score = 0;
score = 10;
```

A variable's type can be specified explicitly:

```cent
mut score: i32 = 0;
```

If no initial value is given, the variable is zero-initialized.

```cent
mut score: i32;
```

Cent is statically typed, so you cannot change the type of a variable.

```cent
mut score = 10;
score = 4.5; // invalid!
```

You can _shadow_ a variable by declaring a new one with the same name:

```cent
mut score = 10;
mut score = 4.5;
score = 7.3;
```

```cent
mut score = 10;
let score = score; // score is no longer mutable
score = 7; // invalid!
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

## Data types

### Integer types

Integer type names start with `i` (signed) or `u` (unsigned), followed by the
size in bits:

```cent
i8 i16 i32 i64 // signed
u8 u16 u32 u64 // unsigned
```

```cent
let a: u64 = 3;
let b: i8 = -128;
```

There are special `usize` and `isize` types. They have the size of the pointer
type and are usually used for indexing.

### Floating-point types

Floating-point types are used to store numbers with decimal points. In Cent,
there are two such types: `f32` and `f64`.

```cent
let a: f32 = 3.5;
let b: f64 = 1.2345678;
```

### The `bool` type

A `bool` value is either `true` or `false`:

```cent
mut raining: bool = false;
raining = true;
```

### The `rune` type

The `rune` type represents a Unicode code point and is 4 bytes long.

```cent
let fire: rune = '🔥';
```

### Array types

Arrays use the `[N]T` syntax and hold multiple values of the same type:

```cent
let data = [4]u8{0xff, 0xff, 0xff, 0x0};
let data = [_]u8{0xff, 0xff, 0xff, 0x0}; // array length can be deduced
```

Arrays can be of _variable length_.

<div class="warning">
    Variable-length arrays are allocated on the stack, which has a limited size.
    If the array size is too large, this can result in a stack overflow.
</div>

```cent
mut n: usize = 16;
n = 1024;
mut data: [n]u8;
```

### Slice types

Slices use the `[]T` syntax and represent a view into a sequence of elements.
Slices have a pointer and a length.

```cent
mut data: [1024]u8;
let slice: []u8 = data;

let len = slice.len;
let ptr = slice.ptr;
```

Slices can be mutable:

```cent
mut data: [1024]u8;
let slice: []mut u8 = data;

slice[10] = 42;
```

### Strings

In Cent, strings are just arrays of bytes. By default, strings are **not**
null-terminated.

```cent
let language: [4]u8 = "Cent";
let language = [_]u8{'C' as u8, 'e' as u8, 'n' as u8, 't' as u8};

let null_terminated = "Hello, world!\0";
```

### Optional types

Optional values can either be `null` or contain a value. To create an optional
type, use the `?T` syntax:

```cent
mut optional: ?i32 = 32; // optional != null

optional = 42;
optional = null; // optional == null
```

To access the contained value without any checks, use the `.!` syntax:

```cent
mut optional: ?i32 = 32;
let value = optional.!;
```

To provide a default value when the optional is `null`, use the `??` operator:

```cent
let x: ?i32 = null;
let y = x ?? 42; // y = 42

let a: ?i32 = 10;
let b = a ?? 42; // b = 10
```

### Pointer types

A pointer references a value in memory. Pointer types use the `*T` syntax.

```cent
mut x = 42;
let ptr: *i32 = &x; // *ptr = 42
x = 422; // *ptr = 422
```

Pointers can be mutable:

```cent
mut x = 42;
let ptr: *mut i32 = &x;
*ptr = 422; // x = 422
```

<div class="note">
    In Cent, pointers can't be <code>null</code>. If you need a nullable
    pointer, use an <b>optional</b> pointer type. An optional pointer has the
    same size as a regular pointer.
</div>

### Tuple types

Tuples use the `(T1, T2, T3, ...)` syntax and hold multiple values of different
types:

```cent
mut data: (i32, f32, bool, [6]u8) = (10, 42.42, true, "Hello!");
data.0 += 32; // data.0 = 42
data.1 = data.0; // data.1 = 42
```

## `with` statements

Use `with` to import an external module.

```cent
with std::io;
with std::fs;

with std::posix as os; // import under a different name
```

You can also only import the things you use:

```cent
with buf::{Vector as Vec};
with io::{printf, eprintf};
```

## Functions

Functions are defined using the `fn` keyword. The `main` function is the entry
point of the program. Functions can be used before they're defined.

```cent
with std::io;

fn main() {
    hello_world();
}

fn hello_world() {
    io::println("Hello, world!");
}
```

The return type goes after the parentheses. If omitted, the function returns
nothing. Use `return` to send a value back:

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

Functions can have default parameters. When arguments are omitted, the default
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

## Control flow

### `if` statements

Use `if` to run different code depending on a condition.

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

### `while` loops

A `while` loop runs as long as the condition is `true`.

```cent
with std::io;

fn main() {
    mut i = 0;

    while i < 10 {
        i += 1;
    }

    io::print_int(i); // 10
    io::print_rune('\n');
}
```

You can use `while true` to create an infinite loop. To exit a loop, use the
`break` keyword.

```cent
with std::io;

fn main() {
    mut i = 0;

    while true {
        if i == 100 {
            break;
        }

        i += 2;
    }

    io::print_int(i); // 100
    io::print_rune('\n');
}
```

To skip an iteration, use the `continue` keyword:

```cent
with std::io;

fn main() {
    mut i = 0;
    mut sum = 0;

    while i < 10 {
        i += 1;

        if i % 2 == 0 {
            continue;
        }

        sum += i;
    }

    io::print_int(sum); // 25
    io::print_rune('\n');
}
```

### `for` loops

`for` loops allow you to iterate through a range or a sequence.

Exclusive ranges are created by using the `x..y` syntax:

```cent
with std::io;

fn main() {
    for i in 1..10 {
        io::print_int(i);
        io::print_rune('\n');
    }
}
```

To create an inclusive range, use the `x..=y` syntax:

```cent
with std::io;

fn main() {
    for i in 1..=10 {
        io::print_int(i);
        io::print_rune('\n');
    }
}
```

You can also iterate over arrays and slices:

```cent
with std::io;

fn main() {
    let data = [4]i32{10, 20, 30, 40};

    for x in data {
        io::print_int(x);
        io::print_rune('\n');
    }
}
```

You can mutate elements:

```cent
with std::io;

fn main() {
    let data = [4]i32{10, 20, 30, 40};

    for mut x in data {
        x = 0;
    }
}
```

## Literals

### Numeric literals

The `0x` prefix creates a hexadecimal literal. Use `0o` for octal and `0b` for
binary.

```cent
let hex = 0xff; // hex = 255
let oct = 0o777; // oct = 511
let bin = 0b101010; // bin = 42
```

You can insert underscores for better readability:

```cent
let big_number = 1_000_000_000; // big_number = 1000000000
```

Scientific notation is supported:

```cent
let one_million = 1e6;
```

### Character literals

You can use escape sequences for special characters:

```cent
let apostrophe = '\'';
let newline = '\n';
let carriage_return = '\r';
let tab = '\t';
let nullbyte = '\0';
```

Unicode characters can also be represented using escape sequences:

```cent
let smiling_face = '\U0001f604';
let omega = '\u03a9'; // '\u' for short codepoints
```

Character literals are of type `rune`.

### String literals

String literals are UTF-8 encoded sequences of bytes.

```cent
let string = "𝒰𝓃𝒾𝒸ℴ𝒹ℯ 💎";
```

## Expressions

### Binary expressions

| Operator                    | Precedence |
| --------------------------- | ---------- |
| `*` `/` `%`                 | 1          |
| `+` `-`                     | 2          |
| `<<` `>>`                   | 3          |
| `<` `>` `==` `!=` `>=` `<=` | 4          |
| `&`                         | 5          |
| `^`                         | 6          |
| `\|`                        | 7          |
| `&&`                        | 8          |
| `\|\|`                      | 9          |
| `??`                        | 10         |

```cent
let a = 2 + 3 * 6; // a = 20
```

### Unary expressions

```cent
let a = 5;
let b = !true; // b = false
mut c = -a; // c = -5
let p = &c;
*p = -c; // c = 5
```
