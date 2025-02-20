from networkx import MultiDiGraph
from pyformlang.regular_expression import Regex
from pyformlang.finite_automaton import DeterministicFiniteAutomaton
import cfpq_data
import pydot
from pyformlang.finite_automaton import EpsilonNFA, State, Symbol, Epsilon

__all__ = ["get_dfa_from_regex", "get_nfa_from_graph"]


def get_dfa_from_regex(regex):
    """takes a regular expression and returns an equivalent deterministic final automaton"""

    dfa = regex.to_epsilon_nfa().minimize()
    return dfa.remove_epsilon_transitions()


def get_nfa_from_graph(graph: MultiDiGraph, start=None, final=None):
    """takes a graph and generates a non-deterministic final automaton based on it.
    lists of start and final states/nodes can be given, otherwise all states
    will be start and final"""

    edges = list(graph.edges(data="label", default="ɛ"))
    nodes = list(graph.nodes())
    nfa = EpsilonNFA()

    states = dict()
    for node in nodes:
        states[node] = State(node)

    if start is None:
        for node in nodes:
            nfa.add_start_state(states[node])
    else:
        for node in start:
            nfa.add_start_state(states[node])

    if final is None:
        for node in nodes:
            nfa.add_final_state(states[node])
    else:
        for node in final:
            nfa.add_final_state(states[node])

    symbols = dict()
    for edge in edges:

        if not edge[2] in symbols:
            if edge[2] == "ɛ":
                symbols[edge[2]] = Epsilon()
            else:
                symbols[edge[2]] = Symbol(edge[2])

        nfa.add_transition(states[edge[0]], symbols[edge[2]], states[edge[1]])

    nfa = nfa.remove_epsilon_transitions()

    return nfa


def get_nfa_from_nfa_graph(graph: MultiDiGraph):
    starts = []
    finals = []
    for state in graph.nodes(data=True):
        if "is_start" in state[1] and state[1]["is_start"]:
            starts.append(state[0])
        if "is_final" in state[1] and state[1]["is_final"]:
            finals.append(state[0])

    return get_nfa_from_graph(graph, starts, finals)
