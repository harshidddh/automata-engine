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


class DFA(Automaton):
    """Deterministic Finite Automaton: Enforces strict 1:1 state transitions."""

    def accepts(self, input_string: str, verbose: bool = False) -> bool:
        current_state = self.start_state

        for symbol in input_string:
            if symbol not in self.alphabet:
                raise ValueError(f"Symbol '{symbol}' not in alphabet.")

            if verbose:
                print(f"  [DFA] Input: {symbol} | Current: {current_state}", end="")

            state_transition = (current_state, symbol)
            if state_transition in self.delta:
                # DFA has exactly one target state per transition
                current_state = list(self.delta[state_transition])[0]
            else:
                if verbose: print(" -> [REJECTED: Missing Transition]")
                return False

            if verbose: print(f" -> Next: {current_state}")

        is_accepted = current_state in self.accept_states
        if verbose:
            print(f"  [DFA] Final State: {current_state} | Accepted: {is_accepted}\n")
        return is_accepted


class NFA(Automaton):
    """Nondeterministic Finite Automaton: Evaluates multiple active branches simultaneously."""

    def accepts(self, input_string: str, verbose: bool = False) -> bool:
        current_states = {self.start_state}

        for symbol in input_string:
            if symbol not in self.alphabet:
                raise ValueError(f"Symbol '{symbol}' not in alphabet.")

            if verbose:
                print(f"  [NFA] Input: {symbol} | Active States: {current_states}", end="")

            next_states = set()
            for state in current_states:
                state_transition = (state, symbol)
                if state_transition in self.delta:
                    for target in self.delta[state_transition]:
                        if target != "-":
                            next_states.add(target)

            current_states = next_states

            if verbose: print(f" -> Next Active: {current_states}")

            if not current_states:
                break  # All branches died

        is_accepted = any(state in self.accept_states for state in current_states)
        if verbose:
            print(f"  [NFA] Final Active States: {current_states} | Accepted: {is_accepted}\n")
        return is_accepted
