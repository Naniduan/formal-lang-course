from networkx import MultiDiGraph
from pyformlang.cfg import Production, Variable, Terminal, CFG, Epsilon
from project.task_3 import FAMatrix, matrix_from_fa_graph
from project.automata_builder import get_nfa_from_graph
from project.task_6 import cfg_to_wcnf


def hellings(grammar: CFG, graph: MultiDiGraph, start="S"):

    """runs Hellings algorithm on a grammar and a graph and
    returns a set of triplets (node1, variable, node2)"""

    original_variables = set([i.value for i in grammar.variables])
    grammar = cfg_to_wcnf(grammar)

    r = []
    variable_from_symbol = dict()
    for symbol in grammar.terminals:
        variable_from_symbol[symbol.value] = set()
    variable_from_symbol["ɛ"] = set()

    for production in grammar.productions:
        if len(production.body) == 0:
            variable_from_symbol["ɛ"].add(production.head.value)
        elif len(production.body) == 1:
            variable_from_symbol[production.body[0].value].add(production.head.value)

    for var in variable_from_symbol["ɛ"]:
        for state in list(graph.nodes(data=False)):
            r.append((var, state, state))

    for edge in list(graph.edges(data="label", default="ɛ")):
        state_from = edge[0]
        state_to = edge[1]
        symbol = edge[2]
        for var in variable_from_symbol[symbol]:
            r.append((var, state_from, state_to))

    m = []
    for i in r:
        m.append(i)

    while m:
        (Ni, v, u) = m.pop(0)

        for (Nj, v_prime, x) in r:
            if x == v:
                for production in grammar.productions:
                    if len(production.body) == 2:
                        V1, V2 = [V.value for V in production.body]
                        if V1 == Nj and V2 == Ni:
                            Nk = production.head.value
                            candidate = (Nk, v_prime, u)

                            candidate_in_r = False
                            for el in r:
                                if el == candidate:
                                    candidate_in_r = True
                                    break

                            if not candidate_in_r:
                                r.append(candidate)
                                m.append(candidate)

        for (Nj, x, v_prime) in r:
            if x == u:
                for production in grammar.productions:
                    if len(production.body) == 2:
                        V1, V2 = [V.value for V in production.body]
                        if V1 == Ni and V2 == Nj:
                            Nk = production.head.value
                            candidate = (Nk, v, v_prime)

                            candidate_in_r = False
                            for el in r:
                                if el == candidate:
                                    candidate_in_r = True
                                    break

                            if not candidate_in_r:
                                r.append(candidate)
                                m.append(candidate)

    answer = set()

    for triplet in r:
        if triplet[0] in original_variables:
            answer.add((triplet[1], triplet[0], triplet[2]))

    return answer


def grammar_in_graph(
    grammar: CFG, graph: MultiDiGraph, starts=None, finals=None, start=None
):

    """returns pairs of states that are connected by a path
    in a graph that is a word in a given grammar"""

    if start is None:
        start = grammar.start_symbol

    if starts is None:
        starts = []
        for node in list(graph.nodes(data=False)):
            starts.append(node)

    if finals is None:
        finals = []
        for node in list(graph.nodes(data=False)):
            finals.append(node)

    triplets = hellings(grammar, graph)

    answer = set()
    for triplet in triplets:
        i, V, j = triplet
        if V == start and i in starts and j in finals:
            answer.add((i, j))

    return answer
