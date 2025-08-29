# 🚀 Quick Start - Gerador de Sudoku

## ⚡ Início Rápido (1 comando)

```bash
make quick-start
```
Isso irá:
- Configurar permissões
- Instalar dependências
- Construir imagem Docker
- Iniciar aplicação
- Abrir em http://localhost:8501

## 🐳 Opções de Execução

### 1. Local (Python)
```bash
# Simples
./run.sh

# Ou com make
make run
```

### 2. Docker Compose (Recomendado)
```bash
# Iniciar
make compose-up

# Parar
make compose-down
```

### 3. Docker Manual
```bash
# Construir e executar
make docker-build
make docker-run

# Parar
make docker-stop
```

## 📋 Comandos Principais

| Comando | Descrição |
|---------|-----------|
| `make help` | Lista todos os comandos |
| `make run` | Execução local |
| `make compose-up` | Docker Compose |
| `make deploy-local` | Deploy local completo |
| `make deploy-production` | Deploy produção |
| `make status` | Status da aplicação |
| `make logs` | Ver logs |
| `make clean` | Limpar tudo |

## 🌐 Deploy em Produção

### Deploy Simples
```bash
make deploy-local
```

### Deploy Completo (Zero Downtime)
```bash
make deploy-production
```

### Rollback
```bash
make rollback
```

## 📊 Monitoramento

```bash
# Status
make status

# Logs em tempo real
make docker-logs

# Saúde da aplicação
make health

# Estatísticas
make stats
```

## 🛠️ Scripts Disponíveis

1. **`run.sh`** - Execução local simples
2. **`docker-run.sh`** - Gerenciamento Docker avançado
3. **`deploy.sh`** - Deploy completo com backup/rollback

## 📁 Estrutura Final

```
sudokuGenerator/
├── app.py                   # Aplicação principal
├── requirements.txt         # Dependências Python
├── Dockerfile              # Container Docker
├── docker-compose.yml      # Orquestração
├── Makefile                # Comandos úteis
├── run.sh                  # Execução local
├── docker-run.sh           # Docker avançado
├── deploy.sh               # Deploy produção
├── DOCKER.md               # Documentação Docker
├── QUICK_START.md          # Este arquivo
├── .streamlit/config.toml  # Configuração Streamlit
├── sudoku_generators/      # Módulos de sudoku
└── generated_pdfs/         # PDFs gerados
```

## 🔧 Troubleshooting

### Porta ocupada
```bash
# Verificar porta
lsof -i :8501

# Usar porta diferente
docker run -p 8502:8501 sudoku-generator
```

### Permissões
```bash
# Dar permissão aos scripts
chmod +x *.sh
```

### Container não inicia
```bash
# Ver logs
make docker-logs

# Entrar no container
make shell
```

## 🎯 Uso da Aplicação

1. **Acesse**: http://localhost:8501
2. **Selecione**: Tipo de sudoku
3. **Configure**: Dificuldade e quantidade
4. **Clique**: "Gerar"
5. **Download**: PDF gerado automaticamente

## 🎉 Pronto!

Sua aplicação está rodando em:
- **Local**: http://localhost:8501
- **Docker**: http://localhost:8501

Para parar: `make compose-down` ou `Ctrl+C`
