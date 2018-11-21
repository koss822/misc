import numpy, math
class Sudoku(object):
    def __init__(self, m):
        self.matrix = numpy.matrix(m)
    def is_valid(self):
        self.mysum = sum(x for x in range(1,len(self.matrix)+1))
        self.mylen = int(math.sqrt(len(self.matrix)))
        # iterate over submatrixes
        for x in range(0,self.mylen):
            for y in range(0, self.mylen):
                submatrix = self.matrix[x*self.mylen:x*self.mylen+self.mylen,y*self.mylen:y*self.mylen+self.mylen]
                for i in range(1,self.mylen):
                    if i not in submatrix.A1.tolist():
                        return False
                if numpy.sum(submatrix) != self.mysum:
                    return False
        results = self.numpy_lines(1) + self.numpy_lines(0) # rows + columns parsing
        for result in results:
            if not result:
                return False
        return True
    def line_sudoku(self, line):
        line = line.tolist()[0]
        if sum(line) != self.mysum:
            return False
        for i in range(1, self.mylen):
            if i not in line:
                return False
        return True
    def numpy_lines(self,axis):
        return numpy.apply_along_axis(self.line_sudoku, axis = axis, arr = self.matrix).tolist()
goodSudoku = Sudoku([
  [1,4, 2,3],
  [3,2, 4,1],
  [4,1, 3,2],
  [2,3, 1,4]
])
print(goodSudoku.is_valid())