# coding:utf-8
# This file contains both the naive recurrent and the dynamic programming solutions for minimum-edit-distance.

def minimum_distance_naive(string_a, string_b, m, n):
  if m == 0:
    return n
  if n == 0:
    return m

  if string_a[m-1] == string_b[n-1]:
    return minimum_distance_naive(string_a, string_b, m-1, n-1)

  return 1 + min(
    minimum_distance_naive(string_a, string_b, m-1, n),   # delete
    minimum_distance_naive(string_a, string_b, m, n-1),   # insert
    minimum_distance_naive(string_a, string_b, m-1, n-1), # replace
  )

def minimum_distance_dp(string_a, string_b):
  len_a = len(string_a)
  len_b = len(string_b)
  matrix = [[0 for _ in range(len_b + 1)] for _ in range(len_a + 1)]
  matrix_backtr_index = [[(0, 0) for _ in range(len_b + 1)] for _ in range(len_a + 1)]
  matrix_backtr = [['' for _ in range(len_b + 1)] for _ in range(len_a + 1)]

  for i in range(len_a + 1):
    for j in range(len_b + 1):
      if i == 0:
        matrix[i][j] = j
      elif j == 0:
        matrix[i][j] = i
      elif string_a[i-1] == string_b[j-1]:
        matrix_backtr_index[i][j] = (i-1, j-1)
        matrix_backtr[i][j] = 'skip'
        matrix[i][j] = matrix[i-1][j-1]
      else:
        add = matrix[i][j-1]
        delete = matrix[i-1][j]
        replace = matrix[i-1][j-1]

        # add
        if add < delete and add < replace:
          matrix[i][j] = 1 + add
          matrix_backtr_index[i][j] = (i, j-1)
          matrix_backtr[i][j] = 'add'
        elif delete < add and delete < replace:
          matrix[i][j] = 1 + delete
          matrix_backtr_index[i][j] = (i-1, j)
          matrix_backtr[i][j] = 'delete'
        else:
          matrix[i][j] = 1 + replace
          matrix_backtr_index[i][j] = (i-1, j-1)
          matrix_backtr[i][j] = 'replace'
  
  return matrix[-1][-1], matrix_backtr, matrix_backtr_index

def back_trace(matrix_backtr, matrix_backtr_index):
  initial = True
  row, col = -1, -1
  processes = []

  while row > 0 or col > 0 or initial:
    processes.append(matrix_backtr[row][col])
    row, col = matrix_backtr_index[row][col]
    initial = False
  
  return list(reversed(processes))

if __name__ == '__main__':
  str1 = "apple"
  str2 = "aplla"
  print(minimum_distance_naive(str1, str2, len(str1), len(str2)))

  distance, matrix_backtr, matrix_backtr_index = minimum_distance_dp(str1, str2)
  back_trace(matrix_backtr, matrix_backtr_index)
