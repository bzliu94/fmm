# 2019-11-13

# had a problem with B12 in M3

# also, had a problem with name collision for C in doStrassenMultiply and doBruteForceMultiply

# also, we hard-coded in A and B for doBruteForceMultiply

# 2019-11-12

# we handle boolean matrix multiplication

# brute-force time is in O(n ^ 3)

# using pypy, for n = 1024 we have time of 13.571 seconds

# strassen time is in O(n ^ 2.8)

# using pypy, for n = 1024 we have time of 6.242 seconds

import random
import string

class Matrix:
  def __init__(self, n):
    self.n = n
    rows = []
    for i in xrange(n):
      row = []
      for j in xrange(n):
        row.append(0)
      rows.append(row)
    self.rows = rows
  def getElement(self, i, j):
    return self.rows[i][j]
  def setElement(self, i, j, value):
    self.rows[i][j] = value
  def doBruteForceMultiply(self, m_B):
    n = self.getSize()
    curr_C = Matrix(n)
    for i in xrange(n):
      for j in xrange(n):
        value = 0
        for k in xrange(n):
          value += self.getElement(i, k) * m_B.getElement(k, j)
        # next_value = 1 if value >= 1 else 0
        curr_C.setElement(i, j, value)
    return curr_C
  # we assume n is a power of two
  def doStrassenMultiply(self, m_B):
    n1 = self.getSize()
    n2 = m_B.getSize()
    if n1 != n2:
      raise Exception()
    n = n1
    # print n
    if n <= 256:
      # print self.toString(), m_B.toString()
      m = self.doBruteForceMultiply(m_B)
      return m
    A11 = self.readQuadrant(0, 0)
    # print "A11:", A11.toString()
    A12 = self.readQuadrant(0, 1)
    # print "A12:", A12.toString()
    A21 = self.readQuadrant(1, 0)
    # print "A21:", A21.toString()
    A22 = self.readQuadrant(1, 1)
    # print "A22:", A22.toString()
    B11 = m_B.readQuadrant(0, 0)
    # print "B11:", B11.toString()
    B12 = m_B.readQuadrant(0, 1)
    # print "B12:", B12.toString()
    B21 = m_B.readQuadrant(1, 0)
    # print "B21:", B21.toString()
    B22 = m_B.readQuadrant(1, 1)
    # print "B22:", B22.toString()
    M1 = (A11.doAdd(A22)).doStrassenMultiply(B11.doAdd(B22))
    # print "for M1:", A11.toString(), A22.toString(), B11.toString(), B22.toString()
    # print "M1:", M1.toString()
    # print A11.doAdd(A22).toString()
    # print B11.doAdd(B22).toString()
    # print ((A11.doAdd(A22)).doBruteForceMultiply(B11.doAdd(B22))).toString()
    # raise Exception()
    M2 = (A21.doAdd(A22)).doStrassenMultiply(B11)
    M3 = A11.doStrassenMultiply(B12.doSubtract(B22))
    M4 = A22.doStrassenMultiply(B21.doSubtract(B11))
    M5 = (A11.doAdd(A12)).doStrassenMultiply(B22)
    M6 = (A21.doSubtract(A11)).doStrassenMultiply(B11.doAdd(B12))
    M7 = (A12.doSubtract(A22)).doStrassenMultiply(B21.doAdd(B22))
    # print "for C11:", M1.toString(), M4.toString(), M5.toString(), M7.toString()
    # raise Exception()
    C11 = ((M1.doAdd(M4)).doSubtract(M5)).doAdd(M7)
    C12 = M3.doAdd(M5)
    C21 = M2.doAdd(M4)
    C22 = ((M1.doSubtract(M2)).doAdd(M3)).doAdd(M6)
    """
    C11 = (A11.doStrassenMultiply(B11)).doAdd(A12.doStrassenMultiply(B21))
    C12 = (A11.doStrassenMultiply(B12)).doAdd(A12.doStrassenMultiply(B22))
    C21 = (A21.doStrassenMultiply(B11)).doAdd(A22.doStrassenMultiply(B21))
    C22 = (A21.doStrassenMultiply(B12)).doAdd(A22.doStrassenMultiply(B22))
    """
    # print "C11:", C11.toString()
    # print "C12:", C12.toString()
    # print "C21:", C21.toString()
    # print "C22:", C22.toString()
    curr_C = Matrix(n)
    curr_C.writeQuadrant(C11, 0, 0)
    curr_C.writeQuadrant(C12, 0, 1)
    curr_C.writeQuadrant(C21, 1, 0)
    curr_C.writeQuadrant(C22, 1, 1)
    return curr_C
  def doAdd(self, m_B):
    n = self.getSize()
    m = Matrix(n)
    for i in xrange(n):
      for j in xrange(n):
        value1 = self.getElement(i, j)
        value2 = m_B.getElement(i, j)
        next_value = value1 + value2
        m.setElement(i, j, next_value)
    return m
  def doNegate(self):
    n = self.getSize()
    m = Matrix(n)
    for i in xrange(n):
      for j in xrange(n):
        value = self.getElement(i, j)
        next_value = -1 * value
        m.setElement(i, j, next_value)
    return m
  def doSubtract(self, m_B):
    return self.doAdd(m_B.doNegate())
  def doBooleanize(self):
    n = self.getSize()
    for i in xrange(n):
      for j in xrange(n):
        value = self.getElement(i, j)
        next_value = 1 if value != 0 else 0
        self.setElement(i, j, next_value)
  def toString(self):
    rows = self.rows
    str_list = []
    for row in rows:
      curr_str = string.join([str(x) for x in row], " ")
      str_list.append(curr_str)
    result_str = string.join([x for x in str_list], "\n")
    return result_str
  def getSize(self):
    return self.n
  # if matrices are identical, return True; otherwise, return False
  def compareWith(self, m_B):
    n1 = self.getSize()
    n2 = m_B.getSize()
    if n1 != n2:
      return False
    n = n1
    for i in xrange(n):
      for j in xrange(n):
        value1 = self.getElement(i, j)
        value2 = m_B.getElement(i, j)
        if value1 != value2:
          print (i, j), value1, value2
          return False
    return True
  # i, j are in {0, 1}
  def readQuadrant(self, i, j):
    n = self.getSize()
    next_n = n / 2
    if n % 2 != 0:
      raise Exception()
    m = Matrix(next_n)
    base_i = None
    base_j = None
    if i == 0:
      base_i = 0
    elif i == 1:
      base_i = next_n
    if j == 0:
      base_j = 0
    elif j == 1:
      base_j = next_n
    for i1 in xrange(next_n):
      for j1 in xrange(next_n):
        value = self.getElement(i1 + base_i, j1 + base_j)
        m.setElement(i1, j1, value)
    return m
  # i, j are in {0, 1}
  # we assume current matrix is larger
  def writeQuadrant(self, M_source, i, j):
    n = self.getSize()
    next_n = M_source.getSize()
    if n != next_n * 2:
      raise Exception()
    base_i = None
    base_j = None
    if i == 0:
      base_i = 0
    elif i == 1:
      base_i = next_n
    if j == 0:
      base_j = 0
    elif j == 1:
      base_j = next_n
    for i1 in xrange(next_n):
      for j1 in xrange(next_n):
        value = M_source.getElement(i1, j1)
        self.setElement(i1 + base_i, j1 + base_j, value)
  def clone(self):
    n = self.getSize()
    m = Matrix(n)
    for i in xrange(n):
      for j in xrange(n):
        value = self.getElement(i, j)
        m.setElement(i, j, value)
    return m

