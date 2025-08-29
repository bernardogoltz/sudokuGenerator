import random
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

class CrossSudokuGenerator:
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
    
    def generate_cross_puzzle(self, difficulty="medium"):
        # Generate center puzzle first
        self.grid = [[0]*9 for _ in range(9)]
        self.fill_grid()
        center_puzzle = [row[:] for row in self.grid]
        
        # Generate top puzzle (bottom 3 rows = center's top 3 rows)
        self.grid = [[0]*9 for _ in range(9)]
        # Set bottom 3 rows to match center's top 3 rows
        for i in range(3):
            for j in range(9):
                self.grid[i + 6][j] = center_puzzle[i][j]
        self.fill_grid()
        top_puzzle = [row[:] for row in self.grid]
        
        # Generate bottom puzzle (top 3 rows = center's bottom 3 rows)
        self.grid = [[0]*9 for _ in range(9)]
        for i in range(3):
            for j in range(9):
                self.grid[i][j] = center_puzzle[i + 6][j]
        self.fill_grid()
        bottom_puzzle = [row[:] for row in self.grid]
        
        # Generate left puzzle (right 3 columns = center's left 3 columns)
        self.grid = [[0]*9 for _ in range(9)]
        for i in range(9):
            for j in range(3):
                self.grid[i][j + 6] = center_puzzle[i][j]
        self.fill_grid()
        left_puzzle = [row[:] for row in self.grid]
        
        # Generate right puzzle (left 3 columns = center's right 3 columns)
        self.grid = [[0]*9 for _ in range(9)]
        for i in range(9):
            for j in range(3):
                self.grid[i][j] = center_puzzle[i][j + 6]
        self.fill_grid()
        right_puzzle = [row[:] for row in self.grid]
        
        puzzles = {
            'center': center_puzzle,
            'top': top_puzzle,
            'bottom': bottom_puzzle,
            'left': left_puzzle,
            'right': right_puzzle
        }
        
        # Remove numbers for difficulty
        difficulty_levels = {
            "easy": 35,
            "medium": 45,
            "hard": 55
        }
        remove_count = difficulty_levels.get(difficulty.lower(), 45)
        
        for puzzle in puzzles.values():
            cells = [(i, j) for i in range(9) for j in range(9)]
            random.shuffle(cells)
            for _ in range(remove_count):
                if cells:
                    row, col = cells.pop()
                    puzzle[row][col] = 0
        
        return puzzles

