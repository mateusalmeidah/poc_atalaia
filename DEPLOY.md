# Como publicar a vitrine no GitHub Pages

A página fica em `webdemo/` e é publicada automaticamente pelo workflow
`.github/workflows/deploy-pages.yml`. Siga os passos abaixo uma única vez.

## 1. Criar o repositório no GitHub

Crie um repositório **vazio** (sem README) na sua conta, por exemplo
`atalaia-poc01-lgpd-lai`. Anote a URL, algo como:

```
https://github.com/SEU_USUARIO/atalaia-poc01-lgpd-lai.git
```

## 2. Subir o projeto (a partir da raiz do projeto)

Execute no terminal, dentro da pasta `ATALAIA_POC01_KIRO`:

```bash
git init
git add .
git commit -m "PoC 0.1 LGPD/LAI + vitrine web"
git branch -M main
git remote add origin https://github.com/SEU_USUARIO/atalaia-poc01-lgpd-lai.git
git push -u origin main
```

> Se o Git pedir identidade na primeira vez:
> `git config --global user.name "Seu Nome"` e
> `git config --global user.email "voce@exemplo.com"`.

## 3. Ativar o GitHub Pages

No GitHub: **Settings → Pages → Build and deployment → Source** e selecione
**GitHub Actions**. Não precisa escolher pasta; o workflow já aponta para `webdemo/`.

## 4. Aguardar a publicação

Vá na aba **Actions**. O workflow "Deploy webdemo (GitHub Pages)" roda sozinho
após o push. Ao terminar (ícone verde), o link público aparece em
**Settings → Pages**, no formato:

```
https://SEU_USUARIO.github.io/atalaia-poc01-lgpd-lai/
```

É esse link que você envia ao professor.

## Atualizações futuras

Qualquer alteração na pasta `webdemo/` republica a página automaticamente:

```bash
git add .
git commit -m "ajuste na vitrine"
git push
```

## Observações

- A vitrine não altera o motor Python nem usa serviços externos — respeita as
  restrições da PoC (sem LLM, sem APIs, apenas dados fictícios).
- A fonte da verdade continua sendo o pacote `src/atalaia_governanca`, coberto por
  testes (`pytest`). O JS da vitrine é um porte verificado por paridade.
