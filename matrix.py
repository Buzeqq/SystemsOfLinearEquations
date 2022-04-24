from copy import deepcopy


class Matrix:
    def __init__(self, n: int = None, value=None, from_list: [[]] = None, size: (int, int) = None):
        if from_list is not None:
            self.from_list(from_list)
            return

        if n is None:
            n = 0

        self.matrix = [[0 if value is None else value for i in range(n if size is None else size[1])]
                       for j in range(n if size is None else size[0])]
        self.size = (n, n) if size is None else size
        self.rows = self.size[0]
        self.cols = self.size[1]

    def from_list(self, matrix_list: [[]]):
        self.matrix = matrix_list
        self.size = (len(matrix_list), len(matrix_list[0]))
        self.rows = self.size[0]
        self.cols = self.size[1]

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

    def _check_index_boundaries(self, row: int, col: int):
        return (0, 0) <= (row, col) < self.size

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
        for i in range(self.rows):
            sum_of_col += self.matrix[i][col]
        return sum_of_col

    def head(self, limit):
        return self.matrix[0:limit]

    def tail(self, limit):
        return self.matrix[-limit:len(self.matrix)]

    def get_max_abs_in_col_below_row(self, col, start_row):
        col_max = float("-inf")
        row_index = 0
        for i in range(start_row, self.rows):
            value = abs(self.get_at(i, col))
            if value > col_max:
                col_max = value
                row_index = i
        return row_index

    def swap_rows(self, fst, scd, p=None, n=None):
        if n is not None:
            self.matrix[fst][:n], self.matrix[scd][:n] = self.matrix[scd][:n], self.matrix[fst][:n]
            return

        self.matrix[fst], self.matrix[scd] = self.matrix[scd], self.matrix[fst]
        if p is not None:
            p.swap_rows(fst, scd)

    def tri_l(self, distance=0):
        res = Matrix(size=(self.rows, self.cols), value=0.0)

        for i in range(self.size[0]):
            for j in range(self.size[1]):
                dst = abs(i - j)
                if i >= j and dst >= distance:
                    res.set_at(i, j, self.matrix[i][j])
        return res

    def tri_u(self, distance=0):
        res = Matrix(size=(self.rows, self.cols), value=0.0)

        for i in range(self.rows):
            for j in range(self.cols):
                dst = abs(i - j)
                if i <= j and dst >= distance:
                    res.set_at(i, j, self.matrix[i][j])
        return res

    def diag(self):
        return Matrix(from_list=[[0 if i != j else self.get_at(i, j) for i in range(self.cols)]
                                 for j in range(self.rows)])

    def set_col(self, col: int, list_of_new_elements: list):
        if len(list_of_new_elements) != self.rows:
            return

        for i in range(self.rows):
            self.set_at(i, col, list_of_new_elements[i])

    def __str__(self):
        return str(self.head(3)) + " ..." + str(self.tail(3))

    def __mul__(self, other):
        if isinstance(other, (int, float)):
            res = deepcopy(self)
            for i in range(res.rows):
                for j in range(res.cols):
                    val = self.get_at(i, j) * other
                    res.set_at(i, j, val)
            return res

        if not isinstance(other, Matrix):
            return None

        if self.cols != other.rows:
            print("Cannot mul matrices with given sizes", self.size, other.size)
            return None

        res = Matrix(size=(self.cols, other.cols))
        for i in range(res.rows):
            for j in range(res.cols):
                value = 0
                for k in range(self.cols):
                    value += self.matrix[i][k] * other.matrix[k][j]

                res.set_at(i, j, value)
        return res

    def __sub__(self, other):
        if isinstance(other, (int, float)):
            res = deepcopy(self)
            for i in range(res.rows):
                for j in range(res.cols):
                    val = self.get_at(i, j) - other
                    res.set_at(i, j, val)
            return res

        if not isinstance(other, Matrix):
            return None

        if self.size != other.size:
            print("Cannot sub matrices with given sizes", self.size, other.size)
            return None

        res = deepcopy(self)
        for i in range(res.rows):
            for j in range(res.cols):
                value = self.get_at(i, j) - other.get_at(i, j)
                res.set_at(i, j, value)
        return res

    def __neg__(self):
        res = deepcopy(self)
        for i in range(res.rows):
            for j in range(res.cols):
                val = -self.get_at(i, j)
                res.set_at(i, j, val)
        return res

    def __add__(self, other):
        if isinstance(other, (int, float)):
            res = deepcopy(self)
            for i in range(res.rows):
                for j in range(res.cols):
                    val = self.get_at(i, j) + other
                    res.set_at(i, j, val)
            return res

        if not isinstance(other, Matrix):
            return None

        if self.size != other.size:
            print("Cannot sub matrices with given sizes", self.size, other.size)
            return None

        res = deepcopy(self)
        for i in range(res.rows):
            for j in range(res.cols):
                value = self.get_at(i, j) + other.get_at(i, j)
                res.set_at(i, j, value)
        return res

    def __eq__(self, other):
        if not isinstance(other, Matrix):
            return False

        for i in range(self.rows):
            for j in range(self.cols):
                if self.get_at(i, j) != other.get_at(i, j):
                    return False
        return True


def ones(n):
    ret = Matrix(n)
    for i in range(ret.rows):
        ret.set_at(i, i, 1.)
    return ret


def is_diagonal(a: Matrix):
    for i in range(a.rows):
        for j in range(a.cols):
            if i != j and a.get_at(i, j) != 0:
                return False
    return True


def diagonal_solver(a: Matrix, b: Matrix):
    if not is_diagonal(a):
        print("Can't use diagonal solver for not diagonal matrices!")
        return None

    if a.rows != b.rows:
        print("Sizes of matrices does not match!")
        return None

    results = Matrix(size=(b.rows, b.cols))
    for c in range(b.cols):
        col = b.get_col(c)

        res = []
        for i in range(a.rows):
            res.append(col[i] / a.get_at(i, i))
        results.set_col(c, res)

    return results


def forward_substitution_solver(a: Matrix, b: Matrix):
    for i in range(a.rows):
        for j in range(i + 1, a.cols):
            if a.get_at(i, j) != 0:
                print("Matrix A is not triangular lower!")
                return None

    if a.cols != b.rows:
        print("Sizes of matrices does not match!")
        return None

    results = Matrix(size=(b.rows, b.cols))
    for c in range(b.cols):
        col = b.get_col(c)

        res = []
        for i in range(a.rows):
            numerator = col[i]
            for j in range(0, i):
                numerator -= a.get_at(i, j) * res[j]
            res.append(numerator/a.get_at(i, i))
        results.set_col(c, res)

    return results
