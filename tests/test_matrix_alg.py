import pytest
from pyformlang.cfg import Production, Variable, Terminal, CFG, Epsilon
from project.cfpq import *
from networkx import MultiDiGraph


def gen_res(grammar: CFG, graph: MultiDiGraph, starts=None, finals=None, start=None):
    return cfpq(
        grammar, graph, algorithm="matrix", starts=starts, finals=finals, start=start
    )


def test_matrix_alg_1():
    productions = """
        S -> a"""

    grammar = CFG.from_text(productions, "S")

    graph = MultiDiGraph()
    graph.add_nodes_from([0, 1, 2])
    graph.add_edge(0, 1, label="a")

    result = gen_res(grammar, graph)
    expected = {(0, 1)}

    assert result == expected


def test_matrix_alg_2():
    productions = """
        S -> epsilon"""

    grammar = CFG.from_text(productions, "S")

    graph = MultiDiGraph()
    graph.add_nodes_from([0, 1, 2])

    result = gen_res(grammar, graph)
    expected = {(0, 0), (1, 1), (2, 2)}

    assert result == expected


def test_matrix_alg_3():
    productions = """
        S -> a S b | epsilon"""

    grammar = CFG.from_text(productions, "S")

    graph = MultiDiGraph()
    graph.add_nodes_from([0, 1, 2, 3])
    graph.add_edge(0, 1, label="a")
    graph.add_edge(1, 0, label="a")
    graph.add_edge(0, 2, label="b")
    graph.add_edge(2, 3, label="b")
    graph.add_edge(3, 0, label="b")

    result = gen_res(grammar, graph, [0], [0, 1, 2, 3])
    expected = {(0, 0), (0, 2), (0, 3)}

    assert result == expected


def test_matrix_alg_4():
    productions = """
        S -> a S b | epsilon"""

    grammar = CFG.from_text(productions, "S")

    graph = MultiDiGraph()
    graph.add_nodes_from([0, 1, 2, 3])
    graph.add_edge(0, 1, label="a")
    graph.add_edge(1, 0, label="a")
    graph.add_edge(0, 2, label="b")
    graph.add_edge(2, 3, label="b")
    graph.add_edge(3, 0, label="b")

    result = gen_res(grammar, graph, [1], [0, 1, 2, 3])
    expected = {(1, 0), (1, 1), (1, 2), (1, 3)}

    assert result == expected


def test_matrix_alg_5():
    productions = """
        S -> A B | C D
        A -> a A | epsilon
        B -> b B c | epsilon
        C -> a C b | epsilon
        D -> c D | epsilon"""

    grammar = CFG.from_text(productions, "S")

    graph = MultiDiGraph()
    graph.add_nodes_from([0, 1, 2, 3, 4])
    graph.add_edge(0, 1, label="a")
    graph.add_edge(1, 2, label="a")

    graph.add_edge(1, 2, label="b")
    graph.add_edge(2, 3, label="b")

    graph.add_edge(3, 4, label="c")
    graph.add_edge(4, 3, label="c")

    result = gen_res(grammar, graph, [0], [0, 1, 2, 3, 4])
    expected = {(0, 0), (0, 1), (0, 2), (0, 3), (0, 4)}

    assert result == expected


def test_matrix_alg_6():
    productions = """
        S -> A B | C D
        A -> a A | epsilon
        B -> b B c | epsilon
        C -> a C b | epsilon
        D -> c D | epsilon"""

    grammar = CFG.from_text(productions, "S")

    graph = MultiDiGraph()
    graph.add_nodes_from([0, 1, 2, 3, 4])
    graph.add_edge(0, 1, label="a")
    graph.add_edge(1, 2, label="a")

    graph.add_edge(1, 2, label="b")
    graph.add_edge(2, 3, label="b")

    graph.add_edge(3, 4, label="c")
    graph.add_edge(4, 3, label="c")

    result = gen_res(grammar, graph, [1, 2, 3, 4], [0, 1, 2, 3, 4])
    expected = {
        (4, 4),
        (2, 4),
        (1, 2),
        (3, 4),
        (4, 3),
        (1, 1),
        (1, 4),
        (3, 3),
        (2, 2),
        (1, 3),
    }

    assert result == expected


def test_matrix_alg_7():
    productions = """
            S -> A B
            S -> A S1
            S1 -> S B
            A -> a
            B -> b"""

    grammar = CFG.from_text(productions, "S")

    graph = MultiDiGraph()
    graph.add_nodes_from([0, 1, 2, 3])
    graph.add_edge(0, 1, label="a")
    graph.add_edge(1, 2, label="a")
    graph.add_edge(2, 0, label="a")

    graph.add_edge(3, 2, label="b")
    graph.add_edge(2, 3, label="b")

    result = gen_res(grammar, graph)
    expected = {(0, 2), (0, 3), (1, 2), (1, 3), (2, 2), (2, 3)}

    assert result == expected


def test_matrix_alg_8():
    productions = """
            X -> epsilon"""

    grammar = CFG.from_text(productions, "X")

    graph = MultiDiGraph()
    graph.add_nodes_from([0, 1, 2])

    result = gen_res(grammar, graph)
    expected = {(0, 0), (1, 1), (2, 2)}

    assert result == expected
