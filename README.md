<div align="center">

# 🛡️ MyBot ATK GENERATOR

**Visual attack-script editor for MyBot PH MOD v16.4 / v16.5**  
Create, edit, validate and export CSV attack files — no hand-editing required.

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue)](https://www.python.org/)
[![PySide6](https://img.shields.io/badge/PySide6-6.6%2B-green)](https://wiki.qt.io/Qt_for_Python)
[![License](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Windows-lightgrey)](#)

---

**Créditos / Credits**  
Desenvolvido por **Tony R0XX**  ·  Marca **T-R0XX**  
Designed by **Tony R0XX**  ·  Brand **T-R0XX**

</div>

---

## 📖 Sumário / Table of Contents

- [Visão Geral / Overview](#-visão-geral--overview)
- [Requisitos / Requirements](#-requisitos--requirements)
- [Instalação & Execução / Install & Run](#-instalação--execução--install--run)
- [Interface / UI Walkthrough](#-interface--ui-walkthrough)
- [Comandos Suportados / Supported Commands](#-comandos-suportados--supported-commands)
- [Fluxo de Trabalho / Workflow](#-fluxo-de-trabalho--workflow)
- [Canvas: Vetores, Zoom/Pan, Clique](#-canvas-vetores-zoompan-clique)
- [Modelos (Templates)](#-modelos-templates)
- [Validação em Tempo Real](#-validação-em-tempo-real)
- [Internacionalização (PT/EN)](#-internacionalização-pten)
- [Estrutura de Pastas / Folder Structure](#-estrutura-de-pastas--folder-structure)
- [Build do Executável / Building the EXE](#-build-do-executável--building-the-exe)
- [Licença / License](#-licença--license)

---

## 🎯 Visão Geral / Overview

| PT | EN |
|----|----|
| Editor **desktop nativo** (PySide6/Qt) para criar arquivos de ataque **CSV** que o **MyBot PH MOD v16.4/16.5** lê da pasta `CSV/Attack`. | Native **desktop editor** (PySide6/Qt) to create **CSV** attack files that **MyBot PH MOD v16.4/16.5** reads from `CSV/Attack`. |
| Gera scripts **do zero** (File → New) ou a partir de **modelos** prontos. | Generate scripts **from scratch** (File → New) or from **built-in templates**. |
| Validação **em tempo real**, tooltips por campo, canvas com vetores, zoom/pan, undo/redo, copiar/colar/duplicar. | **Real-time validation**, per-field tooltips, canvas with vectors, zoom/pan, undo/redo, copy/paste/duplicate. |
| Tema escuro, interface em **PT-BR** ou **EN** (botão na toolbar). | Dark theme, UI in **PT-BR** or **EN** (toolbar button). |
| Salva modelos de usuário em `templates/` (JSON) e exporta CSV para `CSV/Attack/`. | Saves user templates to `templates/` (JSON) and exports CSV to `CSV/Attack/`. |

---

## 💻 Requisitos / Requirements

| Item | Versão mínima |
|------|---------------|
| **Python** | 3.10+ |
| **PySide6** | 6.6+ |
| **Windows** | 10/11 (testado) |
| **UPX** (opcional, build) | no PATH para compressão do `.exe` |

```bash
pip install -r requirements.txt
```

> `UPX` é apenas para o build do executável (`build_exe.bat`). Em desenvolvimento não é necessário.

---

## 🚀 Instalação & Execução / Install & Run

### Desenvolvimento / Development

```bash
cd attack-generator
python main.py
```

### Executável pronto / Pre-built EXE

1. Baixe `MyBot_ATK_GEN.exe` da página de Releases (ou gere com `build_exe.bat`).
2. Coloque na pasta do MyBot (ex.: `MyBot\Tools\`) ou onde preferir.
3. Rode — abre com ícone **T-R0XX** na barra de título e taskbar.

---

## 🖥️ Interface / UI Walkthrough

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  MyBot ATK GENERATOR - Tony R0XX          [PT]  [Undo] [Redo]  [Copy] ...   │
├──────────┬───────────────────────────────┬──────────────────────────────────┤
│ COMANDOS │         CANVAS                │ MODELOS          │ PROPRIEDADES  │
│ (árvore) │  ┌─────────────────────┐      │  (lista c/       │  (editor     │
│          │  │  LEGENDA HORIZONTAL │      │   menu direito)  │   contextual) │
│  +MAKE   │  ├─────────────────────┤      │                  │               │
│  +DROP   │  │                     │      │  MeteorMayhem    │  Vector: [A]  │
│  +WAIT   │  │      DIAMANTE       │      │  EDragLoon       │  Side: FRONT- │
│  +NOTE   │  │   (mapa 44x44)      │      │  QueenCharge     │  LEFT         │
│  +RECALC │  │                     │      │  ...             │  Points: 10   │
│  Del/↑/↓ │  │  Vetores A,B,C...   │      │                  │  Add Tiles: 1 │
│          │  │  Clique no ponto →  │      │  [modelos user]  │  Versus:      │
│          │  │  preenche DROP      │      │                  │  INT-EXT      │
│          │  └─────────────────────┘      │                  │               │
├──────────┴───────────────────────────────┴──────────────────────────────────┤
│ VALIDAÇÃO (dock inferior)  ✓ OK  |  ✗ Erro: linha 3 - unidade inválida     │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Painéis

| Painel | Função |
|--------|--------|
| **Esquerda – Comandos** | Árvore com nº, tipo, resumo. Ícones ✓/✗ de validação. Botões +MAKE, +DROP, +WAIT, +NOTE, +RECALC, Excluir, Subir, Descer. |
| **Centro – Canvas** | Mapa 44×44 (diamante). **Legenda horizontal** mostra vetores criados (MAKE) — clique para mostrar/esconder. **Zoom**: roda do mouse. **Pan**: botão meio/direito + arraste. **Home** = reset view. **Clique em ponto** → preenche `Vector`/`Index` do DROP selecionado. Coordenadas na status bar. |
| **Direita topo – Modelos** | Lista de templates (built-in + usuário). **Duplo-clique** carrega. **Botão direito**: Carregar, Renomear, Excluir, Abrir pasta. |
| **Direita base – Propriedades** | Editor contextual do comando selecionado. **DROP** tem combo dinâmico `Vectors` (letras dos MAKEs). Tooltips em cada campo. |
| **Inferior – Validação** | Lista de problemas (erro/aviso/linha). Clique → seleciona o comando na árvore. |

### Toolbar & Atalhos

| Ação | Atalho | Botão |
|------|--------|-------|
| Desfazer / Refazer | `Ctrl+Z` / `Ctrl+Y` | ↶ ↷ |
| Copiar / Colar / Duplicar | `Ctrl+C` / `Ctrl+V` / `Ctrl+D` | 📋 📋+ |
| Resetar visão do canvas | `Home` | 🏠 |
| Alternar idioma PT/EN | — | Botão `[PT]` / `[EN]` |
| Novo script | `Ctrl+N` | Menu Arquivo → Novo |
| Abrir CSV | `Ctrl+O` | Menu Arquivo → Abrir... |
| Salvar | `Ctrl+S` | Menu Arquivo → Salvar |
| Salvar como / Exportar CSV | `Ctrl+Shift+S` | Menu Arquivo → Exportar para CSV/Attack... |
| Salvar como Modelo | `Ctrl+M` | Menu Arquivo → Salvar como Modelo... |
| Novo a partir de Modelo | `Ctrl+T` | Menu Editar → Novo a partir de Modelo... |
| Validar agora | `F7` | Menu Editar → Validar Agora |
| Nomes curtos das unidades | — | Menu Ajuda → Nomes Curtos das Unidades |

---

## 🧱 Comandos Suportados / Supported Commands

| Comando | Descrição PT | Description EN | Campos principais |
|---------|--------------|----------------|-------------------|
| **MAKE** | Define um **vetor de soltura** (linha de pontos na borda do mapa). | Defines a **drop vector** (line of points on map edge). | `Vector` (A–Z), `Side` (FRONT-LEFT…RANDOM), `Points` (1–10), `Add Tiles` (±), `Versus` (INT-EXT/EXT-INT/IGNORE), `Rand X/Y`, `Building` (alvo opcional). |
| **DROP** | Solta **unidades** (tropas, feitiços, heróis, sieges) nos pontos do vetor. | Deploys **units** (troops, spells, heroes, sieges) on vector points. | `Vectors` (ex.: `A-B` ou `A,C`), `Index` (ponto inicial/fim/ex.: `1-10` ou `5`), `Quantity` (número ou `REMAIN`), `Unit` (short name: `Barb`, `EDrag`, `RSpell`…), `Delay Points`, `Delay Change`, `Sleep After`. |
| **WAIT** | Pausa o script com **condições de quebra** opcionais. | Pauses script with optional **break conditions**. | `Duration` (ms ou faixa `min-max`), `Conditions` (ex.: `TH`, `50%`, `AQ+BK`, `SIEGE`…). |
| **NOTE** | Linha de comentário/documentação (não executada pelo bot). | Comment/documentation line (not executed by bot). | `Text` (linha única, sem pipe). |
| **RECALC** | Re-lê a barra de tropas para atualizar contagens. | Re-reads troop bar to update counts. | (sem parâmetros). |

> **Short names de unidades** — veja Menu **Ajuda → Nomes Curtos das Unidades** (lista completa com housing space). O bot aceita *case-insensitive*; o editor valida contra o catálogo oficial do MyBot v16.4.

---

## 🔄 Fluxo de Trabalho / Workflow

### 1. Criar ataque do zero
```
File → New (Ctrl+N)
→ Clique +MAKE (define vetor A, lado FRONT-LEFT, 10 pts)
→ Clique +DROP (seleciona Vector A, Index 1-10, Unit Barb, Qtd 4)
→ +WAIT (3000 ms)
→ +MAKE (vetor B, lado FRONT-RIGHT…)
→ +DROP (Vector B, Index 5, Unit EDrag…)
→ File → Export to CSV/Attack… (Ctrl+Shift+S)
   → salva em CSV/Attack/MeuAtaque.csv
```

### 2. Usar modelo pronto
```
Edit → New From Template… (Ctrl+T)
→ Escolha "MeteorMayhem" / "EDragLoon" / "QueenCharge"
→ Ajuste propriedades (tropas, quantidades, vetores)
→ Export to CSV/Attack…
```

### 3. Editar CSV existente
```
File → Open… (Ctrl+O)
→ Selecione .csv da pasta CSV/Attack/
→ Edite, adicione, reordene comandos
→ File → Save (Ctrl+S)  ou  Save As…
```

### 4. Salvar seu próprio modelo
```
Monte o script → File → Save as Template… (Ctrl+M)
→ Dê um nome → OK
→ Aparece na lista "Modelos" (painel direito) com menu direito: Renomear/Excluir/Abrir pasta
```

---

## 🎨 Canvas: Vetores, Zoom/Pan, Clique

| Recurso | Como usar |
|---------|-----------|
| **Legenda horizontal** | Acima do canvas. Cada letra = vetor criado por MAKE. Clique para **mostrar/esconder** (útil quando vetores se sobrepõem). |
| **Zoom** | Roda do mouse (scroll) → zoom in/out centrado no cursor. |
| **Pan** | Botão **meio** ou **direito** + arraste → move a vista. |
| **Reset View** | Tecla `Home` ou botão 🏠 na toolbar. |
| **Clique no ponto** | Com um **DROP selecionado** na árvore, clique em um ponto do canvas → abre diálogo "Atualizar este DROP para vetor 'A', ponto 3?" → **Yes** preenche `Vectors` e `Index` automaticamente. |
| **Coordenadas** | Mostradas na status bar (ex.: `Vector A, point 3 (x=12, y=34)`). |

> O canvas desenha o **diamante 44×44** do CoC. Vetores são linhas radiais a partir da borda. `Add Tiles` estende/encurta; `Versus` inverte direção (INT-EXT = fora→dentro, EXT-INT = dentro→fora).

---

## 📦 Modelos (Templates)

### Built-in (sempre disponíveis)
| Template | Estratégia |
|----------|------------|
| **MeteorMayhem** | Meteor Golems + Throwers + Totem/EQ, Log Launcher, heróis. |
| **EDragLoon** | Electro Dragons + Balloons + Rage/Freeze, Battle Blimp. |
| **QueenCharge** | Queen Walk + Healers + siege híbrido. |

### Modelos do usuário
- Salvos em `attack-generator/templates/*.json` (formato JSON serializado do `Script`).
- Menu direito na lista: **Carregar**, **Renomear**, **Excluir**, **Abrir pasta de modelos**.
- **Import/Export**: no diálogo `Ctrl+T` → botões **Importar JSON/ZIP** e **Exportar** (compartilhe ataques com a clan).

---

## ✅ Validação em Tempo Real

- **Ícones na árvore**: ✓ (válido) / ✗ (erro) por linha.
- **Tooltip no item**: passa o mouse → vê o erro exato.
- **Dock Validação** (inferior): lista completa (Erro/Aviso/Info + linha + mensagem).
- **Clique no erro** → seleciona o comando na árvore e abre propriedades.
- Verifica: short names de unidade, faixas numéricas, vetores referenciados, sintaxe WAIT, duplicatas, etc.

> Roda automaticamente a cada edição. `F7` força re-validação completa.

---

## 🌐 Internacionalização (PT/EN)

- **Único idioma por vez** — botão `[PT]` / `[EN]` na toolbar alterna instantaneamente.
- Atualiza: título da janela, menus, tooltips, cabeçalho, legendas, dock titles, property editor, template list, tree headers.
- Arquivo único: `attackgen/i18n.py` (classe `Translator` + dicionário `TR`).

---

## 📁 Estrutura de Pastas / Folder Structure

```
attack-generator/
├── main.py                    # Entry point
├── requirements.txt           # PySide6
├── build_exe.bat              # Build script (PyInstaller + UPX)
├── icon.ico                   # Ícone T-R0XX
├── README.md                  # Este arquivo
├── LICENSE                    # MIT
├── CSV/
│   └── Attack/                # Destino padrão ao exportar CSV
├── templates/                 # Modelos do usuário (*.json)
│   ├── MeuAtaque.json
│   └── ...
└── attackgen/
    ├── __init__.py
    ├── ui_main.py             # Janela principal (toda a UI)
    ├── model.py               # Dataclasses: Make, Drop, Wait, Note, Recalc, Script
    ├── schema.py              # Vocabulário: SIDES, VERSUS, BUILDINGS, TROOPS, SPELLS, HEROES, SIEGES
    ├── parser.py              # CSV → Script
    ├── emitter.py             # Script → CSV (pipe format)
    ├── validate.py            # Validador estático (Problem.index → ícones na árvore)
    ├── geometry.py            # Diamond 44x44, drop points, building anchors
    ├── templates.py           # Built-in templates + user template loader/saver
    ├── i18n.py                # Translator (PT/EN) + tooltips por campo
    ├── stats.py               # Estatísticas do script (tropas, housing, tempo)
    └── cli.py                 # CLI opcional (validação em lote)
```

---

## 🛠️ Build do Executável / Building the EXE

```bash
cd attack-generator
build_exe.bat
```

**O que o script faz:**
1. Limpa `dist/`, `build/`, `*.spec`.
2. Verifica dependências (`PySide6`, `attackgen`).
3. `pyinstaller` com:
   - `--onefile` — único `.exe`
   - `--noconsole` — GUI sem janela preta
   - `--strip` — remove símbolos de debug
   - `--upx-dir=%UPX_DIR%` — compressão UPX (se no PATH)
   - `--icon=icon.ico` — ícone T-R0XX na barra de título/taskbar
   - `--add-data="icon.ico;."` — ícone embutido para runtime
   - `--add-data="templates;templates"` — modelos built-in
   - `--hidden-import=attackgen.*` — garante imports dinâmicos
4. Saída: `dist/MyBot_ATK_GEN.exe` (~42 MB comprimido).

### Code Signing (produção)
```cmd
signtool sign /f cert.pfx /p senha ^
  /tr http://timestamp.digicert.com /fd sha256 ^
  dist\MyBot_ATK_GEN.exe
```
Depois submeta ao **VirusTotal** e **Microsoft Defender Submission** para reputação.

---

## ⚖️ Licença / License

```
MIT License

Copyright (c) 2026 Tony R0XX (T-R0XX)

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

<div align="center">

**Feito com 💙 por Tony R0XX — Marca T-R0XX**  
**Crafted by Tony R0XX — Brand T-R0XX**

*MyBot ATK GENERATOR não é afiliado, endossado ou patrocinado pela Supercell ou MyBot PH MOD.*  
*MyBot ATK GENERATOR is not affiliated with, endorsed by, or sponsored by Supercell or MyBot PH MOD.*

</div>