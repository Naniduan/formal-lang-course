from project.automata_builder import get_nfa_from_graph, get_dfa_from_regex
from project.task_3 import matrix_from_fa_graph, csr_matrices_are_equal, bool_dec
import numpy as np
from scipy.sparse import csr_matrix


def remove_starting(graph):

    """removes the pretty much useless '_starting' states, that have a single epsilon transition
    from them to the actual starting state"""

    for state in list(graph.nodes):
        if "_starting" in str(state):
            graph.remove_node(state)


def find_reachable_states(regex, graph, starts, finals=None):

    """finds states that can be reached in a graph with a given regex and starting states"""

    graph_fa = get_nfa_from_graph(graph, starts, finals)
    graph_graph = graph_fa.to_networkx()
    remove_starting(graph_graph)
    graph_matrix = matrix_from_fa_graph(graph_graph)

    # graph_id_from_state = dict()
    # for i in graph_matrix.states:
    #     graph_id_from_state[graph_matrix.states[i]] = i

    regex_fa = get_dfa_from_regex(regex)
    regex_graph = regex_fa.to_networkx()
    remove_starting(regex_graph)
    regex_matrix = matrix_from_fa_graph(regex_graph)

    # regex_id_from_state = dict()
    # for i in regex_matrix.states:
    #     regex_id_from_state[regex_matrix.states[i]] = i

    front = csr_matrix((regex_matrix.size, graph_matrix.size), dtype=bool)
    visited = csr_matrix((regex_matrix.size, graph_matrix.size), dtype=bool)

    for r_start in regex_matrix.starts:
        for g_start in graph_matrix.starts:
            front[r_start, g_start] = True
            visited[r_start, g_start] = True

    symbols = regex_matrix.symbols | graph_matrix.symbols

    bool_dec_graph = bool_dec(graph_matrix, symbols)
    bool_dec_regex = bool_dec(regex_matrix, symbols)

    while front.count_nonzero() != 0:
        new_front = csr_matrix((regex_matrix.size, graph_matrix.size), dtype=bool)
        for symbol in symbols:
            new_front += (
                bool_dec_regex[symbol].transpose() * front * bool_dec_graph[symbol]
            )
        front = new_front > visited
        visited += front

    answer = set()
    for i in regex_matrix.finals:
        for j in range(graph_matrix.size):
            if visited[i, j]:
                answer.add(graph_matrix.states[j])

    return answer


def find_reachable_states_for_each(regex, graph, starts, finals=None):

    """finds states that can be reached in a graph with a given regex for each starting state separately"""

    answer = dict()
    for state in starts:
        answer[state] = find_reachable_states(regex, graph, [state], finals)

    return answer


def regex_in_graph(regex, graph, starts, finals, separately=False):

    """regex requests for a graph. There are two modes: one returns all final states that can be reached with
    a given regex, the other returns reachable final states for each starting state separately"""

    answer = set()
    if separately:
        answer = find_reachable_states_for_each(regex, graph, starts, finals)
        for state in starts:
            answer[state] &= set(finals)
    else:
        answer = find_reachable_states(regex, graph, starts, finals)
        answer &= set(finals)

    return answer
