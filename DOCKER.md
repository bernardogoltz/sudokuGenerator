# 🐳 Docker Deploy - Gerador de Sudoku

## Scripts Disponíveis

### 1. `run.sh` - Execução Local
Executa o aplicativo diretamente com Python/Streamlit:
```bash
./run.sh
```

### 2. `docker-run.sh` - Gerenciamento Docker
Script principal para operações Docker:

```bash
# Construir e executar
./docker-run.sh run

# Apenas construir imagem
./docker-run.sh build

# Parar aplicação
./docker-run.sh stop

# Ver logs
./docker-run.sh logs

# Modo desenvolvimento (hot reload)
./docker-run.sh dev

# Limpar containers e imagens
./docker-run.sh clean
```

### 3. `deploy.sh` - Deploy Completo
Script para deploy em diferentes ambientes:

```bash
# Deploy local
./deploy.sh local

# Deploy produção (com zero downtime)
./deploy.sh production

# Deploy staging
./deploy.sh staging

# Rollback para versão anterior
./deploy.sh rollback

# Status da aplicação
./deploy.sh status
```

## Comandos Docker Manuais

### Construir Imagem
```bash
docker build -t sudoku-generator .
```

### Executar Container
```bash
docker run -d --name sudoku-generator -p 8501:8501 sudoku-generator
```

### Com Docker Compose
```bash
# Iniciar
docker-compose up -d

# Parar
docker-compose down

# Ver logs
docker-compose logs -f
```

## Estrutura de Arquivos Docker

```
sudokuGenerator/
├── Dockerfile              # Configuração da imagem Docker
├── docker-compose.yml      # Orquestração de containers
├── .dockerignore           # Arquivos ignorados no build
├── run.sh                  # Execução local simples
├── docker-run.sh           # Gerenciamento Docker
├── deploy.sh               # Deploy completo
└── generated_pdfs/         # Volume para PDFs gerados
```

## Portas

- **8501**: Aplicação principal (produção)
- **8502**: Testes temporários
- **8503**: Ambiente staging

## Volumes

- `./generated_pdfs:/app/generated_pdfs` - PDFs gerados persistidos

## Variáveis de Ambiente

- `PYTHONPATH=/app` - Path do Python
- `PYTHONDONTWRITEBYTECODE=1` - Não gerar bytecode
- `PYTHONUNBUFFERED=1` - Output em tempo real

## Troubleshooting

### Container não inicia
```bash
# Ver logs detalhados
docker logs sudoku-generator

# Executar interativamente
docker run -it --rm sudoku-generator bash
```

### Porta ocupada
```bash
# Ver processo usando a porta
lsof -i :8501

# Usar porta diferente
docker run -p 8502:8501 sudoku-generator
```

### Problemas de permissão
```bash
# Dar permissão aos scripts
chmod +x *.sh
```

## Deploy em Produção

1. **Preparação**:
```bash
# Clone o repositório
git clone <repo-url>
cd sudokuGenerator

# Tornar scripts executáveis
chmod +x *.sh
```

2. **Deploy Simples**:
```bash
./deploy.sh local
```

3. **Deploy Produção**:
```bash
./deploy.sh production
```

4. **Monitoramento**:
```bash
# Status
./deploy.sh status

# Logs em tempo real
docker logs -f sudoku-generator
```

## Backup e Rollback

O script de deploy automaticamente:
- Faz backup da versão anterior
- Testa a nova versão antes de trocar
- Permite rollback rápido

```bash
# Rollback para versão anterior
./deploy.sh rollback
```

## Health Check

A aplicação possui health check automático:
- **Endpoint**: `http://localhost:8501/_stcore/health`
- **Intervalo**: 30 segundos
- **Timeout**: 10 segundos

## Segurança

- Container executa com usuário não-root
- Apenas porta necessária exposta
- Imagem baseada em Python slim (menor superfície de ataque)
