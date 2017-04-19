import math


class Vertex:
    def __init__(self, open, close, seq):
        self.open = open
        self.close = close
        self.seq = seq


class SegmentTree:
    def __init__(self, string):
        """ Class initialization """
        self.string = string
        # initialization code goes here

    def __power(self, x):
        q = int(math.log2(x))
        if not(2 ** q == x):
            q += 1
        return 2 ** q

    def __up(self, vert, i):
        open1 = vert[i * 2].open
        seq1 = vert[i * 2].seq
        seq2 = vert[i * 2 + 1].seq
        close2 = vert[i * 2 + 1].close
        vert[i].seq = seq2 + seq1 + min(open1, close2)
        vert[i].open = open1 - min(open1, close2) + vert[i * 2 + 1].open
        vert[i].close = close2 - min(open1, close2) + vert[i * 2].close

    def build(self, current):
        """ Private function to build the tree """
        n = len(self.string)
        size = self.__power(n)
        self.tree = [Vertex(0, 0, 0) for i in range(2 * size)]
        for i in range(size, size + n):
            if self.string[i - size] == '(':
                self.tree[i].open = 1
            elif self.string[i - size] == ')':
                self.tree[i].close = 1
        for i in range(size - 1, 0, -1):
            self.__up(self.tree, i)

    def __query(self, vert, vertl, vertr, left, right):
        if left > right:
            return
        if left == vertl and right == vertr:
            self.answer += self.tree[vert].seq
            add = min(self.tree[vert].close, self.sum_op)
            self.answer += add
            self.sum_op += self.tree[vert].open
            self.sum_op -= add
            return
        vertm = (vertl + vertr) // 2
        self.__query(vert * 2, vertl, vertm, left, min(right, vertm))
        self.__query(vert * 2 + 1, vertm + 1, vertr,
                     max(vertm + 1, left), right)
        return

    def query(self, left, right):
        """ Public version of query function """
        self.answer = 0
        self.sum_op = 0
        self.__query(1, 1, self.__power(len(self.string)), left, right)
        print(self.answer)
        # return the answer for the given query


def check_query(tree):
    left, right = map(int, input().split())
    if left < 1 or right > len(brackets) or right <= left:
        print('Wrong query. Try again')
        check_query(tree)
    else:
        tree.query(left, right)

if __name__ == "__main__":
    brackets = input('String? ')
    queries = int(input('Queries? '))
    tree = SegmentTree(brackets)
    tree.build(brackets)
    for i in range(queries):
        check_query(tree)
