import itertools
import random
import copy


class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        if len(self.cells) == self.count:
            return set(self.cells)
        return set()

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        if self.count == 0:
            return set(self.cells)
        return set()

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        if cell in self.cells:
            self.cells.remove(cell)
            self.count -= 1
            return None

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        if cell in self.cells:
            self.cells.remove(cell)
            return None

class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)


    def neighboring_cells(self, cell):
        """
        Returns all neighboring cells for any cell.
        """
        mines = 0
        i, j = cell
        neighbors = set()
        for row in range(i-1, i+2):
            for col in range(j-1, j+2):
                if ((row >= 0 and row < self.height)
                                and (col >= 0 and col < self.width)
                                and ((row, col) != cell)
                                and ((row, col) not in self.moves_made)):
                    if (row, col) in self.mines:
                        mines += 1
                    elif (row, col) in self.safes:
                        continue
                    else:
                        neighbors.add((row, col))
        return neighbors, mines


    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.
        """
        self.moves_made.add(cell)
        self.safes.add(cell)

        neighbors = self.neighboring_cells(cell)[0]
        detected_mines = self.neighboring_cells(cell)[1]
        count -= detected_mines

        new_sentence = Sentence(neighbors, count)
        if new_sentence not in self.knowledge:
            self.knowledge.append(new_sentence)
        
        # Update knowledge base by interating over sentences.
        for sentence in self.knowledge:
            known_safes = sentence.known_safes()
            for known_safe in known_safes:
                self.mark_safe(known_safe)
        
            known_mines = sentence.known_mines()
            for known_mine in known_mines:
                self.mark_mine(known_mine)
        
        known_sentences = copy.deepcopy(self.knowledge)

        for sentence1 in known_sentences:
            known_sentences.remove(sentence1)
            for sentence2 in known_sentences:
                if (len(sentence2.cells) < len(sentence1.cells)
                                and len(sentence1.cells) != 0
                                and len(sentence2.cells) != 0):
                    subset = sentence2.cells
                    bigset = sentence1.cells
                    diff_count = sentence1.count - sentence2.count
                elif len(sentence1.cells) == len(sentence2.cells):
                    continue
                if (len(sentence2.cells) > len(sentence1.cells)
                                and len(sentence1.cells) != 0
                                and len(sentence2.cells) != 0):
                    subset = sentence1.cells
                    bigset = sentence2.cells
                    diff_count = sentence2.count - sentence1.count
                else:
                    continue

                if subset <= bigset:
                    diff_set = bigset - subset
                    if len(diff_set) == 1:
                        # check if known mine or safe
                        if diff_count == 0:
                            # add to known safe cells
                            new_safe = diff_set.pop()
                            self.mark_safe(new_safe)
                        elif diff_count == 1:
                            # add to known mines
                            new_mine = diff_set.pop()
                            self.mark_mine(new_mine)
                    else:
                        # add new subset knowledge to KB
                        self.knowledge.append(Sentence(diff_set, diff_count))


    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.
        """
        for move in self.safes:
            if move in self.moves_made:
                continue
            else:
                safe_move = move   
                self.moves_made.add(safe_move)
                return safe_move

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
        """
        potential_moves = []
        board = []

        for row in range(0, self.height):
            for column in range(0, self.width):
                board.append((row, column))
        for move in board:
            if move not in self.moves_made and move not in self.mines:
                potential_moves.append(move)
        if len(potential_moves) == 0:
            print(f'Game finished! Start new game.')
        else:
            random_move = random.choice(potential_moves)
            self.moves_made.add(random_move)
            return random_move
