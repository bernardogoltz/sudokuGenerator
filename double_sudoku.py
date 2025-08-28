import random
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch

class SudokuGenerator:
    def __init__(self):
        self.grid = [[0]*9 for _ in range(9)]
    
    def is_valid(self, row, col, num):
        for x in range(9):
            if self.grid[row][x] == num or self.grid[x][col] == num:
                return False
        
        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(3):
            for j in range(3):
                if self.grid[i + start_row][j + start_col] == num:
                    return False
        return True
    
    def fill_grid(self):
        for i in range(9):
            for j in range(9):
                if self.grid[i][j] == 0:
                    numbers = list(range(1, 10))
                    random.shuffle(numbers)
                    for num in numbers:
                        if self.is_valid(i, j, num):
                            self.grid[i][j] = num
                            if self.fill_grid():
                                return True
                            self.grid[i][j] = 0
                    return False
        return True
    
    def remove_numbers_from_grid(self, grid, difficulty):
        cells = [(i, j) for i in range(9) for j in range(9)]
        random.shuffle(cells)
        
        for _ in range(difficulty):
            if cells:
                row, col = cells.pop()
                grid[row][col] = 0
    
    def generate_linked_puzzles(self, difficulty="medium"):
        # Generate first complete puzzle
        self.grid = [[0]*9 for _ in range(9)]
        self.fill_grid()
        first_complete = [row[:] for row in self.grid]
        
        # Extract bottom-right 3x3 from first puzzle
        shared_block = []
        for i in range(6, 9):
            row = []
            for j in range(6, 9):
                row.append(first_complete[i][j])
            shared_block.append(row)
        
        # Create second puzzle with shared block as top-left
        self.grid = [[0]*9 for _ in range(9)]
        for i in range(3):
            for j in range(3):
                self.grid[i][j] = shared_block[i][j]
        
        self.fill_grid()
        second_complete = [row[:] for row in self.grid]
        
        # Create puzzle versions by removing numbers
        first_puzzle = [row[:] for row in first_complete]
        second_puzzle = [row[:] for row in second_complete]
        
        # Set difficulty level
        difficulty_levels = {
            "easy": 35,
            "medium": 45,
            "hard": 55
        }
        remove_count = difficulty_levels.get(difficulty.lower(), 45)
        
        self.remove_numbers_from_grid(first_puzzle, remove_count)
        self.remove_numbers_from_grid(second_puzzle, remove_count)
        
        return first_puzzle, second_puzzle

def draw_sudoku_grid(c, puzzle, start_x, start_y, title):
    cell_size = 20
    
    if title:
        c.setFont("Helvetica-Bold", 12)
        c.drawString(start_x, start_y + 20, title)
    
    for i in range(10):
        line_width = 2 if i % 3 == 0 else 1
        c.setLineWidth(line_width)
        c.line(start_x + i * cell_size, start_y, 
               start_x + i * cell_size, start_y - 9 * cell_size)
        c.line(start_x, start_y - i * cell_size,
               start_x + 9 * cell_size, start_y - i * cell_size)
    
    c.setFont("Helvetica", 10)
    for i in range(9):
        for j in range(9):
            if puzzle[i][j] != 0:
                x = start_x + j * cell_size + cell_size/2 - 3
                y = start_y - i * cell_size - cell_size/2 - 3
                c.drawString(x, y, str(puzzle[i][j]))

def create_pdf_with_linked_sudoku(puzzle_pairs, difficulty, filename):
    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter
    
    for pair_num, (puzzle1, puzzle2) in enumerate(puzzle_pairs):
        if pair_num > 0:
            c.showPage()
        
        c.setFont("Helvetica-Bold", 16)
        c.drawString(50, height - 30, f"{difficulty.title()} Linked Sudoku Puzzles #{pair_num + 1}")
        
        c.setFont("Helvetica", 10)
        c.drawString(50, height - 45, "The puzzles share a 3x3 block (overlapping area)")
        
        # Draw first puzzle (top-left position)
        draw_sudoku_grid(c, puzzle1, 100, height - 100, "")
        
        # Draw second puzzle overlapping: position it so the top-left of puzzle2 
        # overlaps with bottom-right of puzzle1
        overlap_x = 100 + 6 * 20  # start_x + 6 cells
        overlap_y = height - 100 - 6 * 20  # start_y - 6 cells
        draw_sudoku_grid(c, puzzle2, overlap_x, overlap_y, "")
    
    c.save()

def main():
    # CHANGE DIFFICULTY HERE: "easy", "medium", or "hard"
    DIFFICULTY = "medium"
    
    generator = SudokuGenerator()
    puzzle_pairs = []
    
    print(f"Generating {DIFFICULTY} linked Sudoku puzzles...")
    for i in range(3):
        puzzle1, puzzle2 = generator.generate_linked_puzzles(DIFFICULTY)
        puzzle_pairs.append((puzzle1, puzzle2))
        print(f"Linked pair {i+1} generated")
    
    filename = f"{DIFFICULTY}_linked_sudoku_puzzles.pdf"
    create_pdf_with_linked_sudoku(puzzle_pairs, DIFFICULTY, filename)
    print(f"PDF created: {filename}")

if __name__ == "__main__":
    main()