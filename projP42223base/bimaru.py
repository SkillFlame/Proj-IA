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
        matrix = np.full((10,10), '.', dtype=str)
        inp_row = sys.stdin.readline()
        vals_row = [int(x) for x in inp_row.split()[1:]]

        inp_col = sys.stdin.readline()
        vals_col = [int(x) for x in inp_col.split()[1:]]

        num_hints = int(input())
        for i in range(num_hints):
            line = sys.stdin.readline().split()
            matrix[int(line[1])][int(line[2])] = str(line[3])

        # adicionar atributos aqui e possivel board.new_attr = uu

        return Board(matrix, vals_row, vals_col)

    def print_board(self):
        print(self.board)
        print(" ")
        print(self.rowvals, self.colvals)

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
        elif(action == "Something"):
            return state.put_something()
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

    print(board.adjacent_vertical_values(3, 3))
    print(board.adjacent_horizontal_values(3, 3))
    print(board.adjacent_vertical_values(1, 0))
    print(board.adjacent_horizontal_values(1, 0))

    print(" ")

    
    problem = Bimaru(board)
    board.print_board()

    
