package com.example

class Greeter implements Serializable {
    def steps  // Jenkins steps (like echo, sh, etc.)

    Greeter(steps) {
        this.steps = steps
    }

    void greet(String name) {
        steps.echo "Hello, ${name}! This is from the Greeter class in src/."
    }
}
