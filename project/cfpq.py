from networkx import MultiDiGraph
from pyformlang.cfg import Production, Variable, Terminal, CFG, Epsilon
from project.hellings import hellings
from project.matrix_alg import matrix_alg
from project.tensor import tensor
import numpy as np
from scipy.sparse import csr_array

from project.task_3 import matrix_from_fa_graph
from project.task_6 import cfg_to_wcnf
from project.bool_decomposition import BooleanDecomposition


def cfpq(
    grammar: CFG,
    graph: MultiDiGraph,
    algorithm="hellings",
    starts=None,
    finals=None,
    start=None,
):
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

    triplets = set()

    if algorithm == "hellings":
        triplets = hellings(grammar, graph)
    elif algorithm == "matrix":
        triplets = matrix_alg(grammar, graph)
    elif algorithm == "tensor":
        triplets = tensor(grammar, graph)
    else:
        return

    answer = set()
    for triplet in triplets:
        i, V, j = triplet
        if V == start and i in starts and j in finals:
            answer.add((i, j))

    return answer
