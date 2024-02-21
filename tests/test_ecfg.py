import pytest

from project.automata_builder import get_nfa_from_graph, get_nfa_from_nfa_graph
from project.ecfg import *
from pyformlang.cfg import Production, Variable, Terminal, CFG, Epsilon
from pyformlang.finite_automaton import (
    EpsilonNFA,
    State,
    Symbol,
    Epsilon,
    DeterministicFiniteAutomaton,
)


def test_ecfg_cfg_vs_text_1():

    cfg_str = """
    S -> A B | C D
    """

    cfg = CFG.from_text(cfg_str)

    ecfg1 = ECFG.from_cfg(cfg)
    ecfg2 = ECFG.from_text(cfg_str)
    automaton1 = RecursiveAutomaton.from_ecfg(ecfg1)
    automaton2 = RecursiveAutomaton.from_ecfg(ecfg2)

    assert automaton1.automata == automaton2.automata


def test_ecfg_cfg_vs_text_2():

    cfg_str = """
        S -> A B | C D
        A -> a A | epsilon
        B -> b B c | epsilon
        C -> a C b | epsilon
        D -> c D | epsilon"""

    cfg = CFG.from_text(cfg_str)

    ecfg1 = ECFG.from_cfg(cfg)
    ecfg2 = ECFG.from_text(cfg_str)
    automaton1 = RecursiveAutomaton.from_ecfg(ecfg1)
    automaton2 = RecursiveAutomaton.from_ecfg(ecfg2)

    assert automaton1.automata == automaton2.automata


def test_ecfg_cfg_vs_text_3():

    cfg_str = """
        S -> A B | A S1
        S1 -> S B
        A -> a
        B -> b"""

    cfg = CFG.from_text(cfg_str)

    ecfg1 = ECFG.from_cfg(cfg)
    ecfg2 = ECFG.from_text(cfg_str)
    automaton1 = RecursiveAutomaton.from_ecfg(ecfg1)
    automaton2 = RecursiveAutomaton.from_ecfg(ecfg2)

    assert automaton1.automata == automaton2.automata


def test_ecfg_cfg_vs_text_4():

    cfg_str = """
        S -> a S b | epsilon"""

    cfg = CFG.from_text(cfg_str)

    ecfg1 = ECFG.from_cfg(cfg)
    ecfg2 = ECFG.from_text(cfg_str)
    automaton1 = RecursiveAutomaton.from_ecfg(ecfg1)
    automaton2 = RecursiveAutomaton.from_ecfg(ecfg2)

    assert automaton1.automata == automaton2.automata


def test_ecfg_regex_1():

    cfg_str = """
    S -> A B | C D
    """

    ecfg = ECFG.from_text(cfg_str)
    automaton = RecursiveAutomaton.from_ecfg(ecfg)

    dfa = DeterministicFiniteAutomaton()
    dfa.add_transitions([(0, "A", 1), (1, "B", 2)])
    dfa.add_transitions([(0, "C", 3), (3, "D", 4)])
    dfa.add_start_state(0)
    dfa.add_final_state(2)
    dfa.add_final_state(4)

    assert automaton.automata["S"].is_equivalent_to(dfa)


def test_ecfg_regex_2():

    cfg_str = """
    S -> abc|d*
    """

    ecfg = ECFG.from_text(cfg_str)
    automaton = RecursiveAutomaton.from_ecfg(ecfg)

    dfa = DeterministicFiniteAutomaton()
    dfa.add_transitions([(0, "abc", 1), (0, "d", 2), (2, "d", 2)])

    dfa.add_start_state(0)

    dfa.add_final_state(0)
    dfa.add_final_state(1)
    dfa.add_final_state(2)

    assert automaton.automata["S"].is_equivalent_to(dfa)


def test_minimize_1():
    cfg_str = """
        S -> abc|d*
        """

    ecfg = ECFG.from_text(cfg_str)
    automaton = RecursiveAutomaton.from_ecfg(ecfg)
    automaton.minimize()

    dfa = DeterministicFiniteAutomaton()
    dfa.add_transitions([(0, "abc", 1), (0, "d", 2), (2, "d", 2)])

    dfa.add_start_state(0)

    dfa.add_final_state(0)
    dfa.add_final_state(1)
    dfa.add_final_state(2)

    assert automaton.automata["S"].is_equivalent_to(dfa)


def test_minimize_2():
    cfg_str = """
        S -> abc|d*
        """

    ecfg = ECFG.from_text(cfg_str)
    automaton = RecursiveAutomaton.from_ecfg(ecfg)

    non_minimized_dfa = DeterministicFiniteAutomaton()
    non_minimized_dfa.add_transitions(
        [(0, "a", 1), (1, "a", 0), (0, "b", 2), (1, "b", 3)]
    )
    non_minimized_dfa.add_transitions(
        [(2, "a", 4), (3, "b", 5), (3, "a", 4), (2, "b", 5)]
    )
    non_minimized_dfa.add_transitions(
        [(4, "b", 5), (4, "a", 4), (5, "a", 5), (5, "b", 5)]
    )

    non_minimized_dfa.add_start_state(0)

    non_minimized_dfa.add_final_state(2)
    non_minimized_dfa.add_final_state(3)
    non_minimized_dfa.add_final_state(4)

    automaton.automata["A"] = non_minimized_dfa

    minimized_dfa = DeterministicFiniteAutomaton()

    minimized_dfa.add_transitions(
        [(0, "a", 0), (0, "b", 1), (1, "a", 1), (1, "b", 2), (2, "a", 2), (2, "b", 2)]
    )

    minimized_dfa.add_start_state(0)

    minimized_dfa.add_final_state(1)

    automaton.minimize()

    assert automaton.automata["A"].is_equivalent_to(minimized_dfa)
