# Automata Engine

A zero-dependency, lightweight Python engine for parsing and simulating Finite State Machines (FSMs) from first principles. 

This engine supports both **Deterministic Finite Automata (DFA)** and **Nondeterministic Finite Automata (NFA)**, allowing users to define machine logic mathematically via 5-tuple text definitions and execute lexical analysis with full computational tracing.

## Features
* **Zero Dependencies:** Built entirely with standard library Python.
* **Dynamic Parsing:** Ingests machine definitions directly from text files—no hardcoded logic.
* **Nondeterminism Support:** Uses Python sets to accurately track and simulate simultaneous computational branches for NFAs.
* **Verbose Tracing:** Includes a step-by-step terminal visualizer to track state transitions in real-time.

## Installation
Clone the repository. No external libraries or virtual environments are required.
```bash
git clone [https://github.com/harshidddh/automata-engine.git](https://github.com/yourusername/automata-engine.git)
cd automata-engine