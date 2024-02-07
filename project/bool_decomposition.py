from scipy.sparse import csr_array


class BooleanDecomposition:

    """boolean decomposition with built-in addition"""

    def __init__(self, size, variables):
        self.matrix = dict()
        self.size = size
        self.variables = variables
        for symbol in variables:
            self.matrix[symbol] = csr_array((size, size), dtype=bool)

        self.elements = set()

    def set(self, variable, i, j):
        self.elements.add((i, j))
        self.matrix[variable][i, j] = True

    def __add__(self, other):
        answer = BooleanDecomposition(self.size, self.variables)
        answer.elements = self.elements | other.elements

        for variable in self.variables:
            answer.matrix[variable] = self.matrix[variable] + other.matrix[variable]

        return answer
