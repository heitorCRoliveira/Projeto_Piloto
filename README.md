# TechStore — Entrega Contínua e Segurança (MVP)

API simples (Flask) com pipeline de CI/CD no GitHub Actions e entrega via Docker (GHCR).

## Como rodar localmente
```bash
docker build -t techstore .
docker run -p 8000:8000 techstore
curl http://localhost:8000/health
curl http://localhost:8000/products
```

## Fluxo
```
git push / Pull Request
        │
        ▼
 [qualidade]  ─────────┐   flake8 + pytest (cobertura >= 80%)
 [seguranca-codigo] ───┤   Bandit (SAST) + pip-audit (dependências)
                       ▼
                 [imagem]       docker build + Trivy + smoke test
                       ▼
                 [publicar]     só na main → ghcr.io/<usuario>/<repo>:latest e :<sha>
```

## Quando a entrega é interrompida
| Situação | Etapa que falha |
|---|---|
| Código fora do padrão (estilo/erros) | flake8 |
| Teste quebrado ou cobertura < 80% | pytest |
| Código inseguro (ex.: debug ligado, `eval`, senha no código) | Bandit |
| Dependência com CVE conhecida | pip-audit |
| Imagem com vulnerabilidade HIGH/CRITICAL | Trivy |
| Container não sobe / `/health` não responde | smoke test |

## Demonstrações sugeridas
1. **Sucesso:** push na `main` → todas as etapas verdes → imagem publicada no GHCR.
2. **Falha de teste:** troque `"Notebook"` por outro nome em `app/main.py` → `pytest` falha e nada é publicado.
3. **Falha de segurança:** troque `host="127.0.0.1"` por `host="0.0.0.0", debug=True` no `app.run` → o Bandit bloqueia.
4. **Dependência vulnerável:** fixe `flask==0.12` no `requirements.txt` → o pip-audit bloqueia.
