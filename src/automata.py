import os
from typing import Dict, Set, Tuple, List

from bleach.utils import alphabetize_attributes
from docutils.nodes import description


class Automaton:
    """Base mathematical model for Finite State Machines: (Q, Σ, δ, q0, F)."""
    def __init__(self, description: str, alphabet: set, start_state: str, accept_states: set, delta:dict):
        self.description = description
        self.alphabet = alphabet
        self.start_state = start_state
        self.accept_states = accept_states
        self.delta = delta

    def parse_machine_file(filepath:str) -> Automaton:
        """Parses a 5-tuple machine definition file."""
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"File {filepath} not found.")

        with open(filepath, "r", encoding='utf-8') as f:
            # Strips inline comments separated by ';'
            lines = [line.split(';')[0].strip() for line in f if line.strip()]

        machine_type = lines[0].lower()
        description = lines[1]
        alphabet = set(lines[2])
        start_state = lines[3]
        accept_states = set(lines[4].split())

        delta = {}
        for line in lines[5:]:
            parts = line.split()
            if len(parts) >= 2:
                state = parts[0]
                targets = parts[1:]
                for i, symbol in enumerate(lines[2]):
                    if i < len(targets):
                        delta[(state, symbol)] = set(targets[i].split(';'))

        if machine_type == 'dfa':
            from .automata import DFA
            return DFA(description, alphabet, start_state, accept_states, delta)
        elif machine_type == 'nfa':
            from .automata import NFA
            return NFA(description, alphabet, start_state, accept_states, delta)
        else:
            raise ValueError(f"Unknown machine type: must be 'dfa' or 'nfa'")

