import streamlit as st
import sys
import os
import io
import tempfile
from pathlib import Path

# Add sudoku_generators to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'sudoku_generators'))

# Import sudoku generators (using importlib for dynamic imports due to filename issues)
import importlib.util

def load_module_from_path(module_name, file_path):
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

# Load modules dynamically
sudoku_9x9_module = load_module_from_path("sudoku_9x9", "sudoku_generators/classic/9x9_sudoku.py")
sudoku_12x12_module = load_module_from_path("sudoku_12x12", "sudoku_generators/classic/12x12_sudoku.py")
sudoku_16x16_module = load_module_from_path("sudoku_16x16", "sudoku_generators/classic/16x16_sudoku.py")
cross_sudoku_module = load_module_from_path("cross_sudoku", "sudoku_generators/special/cross_sudoku.py")
samurai_sudoku_module = load_module_from_path("samurai_sudoku", "sudoku_generators/special/samurai_sudoku.py")

Sudoku9x9 = sudoku_9x9_module.SudokuGenerator
Sudoku12x12 = sudoku_12x12_module.SudokuGenerator
Sudoku16x16 = sudoku_16x16_module.SudokuGenerator
CrossSudokuGenerator = cross_sudoku_module.CrossSudokuGenerator
SamuraiSudokuGenerator = samurai_sudoku_module.SamuraiSudokuGenerator

    # Configure page
