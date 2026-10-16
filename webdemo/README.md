# Vitrine web — PoC 0.1 LGPD/LAI

Página didática e interativa que demonstra o motor de governança da PoC 0.1
**rodando 100% no navegador**, sem backend. É um porte fiel (mesmos regex, mesma
taxonomia e mesma tabela de decisão) do pacote Python em `../src/atalaia_governanca`,
que é a fonte da verdade e tem 38 testes automatizados.

## O que a página mostra

1. **O que a PoC prova** — contexto da pesquisa.
2. **Fluxo etapa por etapa** — diagrama que acende conforme a análise roda.
3. **Playground ao vivo** — os 4 casos canônicos + campo livre para digitar.
4. **Regra de ouro** — tabela de decisão e a proibição de decisão jurídica final.
5. **Paridade** — compara o resultado do JS com o esperado do Python (verde = idêntico).

## Rodar localmente

A página usa ES modules, então precisa de um servidor HTTP (não abra o
`index.html` por `file://`).

```bash
# a partir desta pasta (webdemo/)
python -m http.server 8777
# depois abra http://localhost:8777
```

## Verificar paridade com o Python (opcional)

```bash
node webdemo/_verifica_paridade.mjs   # a partir da raiz do projeto
```

## Publicar no GitHub Pages

Veja o passo a passo em `../DEPLOY.md`. Em resumo: subir o projeto para um
repositório no GitHub, ativar o Pages com origem **GitHub Actions**, e o workflow
`.github/workflows/deploy-pages.yml` publica esta pasta automaticamente.

## Arquivos

- `index.html` — estrutura e conteúdo explicativo.
- `styles.css` — estilo (tema escuro, responsivo).
- `motor.js` — o motor determinístico (porte do Python).
- `casos.js` — os 4 casos canônicos e os textos de explicação.
- `app.js` — interação, animação do fluxo, GOV-ADR e paridade.
- `_verifica_paridade.mjs` — script auxiliar de verificação (não usado pela página).
