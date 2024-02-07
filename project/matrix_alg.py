import numpy as np
from networkx import MultiDiGraph
from pyformlang.cfg import Production, Variable, Terminal, CFG, Epsilon
from scipy.sparse import csr_array

from project.task_3 import matrix_from_fa_graph
from project.task_6 import cfg_to_wcnf
from project.bool_decomposition import BooleanDecomposition


class MatrixAlgBoolDec(BooleanDecomposition):

    """boolean decomposition of a matrix with built-in multiplication as defined in the matrix algorithm"""

    def __init__(self, size, variables, productions):
        super().__init__(size, variables)

        self.productions = []
        for production in productions:
            if len(production.body) == 2:
                self.productions.append(production)

    def __mul__(self, other):
        answer = MatrixAlgBoolDec(self.size, self.variables, self.productions)

        # for i in range(self.size):
        #     for j in range(self.size):
        #         for k in range(self.size):
        #             for production in self.productions:
        #                 head = production.head.value
        #                 v1 = production.body[0].value
        #                 v2 = production.body[1].value
        #                 if self.matrix[v1][i, k] and other.matrix[v2][k, j]:
        #                     answer.set(head, i, j)

        for (i, k) in self.elements:
            for (k2, j) in other.elements:
                if k == k2:
                    for production in self.productions:
                        head = production.head.value
                        v1 = production.body[0].value
                        v2 = production.body[1].value
                        if self.matrix[v1][i, k] and other.matrix[v2][k, j]:
                            answer.set(head, i, j)
        return answer

    def __add__(self, other):
        answer = MatrixAlgBoolDec(self.size, self.variables, self.productions)
        answer.elements = self.elements | other.elements

        for variable in self.variables:
            answer.matrix[variable] = self.matrix[variable] + other.matrix[variable]

        return answer

    def __eq__(self, other):
        for variable in self.variables:
            if not np.array_equal(
                self.matrix[variable].todense(), other.matrix[variable].todense()
            ):
                return False
        return True


def matrix_alg(grammar: CFG, graph: MultiDiGraph):

    """matrix algorithm for finding state-variable-state triplets based on a graph and a CFG"""

    original_variables = set([i.value for i in grammar.variables])
    grammar = cfg_to_wcnf(grammar)

    edges = list(graph.edges(data="label", default="ɛ"))
    nodes = list(graph.nodes())
    matrix = MatrixAlgBoolDec(len(nodes), grammar.variables, grammar.productions)
    id_from_node = dict()
    for i in range(len(nodes)):
        id_from_node[nodes[i]] = i

    variable_from_symbol = dict()
    for symbol in grammar.terminals:
        variable_from_symbol[symbol.value] = set()
    variable_from_symbol["ɛ"] = set()

    for production in grammar.productions:
        if len(production.body) == 0:
            variable_from_symbol["ɛ"].add(production.head.value)
        elif len(production.body) == 1:
            variable_from_symbol[production.body[0].value].add(production.head.value)

    for state in range(len(nodes)):
        for var in variable_from_symbol["ɛ"]:
            matrix.set(var, state, state)

    for edge in edges:
        state_from = id_from_node[edge[0]]
        state_to = id_from_node[edge[1]]
        symbol = edge[2]
        for var in variable_from_symbol[symbol]:
            matrix.set(var, state_from, state_to)

    old_matrix = MatrixAlgBoolDec(len(nodes), grammar.variables, grammar.productions)

    while not old_matrix == matrix:
        old_matrix = matrix
        matrix = old_matrix + old_matrix * old_matrix

    answer = set()

    for variable in original_variables:
        for (i, j) in matrix.elements:
            if matrix.matrix[variable][i, j]:
                answer.add((nodes[i], variable, nodes[j]))

    return answer
