import pyformlang.finite_automaton
from networkx import MultiDiGraph
from pyformlang.cfg import Production, Variable, Terminal, CFG, Epsilon
from pyformlang.regular_expression import Regex
import re

from project.task_4 import remove_starting


def is_not_empty(line):
    for symbol in line:
        if symbol != "\n" and symbol != " ":
            return True
    return False


def remove_spaces(line):
    return re.sub(" +", " ", line).strip()


class ECFG:
    def __init__(self):
        self.productions = dict()
        self.variables = set()
        self.terminals = set()

    def add_production(self, head, regex: str):
        self.productions[head] = Regex(regex)

    def from_cfg(cfg: CFG):

        ecfg = ECFG()

        for production in cfg.productions:
            head = production.head
            body = production.body
            regex = ""
            for symbol in body:
                if symbol is Terminal:
                    ecfg.terminals.add(symbol.value)
                elif symbol is Variable:
                    ecfg.variables.add(symbol.value)
                regex += str(symbol.value) + " "

            if regex == "":
                regex = "$"

            if head.value not in ecfg.productions.keys():
                ecfg.variables.add(head.value)
                ecfg.productions[head.value] = Regex(regex)
            else:
                ecfg.productions[head.value] = ecfg.productions[head.value].union(
                    Regex(regex)
                )

        return ecfg

    def from_text(text: str):

        ecfg = ECFG()

        text = text.split("\n")
        for line in text:
            if is_not_empty(line):
                line = remove_spaces(line)
                head, arrow, regex = line.split(" ", 2)
                ecfg.productions[head] = Regex(regex)
                ecfg.variables.add(head)
                for symbol in regex.split():
                    if symbol[0].isupper():
                        ecfg.variables.add(symbol)
                    else:
                        ecfg.terminals.add(symbol)

        return ecfg


class RecursiveAutomaton:
    def __init__(self):
        self.automata = dict()

    def from_ecfg(ecfg: ECFG):

        rec_automaton = RecursiveAutomaton()

        for head in ecfg.productions.keys():
            automaton = (
                ecfg.productions[head]
                .to_epsilon_nfa()
                .to_deterministic()
                .remove_epsilon_transitions()
            )
            rec_automaton.automata[head] = automaton

        return rec_automaton

    def minimize(self):

        for head in self.automata.keys():
            self.automata[head] = self.automata[head].minimize()
