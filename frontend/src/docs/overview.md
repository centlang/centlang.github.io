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

You can use escape sequences in strings.

```cent
let message = "Hello\tworld\n";
```

Long string literals can be broken down to smaller ones:

```cent
let long_string = "this is a very "
    "loooooooooooooooooooooooooooooooooooooooooooooooooooooooooong "
    "striiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiing";
```

String literals can span multiple lines.

```cent
let shader =
"#version 330 core
void main() {}";
```

## Expressions

### Binary expressions

| Operator                    | Precedence | Meaning                                                                                                            |
| --------------------------- | ---------- | ------------------------------------------------------------------------------------------------------------------ |
| `*` `/` `%`                 | 1          | `*` - multiplication, `/` - division, `%` - modulo                                                                 |
| `+` `-`                     | 2          | `+` - addition, `-` - subtraction                                                                                  |
| `<<` `>>`                   | 3          | `<<` - left bitwise shift, `>>` - right bitwise shift                                                              |
| `<` `>` `==` `!=` `<=` `>=` | 4          | `<` - less than, `>` - greater than, `==` - equal, `!=` - not equal, `<=` - less or equal, `>=` - greater or equal |
| `&`                         | 5          | bitwise and                                                                                                        |
| `^`                         | 6          | exclusive or (XOR)                                                                                                 |
| `\|`                        | 7          | bitwise or                                                                                                         |
| `&&`                        | 8          | logical and                                                                                                        |
| `\|\|`                      | 9          | logical or                                                                                                         |
| `??`                        | 10         | null-coalescing                                                                                                    |

```cent
let a = 2 + 3 * 6; // a = 20
```

### Unary expressions

| Operator      | Meaning     |
| ------------- | ----------- |
| `-`           | negation    |
| `!`           | logical not |
| `*`           | dereference |
| `&`           | address-of  |
| `~`           | bitwise not |

```cent
let a = 5;
let b = !true; // b = false
mut c = -a; // c = -5
let p = &c;
*p = -c; // c = 5
```

### `as` expressions

The `as` operator converts a value to a different type:

```cent
let x = 42;
let y = x as f64; // y: f64 = 42.0
let z = 3.9 as u8; // z: u8 = 3
let c = 'A' as u8; // c: u8 = 65
```

## Module system

Each source file is a module. Files in the same directory share a translation
unit and can access each other's private items.

To make an item publicly accessible, use the `pub` keyword:

```cent
// src/module.cn

fn private() i32 {
    return 42;
}

pub fn public() i32 {
    return private() + 42;
}
```

```cent
// src/etc/other.cn

fn private() i32 {
    return 42;
}

pub fn public() i32 {
    return private() + 42;
}
```

```cent
// src/main.cn

with module;
with etc::other;

fn main() {
    let a = module::public();
    let b = other::public();

    let a = module::private(); // valid, same translation unit
    let b = other::private(); // invalid!
}
```

## Structs

You can use structs to create custom types. To create a struct, use the `type`
keyword.

```cent
type Vec3 {
    x: f32,
    y: f32,
    z: f32,
}

fn main() {
    let position = Vec3 { x: 10, y: 20, z: 30 };
    let z = position.z; // z == 30

    mut v = position;
    v.x = 42.5; // position.x == 10, v.x == 42.5
}
```

All struct fields are public. If some fields are not meant to be accessed,
prefix them with `_`:

```cent
type Timer {
    _seconds_left: f64,
}
```

### Nested structs

```cent
type Color {
    r: u8,
    g: u8,
    b: u8,
    a: u8,
}

type Button {
    text: []u8,
    color: Color,
}
```

## Unions

Unions are tagged by default. Tagged unions allow a value to be one of several
types.

```cent
union Value {
    int: i32,
    float: f32,
    string: []u8,
}
```

You can use `switch` on tagged unions.

```cent
fn main() {
    let v = Value { float: 42 };

    switch v {
        Value::int { io::print_int(v.int); }
        Value::float { io::print_float(v.float); }
        Value::string { io::print(v.string); }
    }
}
```

If you need a C-style union, mark it as `#(untagged)`:

```cent
type Rgb {
    r: u8,
    g: u8,
    b: u8,
    a: u8,
}

#(untagged)
union Pixel {
    colors: Rgb,
    raw: u32,
}
```

## Enums

Enums represent a type with a fixed set of possible values:

```cent
enum Color {
    red,
    green,
    blue,
}

enum Numbers {
    one = 1,
    two, // = 2
    three, // = 3
}
```

You can use `switch` on enum types.

```cent
fn main() {
    let c = Color::red;

    switch c {
        Color::red { io::println("red"); }
        Color::green { io::println("green"); }
        Color::blue { io::println("blue"); }
    }
}
```

You can explicitly specify the underlying type.

```cent
enum Color u8 {
    red,
    green,
    blue,
}
```

## Attributes

Attributes use the `#(...)` syntax:

```cent
#(extern, posix)
fn fork() pid_t;
```

You can apply attributes to multiple declarations at once:

```cent
#(extern, posix) {
    fn fork() pid_t;
    fn getpid() pid_t;
}
```

## Type aliases

Use the `type` keyword to create a type alias:

```cent
type Age = i32;

fn main() {
    mut age: Age = 25;
    age += 2;
}
```

If you don't want an alias type to be treated exactly like the original type,
mark it as `#(distinct)`:

```cent
#(distinct)
type Id = i32;

fn main() {
    mut id = 123456 as Id;
    id += 2; // invalid!
}
```

## `for` blocks

Methods and associated functions are defined inside `for` blocks.

```cent
type Vec2 {
    x: f32,
    y: f32,
}

for Vec2 {
    fn right(length: f32) Self {
        return Self { x: length, y: 0 };
    }

    fn length_squared(self: Self) f32 {
        return self.x * self.x + self.y * self.y;
    }
}

fn main() {
    let v = Vec2::right();
    let l = v.length_squared();
}
```

Modifying methods take a mutable pointer to `self`.

```cent
for Vec2 {
    fn reset(self: *mut Self) {
        self.x = 0;
        self.y = 0;
    }
}
```

## Function pointers

Function pointer types use the `*fn(a: T, b: U, ...) R` syntax:

```cent
fn add(a: i32, b: i32) i32 {
    return a + b;
}

fn main() {
    let fn_ptr: *fn(a: i32, b: i32) i32 = &add;
    let seven = fn_ptr(3, 4);
}
```

## `defer` statements

The `defer` statement schedules a block of code to run when the current scope is
exited.

```cent
with std::fs;

fn main() {
    let file = fs::open("text.txt", fs::Mode::read)
        ?? core::panic("failed to open file");

    defer file.close();
}
```

## `unreachable` statements

`unreachable` indicates that a code path should never be reached at runtime:

```cent
fn divide(a: i32, b: i32) i32 {
    if b != 0 {
        return a / b;
    }

    unreachable;
}
```

Reaching `unreachable` is undefined behavior.