def draw_cross_combined_grid(c, puzzles, start_x, start_y):
    cell_size = 15  # Increased from 12 to 15
    
    # Create combined 21x21 grid
    combined = [[0]*21 for _ in range(21)]
    
    # Place center puzzle (6-14, 6-14)
    for i in range(9):
        for j in range(9):
            combined[i + 6][j + 6] = puzzles['center'][i][j]
    
    # Place top puzzle (0-5, 6-14)
    for i in range(6):
        for j in range(9):
            combined[i][j + 6] = puzzles['top'][i][j]
    
    # Place bottom puzzle (15-20, 6-14)
    for i in range(6):
        for j in range(9):
            combined[i + 15][j + 6] = puzzles['bottom'][i + 3][j]
    
    # Place left puzzle (6-14, 0-5)
    for i in range(9):
        for j in range(6):
            combined[i + 6][j] = puzzles['left'][i][j]
    
    # Place right puzzle (6-14, 15-20)
    for i in range(9):
        for j in range(6):
            combined[i + 6][j + 15] = puzzles['right'][i][j + 3]
    
    # Define cross areas
    def is_in_cross(row, col):
        vertical_part = 6 <= col <= 14 and 0 <= row <= 20
        horizontal_part = 6 <= row <= 14 and 0 <= col <= 20
        return vertical_part or horizontal_part
    
    # Draw all horizontal lines
    for i in range(22):
        if i > 21:
            continue
        line_width = 2 if i % 3 == 0 else 1
        c.setLineWidth(line_width)
        
        # Find horizontal extent for this row
        start_col = None
        end_col = None
        for j in range(22):
            if is_in_cross(i, j) or is_in_cross(i-1, j):
                if start_col is None:
                    start_col = j
                end_col = j
        
        if start_col is not None and end_col is not None:
            c.line(start_x + start_col * cell_size, start_y - i * cell_size,
                   start_x + (end_col + 1) * cell_size, start_y - i * cell_size)
    
    # Draw all vertical lines
    for j in range(22):
        if j > 21:
            continue
        line_width = 2 if j % 3 == 0 else 1
        c.setLineWidth(line_width)
        
        # Find vertical extent for this column
        start_row = None
        end_row = None
        for i in range(22):
            if is_in_cross(i, j) or is_in_cross(i, j-1):
                if start_row is None:
                    start_row = i
                end_row = i
        
        if start_row is not None and end_row is not None:
            c.line(start_x + j * cell_size, start_y - start_row * cell_size,
                   start_x + j * cell_size, start_y - (end_row + 1) * cell_size)
    
    # Fill numbers
    c.setFont("Helvetica", 10)  # Increased from 8 to 10
    for i in range(21):
        for j in range(21):
            if combined[i][j] != 0:
                if is_in_cross(i, j):
                    x = start_x + j * cell_size + cell_size/2 - 3
                    y = start_y - i * cell_size - cell_size/2 - 3
                    c.drawString(x, y, str(combined[i][j]))

def create_pdf_with_cross_sudoku(cross_puzzles, difficulty, filename):
    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter
    
    for puzzle_num in range(0, len(cross_puzzles), 2):  # Process 2 puzzles at a time
        if puzzle_num > 0:
            c.showPage()
        
        # Calculate positions for two puzzles vertically stacked with minimal margins
        cell_size = 15
        cross_width = 21 * cell_size
        cross_height = 21 * cell_size
        
        # Small margins
        top_margin = 30
        bottom_margin = 30
        
        # Calculate spacing to use remaining space efficiently
        available_height = height - top_margin - bottom_margin
        spacing = (available_height - 2 * cross_height) / 1  # Space between puzzles
        
        # Center horizontally
        start_x = (width - cross_width) / 2
        
        # First puzzle position (top)
        first_y = height - top_margin
        
        # Second puzzle position (bottom)
        second_y = first_y - cross_height - spacing
        
        # Draw first puzzle
        draw_cross_combined_grid(c, cross_puzzles[puzzle_num], start_x, first_y)
        
        # Draw second puzzle if it exists
        if puzzle_num + 1 < len(cross_puzzles):
            draw_cross_combined_grid(c, cross_puzzles[puzzle_num + 1], start_x, second_y)
    
    c.save()

def main():
    # CHANGE DIFFICULTY HERE: "easy", "medium", or "hard"
    DIFFICULTY = "hard"
    
    # CHANGE NUMBER OF PUZZLES TO GENERATE
    NUM_PUZZLES = 20
    
    generator = CrossSudokuGenerator()
    cross_puzzles = []
    
    print(f"Generating {NUM_PUZZLES} {DIFFICULTY} Cross Sudoku puzzles...")
    for i in range(NUM_PUZZLES):
        puzzles = generator.generate_cross_puzzle(DIFFICULTY)
        cross_puzzles.append(puzzles)
        print(f"Cross puzzle {i+1} generated")
    
    filename = f"{DIFFICULTY}_cross_sudoku_puzzles.pdf"
    print(f"Creating PDF: {filename}")
    
    create_pdf_with_cross_sudoku(cross_puzzles, DIFFICULTY, filename)
    
    import os
    if os.path.exists(filename):
        print(f"PDF created successfully: {filename}")
    else:
        print(f"Error: PDF file was not created")

if __name__ == "__main__":
    main()