# bimaru.py: Template para implementação do projeto de Inteligência Artificial 2022/2023.
# Devem alterar as classes e funções neste ficheiro de acordo com as instruções do enunciado.
# Além das funções e classes já definidas, podem acrescentar outras que considerem pertinentes.

# Grupo 13:
# 99105 Marco Cunha
# 103590 Tiago Firmino

import sys
import numpy as np
import copy as cp
from search import (
	Problem,
	Node,
	astar_search,
	breadth_first_tree_search,
	depth_first_tree_search,
	greedy_search,
	recursive_best_first_search,
)


class BimaruState:
	state_id = 0

	def __init__(self, board):
		self.board = board
		self.id = BimaruState.state_id
		BimaruState.state_id += 1

	def __lt__(self, other):
		return self.id < other.id

	# TODO: outros metodos da classe


class Board:
	"""Representação interna de um tabuleiro de Bimaru."""

	def __init__(self, board, row_vals = [], col_vals = [], copyhints = []):
		self.board = board
		self.size = 10
		self.rowvals = row_vals
		self.colvals = col_vals
		self.copyrow = cp.deepcopy(row_vals)
		self.copycol = cp.deepcopy(col_vals)
		self.copyhints = copyhints
		# Index is the boat length
		self.boats_left = [0, 4, 3, 2, 1]

	def get_value(self, row: int, col: int) -> str:
		"""Devolve o valor na respetiva posição do tabuleiro."""
		if self.is_valid_position(row, col):
			return self.board[row][col]

	def set_value(self, row: int, col: int, value: int):
		if self.is_valid_position(row, col):
			self.board[row][col] = value

	def adjacent_vertical_values(self, row: int, col: int) -> (str, str):
		"""Devolve os valores imediatamente acima e abaixo,
		respectivamente."""
		if(row == 0):
			top = None
			bottom = self.get_value(row + 1, col).upper()
		elif(row == self.size - 1):
			bottom = None
			top = self.get_value(row - 1, col).upper()
		else:
			top = self.get_value(row -1 , col).upper()
			bottom = self.get_value(row + 1, col).upper()

		if top == ' ':
			top = None
		if bottom == ' ':
			bottom = None

		return (top, bottom)

	def adjacent_horizontal_values(self, row: int, col: int) -> (str, str):
		"""Devolve os valores imediatamente à esquerda e à direita,
		respectivamente."""
		if(col == 0):
			left = None
			right = self.get_value(row, col + 1).upper()
		elif(col == self.size - 1):
			right = None
			left = self.get_value(row, col - 1).upper()
		else:
			left = self.get_value(row, col - 1).upper()
			right = self.get_value(row, col + 1).upper()

		if left == ' ':
			left = None
		if right == ' ':
			right = None

		return (left, right)



	@staticmethod
	def parse_instance():
		"""Lê o test do standard input (stdin) que é passado como argumento
		e retorna uma instância da classe Board.

		Por exemplo:
			$ python3 bimaru.py < input_T01

			> from sys import stdin
			> line = stdin.readline().split()
		"""
		matrix = np.full((10,10), ' ', dtype=str)
		inp_row = sys.stdin.readline()
		vals_row = [int(x) for x in inp_row.split()[1:]]

		inp_col = sys.stdin.readline()
		vals_col = [int(x) for x in inp_col.split()[1:]]

		num_hints = int(input())
		subs = 0
		copyhints = []
		for i in range(num_hints):
			line = sys.stdin.readline().split()
			copyhints.append(line)
			matrix[int(line[1])][int(line[2])] = str(line[3])

		# adicionar atributos aqui e possivel board.new_attr = uu

		return Board(matrix, vals_row, vals_col, copyhints)

	def print_board(self):
		print(self.board)
		print(" ")
		print(self.rowvals, self.colvals, self.copyhints)

	def fill_the_board(self):
		self.put_line_waters()
		self.put_water_around_boat()
		self.put_possible_parts()
		self.put_water_around_boat()
		self.fill_occupied_rows()
		self.complete_possible_boats()
		#self.complete_boat()
		#self.update()


	def put_line_waters(self):
		i = 0
		while i < self.size:
			if self.rowvals[i] == 0:
				row = self.board[i]
				j = 0
				while j < self.size:
					self.set_value(i, j, "w")
					j += 1
			i += 1
		i = 0
		while i < self.size:
			if self.colvals[i] == 0:
				col = self.board[:, i]
				j = 0
				while j < self.size:
					self.set_value(j, i, "w")
					j += 1
			i += 1
		
		i = 0
		while i < self.size:
			if self.rowvals[i] == 1:
				row = self.board[i]
				if np.count_nonzero(row == " ") + np.count_nonzero(row == "W") + np.count_nonzero(row == "w") != self.size:
					j = 0
					while j < self.size:
						if row[j] == " ":
							self.set_value(i, j, "w")
						j += 1
			i += 1
		i = 0
		while i < self.size:
			if self.colvals[i] == 1:
				col = self.board[:, i]
				if np.count_nonzero(col == " ") + np.count_nonzero(col == "W") + np.count_nonzero(col == "w") != self.size:
					j = 0
					while j < self.size:
						if col[j] == " ":
							self.set_value(j, i, "w")
						j += 1
			i += 1

	def is_valid_position(self, row, col):
		return 0 <= row <= 9 and 0 <= col <= 9

	def put_water_around_boat(self):
		t_pos_list = np.nonzero((self.board == "T") | (self.board == "t"))
		i = 0
		while i < len(t_pos_list[0]):
			row = t_pos_list[0][i]
			col = t_pos_list[1][i]
			self.set_value(row + 1, col - 1, "w")
			self.set_value(row, col - 1, "w")
			self.set_value(row - 1, col - 1, "w")
			self.set_value(row - 1, col, "w")
			self.set_value(row - 1, col + 1, "w")
			self.set_value(row, col + 1, "w")
			self.set_value(row + 1, col + 1, "w")
			i += 1

		t_pos_list = np.nonzero((self.board == "B") | (self.board == "b"))
		i = 0
		while i < len(t_pos_list[0]):
			row = t_pos_list[0][i]
			col = t_pos_list[1][i]
			self.set_value(row + 1, col - 1, "w")
			self.set_value(row, col - 1, "w")
			self.set_value(row - 1, col - 1, "w")
			self.set_value(row - 1, col + 1, "w")
			self.set_value(row, col + 1, "w")
			self.set_value(row + 1, col + 1, "w")
			self.set_value(row + 1, col, "w")
			i += 1

		t_pos_list = np.nonzero((self.board == "L") | (self.board == "l"))
		i = 0
		while i < len(t_pos_list[0]):
			row = t_pos_list[0][i]
			col = t_pos_list[1][i]
			self.set_value(row + 1, col - 1, "w")
			self.set_value(row, col - 1, "w")
			self.set_value(row - 1, col - 1, "w")
			self.set_value(row - 1, col, "w")
			self.set_value(row - 1, col + 1, "w")
			self.set_value(row + 1, col + 1, "w")
			self.set_value(row + 1, col, "w")
			i += 1

		t_pos_list = np.nonzero((self.board == "R") | (self.board == "r"))
		i = 0
		while i < len(t_pos_list[0]):
			row = t_pos_list[0][i]
			col = t_pos_list[1][i]
			self.set_value(row + 1, col - 1, "w")
			self.set_value(row - 1, col - 1, "w")
			self.set_value(row - 1, col, "w")
			self.set_value(row - 1, col + 1, "w")
			self.set_value(row, col + 1, "w")
			self.set_value(row + 1, col + 1, "w")
			self.set_value(row + 1, col, "w")
			i += 1
		
		t_pos_list = np.nonzero((self.board == "M") | (self.board == "m") | (self.board == "X"))
		i = 0
		while i < len(t_pos_list[0]):
			row = t_pos_list[0][i]
			col = t_pos_list[1][i]
			self.set_value(row + 1, col - 1, "w")
			self.set_value(row - 1, col - 1, "w")
			self.set_value(row - 1, col + 1, "w")
			self.set_value(row + 1, col + 1, "w")
			i += 1

		t_pos_list = np.nonzero((self.board == "C") | (self.board == "c"))
		i = 0
		while i < len(t_pos_list[0]):
				
			row = t_pos_list[0][i]
			col = t_pos_list[1][i]
			
			self.set_value(row + 1, col - 1, "w")
			self.set_value(row, col - 1, "w")
			self.set_value(row - 1, col - 1, "w")
			self.set_value(row - 1, col, "w")
			self.set_value(row - 1, col + 1, "w")
			self.set_value(row, col + 1, "w")
			self.set_value(row + 1, col + 1, "w")
			self.set_value(row + 1, col, "w")
			i += 1

	def put_possible_parts(self):
		i = 0
		while i < self.size:
			j = 0
			while j < self.size:
				if self.board[i][j] == 'C':
					self.set_value(i, j, 'X')
				if self.board[i][j] == 'T':
					if i == self.size - 2:
						self.set_value(i + 1, j, 'X')
					else:
						self.set_value(i + 1, j, 'X')
					self.set_value(i, j, 'X')
				elif self.board[i][j] == 'M':
					hor_vals = self.adjacent_horizontal_values(i, j)
					ver_vals = self.adjacent_vertical_values(i, j)
					if ver_vals == (None, None) or ver_vals == ('w', 'w') or ver_vals == ('W', 'w') or ver_vals == ('W', 'W'):
						if i == 1:
							self.set_value(i - 1, j, 'X')
						elif self.get_value(i - 1, j) != 'w':
							self.set_value(i - 1, j, 'X')
						if i == self.size - 2:
							self.set_value(i + 1, j, 'X')
						elif self.get_value(i + 1, j) != 'w':
							self.set_value(i + 1, j, 'X')
			
					if hor_vals == (None, None) or hor_vals == ('w', 'w') or hor_vals == ('W', 'w') or hor_vals == ('W', 'W'):
						if j == 1:
							self.set_value(i, j - 1, 'X')
						elif self.get_value(i, j - 1) != 'w':
							self.set_value(i, j - 1, 'X')
						if j == self.size - 2:
							self.set_value(i, j + 1, 'X')
						elif self.get_value(i, j + 1) != 'w':
							self.set_value(i, j + 1, 'X')
					self.set_value(i, j, 'X')
						
				elif self.board[i][j] == 'B':
					if i == 1:
						self.set_value(i - 1, j, 'X')
					else:
						self.set_value(i - 1, j, 'X')
					self.set_value(i, j, 'X')
				elif self.board[i][j] == 'L':
					if j == self.size - 2:
						self.set_value(i, j + 1, 'X')
					else:
						self.set_value(i, j + 1, 'X')
					self.set_value(i, j, 'X')
				elif self.board[i][j] == 'R':
					if j == 1:
						self.set_value(i, j - 1, 'X')
					self.set_value(i, j - 1, 'X')
					self.set_value(i, j, 'X')
				
				j +=1
			
			i += 1

	def fill_occupied_rows(self):
		i = 0
		parts = ['T', 't', 'M', 'm', 'B', 'b', 'L', 'l', 'R', 'r', 'X']
		while i < self.size:
			j = 0
			while j < self.size:
				num_parts_line = np.count_nonzero(np.char.strip(self.board[i]) == np.array(parts)[:, None])
				if self.rowvals[i] == num_parts_line:
					if self.get_value(i, j) == ' ':
						self.set_value(i, j, 'w')
				num_parts_col = np.count_nonzero(np.char.strip(self.board[:, j]) == np.array(parts)[:, None])
				if self.colvals[j] == num_parts_col:
					if self.get_value(i, j) == ' ':
						self.set_value(i, j, 'w')

				j += 1
			i += 1
	
	def complete_possible_boats(self): #TODO FALTAM CASOS SUPOSTAMENTE -- ESTA FUNCAO NAO TA BOA
		i = 0
		#parts = ['T', 't', 'M', 'm', 'B', 'b', 'L', 'l', 'R', 'r']
		while i < self.size:
			j = 0
			while j < self.size:
				
				if self.rowvals[i] == np.count_nonzero(self.board[i] == 'X') + np.count_nonzero(self.board[i] == ' '):
					if self.get_value(i, j) == ' ':
						self.set_value(i, j, 'X')
						self.fill_occupied_rows()
				
				if self.colvals[j] == np.count_nonzero(self.board[:, j] == 'X') + np.count_nonzero(self.board[:, j] == ' '):
					if self.get_value(i, j) == ' ':
						self.set_value(i, j, 'X')
						self.fill_occupied_rows()
				
				j += 1
			i += 1

		self.put_water_around_boat()

		i = 0
		while i < self.size:
			j = 0
			while j < self.size:
				if self.get_value(i, j) == ' ':
					self.set_value(i, j, '?')
				j += 1
			i += 1

		i = 0
		while i < self.size:
			j = 0
			while j < self.size:
				if self.get_value(i, j) == 'w' or self.get_value(i, j) == 'W':
					self.set_value(i, j, ' ')
				j += 1
			i += 1
			#if self.rowvals[i] == np.count_nonzero(self.board[i] == 'X'):
			#	self.board[i] == np.where(self.board[i] == ' ', 'w', self.board[i])
			#if self.colvals[j] == np.count_nonzero(self.board[:,j] == 'X'):
			#	self.board[:, j] == np.where(self.board[:, j] == ' ', 'w', self.board[:, j])
	
	def update(self):
		for i in range(len(self.copyhints)):
			values = self.copyhints[i][1:4]
			self.set_value(int(values[0]), int(values[1]), values[2])



	'''
	T X	X X	T T	T X	X X X|T X X T T X  X|T X T X|L M M R - L X X X - X M X X|L M R - L M X|L R|
	M M	X X	X M	M X	X M M|M M X X M X  M|B B X X|X M M R - L M X X - X X M X|X M R - X X X|X R|
	M M	M X	X X	M X	M X M|B B B X X X  X|	    |X X M R - L M M X - X M M X|X X R - X M X|L X|
	B B	B B	X X	X X	X X X|		   	    |	    |X X X R - X X X X          |L X X 	      |X X|
	'''


	def complete_boat(self): 
		i = 0
		while i < self.size:
			j = 0
			while j < self.size:
				if self.get_value(i, j) == 'X':
					#one
					if self.adjacent_vertical_values(i, j) == (None, None) and \
					 self.adjacent_horizontal_values(i, j) == (None, None):
						self.set_value(i, j, 'c')
						self.boats_left[1] -= 1
					# VERTICAL T X
					elif self.adjacent_vertical_values(i, j) == ('T', None):
						self.set_value(i, j, 'b')
						self.boats_left[2] -= 1
					# VERTICAL X B
					elif self.adjacent_vertical_values(i, j) == (None, 'B'):
						self.set_value(i, j, 't')
						self.boats_left[2] -= 1
					# HORIZONTAL L X
					elif self.adjacent_horizontal_values(i, j) == ('L', None):
						self.set_value(i, j, 'r')
						self.boats_left[2] -= 1
					# HORIZONTAL X R
					elif self.adjacent_horizontal_values(i, j) == (None, 'R'):
						self.set_value(i, j, 'l')
						self.boats_left[2] -= 1
					# VERTICAL X X
					elif (self.adjacent_vertical_values(i, j) == (None, 'X') or self.adjacent_vertical_values(i, j) == ('W', 'X')) and \
					 (self.adjacent_vertical_values(i + 1, j) == ('X', None) or self.adjacent_vertical_values(i + 1, j) == ('X', 'W')):
						self.set_value(i, j, 't')
						self.set_value(i + 1, j, 'b')
						self.boats_left[2] -= 1
					# HORIZONTAL X X
					elif (self.adjacent_horizontal_values(i, j) == (None, 'X') or self.adjacent_horizontal_values(i, j) == ('W', 'X')) and \
					 (self.adjacent_horizontal_values(i, j + 1) == ('X', None) or self.adjacent_horizontal_values(i, j + 1) == ('X', 'W')):
						self.set_value(i, j, 'l')
						self.set_value(i, j + 1, 'r')
						self.boats_left[2] -= 1
					# VERTICAL X X X
					elif (self.adjacent_vertical_values(i, j) == (None, 'X') or self.adjacent_vertical_values(i, j) == ('W', 'X')) and \
					 self.adjacent_vertical_values(i + 1, j) == ('X', 'X') and \
					 (self.adjacent_vertical_values(i + 2, j) == ('X', None) or self.adjacent_vertical_values(i + 2, j) == ('X', 'W')):
						self.set_value(i, j, 't')
						self.set_value(i + 1, j, 'm')
						self.set_value(i + 2, j, 'b')
						self.boats_left[3] -= 1
					# HORIZONTAL X X X
					elif (self.adjacent_horizontal_values(i, j) == (None, 'X') or self.adjacent_horizontal_values(i, j) == ('W', 'X')) and \
					 self.adjacent_horizontal_values(i, j + 1) == ('X', 'X') and \
					 (self.adjacent_horizontal_values(i, j + 2) == ('X', None) or self.adjacent_horizontal_values(i, j + 2) == ('X', 'W')):
						self.set_value(i, j, 'l')
						self.set_value(i, j + 1, 'm')
						self.set_value(i, j + 2, 'r')
						self.boats_left[3] -= 1
					# VERTICAL X X X X
					elif (self.adjacent_vertical_values(i, j) == (None, 'X') or self.adjacent_vertical_values(i, j) == ('W', 'X')) and \
					 self.adjacent_vertical_values(i + 1, j) == ('X', 'X') and \
					 self.adjacent_vertical_values(i + 2, j) == ('X', 'X') and \
					 (self.adjacent_vertical_values(i + 3, j) == ('X', None) or self.adjacent_vertical_values(i + 3, j) == ('X', 'W')):
						self.set_value(i, j, 't')
						self.set_value(i + 1, j, 'm')
						self.set_value(i + 2, j, 'm')
						self.set_value(i + 3, j, 'b')
						self.boats_left[4] -= 1
					# HORIZONTAL X X X X
					elif (self.adjacent_horizontal_values(i, j) == (None, 'X') or self.adjacent_horizontal_values(i, j) == ('W', 'X')) and \
					 self.adjacent_horizontal_values(i, j + 1) == ('X', 'X') and \
					 self.adjacent_horizontal_values(i, j + 2) == ('X', 'X') and \
					 (self.adjacent_horizontal_values(i, j + 3) == ('X', None) or self.adjacent_horizontal_values(i, j + 3) == ('X', 'W')):
						self.set_value(i, j, 'l')
						self.set_value(i, j + 1, 'm')
						self.set_value(i, j + 2, 'm')
						self.set_value(i, j+ 3, 'r')
						
						self.boats_left[4] -= 1
					# VERTICAL T X X
					elif self.adjacent_vertical_values(i, j) == ('T', 'X') and \
					 self.adjacent_vertical_values(i + 1, j) == ('X', None):
						self.set_value(i, j, 'm')
						self.set_value(i + 1, j, 'b')
						self.boats_left[3] -= 1
					# VERTICAL T M X
					elif self.adjacent_vertical_values(i, j) == ('M', None) and \
					 self.adjacent_vertical_values(i - 1, j) == ('T', 'X'):
						self.set_value(i, j, 'b')
						self.boats_left[3] -= 1
					# VERTICAL X X B
					elif self.adjacent_vertical_values(i, j) == (None, 'X') and \
					 self.adjacent_vertical_values(i + 1, j) == ('X', 'B'):
						self.set_value(i, j, 't')
						self.set_value(i + 1, j, 'm')
						self.boats_left[3] -= 1
					# VERTICAL X M B
					elif self.adjacent_vertical_values(i, j) == (None, 'M') and \
					 self.adjacent_vertical_values(i + 1, j) == ('X', 'B'):
						self.set_value(i, j, 't')
						self.boats_left[3] -= 1
					# VERTICAL T X X X
					elif self.adjacent_vertical_values(i, j) == ('T', 'X') and \
					 self.adjacent_vertical_values(i + 1, j) == ('X', 'X') and \
					 self.adjacent_vertical_values(i + 2, j) == ('X', None):
						self.set_value(i, j, 'm')
						self.set_value(i + 1, j, 'm')
						self.set_value(i + 2, j, 'b')
						self.boats_left[4] -= 1
					# VERTICAL T M X X
					elif self.adjacent_vertical_values(i, j) == ('M', 'X') and \
					 self.adjacent_vertical_values(i + 1, j) == ('X', None) and \
					 self.adjacent_vertical_values(i - 1, j) == ('T', 'X'):
						self.set_value(i, j, 'm')
						self.set_value(i + 1, j, 'b')
						self.boats_left[4] -= 1
					# VERTICAL T M M X
					elif self.adjacent_vertical_values(i, j) == ('M', None) and \
					 self.adjacent_vertical_values(i - 1, j) == ('M', 'X') and \
					 self.adjacent_vertical_values(i - 2, j) == ('T', 'M') and \
					 self.adjacent_vertical_values(i - 3, j) == (None, 'M'):
						self.set_value(i, j, 'b')
						self.boats_left[4] -= 1
					# VERTICAL X X X B
					elif self.adjacent_horizontal_values(i, j) == (None, 'X') and \
					 self.adjacent_vertical_values(i + 1, j) == ('X', 'X') and \
					 self.adjacent_horizontal_values(i + 2, j) == ('X', 'B'):
						self.set_value(i, j, 't')
						self.set_value(i + 1, j, 'm')
						self.set_value(i + 2, j, 'm')
						self.boats_left[4] -= 1
					# VERTICAL X X M B
					elif self.adjacent_vertical_values(i, j) == (None, 'X') and \
					 self.adjacent_vertical_values(i + 1, j) == ('X', 'M') and \
					 self.adjacent_vertical_values(i + 2, j) == ('X', 'B') and \
					 self.adjacent_vertical_values(i + 3, j) == ('M', None):
						self.set_value(i, j, 't')
						self.set_value(i + 1, j ,'m')
						self.boats_left[4] -= 1
					# VERTICAL X M M B
					elif self.adjacent_vertical_values(i, j) == (None, 'M') and \
					 self.adjacent_vertical_values(i + 1, j) == ('X', 'M') and \
					 self.adjacent_vertical_values(i + 2, j) == ('M', 'B') and \
					 self.adjacent_vertical_values(i + 3, j) == ('M', None):
						self.set_value(i, j, 't')
						self.boats_left[4] -= 1
					# HORIZONTAL X M R
					elif self.adjacent_horizontal_values(i, j) == (None, 'M') and \
					 self.adjacent_horizontal_values(i, j + 1) == ('M', None):
						self.set_value(i, j, 'l')
						self.boats_left[3] -= 1
					# HORIZONTAL X X R
					elif self.adjacent_horizontal_values(i, j) == (None, 'X') and \
					 self.adjacent_horizontal_values(i, j + 1) == ('X', 'R') and \
					 self.adjacent_horizontal_values(i, j + 2) == ('X', None):
						self.set_value(i, j, 'l')
						self.set_value(i, j, 'm')
						self.boats_left[3] -= 1
					# HORIZONTAL L X X
					elif self.adjacent_horizontal_values(i, j) == ('L', 'X') and \
					 self.adjacent_horizontal_values(i, j + 1) == ('X', None) and \
					 self.adjacent_horizontal_values(i, j - 1) == (None, 'X'):
						self.set_value(i, j, 'm')
						self.set_value(i, j + 1, 'r')
						self.boats_left[3] -= 1
					# HORIZONTAL L M X
					elif self.adjacent_horizontal_values(i, j) == ('M', None) and \
					 self.adjacent_horizontal_values(i, j - 1) == ('L', 'X') and \
					 self.adjacent_horizontal_values(i, j - 2) == (None, 'M'):
						self.set_value(i, j, 'r')
						self.boats_left[3] -= 1
					# HORIZONTAL X M M R
					elif self.adjacent_horizontal_values(i, j) == (None, 'M') and \
					 self.adjacent_horizontal_values(i, j + 1) == ('X', 'M') and \
					 self.adjacent_horizontal_values(i, j + 2) == ('M', 'R') and \
					 self.adjacent_horizontal_values(i, j + 3) == ('M', None):
						self.set_value(i, j, 'l')
						self.boats_left[4] -= 1
					# HORIZONTAL X X M R
					elif self.adjacent_horizontal_values(i, j) == (None, 'X') and \
					 self.adjacent_horizontal_values(i, j + 1) == ('X', 'M')  and \
					 self.adjacent_horizontal_values(i, j + 2) == ('X', 'R') and \
					 self.adjacent_horizontal_values(i, j + 3) == ('M', None):
						self.set_value(i, j, 'l')
						self.set_value(i, j + 1, 'm')
						self.boats_left[4] -= 1
					# HORIZONTAL X X X R
					elif self.adjacent_horizontal_values(i, j) == (None, 'X') and \
					 self.adjacent_horizontal_values(i, j + 1) == ('X', 'X') and \
					 self.adjacent_horizontal_values(i, j + 2) == ('X', 'R') and \
					 self.adjacent_horizontal_values(i, j + 3) == ('X', None):
						self.set_value(i, j, 'l')
						self.set_value(i, j + 1, 'm')
						self.set_value(i, j + 2, 'm')
						self.boats_left[4] -= 1
					# HORIZONTAL L X X X
					elif self.adjacent_horizontal_values(i, j) == ('L', 'X') and \
					 self.adjacent_horizontal_values(i, j + 1) == ('X', 'X') and \
					 self.adjacent_horizontal_values(i, j + 2) == ('X', None) and \
					 self.adjacent_horizontal_values(i, j - 1) == (None, 'X'):
						self.set_value(i, j, 'm')
						self.set_value(i, j + 1, 'm')
						self.set_value(i, j + 2, 'r')
						self.boats_left[4] -= 1
					# HORIZONTAL L M X X
					elif self.adjacent_horizontal_values(i, j) == ('M', 'X') and \
					 self.adjacent_horizontal_values(i, j + 1) == ('X', 'X') and \
					 self.adjacent_horizontal_values(i, j - 1) == ('L', 'X') and \
					 self.adjacent_horizontal_values(i, j - 2) == (None, 'M'):
						self.set_value(i, j, 'm')
						self.set_value(i, j + 1, 'r')
						self.boats_left[4] -= 1
					# HORIZONTAL L M M X
					elif self.adjacent_horizontal_values(i, j) == ('M', None) and \
					 self.adjacent_horizontal_values(i, j - 1) == ('M', 'X') and \
					 self.adjacent_horizontal_values(i, j - 2) == ('L', 'M') and \
					 self.adjacent_horizontal_values(i, j - 3) == (None, 'M'):
						self.set_value(i, j, 'r')
						self.boats_left[4] -= 1
					# HORIZONTAL X X M X
					elif self.adjacent_horizontal_values(i, j) == (None, 'X') and \
					 self.adjacent_horizontal_values(i, j + 1) == ('X', 'M') and \
					 self.adjacent_horizontal_values(i, j + 2) == ('X', 'X') and \
					 self.adjacent_horizontal_values(i, j + 3) == ('M', None):
						self.set_value(i, j, 'l')
						self.set_value(i, j + 1, 'm')
						self.set_value(i, j + 3, 'r')
						self.boats_left[4] -= 1
					# HORIZONTAL X M X X
					elif self.adjacent_horizontal_values(i, j) == (None, 'M') and \
					 self.adjacent_horizontal_values(i, j + 1) == ('X','X') and \
					 self.adjacent_horizontal_values(i, j + 2) == ('M', 'X') and \
					 self.adjacent_horizontal_values(i, j + 3) == ('X', None):
						self.set_value(i, j, 'l')
						self.set_value(i, j + 2, 'm')
						self.set_value(i, j + 3, 'r')
						self.boats_left[4] -= 1
					# HORIZONTAL X M M X
					elif self.adjacent_horizontal_values(i, j) == (None, 'M') and \
					 self.adjacent_horizontal_values(i, j + 1) == ('X','M') and \
					 self.adjacent_horizontal_values(i, j + 2) == ('M', 'X') and \
					 self.adjacent_horizontal_values(i, j + 3) == ('M', None):
						self.set_value(i, j, 'l')
						self.set_value(i, j + 3, 'r')
						self.boats_left[4] -= 1
					# VERTICAL X X M X
					elif self.adjacent_vertical_values(i, j) == (None, 'X') and \
					 self.adjacent_vertical_values(i + 1, j) == ('X', 'M') and \
					 self.adjacent_vertical_values(i + 2, j) == ('X', 'X') and \
					 self.adjacent_vertical_values(i + 3, j) == ('M', None):
						self.set_value(i, j, 't')
						self.set_value(i + 1, j, 'm')
						self.set_value(i + 3, j, 'b')
						self.boats_left[4] -= 1
					# VERTICAL X M X X
					elif self.adjacent_vertical_values(i, j) == (None, 'M') and \
					 self.adjacent_vertical_values(i + 1, j) == ('X','X') and \
					 self.adjacent_vertical_values(i + 2, j) == ('M', 'X') and \
					 self.adjacent_vertical_values(i + 3, j) == ('X', None):
						self.set_value(i, j, 't')
						self.set_value(i + 2, j, 'm')
						self.set_value(i + 3, j, 'b')
						self.boats_left[4] -= 1
					# VERTICAL X M M X
					elif self.adjacent_vertical_values(i, j) == (None, 'M') and \
					 self.adjacent_vertical_values(i + 1, j) == ('X','M') and \
					 self.adjacent_vertical_values(i + 2, j) == ('M', 'X') and \
					 self.adjacent_vertical_values(i + 3, j) == ('M', None):
						self.set_value(i, j, 't')
						self.set_value(i + 3, j, 'b')
						self.boats_left[4] -= 1
					# VERTICAL X M X
					elif self.adjacent_vertical_values(i, j) == (None, 'M') and \
					 self.adjacent_vertical_values(i + 1, j) == ('X', 'X') and \
					 self.adjacent_vertical_values(i + 2, j) == ('M', None):
						self.set_value(i, j, 't')
						self.set_value(i + 2, j, 'b')
						self.boats_left[3] -= 1
					# HORIZONTAL X M X
					elif self.adjacent_horizontal_values(i, j) == (None, 'M') and \
					 self.adjacent_horizontal_values(i, j + 1) == ('X', 'X') and \
					 self.adjacent_horizontal_values(i, j + 2) == ('M', None):
						self.set_value(i, j, 'l')
						self.set_value(i, j + 2, 'r')
						self.boats_left[3] -= 1
				j += 1

			i += 1

	def print_pretty_board(self):
		matrix = self.board
		rows, cols = matrix.shape
		for i in range(rows):
			row_str = ''
			for j in range(cols):
				if matrix[i][j] == ' ':
					row_str += '.'
				else:
					row_str += matrix[i][j]
			print(row_str)

	# TODO: outros metodos da classe

