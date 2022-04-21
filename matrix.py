from copy import deepcopy


class Matrix:
    def __init__(self, n: int = None, m=None, value=None, from_list: [[]] = None):
        if from_list is not None:
            self.from_list(from_list)
            return

        if n is None:
            self.matrix = None
            self.size = (0, 0)
            return

        self.matrix = [[0 if value is None else value for i in range(n if m is None else m)] for j in range(n)]
        self.size = (n, n) if m is None else (n, m)

    def from_list(self, matrix_list: [[]]):
        self.matrix = matrix_list
        self.size = (len(matrix_list), len(matrix_list[0]))

    def set_at(self, i: int, j: int = 0, value=0.0):
        if not self._check_index_boundaries(i, j):
            print("Invalid i or j, when setting value in matrix.", i, j)
            return

        self.matrix[i][j] = value

    def get_at(self, i: int, j: int = 0):
        if not self._check_index_boundaries(i, j):
            print("Invalid i or j, when setting value in matrix.", i, j)
            return

        return self.matrix[i][j]

    def get_size(self):
        return self.size

    def _check_index_boundaries(self, row: int, col: int):
        return (0, 0) <= (row, col) < self.get_size()

    def get_row(self, row):
        return self.matrix[row]

    def get_col(self, col):
        res = []
        for i in range(self.size[0]):
            res.append(self.matrix[i][col])
        return res

    def get_row_sum(self, row):
        return sum(self.matrix[row])

    def get_col_sum(self, col):
        sum_of_col = 0
        for i in range(self.size[0]):
            sum_of_col += self.matrix[i][col]
        return sum_of_col

    def head(self, limit):
        return self.matrix[0:limit]

    def tail(self, limit):
        return self.matrix[-limit:len(self.matrix)]

    def tri_l(self, distance=0):
        res = Matrix(self.size[0], m=self.size[1], value=0.0)

        for i in range(self.size[0]):
            for j in range(self.size[1]):
                dst = abs(i - j)
                if i >= j and dst >= distance:
                    res.set_at(i, j, self.matrix[i][j])
        return res

    def tri_u(self, distance=0):
        res = Matrix(self.size[0], m=self.size[1], value=0.0)

        for i in range(self.size[0]):
            for j in range(self.size[1]):
                dst = abs(i - j)
                if i <= j and dst >= distance:
                    res.set_at(i, j, self.matrix[i][j])
        return res

    def diag(self):
        return Matrix(from_list=[[0 if i != j else self.get_at(i, j) for i in range(self.size[1])]
                                 for j in range(self.size[0])])

    def set_col(self, col: int, list_of_new_elements: list):
        if len(list_of_new_elements) != self.size[0]:
            return

        for i in range(self.size[0]):
            self.set_at(i, col, list_of_new_elements[i])

    def __str__(self):
        return str(self.head(3)) + " ..." + str(self.tail(3))

    def __mul__(self, other):
        if isinstance(other, (int, float)):
            res = deepcopy(self)
            for i in range(res.get_size()[0]):
                for j in range(res.get_size()[1]):
                    val = self.get_at(i, j) * other
                    res.set_at(i, j, val)
            return res

        if not isinstance(other, Matrix):
            return None

        if self.get_size()[1] != other.get_size()[0]:
            print("Cannot mul matrices with given sizes", self.get_size(), other.get_size())
            return None

        res = Matrix(self.size[0], m=other.get_size()[1])
        for i in range(res.get_size()[0]):
            for j in range(res.get_size()[1]):
                value = 0
                for k in range(self.get_size()[1]):
                    value += self.matrix[i][k] * other.matrix[k][j]

                res.set_at(i, j, value)
        return res

    def __sub__(self, other):
        if isinstance(other, (int, float)):
            res = deepcopy(self)
            for i in range(res.get_size()[0]):
                for j in range(res.get_size()[1]):
                    val = self.get_at(i, j) - other
                    res.set_at(i, j, val)
            return res

        if not isinstance(other, Matrix):
            return None

        if self.get_size() != other.get_size():
            print("Cannot sub matrices with given sizes", self.get_size(), other.get_size())
            return None

        res = deepcopy(self)
        for i in range(res.get_size()[0]):
            for j in range(res.get_size()[1]):
                value = self.get_at(i, j) - other.get_at(i, j)
                res.set_at(i, j, value)
        return res

    def __neg__(self):
        res = deepcopy(self)
        for i in range(res.get_size()[0]):
            for j in range(res.get_size()[1]):
                val = -self.get_at(i, j)
                res.set_at(i, j, val)
        return res

    def __add__(self, other):
        if isinstance(other, (int, float)):
            res = deepcopy(self)
            for i in range(res.get_size()[0]):
                for j in range(res.get_size()[1]):
                    val = self.get_at(i, j) + other
                    res.set_at(i, j, val)
            return res

        if not isinstance(other, Matrix):
            return None

        if self.get_size() != other.get_size():
            print("Cannot sub matrices with given sizes", self.get_size(), other.get_size())
            return None

        res = deepcopy(self)
        for i in range(res.get_size()[0]):
            for j in range(res.get_size()[1]):
                value = self.get_at(i, j) + other.get_at(i, j)
                res.set_at(i, j, value)
        return res


def is_diagonal(a: Matrix):
    for i in range(a.get_size()[0]):
        for j in range(a.get_size()[1]):
            if i != j and a.get_at(i, j) != 0:
                return False
    return True


def diagonal_solver(a: Matrix, b: Matrix):
    if not is_diagonal(a):
        print("Can't use diagonal solver for not diagonal matrices!")
        return None

    if a.get_size()[0] != b.get_size()[0]:
        print("Sizes of matrices does not match!")
        return None

    results = Matrix(n=b.get_size()[0], m=b.get_size()[1])
    for c in range(b.get_size()[1]):
        col = b.get_col(c)

        res = []
        for i in range(a.get_size()[0]):
            res.append(col[i] / a.get_at(i, i))
        results.set_col(c, res)

    return results


def forward_substitution_solver(a: Matrix, b: Matrix):
    # TODO check if A is triangular

    if a.get_size()[0] != b.get_size()[0]:
        print("Sizes of matrices does not match!")
        return None

    results = Matrix(n=b.get_size()[0], m=b.get_size()[1])
    for c in range(b.get_size()[1]):
        col = b.get_col(c)

        res = []
        for i in range(a.get_size()[0]):
            numerator = col[i]
            for j in range(0, i):
                numerator -= a.get_at(i, j) * res[j]
            res.append(numerator/a.get_at(i, i))
        results.set_col(c, res)

    return results
