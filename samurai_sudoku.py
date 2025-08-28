import random
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

class SamuraiSudokuGenerator:
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
    
    def generate_samurai_puzzles(self, difficulty="medium"):
        # Generate center puzzle first
        self.grid = [[0]*9 for _ in range(9)]
        self.fill_grid()
        center_complete = [row[:] for row in self.grid]
        
        # Extract the 4 corner 3x3 blocks from center
        corners = {
            'top_left': [[center_complete[i][j] for j in range(3)] for i in range(3)],
            'top_right': [[center_complete[i][j] for j in range(6,9)] for i in range(3)],
            'bottom_left': [[center_complete[i][j] for j in range(3)] for i in range(6,9)],
            'bottom_right': [[center_complete[i][j] for j in range(6,9)] for i in range(6,9)]
        }
        
        # Generate 4 outer puzzles using corners as constraints
        outer_puzzles = {}
        
        for corner_name, corner_block in corners.items():
            self.grid = [[0]*9 for _ in range(9)]
            
            # Place corner block in appropriate position
            if corner_name == 'top_left':
                pos = (6, 6)  # bottom-right of outer puzzle
            elif corner_name == 'top_right':
                pos = (6, 0)  # bottom-left of outer puzzle
            elif corner_name == 'bottom_left':
                pos = (0, 6)  # top-right of outer puzzle
            else:  # bottom_right
                pos = (0, 0)  # top-left of outer puzzle
            
            # Place the shared block
            for i in range(3):
                for j in range(3):
                    self.grid[pos[0] + i][pos[1] + j] = corner_block[i][j]
            
            self.fill_grid()
            outer_puzzles[corner_name] = [row[:] for row in self.grid]
        
        # Create puzzle versions by removing numbers
        center_puzzle = [row[:] for row in center_complete]
        
        difficulty_levels = {
            "easy": 35,
            "medium": 45,
            "hard": 55
        }
        remove_count = difficulty_levels.get(difficulty.lower(), 45)
        
        self.remove_numbers_from_grid(center_puzzle, remove_count)
        
        for corner_name in outer_puzzles:
            self.remove_numbers_from_grid(outer_puzzles[corner_name], remove_count)
        
        return center_puzzle, outer_puzzles

def draw_sudoku_grid(c, puzzle, start_x, start_y, title):
    cell_size = 20
    
    if title:
        c.setFont("Helvetica-Bold", 12)
        c.drawString(start_x, start_y + 25, title)
    
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

def create_pdf_with_samurai_sudoku(samurai_puzzles, difficulty, filename):
    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter
    
    for puzzle_num, (center, outers) in enumerate(samurai_puzzles):
        if puzzle_num > 0:
            c.showPage()
        
        c.setFont("Helvetica-Bold", 18)
        c.drawString(200, height - 30, "SAMURAI SUDOKU PUZZLE")
        
        c.setFont("Helvetica", 12)
        c.drawString(150, height - 50, f"{difficulty.upper()} PUZZLE {puzzle_num + 1}")
        
        c.setFont("Helvetica", 10)
        c.drawString(100, height - 70, "Complete each of the five overlapping grids so that each row, each column, and each")
        c.drawString(100, height - 82, "outlined 3x3 square contains the numbers 1-9 exactly one time each.")
        
        # Center puzzle position
        center_x, center_y = 250, height - 250
        
        # Draw center puzzle
        draw_sudoku_grid(c, center, center_x, center_y, "")
        
        # Calculate positions for outer puzzles to create overlaps
        # Top-left outer puzzle (shares top-left corner with center)
        tl_x = center_x - 6 * 20
        tl_y = center_y + 6 * 20
        draw_sudoku_grid(c, outers['top_left'], tl_x, tl_y, "")
        
        # Top-right outer puzzle (shares top-right corner with center)
        tr_x = center_x + 6 * 20
        tr_y = center_y + 6 * 20
        draw_sudoku_grid(c, outers['top_right'], tr_x, tr_y, "")
        
        # Bottom-left outer puzzle (shares bottom-left corner with center)
        bl_x = center_x - 6 * 20
        bl_y = center_y - 6 * 20
        draw_sudoku_grid(c, outers['bottom_left'], bl_x, bl_y, "")
        
        # Bottom-right outer puzzle (shares bottom-right corner with center)
        br_x = center_x + 6 * 20
        br_y = center_y - 6 * 20
        draw_sudoku_grid(c, outers['bottom_right'], br_x, br_y, "")
    
    c.save()

def main():
    # CHANGE DIFFICULTY HERE: "easy", "medium", or "hard"
    DIFFICULTY = "medium"
    
    generator = SamuraiSudokuGenerator()
    samurai_puzzles = []
    
    print(f"Generating {DIFFICULTY} Samurai Sudoku puzzles...")
    for i in range(2):  # Generate 2 samurai puzzles
        center, outers = generator.generate_samurai_puzzles(DIFFICULTY)
        samurai_puzzles.append((center, outers))
        print(f"Samurai puzzle {i+1} generated")
    
    filename = f"{DIFFICULTY}_samurai_sudoku_puzzles.pdf"
    create_pdf_with_samurai_sudoku(samurai_puzzles, DIFFICULTY, filename)
    print(f"PDF created: {filename}")

if __name__ == "__main__":
    main()