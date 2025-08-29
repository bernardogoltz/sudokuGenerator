# 🧩 Sudoku Generator

Um gerador completo de puzzles Sudoku com interface web interativa construída com Streamlit.

## 📁 Estrutura do Projeto

```
sudokuGenerator/
├── app.py                          # Aplicação Streamlit principal
├── requirements.txt                # Dependências do projeto
├── README.md                      # Documentação
├── static/                        # Arquivos estáticos (CSS, imagens)
└── sudoku_generators/             # Módulos de geração de sudoku
    ├── classic/                   # Sudokus clássicos
    │   ├── 9x9_sudoku.py         # Sudoku tradicional 9x9
    │   ├── 12x12_sudoku.py       # Sudoku expandido 12x12
    │   └── 16x16_sudoku.py       # Sudoku grande 16x16
    └── special/                   # Sudokus especiais
        ├── cross_sudoku.py       # Sudoku em cruz (5 grids)
        ├── samurai_sudoku.py     # Sudoku samurai (5 grids)
        ├── double_linked_sudoku.py
        └── sohei_sudoku.py
```

## 🚀 Como Usar

### Pré-requisitos
- Python 3.7 ou superior
- pip (gerenciador de pacotes Python)

### Instalação

1. Clone o repositório:
```bash
git clone <url-do-repositorio>
cd sudokuGenerator
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

### Executar a Aplicação Web

```bash
streamlit run app.py
```

A aplicação será aberta automaticamente no seu navegador em `http://localhost:8501`

## 🎮 Funcionalidades

### Tipos de Sudoku Disponíveis

1. **Sudoku Clássico 9x9**
   - Sudoku tradicional com números de 1 a 9
   - 3 níveis de dificuldade: Fácil, Médio, Difícil

2. **Sudoku 12x12**
   - Versão expandida com números de 1 a 12
   - Blocos 3x4 para maior desafio

3. **Sudoku 16x16**
   - Versão grande com números de 1 a 16
   - Blocos 4x4 para especialistas

4. **Cross Sudoku**
   - 5 sudokus 9x9 interconectados em formato de cruz
   - Compartilham linhas e colunas entre si

5. **Samurai Sudoku**
   - 5 sudokus 9x9 interconectados em formato de samurai
   - Cantos dos sudokus externos se sobrepõem ao central

### Configurações

- **Dificuldade**: Easy (Fácil), Medium (Médio), Hard (Difícil)
- **Quantidade**: Gere de 1 a 50 puzzles por vez
- **Visualização**: Interface web amigável com grids formatados

## 🛠️ Uso Individual dos Geradores

Cada gerador também pode ser executado individualmente:

```bash
# Sudoku 9x9
python sudoku_generators/classic/9x9_sudoku.py

# Sudoku 12x12
python sudoku_generators/classic/12x12_sudoku.py

# Cross Sudoku
python sudoku_generators/special/cross_sudoku.py

# Samurai Sudoku
python sudoku_generators/special/samurai_sudoku.py
```

Cada script gerará um arquivo PDF com os puzzles criados.

## 📦 Dependências

- **Streamlit**: Framework para criação da interface web
- **ReportLab**: Biblioteca para geração de PDFs

## 🤝 Contribuindo

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## 🧩 Sobre os Algoritmos

Os geradores utilizam algoritmos de backtracking para criar sudokus válidos e únicos. O processo inclui:

1. **Geração da solução completa**: Preenchimento completo e válido do grid
2. **Remoção estratégica**: Remoção de números baseada na dificuldade
3. **Validação**: Garantia de que existe solução única

Cada tipo especial (Cross, Samurai) implementa regras adicionais de interconexão entre os grids.
