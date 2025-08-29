import random
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch

class SudokuGenerator:
    def __init__(self):
        self.size = 16
        self.grid = [[0]*self.size for _ in range(self.size)]
    
    def is_valid(self, row, col, num):
        # Check row
        for x in range(self.size):
            if self.grid[row][x] == num:
                return False
        
        # Check column
        for x in range(self.size):
            if self.grid[x][col] == num:
                return False
        
        # Check 4x4 box
        start_row, start_col = 4 * (row // 4), 4 * (col // 4)
        for i in range(4):
            for j in range(4):
                if self.grid[i + start_row][j + start_col] == num:
                    return False
        return True
    
    def fill_grid(self):
        for i in range(self.size):
            for j in range(self.size):
                if self.grid[i][j] == 0:
                    numbers = list(range(1, self.size + 1))
                    random.shuffle(numbers)
                    for num in numbers:
                        if self.is_valid(i, j, num):
                            self.grid[i][j] = num
                            if self.fill_grid():
                                return True
                            self.grid[i][j] = 0
                    return False
        return True
    
    def generate_puzzle(self, difficulty="medium"):
        print(f"Generating {self.size}x{self.size} Sudoku puzzle...")
        
        # Reset grid
        self.grid = [[0]*self.size for _ in range(self.size)]
        
        # Try to fill the grid
        if not self.fill_grid():
            print("Failed to generate valid puzzle")
            return [[0]*self.size for _ in range(self.size)]
        
        print(f"Successfully generated {self.size}x{self.size} complete grid")
        
        # Remove numbers for difficulty
        difficulty_levels = {
            "easy": 80,
            "medium": 110, 
            "hard": 140
        }
        remove_count = difficulty_levels.get(difficulty.lower(), 110)
        
        cells = [(i, j) for i in range(self.size) for j in range(self.size)]
        random.shuffle(cells)
        
        removed = 0
        for row, col in cells:
            if removed >= remove_count:
                break
            self.grid[row][col] = 0
            removed += 1
        
        print(f"Removed {removed} numbers. Final grid size: {len(self.grid)}x{len(self.grid[0])}")
        return [row[:] for row in self.grid]

def create_pdf_with_sudoku(puzzles, difficulty, puzzles_per_page, filename):
    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter
    
    # Fixed size is 16x16
    SIZE = 16
    
    # Calculate cell sizes for 16x16 grids
    if puzzles_per_page == 1:
        cell_size = 18
        positions = [((width - SIZE * cell_size) / 2, (height + SIZE * cell_size) / 2 - 100)]
    elif puzzles_per_page == 2:
        cell_size = 15
        grid_height = SIZE * cell_size
        spacing = 40
        start_y = height - 60
        positions = [
            ((width - SIZE * cell_size) / 2, start_y),
            ((width - SIZE * cell_size) / 2, start_y - grid_height - spacing)
        ]
    else:  # 3 or 4 puzzles per page
        cell_size = 12
        grid_width = SIZE * cell_size
        grid_height = SIZE * cell_size
        margin_x = (width - 2 * grid_width - 20) / 2
        margin_y = 30
        
        positions = [
            (margin_x, height - margin_y - grid_height),
            (margin_x + grid_width + 20, height - margin_y - grid_height),
            (margin_x, height - margin_y - 2 * grid_height - 20),
            (margin_x + grid_width + 20, height - margin_y - 2 * grid_height - 20)
        ]
    
    puzzle_count = 0
    for puzzle_num, puzzle in enumerate(puzzles):
        page_position = puzzle_count % puzzles_per_page
        
        if puzzle_count > 0 and page_position == 0:
            c.showPage()
        
        # Title
        if page_position == 0:
            c.setFont("Helvetica-Bold", 16)
            title = f"{difficulty.title()} {SIZE}x{SIZE} Sudoku"
            c.drawString(50, height - 50, title)
        
        start_x, start_y = positions[page_position]
        
        # Verify puzzle dimensions
        if len(puzzle) != SIZE or any(len(row) != SIZE for row in puzzle):
            print(f"ERROR: Puzzle has wrong dimensions: {len(puzzle)}x{len(puzzle[0]) if puzzle else 0}")
            continue
        
        # Draw 16x16 grid
        for i in range(SIZE + 1):
            line_width = 2 if i % 4 == 0 else 1
            c.setLineWidth(line_width)
            c.line(start_x, start_y - i * cell_size,
                   start_x + SIZE * cell_size, start_y - i * cell_size)
        
        for j in range(SIZE + 1):
            line_width = 2 if j % 4 == 0 else 1
            c.setLineWidth(line_width)
            c.line(start_x + j * cell_size, start_y,
                   start_x + j * cell_size, start_y - SIZE * cell_size)
        
        # Fill numbers
        font_size = max(6, min(10, cell_size - 2))
        c.setFont("Helvetica", font_size)
        
        for i in range(SIZE):
            for j in range(SIZE):
                if puzzle[i][j] != 0:
                    text = str(puzzle[i][j])
                    # Center text in cell
                    text_width = c.stringWidth(text)
                    x = start_x + j * cell_size + (cell_size - text_width) / 2
                    y = start_y - i * cell_size - cell_size/2 - font_size/3
                    c.drawString(x, y, text)
        
        puzzle_count += 1
    
    c.save()

def main():
    # CHANGE DIFFICULTY HERE: "easy", "medium", or "hard"
    DIFFICULTY = "hard"
    
    # CHANGE NUMBER OF PUZZLES TO GENERATE  
    NUM_PUZZLES = 2  # Start with 1 for testing
    
    # CHANGE PUZZLES PER PAGE (max 4)
    PUZZLES_PER_PAGE = 2
    
    generator = SudokuGenerator()
    puzzles = []
    
    print(f"Generating {NUM_PUZZLES} {DIFFICULTY} 16x16 Sudoku puzzles...")
    for i in range(NUM_PUZZLES):
        puzzle = generator.generate_puzzle(DIFFICULTY)
        puzzles.append(puzzle)
        print(f"Generated puzzle {i+1}: {len(puzzle)}x{len(puzzle[0]) if puzzle else 0}")
    
    filename = f"{DIFFICULTY}_16x16_sudoku_puzzles.pdf"
    create_pdf_with_sudoku(puzzles, DIFFICULTY, PUZZLES_PER_PAGE, filename)
    print(f"PDF created: {filename}")

if __name__ == "__main__":
    main()