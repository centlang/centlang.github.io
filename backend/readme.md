# Backend Structure

## `/run`

A run request simply consists of the source code and a build mode (`debug` or
`release`). The server starts a very small Alpine-based Docker container with a
static `centc` executable installed, then compiles and runs the code inside it.
Each run request has a 5-second timeout.
