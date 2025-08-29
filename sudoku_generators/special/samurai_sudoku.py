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
    cell_size = 15  # Increased from 12 to 15
    
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
    
    c.setFont("Helvetica", 10)  # Increased font size from 8 to 10
    for i in range(9):
        for j in range(9):
            if puzzle[i][j] != 0:
                x = start_x + j * cell_size + cell_size/2 - 3
                y = start_y - i * cell_size - cell_size/2 - 3
                c.drawString(x, y, str(puzzle[i][j]))

def create_pdf_with_samurai_sudoku(samurai_puzzles, difficulty, filename):
    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter
    
    for puzzle_num in range(0, len(samurai_puzzles), 2):  # Process 2 puzzles at a time
        if puzzle_num > 0:
            c.showPage()
        
        # Calculate positions more directly
        cell_size = 15
        
        # Each samurai puzzle needs about 21x21 cells of space (center + outer grids)
        total_puzzle_height = 21 * cell_size
        
        # Margins
        top_margin = 10
        bottom_margin = 50
        spacing = 20
        
        # Calculate available space and scale down if needed
        available_height = height - top_margin - bottom_margin
        max_puzzle_height = (available_height - spacing) / 2
        
        # If puzzles are too big, scale down
        if total_puzzle_height > max_puzzle_height:
            scale_factor = max_puzzle_height / total_puzzle_height
            cell_size = int(cell_size * scale_factor)
            total_puzzle_height = max_puzzle_height
        
        # Center horizontally
        puzzle_width = 21 * cell_size
        start_x = (width - puzzle_width) / 2
        
        # Position puzzles with exact spacing
        first_puzzle_center_y = height - top_margin - total_puzzle_height/2
        second_puzzle_center_y = height - top_margin - total_puzzle_height - spacing - total_puzzle_height/2
        
        # Draw first samurai puzzle
        center, outers = samurai_puzzles[puzzle_num]
        draw_samurai_puzzle(c, center, outers, start_x + puzzle_width/2 - 4.5*cell_size, first_puzzle_center_y, cell_size)
        
        # Draw second samurai puzzle if it exists
        if puzzle_num + 1 < len(samurai_puzzles):
            center2, outers2 = samurai_puzzles[puzzle_num + 1]
            draw_samurai_puzzle(c, center2, outers2, start_x + puzzle_width/2 - 4.5*cell_size, second_puzzle_center_y, cell_size)
    
    c.save()

def draw_samurai_puzzle(c, center, outers, center_x, center_y, cell_size):
    # Draw center puzzle
    draw_sudoku_grid(c, center, center_x, center_y, "")
    
    # Calculate positions for outer puzzles to create overlaps
    # Top-left outer puzzle
    tl_x = center_x - 6 * cell_size
    tl_y = center_y + 6 * cell_size
    draw_sudoku_grid(c, outers['top_left'], tl_x, tl_y, "")
    
    # Top-right outer puzzle
    tr_x = center_x + 6 * cell_size
    tr_y = center_y + 6 * cell_size
    draw_sudoku_grid(c, outers['top_right'], tr_x, tr_y, "")
    
    # Bottom-left outer puzzle
    bl_x = center_x - 6 * cell_size
    bl_y = center_y - 6 * cell_size
    draw_sudoku_grid(c, outers['bottom_left'], bl_x, bl_y, "")
    
    # Bottom-right outer puzzle
    br_x = center_x + 6 * cell_size
    br_y = center_y - 6 * cell_size
    draw_sudoku_grid(c, outers['bottom_right'], br_x, br_y, "")

def main():
    # CHANGE DIFFICULTY HERE: "easy", "medium", or "hard"
    DIFFICULTY = "hard"
    
    # CHANGE NUMBER OF PUZZLES TO GENERATE
    NUM_PUZZLES = 20
    
    generator = SamuraiSudokuGenerator()
    samurai_puzzles = []
    
    print(f"Generating {NUM_PUZZLES} {DIFFICULTY} Samurai Sudoku puzzles...")
    for i in range(NUM_PUZZLES):
        center, outers = generator.generate_samurai_puzzles(DIFFICULTY)
        samurai_puzzles.append((center, outers))
        print(f"Samurai puzzle {i+1} generated")
    
    filename = f"{DIFFICULTY}_samurai_sudoku_puzzles.pdf"
    create_pdf_with_samurai_sudoku(samurai_puzzles, DIFFICULTY, filename)
    print(f"PDF created: {filename} with {NUM_PUZZLES} puzzles")

if __name__ == "__main__":
    main()