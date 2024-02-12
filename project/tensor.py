import scipy.sparse as sp
from networkx import MultiDiGraph
from pyformlang.cfg import CFG

from project.bool_decomposition import BooleanDecomposition
from project.task_3 import matrix_from_fa_graph, kronecker, csr_matrices_are_equal


def recursive_graph_from_grammar(grammar: CFG):
    graph = MultiDiGraph()

    n = 0

    n_to_variable = []

    for production in grammar.productions:
        variable = production.head.value
        symbols = [i.value for i in production.body]
        n_to_variable.append(variable)
        if len(symbols) == 0:
            graph.add_node(str(n) + " 0", is_start=True, is_final=True)
            n += 1
        else:
            graph.add_node(str(n) + " " + str(0), is_start=True, is_final=False)
            for i in range(len(symbols) - 1):
                graph.add_node(
                    str(n) + " " + str(i + 1), is_start=False, is_final=False
                )
            graph.add_node(
                str(n) + " " + str(len(symbols)), is_start=False, is_final=True
            )

            for i in range(len(symbols)):
                graph.add_edge(
                    str(n) + " " + str(i), str(n) + " " + str(i + 1), label=symbols[i]
                )

            n += 1

    return graph, n_to_variable


def matrices_are_equal(matrix1, matrix2, n):
    for i in range(n):
        for j in range(n):
            if matrix1[i][j] != matrix2[i][j]:
                return False
    return True


def tensor(grammar: CFG, graph: MultiDiGraph) -> set:
    variables = set([i.value for i in grammar.variables])
    terminals = set([i.value for i in grammar.terminals])

    grammar_graph, get_nonterminals = recursive_graph_from_grammar(grammar)

    grammar_matrix = matrix_from_fa_graph(grammar_graph)
    graph_matrix = matrix_from_fa_graph(graph)

    symbols = variables | terminals | graph_matrix.symbols

    for production in grammar.productions:
        if len(production.body) == 0:
            for i in range(graph_matrix.size):
                graph_matrix.matrix[i][i].add(production.head.value)

    prev_matrix = []
    size = len(graph.nodes)
    for i in range(size):
        prev_matrix.append([set() for _ in range(size)])

    matrix_has_changed = True

    while matrix_has_changed:
        matrix_has_changed = False
        matrix = kronecker(grammar_matrix, graph_matrix, symbols)

        bool_matrix = sp.csr_matrix((matrix.size, matrix.size), dtype=bool)

        for i in range(matrix.size):
            for j in range(matrix.size):
                if matrix.matrix[i][j] == set():
                    bool_matrix[i, j] = False
                else:
                    bool_matrix[i, j] = True
                if i == j:
                    bool_matrix[i, j] = True

        transitive_closure = bool_matrix * bool_matrix + bool_matrix

        while not csr_matrices_are_equal(transitive_closure, bool_matrix, matrix.size):
            bool_matrix = transitive_closure
            transitive_closure = bool_matrix * bool_matrix + bool_matrix

        for i in range(matrix.size):
            for j in range(matrix.size):
                if transitive_closure[i, j]:
                    grammar_i, graph_i = matrix.states[i]
                    grammar_j, graph_j = matrix.states[j]

                    grammar_i_id, graph_i_id = (
                        i // graph_matrix.size,
                        i % graph_matrix.size,
                    )
                    grammar_j_id, graph_j_id = (
                        j // graph_matrix.size,
                        j % graph_matrix.size,
                    )

                    if (
                        grammar_i_id in grammar_matrix.starts
                        and grammar_j_id in grammar_matrix.finals
                    ):
                        n, number = [i for i in grammar_j.split()]
                        variable = get_nonterminals[int(n)]
                        if variable not in graph_matrix.matrix[graph_i_id][graph_j_id]:
                            matrix_has_changed = True
                            graph_matrix.matrix[graph_i_id][graph_j_id].add(variable)

    answer = set()

    for i in range(graph_matrix.size):
        for j in range(graph_matrix.size):
            for variable in graph_matrix.matrix[i][j]:
                state_from = graph_matrix.states[i]
                state_to = graph_matrix.states[j]
                answer.add((state_from, variable, state_to))

    return answer
