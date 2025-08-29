import random
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

class SoheiSudokuGenerator:
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
    
    def generate_sohei_puzzle(self, difficulty="medium"):
        # Generate 4 complete independent puzzles first
        puzzles = []
        for _ in range(4):
            self.grid = [[0]*9 for _ in range(9)]
            self.fill_grid()
            puzzles.append([row[:] for row in self.grid])
        
        top_puzzle, right_puzzle, left_puzzle, bottom_puzzle = puzzles
        
        # Force shared overlaps by copying blocks
        # Top shares bottom-right with right's top-left
        shared_tr = [[top_puzzle[i][j] for j in range(6, 9)] for i in range(6, 9)]
        for i in range(3):
            for j in range(3):
                right_puzzle[i][j] = shared_tr[i][j]
        
        # Top shares bottom-left with left's top-right  
        shared_tl = [[top_puzzle[i][j] for j in range(0, 3)] for i in range(6, 9)]
        for i in range(3):
            for j in range(3):
                left_puzzle[i][j + 6] = shared_tl[i][j]
        
        # Right shares bottom-left with bottom's top-right
        shared_rb = [[right_puzzle[i][j] for j in range(0, 3)] for i in range(6, 9)]
        for i in range(3):
            for j in range(3):
                bottom_puzzle[i][j + 6] = shared_rb[i][j]
        
        # Left shares bottom-right with bottom's top-left
        shared_lb = [[left_puzzle[i][j] for j in range(6, 9)] for i in range(6, 9)]
        for i in range(3):
            for j in range(3):
                bottom_puzzle[i][j] = shared_lb[i][j]
        
        # Create cross-shaped combined grid
        puzzles = {
            'top': top_puzzle,
            'right': right_puzzle,
            'left': left_puzzle, 
            'bottom': bottom_puzzle
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

def draw_single_sudoku(c, puzzle, start_x, start_y, cell_size):
    # Draw grid lines
    for i in range(10):
        line_width = 2 if i % 3 == 0 else 1
        c.setLineWidth(line_width)
        c.line(start_x + i * cell_size, start_y, 
               start_x + i * cell_size, start_y - 9 * cell_size)
        c.line(start_x, start_y - i * cell_size,
               start_x + 9 * cell_size, start_y - i * cell_size)
    
    # Fill numbers
    c.setFont("Helvetica", 8)  # Reduced font size for two per page
    for i in range(9):
        for j in range(9):
            if puzzle[i][j] != 0:
                x = start_x + j * cell_size + cell_size/2 - 2
                y = start_y - i * cell_size - cell_size/2 - 2
                c.drawString(x, y, str(puzzle[i][j]))

def draw_sohei_cross(c, puzzles, start_x, start_y, cell_size):
    # Calculate positions for cross layout
    # Top puzzle position
    top_x = start_x + 6 * cell_size
    top_y = start_y
    
    # Left puzzle position  
    left_x = start_x
    left_y = start_y - 6 * cell_size
    
    # Right puzzle position
    right_x = start_x + 12 * cell_size  
    right_y = start_y - 6 * cell_size
    
    # Bottom puzzle position
    bottom_x = start_x + 6 * cell_size
    bottom_y = start_y - 12 * cell_size
    
    # Draw each puzzle
    draw_single_sudoku(c, puzzles['top'], top_x, top_y, cell_size)
    draw_single_sudoku(c, puzzles['left'], left_x, left_y, cell_size)
    draw_single_sudoku(c, puzzles['right'], right_x, right_y, cell_size)
    draw_single_sudoku(c, puzzles['bottom'], bottom_x, bottom_y, cell_size)

def create_pdf_with_sohei_sudoku(sohei_puzzles, difficulty, filename):
    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter
    
    for puzzle_num in range(0, len(sohei_puzzles), 2):  # Process 2 puzzles at a time
        if puzzle_num > 0:
            c.showPage()
        
        # Calculate positions for two sohei puzzles vertically stacked
        cell_size = 16
        
        # Each sohei puzzle needs about 18x18 cells of space (cross formation)
        total_puzzle_height = 18 * cell_size
        
        # Margins
        top_margin = 30
        bottom_margin = 20
        spacing = 80
        
        # Calculate available space and scale down if needed
        available_height = height - top_margin - bottom_margin
        max_puzzle_height = (available_height - spacing) / 2
        
        # If puzzles are too big, scale down
        if total_puzzle_height > max_puzzle_height:
            scale_factor = max_puzzle_height / total_puzzle_height
            cell_size = int(cell_size * scale_factor)
            total_puzzle_height = max_puzzle_height
        
        # Center horizontally
        puzzle_width = 18 * cell_size
        start_x = (width - puzzle_width) / 2
        
        # Position puzzles with exact spacing
        first_puzzle_start_y = height - top_margin
        second_puzzle_start_y = height - top_margin - total_puzzle_height - spacing
        
        # Draw first sohei puzzle
        puzzles = sohei_puzzles[puzzle_num]
        draw_sohei_cross(c, puzzles, start_x, first_puzzle_start_y, cell_size)
        
        # Draw second sohei puzzle if it exists
        if puzzle_num + 1 < len(sohei_puzzles):
            puzzles2 = sohei_puzzles[puzzle_num + 1]
            draw_sohei_cross(c, puzzles2, start_x, second_puzzle_start_y, cell_size)
    
    c.save()

def main():
    # CHANGE DIFFICULTY HERE: "easy", "medium", or "hard"
    DIFFICULTY = "medium"
    
    # CHANGE NUMBER OF PUZZLES TO GENERATE
    NUM_PUZZLES = 12
    
    generator = SoheiSudokuGenerator()
    sohei_puzzles = []
    
    print(f"Generating {NUM_PUZZLES} {DIFFICULTY} Sohei Sudoku puzzles...")
    for i in range(NUM_PUZZLES):
        puzzles = generator.generate_sohei_puzzle(DIFFICULTY)
        sohei_puzzles.append(puzzles)
        print(f"Sohei puzzle {i+1} generated")
    
    filename = f"{DIFFICULTY}_sohei_sudoku_puzzles.pdf"
    print(f"Creating PDF: {filename}")
    
    create_pdf_with_sohei_sudoku(sohei_puzzles, DIFFICULTY, filename)
    
    import os
    if os.path.exists(filename):
        print(f"PDF created successfully: {filename} with {NUM_PUZZLES} puzzles")
    else:
        print(f"Error: PDF file was not created")

if __name__ == "__main__":
    main()