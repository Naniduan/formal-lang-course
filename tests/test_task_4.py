import pytest
import networkx as nx
from pyformlang.regular_expression import Regex

from project.automata_builder import get_nfa_from_graph
from project.task_4 import *


def test_reachable_1():
    regex = Regex("a")
    graph = nx.MultiDiGraph()

    graph.add_nodes_from([0, 1])
    graph.add_edge(0, 1, label="a")

    assert find_reachable_states(regex, graph, [0]) == {1}


def test_request_non_sep_1():
    regex = Regex("a")
    graph = nx.MultiDiGraph()

    graph.add_nodes_from([0, 1])
    graph.add_edge(0, 1, label="a")

    assert regex_in_graph(regex, graph, [0], [1], separately=False) == {1}


def test_request_sep_1():
    regex = Regex("a")
    graph = nx.MultiDiGraph()

    graph.add_nodes_from([0, 1])
    graph.add_edge(0, 1, label="a")

    answer = regex_in_graph(regex, graph, [0], [1], separately=True)

    assert [answer[0]] == [{1}]


def test_request_non_sep_2():
    regex = Regex("a|b")
    graph = nx.MultiDiGraph()

    graph.add_nodes_from([0, 1, 2])
    graph.add_edge(0, 1, label="a")
    graph.add_edge(0, 2, label="b")

    answer = regex_in_graph(regex, graph, [0], [1, 2], separately=False)

    assert answer == {1, 2}


def test_request_non_sep_3():
    regex = Regex("a (a a a a a a a)*")
    graph = nx.MultiDiGraph()

    graph.add_nodes_from([0, 1, 2, 3])
    graph.add_edge(0, 1, label="a")
    graph.add_edge(0, 2, label="a")
    graph.add_edge(2, 0, label="a")

    answer = regex_in_graph(regex, graph, [0], [3], separately=False)

    print(answer)

    assert answer == set()


def test_request_sep_2():
    regex = Regex("a*")
    graph = nx.MultiDiGraph()

    graph.add_nodes_from([0, 1, 2])
    graph.add_edge(0, 1, label="a")
    graph.add_edge(1, 2, label="a")

    answer = regex_in_graph(regex, graph, [0, 1, 2], [0, 1, 2], separately=True)

    assert [answer[0], answer[1], answer[2]] == [{0, 1, 2}, {1, 2}, {2}]
