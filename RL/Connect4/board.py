import numpy as np

# Constants
NUM_ROWS = 6
NUM_COLS = 7
EMPTY = 0
RED = 1
YELLOW = 2

class Board:
  def __init__(self, online=False):
    self._init_board = np.zeros(shape=(6, 7), dtype=np.uint8)
    self.player = RED
    self.current_board = self._init_board
    self.winner = None
    self.online = online
    if self.online:
      self._write() # reset board file for serving

  # Public Interface
  '''
  Places the current turn's piece in a given column. Fails on a full column or
  index out of bounds.
  '''
  def place_piece(self, column):
    assert self.current_board[0][column] == EMPTY, "Column is full!"
    for row in range(5):
      # Got to the last row so simply place the piece
      if self.current_board[row+1][column] != EMPTY:
        self.current_board[row][column] = self.player
        break
    else:
      self.current_board[-1][column] = self.player
    # Alternate between RED and YELLOW
    self.player = (self.player % 2) + 1
    if self.online:
      self._write();

  '''
  Checks if either player has won. Returns True and sets the winner if so, False
  otherwise.
  '''
  def winner(self):
    for r in range(NUM_ROWS):
      for c in range(NUM_COLS):
        row_win = self._row_window(r, c)
        col_win = self._col_window(r, c)
        pos_diag_win = self._pos_diag_window(r, c)
        neg_diag_win = self._neg_diag_window(r, c)
        for window in (row_win, col_win, pos_diag_win, neg_diag_win):
          has_winner, winner = self._is_winning_window(window)
          if has_winner:
            self.winner = winner
            return True
    return False

  '''
  Returns the valid action set (i.e. the column indices which may have a new
  piece placed in them)
  '''
  def actions(self):
    return [
      col for col in range(NUM_COLS) if self.current_board[0, col] == EMPTY
    ]

  # Private Utilities
  '''
  Checks if a window of four pieces (vertical, horizontal, or diagonal) is a
  winning sequence. Returns True and the winner if so, False and None otherwise.
  '''
  def _is_winning_window(self, window):
    if window is None:
      return (False, None)
    # filter duplicates
    window = set(window)
    has_winner = (EMPTY not in window and len(window) == 1)
    winner = None
    if has_winner:
      winner = window.pop()
    return (has_winner, winner)

  '''
  Gets and returns a sequence of slots (left to right) along a row starting at
  the given column.
  '''
  def _row_window(self, row, col):
    if col > NUM_COLS - 4:
      return None
    return self._current_board[row, col:col+4]

  '''
  Gets and returns a sequence of slots (up to down) along a column starting at
  the given row.
  '''
  def _col_window(self, row, col):
    if row > NUM_ROWS - 4:
      return None
    return self._current_board[row:row+4, col]

  '''
  Gets and returns a sequence of slots (lower-left to upper-right) of a positive
  diagonal (i.e. one which looks like / ) starting at the given row and column.
  '''
  def _pos_diag_window(self, row, col):
    if row <= NUM_ROWS - 4 or col > NUM_COLS - 4:
      return None
    rows = tuple(range(row, row-4, -1))
    cols = tuple(range(col, col+4))
    return self._current_board[rows, cols]

  '''
  Gets and returns a sequence of slots (upper-left to lower-right) of a negative
  diagonal (i.e. one which looks like \ ) starting at the given row and column.
  '''
  def _neg_diag_window(self, row, col):
    if row > NUM_ROWS - 4 or col > NUM_COLS - 4:
      return None
    rows = tuple(range(row, row+4))
    cols = tuple(range(col, col+4))
    return self._current_board[rows, cols]

  '''
  Simple function for writing the board state to a file for serving
  '''
  def _write(self):
    with open('visualizer/output/board.txt', 'w') as f:
      f.write(self.__str__())

  # Python Dunders
  '''
  For printing the board
  '''
  def __str__(self):
    rep = []
    for row in self._current_board:
      row_rep = str(row).strip('[]')
      row_rep = row_rep.replace('0', '.').replace('1', 'R').replace('2', 'Y')
      rep.append(row_rep)
    return '\n'.join(rep)

  '''
  For printing the board interactively or from a collection context
  '''
  def __repr__(self):
    return self.__str__()
