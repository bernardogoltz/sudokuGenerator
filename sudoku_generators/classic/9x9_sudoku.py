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
    
    def generate_puzzle(self, difficulty="medium"):
        self.grid = [[0]*9 for _ in range(9)]
        self.fill_grid()
        
        # Set difficulty level
        difficulty_levels = {
            "easy": 35,
            "medium": 45,
            "hard": 55
        }
        remove_count = difficulty_levels.get(difficulty.lower(), 45)
        
        cells = [(i, j) for i in range(9) for j in range(9)]
        random.shuffle(cells)
        
        for _ in range(remove_count):
            if cells:
                row, col = cells.pop()
                self.grid[row][col] = 0
        
        return [row[:] for row in self.grid]

def create_pdf_with_sudoku(puzzles, difficulty, puzzles_per_page, filename):
    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter
    
    # Calculate cell size and positions based on puzzles per page
    if puzzles_per_page == 1:
        cell_size = 30
        positions = [((width - 9 * cell_size) / 2, (height + 9 * cell_size) / 2 - 100)]
    elif puzzles_per_page == 2:
        cell_size = 25
        grid_height = 9 * cell_size
        spacing = 80
        start_y = height - 100
        positions = [
            ((width - 9 * cell_size) / 2, start_y),
            ((width - 9 * cell_size) / 2, start_y - grid_height - spacing)
        ]
    elif puzzles_per_page == 3:
        cell_size = 20
        positions = [
            ((width - 9 * cell_size) / 2, height - 120),
            (80, height - 350),
            (width - 80 - 9 * cell_size, height - 350)
        ]
    else:  # 4 puzzles per page
        cell_size = 18
        grid_width = 9 * cell_size
        grid_height = 9 * cell_size
        margin_x = (width - 2 * grid_width - 40) / 2
        margin_y = 50
        
        positions = [
            (margin_x, height - margin_y - grid_height),
            (margin_x + grid_width + 40, height - margin_y - grid_height),
            (margin_x, height - margin_y - 2 * grid_height - 40),
            (margin_x + grid_width + 40, height - margin_y - 2 * grid_height - 40)
        ]
    
    puzzle_count = 0
    for puzzle_num, puzzle in enumerate(puzzles):
        page_position = puzzle_count % puzzles_per_page
        
        if puzzle_count > 0 and page_position == 0:
            c.showPage()
        
        # Title only on first puzzle of each page
        if page_position == 0:
            c.setFont("Helvetica-Bold", 16)
            title = f"{difficulty.title()} Sudoku Puzzles"
            if puzzles_per_page > 1:
                start_puzzle = puzzle_count + 1
                end_puzzle = min(puzzle_count + puzzles_per_page, len(puzzles))
                title += f" #{start_puzzle}-{end_puzzle}"
            else:
                title += f" #{puzzle_num + 1}"
            c.drawString(50, height - 50, title)
        
        start_x, start_y = positions[page_position]
        
        # Draw grid
        for i in range(10):
            line_width = 2 if i % 3 == 0 else 1
            c.setLineWidth(line_width)
            # Vertical lines
            c.line(start_x + i * cell_size, start_y, 
                   start_x + i * cell_size, start_y - 9 * cell_size)
            # Horizontal lines
            c.line(start_x, start_y - i * cell_size,
                   start_x + 9 * cell_size, start_y - i * cell_size)
        
        # Fill numbers
        font_size = max(8, min(14, cell_size - 4))
        c.setFont("Helvetica", font_size)
        offset = font_size / 3
        
        for i in range(9):
            for j in range(9):
                if puzzle[i][j] != 0:
                    x = start_x + j * cell_size + cell_size/2 - offset
                    y = start_y - i * cell_size - cell_size/2 - offset
                    c.drawString(x, y, str(puzzle[i][j]))
        
        puzzle_count += 1
    
    c.save()

def main():
    # CHANGE DIFFICULTY HERE: "easy", "medium", or "hard"
    DIFFICULTY = "hard"
    
    # CHANGE NUMBER OF PUZZLES TO GENERATE
    NUM_PUZZLES = 8
    
    # CHANGE PUZZLES PER PAGE (max 4)
    PUZZLES_PER_PAGE = min(4, max(1, 4))  # Change the middle number (1-4)
    
    generator = SudokuGenerator()
    puzzles = []
    
    print(f"Generating {NUM_PUZZLES} {DIFFICULTY} Sudoku puzzles...")
    for i in range(NUM_PUZZLES):
        puzzle = generator.generate_puzzle(DIFFICULTY)
        puzzles.append(puzzle)
        print(f"Puzzle {i+1} generated")
    
    filename = f"{DIFFICULTY}_9x9_sudoku_puzzles.pdf"
    create_pdf_with_sudoku(puzzles, DIFFICULTY, PUZZLES_PER_PAGE, filename)
    print(f"PDF created: {filename}")

if __name__ == "__main__":
    main()