n = 1024
# n = 16
A = Matrix(n)
B = Matrix(n)

for i in xrange(n):
  for j in xrange(n):
    # value = random.randint(0, 1)
    value = random.choice([0] * 2 + [1])
    A.setElement(i, j, value)

"""
A = Matrix(2)
A.setElement(0, 0, 1)
A.setElement(0, 1, 0)
A.setElement(1, 0, 1)
A.setElement(1, 1, 1)
"""

for i in xrange(n):
  row = []
  for j in xrange(n):
    # value = random.randint(0, 1)
    value = random.choice([0] * 2 + [1])
    B.setElement(i, j, value)

"""
B = Matrix(2)
B.setElement(0, 0, 1)
B.setElement(0, 1, 0)
B.setElement(1, 0, 0)
B.setElement(1, 1, 0)
"""

"""
C = A.doBruteForceMultiply(B)
C.doBooleanize()
"""

"""
print "A:"
print A.toString()
print
"""

"""
print "B:"
print B.toString()
print
"""

"""
print "C:"
print C.toString()
print
"""

"""
print "D:"
print B.readQuadrant(1, 0).toString()
print
"""
"""
print "E:"
E = Matrix(n)
E.writeQuadrant(B.readQuadrant(1, 0), 1, 0)
print E.toString()
print
"""

"""
print "A + B:"
print A.doAdd(B).toString()
print
"""

"""
A_clone = A.clone()
print A.compareWith(A_clone)
print
"""

"""
print "A + B (booleanized):"
result = A.doAdd(B)
result.doBooleanize()
print result.toString()
print
"""

print "F = A * B (strassen):"
F = A.doStrassenMultiply(B)
# F.doBooleanize()
print F.toString()
print

"""
G = F.clone()
G.doBooleanize()
print G.compareWith(C)
print
"""


