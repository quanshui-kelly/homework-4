############################################################
# CIS 521: Homework 4
############################################################

############################################################
# Imports
############################################################

# Include your imports here, if any are used.
import collections
import copy
import itertools
import random
import math

############################################################

student_name = "Xinyuan Quan"

############################################################
# Section 1: Dominoes Game
############################################################


def create_dominoes_game(rows, cols):
    ans = []
    for i in range(rows):
        lst = []
        for j in range(cols):
            lst.append(False)
        ans.append(lst)
    return DominoesGame(ans)


class DominoesGame(object):

    
    # Required
    def __init__(self, board):
        self.board = board
        self.rows = len(board)
        self.cols = len(board[0])

    def get_board(self):
        return self.board

    def reset(self):
        self.board = create_dominoes_game(self.rows, self.cols)

    def is_legal_move(self, row, col, vertical):
        if vertical:
            if row + 1 >= self.rows:
                return False

            if self.board[row][col] == False and \
                    self.board[row + 1][col] == False:  # noqa: SIM103
                return True

            return False

        else:
            if col + 1 >= self.cols:
                return False

            if self.board[row][col] == False and \
                    self.board[row][col + 1] == False:  # noqa: SIM103
                return True

            return False

    def legal_moves(self, vertical):
        for i in range(self.rows):
            for j in range(self.cols):
                if self.is_legal_move(i, j, vertical):
                    yield (i, j)

    def perform_move(self, row, col, vertical):
        if vertical and self.is_legal_move(row, col, vertical):
            self.board[row][col] = True
            self.board[row + 1][col] = True
        if not vertical and self.is_legal_move(row, col, vertical):
            self.board[row][col] = True
            self.board[row][col + 1] = True

    def game_over(self, vertical):
        for _ in self.legal_moves(vertical):
            return False
        return True

    def copy(self):
        new_one = []
        for i in range(self.rows):
            instance = []
            for j in range(self.cols):
                instance.append(self.board[i][j])
            new_one.append(instance)
        return DominoesGame(new_one)

    def successors(self, vertical):
        for move in self.legal_moves(vertical):
            new_game = self.copy()
            new_game.perform_move(
                move[0],
                move[1],
                vertical
            )
            yield (move, new_game)

    def get_random_move(self, vertical):
        moves = list(self.legal_moves(vertical))

        if not moves:
            return None

        return random.choice(moves)

    # Required
    def get_best_move(self, vertical, limit):
        root_player = vertical

        def evaluate(game):
            player_score = sum(
                1 for i in game.legal_moves(root_player)
            )

            opponent_score = sum(
                1 for i in game.legal_moves(not root_player)
            )

            return player_score - opponent_score

        def max_value(game, depth, alpha, beta):
            if depth == limit or game.game_over(root_player):
                return evaluate(game), 1

            value = -math.inf
            leaves = 0

            for move, new_game in game.successors(root_player):
                child_value, child_leaves = min_value(
                    new_game,
                    depth + 1,
                    alpha,
                    beta
                )

                value = max(value, child_value)
                leaves += child_leaves

                if value >= beta:
                    break

                alpha = max(alpha, value)

            return value, leaves

        def min_value(game, depth, alpha, beta):
            opponent = not root_player

            if depth == limit or game.game_over(opponent):
                return evaluate(game), 1

            value = math.inf
            leaves = 0

            for move, new_game in game.successors(opponent):
                child_value, child_leaves = max_value(
                    new_game,
                    depth + 1,
                    alpha,
                    beta
                )

                value = min(value, child_value)
                leaves += child_leaves

                if value <= alpha:
                    break

                beta = min(beta, value)

            return value, leaves

        best_move = None
        best_value = -math.inf
        alpha = -math.inf
        beta = math.inf
        leaf_count = 0

        for move, new_game in self.successors(root_player):
            value, leaves = min_value(
                new_game,
                1,
                alpha,
                beta
            )

            leaf_count += leaves

            if value > best_value:
                best_value = value
                best_move = move

            alpha = max(alpha, best_value)

        return best_move, best_value, leaf_count

############################################################
# Section 2: Feedback
############################################################


# Just an approximation is fine.
feedback_question_1 = """
6
"""

feedback_question_2 = """
The last part is kind of difficult, but generally is easier
than previous ones.
"""

feedback_question_3 = """
Very clear and structual, easy to think under hints and each steps.
"""
