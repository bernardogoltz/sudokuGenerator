import random
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch

class SudokuGenerator:
    def __init__(self):
        self.grid = [[0]*12 for _ in range(12)]
    
    def is_valid(self, row, col, num):
        for x in range(12):
            if self.grid[row][x] == num or self.grid[x][col] == num:
                return False
        
        # Use 4x3 boxes for 12x12 sudoku (4 cols, 3 rows)
        start_row, start_col = 3 * (row // 3), 4 * (col // 4)
        for i in range(3):
            for j in range(4):
                if self.grid[i + start_row][j + start_col] == num:
                    return False
        return True
    
    def fill_grid(self):
        for i in range(12):
            for j in range(12):
                if self.grid[i][j] == 0:
                    numbers = list(range(1, 13))
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
        self.grid = [[0]*12 for _ in range(12)]
        self.fill_grid()
        
        # Set difficulty level (more cells to remove for 12x12)
        difficulty_levels = {
            "easy": 60,
            "medium": 80,
            "hard": 100
        }
        remove_count = difficulty_levels.get(difficulty.lower(), 80)
        
        cells = [(i, j) for i in range(12) for j in range(12)]
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
        cell_size = 24
        positions = [((width - 12 * cell_size) / 2, (height + 12 * cell_size) / 2 - 100)]
    elif puzzles_per_page == 2:
        cell_size = 20
        grid_height = 12 * cell_size
        spacing = 60
        start_y = height - 80
        positions = [
            ((width - 12 * cell_size) / 2, start_y),
            ((width - 12 * cell_size) / 2, start_y - grid_height - spacing)
        ]
    elif puzzles_per_page == 3:
        cell_size = 16
        positions = [
            ((width - 12 * cell_size) / 2, height - 100),
            (60, height - 320),
            (width - 60 - 12 * cell_size, height - 320)
        ]
    else:  # 4 puzzles per page
        cell_size = 14
        grid_width = 12 * cell_size
        grid_height = 12 * cell_size
        margin_x = (width - 2 * grid_width - 30) / 2
        margin_y = 40
        
        positions = [
            (margin_x, height - margin_y - grid_height),
            (margin_x + grid_width + 30, height - margin_y - grid_height),
            (margin_x, height - margin_y - 2 * grid_height - 30),
            (margin_x + grid_width + 30, height - margin_y - 2 * grid_height - 30)
        ]
    
    puzzle_count = 0
    for puzzle_num, puzzle in enumerate(puzzles):
        page_position = puzzle_count % puzzles_per_page
        
        if puzzle_count > 0 and page_position == 0:
            c.showPage()
        
        # Title only on first puzzle of each page
        if page_position == 0:
            c.setFont("Helvetica-Bold", 16)
            title = f"{difficulty.title()} 12x12 Sudoku Puzzles"
            if puzzles_per_page > 1:
                start_puzzle = puzzle_count + 1
                end_puzzle = min(puzzle_count + puzzles_per_page, len(puzzles))
                title += f" #{start_puzzle}-{end_puzzle}"
            else:
                title += f" #{puzzle_num + 1}"
            c.drawString(50, height - 50, title)
        
        start_x, start_y = positions[page_position]
        
        # Draw grid (12x12 with 3x3 boxes)
        for i in range(13):
            line_width = 2 if i % 3 == 0 else 1
            c.setLineWidth(line_width)
            # Horizontal lines
            c.line(start_x, start_y - i * cell_size,
                   start_x + 12 * cell_size, start_y - i * cell_size)
        
        for j in range(13):
            line_width = 2 if j % 4 == 0 else 1
            c.setLineWidth(line_width)
            # Vertical lines
            c.line(start_x + j * cell_size, start_y,
                   start_x + j * cell_size, start_y - 12 * cell_size)
        
        # Fill numbers
        font_size = max(6, min(12, cell_size - 2))
        c.setFont("Helvetica", font_size)
        offset = font_size / 3
        
        for i in range(12):
            for j in range(12):
                if puzzle[i][j] != 0:
                    # Handle double digits
                    text = str(puzzle[i][j])
                    if len(text) == 2:
                        x = start_x + j * cell_size + cell_size/2 - offset * 1.5
                    else:
                        x = start_x + j * cell_size + cell_size/2 - offset
                    y = start_y - i * cell_size - cell_size/2 - offset
                    c.drawString(x, y, text)
        
        puzzle_count += 1
    
    c.save()

def main():
    # CHANGE DIFFICULTY HERE: "easy", "medium", or "hard"
    DIFFICULTY = "medium"
    
    # CHANGE NUMBER OF PUZZLES TO GENERATE
    NUM_PUZZLES = 8
    
    # CHANGE PUZZLES PER PAGE (max 4)
    PUZZLES_PER_PAGE = min(4, max(1, 2))  # Change the middle number (1-4)
    
    generator = SudokuGenerator()
    puzzles = []
    
    print(f"Generating {NUM_PUZZLES} {DIFFICULTY} Sudoku puzzles...")
    for i in range(NUM_PUZZLES):
        puzzle = generator.generate_puzzle(DIFFICULTY)
        puzzles.append(puzzle)
        print(f"Puzzle {i+1} generated")
    
    filename = f"{DIFFICULTY}_12x12_sudoku_puzzles.pdf"
    create_pdf_with_sudoku(puzzles, DIFFICULTY, PUZZLES_PER_PAGE, filename)
    print(f"PDF created: {filename}")

if __name__ == "__main__":
    main()