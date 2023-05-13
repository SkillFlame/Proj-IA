# bimaru.py: Template para implementação do projeto de Inteligência Artificial 2022/2023.
# Devem alterar as classes e funções neste ficheiro de acordo com as instruções do enunciado.
# Além das funções e classes já definidas, podem acrescentar outras que considerem pertinentes.

# Grupo 13:
# 99105 Marco Cunha
# 103590 Tiago Firmino

import sys
import numpy as np
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

	def equals(self, other): #added
		return self.id == other.id

	def get_board(self): #added
		return self.board

	# TODO: outros metodos da classe


class Board:
	"""Representação interna de um tabuleiro de Bimaru."""

	def __init__(self, board, row_vals = [], col_vals = []):
		self.board = board
		self.size = 10
		self.rowvals = row_vals
		self.colvals = col_vals

	def get_value(self, row: int, col: int) -> str:
		"""Devolve o valor na respetiva posição do tabuleiro."""
		return self.board[row][col]

	def set_value(self, row: int, col: int, value: int):
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

		if top == '.' or top == 'w' or top == 'W' or top == ' ':
			top = None
		if bottom == '.' or bottom == 'w' or bottom == 'W' or bottom == ' ':
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

		if left == '.' or left == 'w' or left == 'W' or left == ' ':
			left = None
		if right == '.' or right == 'w' or right == 'W' or right == ' ':
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
		# TODO
		matrix = np.full((10,10), ' ', dtype=str)
		inp_row = sys.stdin.readline()
		vals_row = [int(x) for x in inp_row.split()[1:]]

		inp_col = sys.stdin.readline()
		vals_col = [int(x) for x in inp_col.split()[1:]]

		num_hints = int(input())
		for i in range(num_hints):
			line = sys.stdin.readline().split()
			# FIXME change this
			'''
			if str(line[3]) == "W":
				line[3] = "."
			'''
			matrix[int(line[1])][int(line[2])] = str(line[3])

		# adicionar atributos aqui e possivel board.new_attr = uu

		return Board(matrix, vals_row, vals_col)

	def print_board(self):
		print(self.board)
		print(" ")
		print(self.rowvals, self.colvals)

	def fill_the_board(self):
		self.put_line_waters()
		self.put_possible_positions()

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

	def put_water_around_boat(self):
		np.nonzero(self.board == "T")


	def put_possible_positions(self):
		pass
	
	# TODO: outros metodos da classe



class Bimaru(Problem):
	def __init__(self, board: Board): #,goal):
		"""O construtor especifica o estado inicial."""
		# TODO
		#criar um board para criar um state
		self.initial = BimaruState(board)
		#self.goal = goal
		pass

	def actions(self, state: BimaruState) -> list:
		"""Retorna uma lista de ações que podem ser executadas a
		partir do estado passado como argumento."""
		# TODO
		return ["Water", "Top", "Bottom", "Left", "Right", "Middle", "FillLine", "FillColumn", "Remove", "Something"]
		pass

	def result(self, state: BimaruState, action):
		"""Retorna o estado resultante de executar a 'action' sobre
		'state' passado como argumento. A ação a executar deve ser uma
		das presentes na lista obtida pela execução de
		self.actions(state)."""
		# TODO

		if(action == "Water"):
			return state.put_water()
		elif(action == "Top"):
			return state.put_top()
		elif(action == "Bottom"):
			return state.put_bottom()
		elif(action == "Left"):
			return state.put_left()
		elif(action == "Right"):
			return state.put_right()
		elif(action == "Middle"):
			return state.put_middle()
		elif(action == "FillLine"):
			return state.fill_line()
		elif(action == "FillColumn"):
			return state.fill_column
		elif(action == "Remove"):
			return state.remove()
		elif(action == "Mark"):
			return state.mark_spot()
		else:
			return NotImplementedError()

	def goal_test(self, state: BimaruState):
		"""Retorna True se e só se o estado passado como argumento é
		um estado objetivo. Deve verificar se todas as posições do tabuleiro
		estão preenchidas de acordo com as regras do problema."""
		# TODO
		#return self.goal == state.board
		pass

	def h(self, node: Node):
		"""Função heuristica utilizada para a procura A*."""
		# TODO
		pass

	# TODO: outros metodos da classe


if __name__ == "__main__":
	# TODO:
	# Ler o ficheiro do standard input,
	# Usar uma técnica de procura para resolver a instância,
	# Retirar a solução a partir do nó resultante,
	# Imprimir para o standard output no formato indicado.
	board = Board.parse_instance()

	board.fill_the_board()

	print(board.adjacent_vertical_values(3, 3))
	print(board.adjacent_horizontal_values(3, 3))
	print(board.adjacent_vertical_values(1, 0))
	print(board.adjacent_horizontal_values(1, 0))

	print(" ")

	
	problem = Bimaru(board)
	board.print_board()

	
