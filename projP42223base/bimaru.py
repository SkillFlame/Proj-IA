# bimaru.py: Template para implementação do projeto de Inteligência Artificial 2022/2023.
# Devem alterar as classes e funções neste ficheiro de acordo com as instruções do enunciado.
# Além das funções e classes já definidas, podem acrescentar outras que considerem pertinentes.

# Grupo 13:
# 99105 Marco Cunha
# 103590 Tiago Firmino

import sys
import numpy as np
import copy as cp
import time
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
		self.copyhints = copyhints
		self.copyrow = cp.deepcopy(self.rowvals)
		self.copycol = cp.deepcopy(self.colvals)
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
			bottom = self.get_value(row + 1, col)
		elif(row == self.size - 1):
			bottom = None
			top = self.get_value(row - 1, col)
		else:
			top = self.get_value(row -1 , col)
			bottom = self.get_value(row + 1, col)

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
			right = self.get_value(row, col + 1)
		elif(col == self.size - 1):
			right = None
			left = self.get_value(row, col - 1)
		else:
			left = self.get_value(row, col - 1)
			right = self.get_value(row, col + 1)

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
		return Board(matrix, vals_row, vals_col, copyhints)
		#FIXME USAR O QUE ESTA A BAIXO PARA DEBUG 
		#with open('instance03.txt', 'r') as file:
		#	copyhints = []
		#	for line in file:
		#		if line.startswith('ROW'):
		#			# Split the line and convert the values to integers
		#			rows = [int(x) for x in line.split()[1:]]
		#		elif line.startswith('COLUMN'):
		#			# Split the line and convert the values to integers
		#			columns = [int(x) for x in line.split()[1:]]
		#		elif line.startswith('HINT'):
		#			# Split the line and extract the hint information
		#			line = line.split()
		#			copyhints.append(line)
		#			matrix[int(line[1])][int(line[2])] = str(line[3])
		#return Board(matrix, rows, columns, copyhints)

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
		#self.put_water_around_search()

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
					#if (ver_vals == (None, None) or ver_vals == ('w', 'w') or ver_vals == ('W', 'w') or ver_vals == ('W', 'W')) and i < 9:
					#	if i == 1:
					#		self.set_value(i - 1, j, 'X')
					#	elif self.get_value(i - 1, j) != 'w':
					#		self.set_value(i - 1, j, 'X')
					#	if i == self.size - 2:
					#		self.set_value(i + 1, j, 'X')
					#	elif self.get_value(i + 1, j) != 'w':
					#		self.set_value(i + 1, j, 'X')
			#
					#if (hor_vals == (None, None) or hor_vals == ('w', 'w') or hor_vals == ('W', 'w') or hor_vals == ('W', 'W')) and j < 9:
					#	if j == 1:
					#		self.set_value(i, j - 1, 'X')
					#	elif self.get_value(i, j - 1) != 'w':
					#		self.set_value(i, j - 1, 'X')
					#	if j == self.size - 2:
					#		self.set_value(i, j + 1, 'X')
					#	elif self.get_value(i, j + 1) != 'w':
					#		self.set_value(i, j + 1, 'X')
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
	
	def complete_possible_boats(self):
		i = 0
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
	

	def check_for_bigger_boat(self, boat_size, boat_list):
		for i in range(boat_size + 1, len(boat_list)):
			print(len(boat_list))
			if boat_list[i] > 0:
				return True
		return False

	def get_actions(self):
		num_boats = [0, 4, 3, 2, 1] #number_boats[boat_size]
		row_vals = cp.deepcopy(self.rowvals)
		col_vals = cp.deepcopy(self.colvals)
		adjacent_cases = [(None, None), ("?", None), (None, "?"), ("?", "?")]

		for i in range(self.size):
			row = self.board[i]
			boat_count = 0
			for j in range(self.size):
				if row[j] == 'X':
					row_vals[i] -= 1

				if row[j] == 'X' and self.adjacent_vertical_values(i, j) in adjacent_cases:
					boat_count += 1
				elif row[j] == '?':
					if boat_count == 4 or not self.check_for_bigger_boat(boat_count, num_boats):
						print("cona")
						num_boats[boat_count] -= 1
					boat_count = 0
				elif row[j] == ' ' and boat_count != 0:
					num_boats[boat_count] -= 1
					boat_count = 0
				if j == 9 and boat_count != 0:
					if boat_count >= 1:
						num_boats[boat_count] -= 1
					boat_count = 0
			if boat_count >= 1:
				num_boats[boat_count] -= 1
		
		for i in range(self.size):
			col = self.board[:, i]
			boat_count = 0
			for j in range(self.size):
				if col[j] == 'X':
					col_vals[i] -= 1
				
				if col[j] == 'X' and self.adjacent_horizontal_values(j, i) in adjacent_cases:
					boat_count += 1	
				elif col[j] == '?':
					if boat_count == 4 or not self.check_for_bigger_boat(boat_count, num_boats):
						num_boats[boat_count] -= 1
					boat_count = 0
				elif col[j] == ' ' and boat_count != 0:
					if boat_count > 1:
						num_boats[boat_count] -= 1
					boat_count = 0
				if j == 9 and boat_count != 0:
					if boat_count > 1:
						num_boats[boat_count] -= 1
					boat_count = 0
		boat_size = 4
		while boat_size > 0:
			if num_boats[boat_size] > 0:
				break
			else:
				boat_size -= 1

		
		actions = []
		for i in range(self.size):
			row = self.board[i]
			if(row_vals[i] + np.count_nonzero(row == 'X') >= boat_size):
				for w in range(self.size):
					if (row[w] == 'X' or row[w] == '?') and self.get_value(i, w-1) != 'X':
						start = [i, w]
						x_count = 0
						empty_count = 0
						for j in range(w, self.size):
							if row[j] == 'X' and self.adjacent_vertical_values(i, j) in adjacent_cases:
								x_count += 1
							elif row[j] == '?' and self.adjacent_vertical_values(i, j) in adjacent_cases:
								empty_count += 1
							elif row[j] == ' ':
								if x_count < boat_size and empty_count + x_count >= boat_size and row_vals[i] + x_count >= boat_size and self.adjacent_vertical_values(i, j) in adjacent_cases:
									offset = (empty_count + x_count) - boat_size
									if empty_count - offset <= row_vals[i]:
										actions.append((boat_size, start[0], start[1] + offset, "h"))
								x_count = 0
								empty_count = 0
								break

							if x_count < boat_size and empty_count + x_count == boat_size and row_vals[i] + x_count >= boat_size and j < 9 and row[j + 1] != 'X' and self.adjacent_vertical_values(i, j) in adjacent_cases:
								actions.append((boat_size, start[0], start[1], "h"))
								x_count = 0
								empty_count = 0
								break
							elif x_count > boat_size:
								x_count = 0
								empty_count = 0
								break
							
						if x_count < boat_size and empty_count + x_count == boat_size and row_vals[i] + x_count >= boat_size and self.adjacent_vertical_values(i, j) in adjacent_cases:	
							actions.append((boat_size, start[0], start[1], "h"))
		if boat_size > 1:
			for i in range(self.size):
				col = self.board[:, i]
				if(col_vals[i] + np.count_nonzero(col == 'X') >= boat_size):
					for w in range(self.size):
						if (col[w] == 'X' or col[w] == '?') and self.get_value(w-1, i) != 'X':
							start = [w, i]
							x_count = 0
							empty_count = 0
							for j in range(w, self.size):
								if col[j] == 'X' and self.adjacent_horizontal_values(j, i) in adjacent_cases:
									x_count += 1
								elif col[j] == '?' and self.adjacent_horizontal_values(j, i) in adjacent_cases:
									empty_count += 1
								elif col[j] == ' ':
									if x_count < boat_size and empty_count + x_count >= boat_size and col_vals[i] + x_count >= boat_size and self.adjacent_horizontal_values(j, i) in adjacent_cases:
										offset = (empty_count + x_count) - boat_size
										if empty_count - offset <= col_vals[i]:
											actions.append((boat_size, start[0] + offset, start[1], "v"))
									x_count = 0
									empty_count = 0
									break
								
								if x_count < boat_size and empty_count + x_count == boat_size and col_vals[i] + x_count >= boat_size and j < 9 and col[j + 1] != 'X' and self.adjacent_horizontal_values(j, i) in adjacent_cases:
									actions.append((boat_size, start[0], start[1], "v"))
									x_count = 0
									empty_count = 0
									break
								elif x_count > boat_size:
									x_count = 0
									empty_count = 0
									break
							if x_count < boat_size and empty_count + x_count == boat_size and col_vals[i] + x_count >= boat_size and self.adjacent_horizontal_values(j, i) in adjacent_cases:
								actions.append((boat_size, start[0], start[1], "v"))
		if boat_size == 3:
			print(sorted(actions, key=self.sort_aux))
			print(num_boats)
			self.print_board()
			time.sleep(1)
		return sorted(actions, key=self.sort_aux)

	def sort_aux(self, list):
		return list[0]


	def update(self):
		for i in range(len(self.copyhints)):
			values = self.copyhints[i][1:4]
			self.set_value(int(values[0]), int(values[1]), values[2])

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
					# VERTICAL X X
					elif self.adjacent_vertical_values(i, j) == (None, 'X') and self.adjacent_vertical_values(i + 1, j) == ('X', None):
						self.set_value(i, j, 't')
						self.set_value(i + 1, j, 'b')
						self.boats_left[2] -= 1
					# HORIZONTAL X X
					elif self.adjacent_horizontal_values(i, j) == (None, 'X') and self.adjacent_horizontal_values(i, j + 1) == ('X', None):
						self.set_value(i, j, 'l')
						self.set_value(i, j + 1, 'r')
						self.boats_left[2] -= 1
					# VERTICAL X X X
					elif self.adjacent_vertical_values(i, j) == (None, 'X') and self.adjacent_vertical_values(i + 1, j) == ('X', 'X') and \
					 self.adjacent_vertical_values(i + 2, j) == ('X', None):
						self.set_value(i, j, 't')
						self.set_value(i + 1, j, 'm')
						self.set_value(i + 2, j, 'b')
						self.boats_left[3] -= 1
					# HORIZONTAL X X X
					elif self.adjacent_horizontal_values(i, j) == (None, 'X') and self.adjacent_horizontal_values(i, j + 1) == ('X', 'X') and \
					 self.adjacent_horizontal_values(i, j + 2) == ('X', None):
						self.set_value(i, j, 'l')
						self.set_value(i, j + 1, 'm')
						self.set_value(i, j + 2, 'r')
						self.boats_left[3] -= 1
					# VERTICAL X X X X
					elif self.adjacent_vertical_values(i, j) == (None, 'X') and self.adjacent_vertical_values(i + 1, j) == ('X', 'X') and \
					 self.adjacent_vertical_values(i + 2, j) == ('X', 'X') and self.adjacent_vertical_values(i + 3, j) == ('X', None):
						self.set_value(i, j, 't')
						self.set_value(i + 1, j, 'm')
						self.set_value(i + 2, j, 'm')
						self.set_value(i + 3, j, 'b')
						self.boats_left[4] -= 1
					# HORIZONTAL X X X X
					elif self.adjacent_horizontal_values(i, j) == (None, 'X') and self.adjacent_horizontal_values(i, j + 1) == ('X', 'X') and \
					 self.adjacent_horizontal_values(i, j + 2) == ('X', 'X') and self.adjacent_horizontal_values(i, j + 3) == ('X', None):
						self.set_value(i, j, 'l')
						self.set_value(i, j + 1, 'm')
						self.set_value(i, j + 2, 'm')
						self.set_value(i, j + 3, 'r')
				j += 1
			i += 1
		
	def fill_with_search(self):
		i = 0
		parts = ['X']
		while i < self.size:
			j = 0
			while j < self.size:
				if self.get_value(i, j) == '?':
					num_parts_line = np.count_nonzero(np.char.strip(self.board[i]) == np.array(parts))
					num_parts_col = np.count_nonzero(np.char.strip(self.board[:, j]) == np.array(parts))
					
					if self.rowvals[i] == num_parts_line or self.colvals[j] == num_parts_col:
						self.set_value(i, j, ' ')
				
				j += 1
			i += 1

	def complete_possible_search(self):
		i = 0
		while i < self.size:
			j = 0
			while j < self.size:
				
				if self.rowvals[i] == np.count_nonzero(self.board[i] == 'X') + np.count_nonzero(self.board[i] == '?'):
					if self.get_value(i, j) == '?':
						self.set_value(i, j, 'X')
						self.fill_with_search()
				
				if self.colvals[j] == np.count_nonzero(self.board[:, j] == 'X') + np.count_nonzero(self.board[:, j] == '?'):
					if self.get_value(i, j) == '?':
						self.set_value(i, j, 'X')
						self.fill_with_search()
				
				j += 1
			i += 1
	
	def put_water_around_search(self):
		t_pos_list = np.nonzero(self.board == "X")
		i = 0
		while i < len(t_pos_list[0]):
			row = t_pos_list[0][i]
			col = t_pos_list[1][i]
			self.set_value(row + 1, col - 1, " ")
			self.set_value(row - 1, col - 1, " ")
			self.set_value(row - 1, col + 1, " ")
			self.set_value(row + 1, col + 1, " ")
			i += 1

	def apply_actions(self, action):
		boat_size = action[0]
		row_val = action[1]
		col_val = action[2]
		direction = action[3]

		if direction == 'v':
			i = row_val
			while i < boat_size + row_val:
				if self.get_value(i, col_val) == '?':
					self.set_value(i, col_val, 'X')
				i += 1
		elif direction == 'h':
			i = col_val
			while i < boat_size + col_val:
				if self.get_value(row_val, i) == '?':
					self.set_value(row_val, i, 'X')
				i += 1
		self.put_water_around_search()
		self.fill_with_search() # novo barco posto, se preencher linha/coluna chamar isto
	
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
	def __init__(self, board: Board):
		"""O construtor especifica o estado inicial."""
		# TODO
		#criar um board para criar um state
		self.initial = BimaruState(board)
		self.board = board

	def actions(self, state: BimaruState) -> list:
		"""Retorna uma lista de ações que podem ser executadas a
		partir do estado passado como argumento."""
		
		actions = state.board.get_actions()
		return actions

	def result(self, state: BimaruState, action):
		"""Retorna o estado resultante de executar a 'action' sobre
		'state' passado como argumento. A ação a executar deve ser uma
		das presentes na lista obtida pela execução de
		self.actions(state)."""
		# TODO
		# aplicar action ao estado
		new_state = BimaruState(cp.deepcopy(state.board))
		new_state.board.apply_actions(action)
		return new_state

	def goal_test(self, state: BimaruState):
		"""Retorna True se e só se o estado passado como argumento é
		um estado objetivo. Deve verificar se todas as posições do tabuleiro
		estão preenchidas de acordo com as regras do problema."""
		test_board = state.board
		return self.is_goal(test_board)

	def h(self, node: Node):
		"""Função heuristica utilizada para a procura A*."""
		# TODO
		pass

	def is_goal(self, board):
		num_boats = [0, 4, 3, 2, 1] #boat size : number boats
	
		#print(np.count_nonzero(board.board == 'X'))
		if np.count_nonzero(board.board == 'X') != 20:
			return False

		for i in range(10):
			row = board.board[i]
			x_count = 0
			boat_count = 0
			for j in range(10):
				if row[j] == 'X':
					x_count += 1
				if row[j] == 'X' and board.adjacent_vertical_values(i, j) == (None, None):
					boat_count += 1
				elif row[j] == ' ' and boat_count != 0:
					num_boats[boat_count] -= 1
					boat_count = 0
				if j == 9 and boat_count != 0:
					if boat_count >= 1:
						num_boats[boat_count] -= 1
					boat_count = 0
			if boat_count >= 1:
				num_boats[boat_count] -= 1
			
			if x_count != board.rowvals[i]:
				return False
		
		for i in range(10):
			col = board.board[:, i]
			x_count = 0
			boat_count = 0
			for j in range(10):
				if col[j] == 'X':
					x_count += 1
				if col[j] == 'X' and board.adjacent_horizontal_values(j, i) == (None, None):
					boat_count += 1
				elif col[j] == ' ' and boat_count != 0:
					if boat_count > 1:
						num_boats[boat_count] -= 1
					boat_count = 0
				if j == 9 and boat_count != 0:
					if boat_count > 1:
						num_boats[boat_count] -= 1
					boat_count = 0
			
			if x_count != board.colvals[i]:
				return False

		if num_boats.count(0) != 5:
			return False
		return True
	# TODO: outros metodos da classe

if __name__ == "__main__":
	# TODO:
	# Ler o ficheiro do standard input,
	# Usar uma técnica de procura para resolver a instância,
	# Retirar a solução a partir do nó resultante,
	# Imprimir para o standard output no formato indicado.
	board = Board.parse_instance()

	board.fill_the_board()
	
	problem = Bimaru(board)
	goal_node = depth_first_tree_search(problem)
	#problem.board.print_board()
	
	goal_node.state.board.complete_boat()
	goal_node.state.board.update()
	goal_node.state.board.print_pretty_board()
	#print("")
	#problem.board.print_pretty_board()
	#goal_node.print_pretty_board()

	