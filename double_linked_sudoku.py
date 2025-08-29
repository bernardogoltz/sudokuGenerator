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
    cell_size = 16  # Reduced from 20 to fit two pairs per page
    
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
    
    c.setFont("Helvetica", 9)  # Reduced font size from 10 to 9
    for i in range(9):
        for j in range(9):
            if puzzle[i][j] != 0:
                x = start_x + j * cell_size + cell_size/2 - 3
                y = start_y - i * cell_size - cell_size/2 - 3
                c.drawString(x, y, str(puzzle[i][j]))

def create_pdf_with_linked_sudoku(puzzle_pairs, difficulty, filename):
    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter
    
    for pair_num in range(0, len(puzzle_pairs), 2):  # Process 2 pairs at a time
        if pair_num > 0:
            c.showPage()
        
        # Calculate positions for two linked puzzle pairs vertically stacked
        cell_size = 16
        overlap_width = 6 * cell_size  # Width of overlap
        overlap_height = 6 * cell_size  # Height of overlap
        
        # Small margins
        top_margin = 50
        bottom_margin = 50
        
        # Calculate total height needed for one linked pair
        pair_height = 9 * cell_size + overlap_height
        
        # Calculate spacing
        available_height = height - top_margin - bottom_margin
        spacing = (available_height - 2 * pair_height) / 1
        
        # Center horizontally
        pair_width = 9 * cell_size + overlap_width
        start_x = (width - pair_width) / 2
        
        # First pair position (top)
        first_y = height - top_margin
        
        # Second pair position (bottom)
        second_y = first_y - pair_height - spacing
        
        # Draw first linked pair
        puzzle1, puzzle2 = puzzle_pairs[pair_num]
        
        # First puzzle of first pair
        draw_sudoku_grid(c, puzzle1, start_x, first_y, "")
        
        # Second puzzle overlapping with first puzzle
        overlap_x = start_x + overlap_width
        overlap_y = first_y - overlap_height
        draw_sudoku_grid(c, puzzle2, overlap_x, overlap_y, "")
        
        # Draw second linked pair if it exists
        if pair_num + 1 < len(puzzle_pairs):
            puzzle3, puzzle4 = puzzle_pairs[pair_num + 1]
            
            # First puzzle of second pair
            draw_sudoku_grid(c, puzzle3, start_x, second_y, "")
            
            # Second puzzle overlapping with first puzzle
            overlap_x2 = start_x + overlap_width
            overlap_y2 = second_y - overlap_height
            draw_sudoku_grid(c, puzzle4, overlap_x2, overlap_y2, "")
    
    c.save()

def main():
    # CHANGE DIFFICULTY HERE: "easy", "medium", or "hard"
    DIFFICULTY = "hard"
    
    # CHANGE NUMBER OF PUZZLE PAIRS TO GENERATE
    NUM_PUZZLE_PAIRS = 12
    
    generator = SudokuGenerator()
    puzzle_pairs = []
    
    print(f"Generating {NUM_PUZZLE_PAIRS} {DIFFICULTY} linked Sudoku puzzle pairs...")
    for i in range(NUM_PUZZLE_PAIRS):
        puzzle1, puzzle2 = generator.generate_linked_puzzles(DIFFICULTY)
        puzzle_pairs.append((puzzle1, puzzle2))
        print(f"Linked pair {i+1} generated")
    
    filename = f"{DIFFICULTY}_linked_sudoku_puzzles.pdf"
    create_pdf_with_linked_sudoku(puzzle_pairs, DIFFICULTY, filename)
    print(f"PDF created: {filename} with {NUM_PUZZLE_PAIRS} linked puzzle pairs")

if __name__ == "__main__":
    main()