st.set_page_config(
    page_title="Gerador de Sudoku",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS - Minimal White Theme with Black Text
st.markdown("""
<style>
    .stApp {
        background-color: white;
        color: black;
    }
    .main-header {
        text-align: center;
        color: black !important;
        font-size: 2rem;
        font-weight: 300;
        margin-bottom: 1rem;
        border-bottom: 1px solid #eeeeee;
        padding-bottom: 1rem;
    }
    .stButton > button {
        background-color: #333333;
        color: white !important;
        border: none;
        border-radius: 4px;
        padding: 0.5rem 1.5rem;
        font-weight: 400;
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        background-color: #555555;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        color: white !important;
    }
    /* Download button specific styling */
    .stDownloadButton > button {
        background-color: #333333 !important;
        color: white !important;
        border: none !important;
        border-radius: 4px !important;
        padding: 0.5rem 1.5rem !important;
        font-weight: 400 !important;
        transition: all 0.3s ease !important;
    }
    .stDownloadButton > button:hover {
        background-color: #555555 !important;
        color: white !important;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1) !important;
    }
    .stSelectbox > div > div {
        background-color: white;
        border: 1px solid #dddddd;
        color: black !important;
    }
    .stSelectbox label {
        color: black !important;
    }
    .stNumberInput > div > div > input {
        background-color: white;
        border: 1px solid #dddddd;
        color: black !important;
    }
    .stNumberInput label {
        color: black !important;
    }
    .stSidebar {
        background-color: #fafafa;
        border-right: 1px solid #eeeeee;
    }


    /* Force all text to be black */
    .stMarkdown, .stMarkdown p, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3, .stMarkdown h4, .stMarkdown h5, .stMarkdown h6 {
        color: black !important;
    }
    .stSuccess {
        color: black !important;
    }
    .stError {
        color: black !important;
    }
    .stWarning {
        color: black !important;
    }
    .stInfo {
        color: black !important;
    }
    /* Tabs text */
    .stTabs [data-baseweb="tab-list"] {
        color: black !important;
    }
    .stTabs [data-baseweb="tab"] {
        color: black !important;
    }

    /* Spinner text */
    .stSpinner > div {
        color: black !important;
    }
    /* Success/Error messages text */
    .stAlert {
        color: black !important;
    }
    .stAlert > div {
        color: black !important;
    }
</style>
""", unsafe_allow_html=True)

# Display function removed - no preview needed

def create_pdf_download(puzzles, sudoku_type, difficulty):
    """Create PDF for download"""
    import tempfile
    
    try:
        if sudoku_type == "Clássico 9x9":
            # Use the loaded module
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
                filename = tmp_file.name
                sudoku_9x9_module.create_pdf_with_sudoku(puzzles, difficulty, 1, filename)
                return filename
        
        elif sudoku_type == "Clássico 12x12":
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
                filename = tmp_file.name
                sudoku_12x12_module.create_pdf_with_sudoku(puzzles, difficulty, 1, filename)
                return filename
        
        elif sudoku_type == "Cross Sudoku":
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
                filename = tmp_file.name
                cross_sudoku_module.create_pdf_with_cross_sudoku(puzzles, difficulty, filename)
                return filename
        
        elif sudoku_type == "Samurai Sudoku":
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
                filename = tmp_file.name
                samurai_sudoku_module.create_pdf_with_samurai_sudoku(puzzles, difficulty, filename)
                return filename
        
    except Exception as e:
        print(f"Error creating PDF: {e}")
        return None
    
    return None

def main():
    # Header
    st.markdown('<h1 class="main-header">Gerador de Sudoku</h1>', unsafe_allow_html=True)
    
    # Minimal layout - single column with controls at top
    st.markdown("### Configurações")
    
    # Controls in columns
    col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
    
    with col1:
        sudoku_type = st.selectbox(
            "Tipo de Sudoku",
            ["Clássico 9x9", "Clássico 12x12", "Clássico 16x16", "Cross Sudoku", "Samurai Sudoku"],
            label_visibility="collapsed",
            placeholder="Selecione o tipo de sudoku"
        )
    
    with col2:
        difficulty = st.selectbox(
            "Dificuldade",
            ["easy", "medium", "hard"],
            index=1,
            label_visibility="collapsed"
        )
    
    with col3:
        num_puzzles = st.number_input(
            "Número",
            min_value=1,
            max_value=10,
            value=1,
            label_visibility="collapsed"
        )
    
    with col4:
        generate_button = st.button("Gerar", use_container_width=True)
    
    # Main content area
    if generate_button:
        with st.spinner("Gerando sudoku..."):
            try:
                puzzles = []
                
                if sudoku_type == "Clássico 9x9":
                    generator = Sudoku9x9()
                    for i in range(num_puzzles):
                        puzzle = generator.generate_puzzle(difficulty)
                        puzzles.append(puzzle)
                
                elif sudoku_type == "Clássico 12x12":
                    generator = Sudoku12x12()
                    for i in range(num_puzzles):
                        puzzle = generator.generate_puzzle(difficulty)
                        puzzles.append(puzzle)
                
                elif sudoku_type == "Cross Sudoku":
                    generator = CrossSudokuGenerator()
                    for i in range(num_puzzles):
                        puzzle_dict = generator.generate_cross_puzzle(difficulty)
                        puzzles.append(puzzle_dict)
                
                elif sudoku_type == "Samurai Sudoku":
                    generator = SamuraiSudokuGenerator()
                    for i in range(num_puzzles):
                        center, outers = generator.generate_samurai_puzzles(difficulty)
                        puzzles.append((center, outers))
                
                # Download button without container
                if puzzles:
                    try:
                        pdf_file = create_pdf_download(puzzles, sudoku_type, difficulty)
                        if pdf_file:
                            with open(pdf_file, "rb") as file:
                                st.download_button(
                                    label="Baixar PDF",
                                    data=file.read(),
                                    file_name=f"{sudoku_type.lower().replace(' ', '_')}_{difficulty}_{num_puzzles}puzzles.pdf",
                                    mime="application/pdf",
                                    use_container_width=True
                                )
                    except Exception as e:
                        st.warning("PDF não disponível para este tipo de sudoku")
                st.success(f"{num_puzzles} puzzle(s) gerado(s) com sucesso! Use o botão acima para fazer o download do PDF.")
                
            except Exception as e:
                st.error(f"Erro ao gerar sudoku: {str(e)}")
    
    else:
        # Welcome message
        st.markdown("### Bem-vindo!")
        st.markdown("Selecione o tipo de sudoku, dificuldade e quantidade, depois clique em **Gerar**.")
    
    # Footer
    st.markdown("---")
    st.markdown("*Gerador de Sudoku - Desenvolvido com Streamlit*")

if __name__ == "__main__":
    main()