class Bimaru(Problem):
	def __init__(self, board: Board): #,goal):
		"""O construtor especifica o estado inicial."""
		# TODO
		#criar um board para criar um state
		self.initial = BimaruState(board)
		self.board = board
		#self.goal = goal
		pass

	def actions(self, state: BimaruState) -> list:
		"""Retorna uma lista de ações que podem ser executadas a
		partir do estado passado como argumento."""
		return [4, 3, 2, 1]
		pass #METER BARCOS

	def result(self, state: BimaruState, action):
		"""Retorna o estado resultante de executar a 'action' sobre
		'state' passado como argumento. A ação a executar deve ser uma
		das presentes na lista obtida pela execução de
		self.actions(state)."""
		# TODO

		if action == 4:
			pass
		elif action == 3:
			pass
		elif action == 2:
			pass
		elif action == 1:
			pass
		else:
			pass

	def goal_test(self, state: BimaruState):
		"""Retorna True se e só se o estado passado como argumento é
		um estado objetivo. Deve verificar se todas as posições do tabuleiro
		estão preenchidas de acordo com as regras do problema."""
		return self.is_goal(state.board)

	def h(self, node: Node):
		"""Função heuristica utilizada para a procura A*."""
		# TODO
		pass

	# TODO: outros metodos da classe
	def is_goal(self, board):
		num_boats = [0, 4, 3, 2, 1] #boat size : number boats

		if self.board.count_nonzero('X') != 20:
			return False

		for i in range(10):
			row = self.board[i]
			x_count = 0
			boat_count = 0
			for j in range(10):
				if row[j] == 'X' and self.board.adjacent_vertical_values(i, j) == (None, None):
					boat_count += 1
					x_count += 1
				elif row[j] == ' ':
					num_boats[boat_count] -= 1
					boat_count = 0
			
			if x_count != self.board.copyrow[i]:
				return False
		
		for i in range(10):
			col = self.board[:, i]
			x_count = 0
			boat_count = 0
			for j in range(10):
				if col[j] == 'X' and self.board.adjacent_horizontal_values(j, i) == (None, None):
					boat_count += 1
					x_count += 1
				elif col[j] == ' ':
					if boat_count != 1:
						num_boats[boat_count] -= 1
						boat_count = 0
			
			if x_count != self.board.copycol[i]:
				return False

		if num_boats.count(0) != 5:
			return False
		
		return True


if __name__ == "__main__":
	# TODO:
	# Ler o ficheiro do standard input,
	# Usar uma técnica de procura para resolver a instância,
	# Retirar a solução a partir do nó resultante,
	# Imprimir para o standard output no formato indicado.
	board = Board.parse_instance()


	#print(board.adjacent_vertical_values(3, 3))
	#print(board.adjacent_horizontal_values(3, 3))
	#print(board.adjacent_vertical_values(1, 0))
	#print(board.adjacent_horizontal_values(1, 0))

	board.fill_the_board()
	#print(" ")

	
	problem = Bimaru(board)
	#initial_state = BimaruState(board)
	#result_state = problem.result(initial_state, (3, 3, 'w'))
	board.print_board()
	print(board.boats_left)
	print("")
	board.print_pretty_board()

	
