import pytest
from pyformlang.cfg import Production, Variable, Terminal, CFG, Epsilon
from project.task_6 import *


def test_wcnf_1():
    print()
    productions = """
    S -> a b"""

    grammar = CFG.from_text(productions, "S")
    grammar = cfg_to_wcnf(grammar)

    expected = """
    S -> Va Vb
    Va -> a
    Vb -> b"""

    assert grammar.productions == CFG.from_text(expected, "S").productions


def test_wcnf_2():
    productions = """
    S -> A b A
    A -> a | epsilon"""

    grammar = CFG.from_text(productions, "S")
    grammar = cfg_to_wcnf(grammar)

    expected = """
    S -> A V0
    V0 -> Vb A
    A -> a
    Vb -> b
    A -> epsilon"""

    assert grammar.productions == CFG.from_text(expected, "S").productions


def test_wcnf_3():
    productions = """
    S -> X | a b c d
    X -> a A
    A -> B | C | D
    B -> B
    C -> C c
    D -> a S | epsilon
    E -> e"""

    grammar = CFG.from_text(productions, "S")
    grammar = cfg_to_wcnf(grammar)

    expected = """
    S -> Va A | Va V0
    V0 -> Vb V1
    V1 -> Vc Vd
    A -> Va S
    Va -> a
    Vc -> c
    Vb -> b
    Vd -> d
    A -> epsilon"""

    assert grammar.productions == CFG.from_text(expected, "S").productions


def test_read_from_file():
    expected = """
    S -> Va A | Va V0
    V0 -> Vb V1
    V1 -> Vc Vd
    A -> Va S
    Va -> a
    Vc -> c
    Vb -> b
    Vd -> d
    A -> epsilon"""

    grammar = cfg_from_file("tests/read_cfg_from_file.txt")

    assert grammar.productions == CFG.from_text(expected, "S").productions
