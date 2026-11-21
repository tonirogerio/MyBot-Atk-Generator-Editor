"""Internationalisation and per-field documentation for the editor.

Two languages are supported (English and Brazilian Portuguese). Besides UI
labels this module holds the explanation shown for the command currently
selected in the tree: what the command does and what each parameter means,
with the real value of the selected row.
"""

from __future__ import annotations

from .model import Drop, Make, Note, Recalc, Wait

LANGUAGES = {"pt": "Português (BR)", "en": "English"}

# --------------------------------------------------------------------------- #
# UI strings
# --------------------------------------------------------------------------- #
UI = {
    "app_title": {"en": "MyBot ATK GENERATOR - Tony R0XX", "pt": "MyBot ATK GENERATOR - Tony R0XX"},
    "app_subtitle": {"en": "Creation and editing of CSV scripts for MyBot", "pt": "Criação e edição de scripts CSV para o MyBot"},
    "menu_file": {"en": "File", "pt": "Arquivo"},
    "menu_edit": {"en": "Edit", "pt": "Editar"},
    "menu_help": {"en": "Help", "pt": "Ajuda"},
    "action_new": {"en": "New", "pt": "Novo"},
    "action_open": {"en": "Open...", "pt": "Abrir..."},
    "action_save": {"en": "Save", "pt": "Salvar"},
    "action_save_as": {"en": "Save As...", "pt": "Salvar Como..."},
    "action_export": {"en": "Export to CSV/Attack...", "pt": "Exportar para CSV/Attack..."},
    "action_save_template": {"en": "Save as Template...", "pt": "Salvar como Modelo..."},
    "action_exit": {"en": "Exit", "pt": "Sair"},
    "action_template": {"en": "New From Template...", "pt": "Novo a partir de Modelo..."},
    "action_validate": {"en": "Validate Now", "pt": "Validar Agora"},
    "action_units": {"en": "Unit Short Names", "pt": "Nomes Curtos das Unidades"},
    "action_undo": {"en": "Undo", "pt": "Desfazer"},
    "action_redo": {"en": "Redo", "pt": "Refazer"},
    "action_copy": {"en": "Copy", "pt": "Copiar"},
    "action_paste": {"en": "Paste", "pt": "Colar"},
    "action_duplicate": {"en": "Duplicate", "pt": "Duplicar"},
    "action_reset_view": {"en": "Reset View", "pt": "Resetar Visão"},
    "tree_num": {"en": "#", "pt": "#"},
    "tree_command": {"en": "Command", "pt": "Comando"},
    "tree_summary": {"en": "Summary", "pt": "Resumo"},
    "btn_make": {"en": "+ MAKE", "pt": "+ MAKE"},
    "btn_drop": {"en": "+ DROP", "pt": "+ DROP"},
    "btn_wait": {"en": "+ WAIT", "pt": "+ WAIT"},
    "btn_note": {"en": "+ NOTE", "pt": "+ NOTE"},
    "btn_recalc": {"en": "+ RECALC", "pt": "+ RECALC"},
    "btn_delete": {"en": "Delete", "pt": "Excluir"},
    "btn_up": {"en": "Move Up", "pt": "Subir"},
    "btn_down": {"en": "Move Down", "pt": "Descer"},
    "btn_make_tooltip": {"en": "Add MAKE command: defines a drop vector (line of points on the map edge)", "pt": "Adiciona MAKE: define um vetor de soltura (linha de pontos na borda do mapa)"},
    "btn_drop_tooltip": {"en": "Add DROP command: deploys units (troops/spells/heroes/sieges) on vector points", "pt": "Adiciona DROP: solta unidades (tropas/feitiços/heróis/sieges) nos pontos do vetor"},
    "btn_wait_tooltip": {"en": "Add WAIT command: pauses the script with optional break conditions", "pt": "Adiciona WAIT: pausa o script com condições de quebra opcionais"},
    "btn_note_tooltip": {"en": "Add NOTE command: adds a comment line for documentation", "pt": "Adiciona NOTE: adiciona uma linha de comentário para documentação"},
    "btn_recalc_tooltip": {"en": "Add RECALC command: re-reads the troop bar to update counts", "pt": "Adiciona RECALC: relê a barra de tropas para atualizar contagens"},
    "btn_delete_tooltip": {"en": "Delete selected command(s)", "pt": "Exclui comando(s) selecionado(s)"},
    "btn_up_tooltip": {"en": "Move selected command up", "pt": "Move comando selecionado para cima"},
    "btn_down_tooltip": {"en": "Move selected command down", "pt": "Move comando selecionado para baixo"},
    "dock_validation": {"en": "Validation", "pt": "Validação"},
    "dock_templates": {"en": "Templates (examples)", "pt": "Modelos (exemplos)"},
    "legend_title": {"en": "Vectors (show / hide)", "pt": "Vetores (mostrar / ocultar)"},
    "legend_show_all": {"en": "Show all", "pt": "Mostrar todos"},
    "legend_hide_all": {"en": "Hide all", "pt": "Ocultar todos"},
    "legend_empty": {"en": "Add a MAKE to create vectors.", "pt": "Adicione um MAKE para criar vetores."},
    "help_title": {"en": "Parameter help", "pt": "Ajuda dos parâmetros"},
    "help_none": {
        "en": "Select a command in the tree to see what it does and what each parameter means.",
        "pt": "Selecione um comando na árvore para ver o que ele faz e o que cada parâmetro significa.",
    },
    "validation_ok": {"en": "OK - no problems", "pt": "OK - sem problemas"},
    "language": {"en": "Language", "pt": "Idioma"},
    "none": {"en": "(none)", "pt": "(nenhum)"},
    "row": {"en": "Row", "pt": "Linha"},
    "value": {"en": "Value", "pt": "Valor"},
    "field": {"en": "Parameter", "pt": "Parâmetro"},
    "meaning": {"en": "Meaning", "pt": "Significado"},
    "status_undo": {"en": "Undone", "pt": "Desfeito"},
    "status_redo": {"en": "Redone", "pt": "Refeito"},
}

# --------------------------------------------------------------------------- #
# Command descriptions
# --------------------------------------------------------------------------- #
COMMAND_NAMES = {
    "MAKE": {"en": "MAKE - build a drop vector", "pt": "MAKE - cria um vetor de soltura"},
    "DROP": {"en": "DROP - deploy a unit", "pt": "DROP - solta uma unidade"},
    "WAIT": {"en": "WAIT - pause with conditions", "pt": "WAIT - pausa com condições"},
    "RECALC": {"en": "RECALC - refresh troop bar", "pt": "RECALC - atualiza a barra de tropas"},
    "NOTE": {"en": "NOTE - comment", "pt": "NOTE - comentário"},
    "RAW": {"en": "RAW - raw line", "pt": "RAW - linha crua"},
}

COMMAND_DESC = {
    "MAKE": {
        "en": "Defines a drop vector: a line of points built on one edge of the red zone the bot detects. DROP commands place troops on these points.",
        "pt": "Define um vetor de soltura: uma linha de pontos construída sobre uma borda da redline que o bot detecta. Os comandos DROP soltam tropas nesses pontos.",
    },
    "DROP": {
        "en": "Deploys a unit (troop, spell, hero or siege) on the points of one or more vectors, in a chosen order and with delays.",
        "pt": "Solta uma unidade (tropa, feitiço, herói ou siege) nos pontos de um ou mais vetores, numa ordem escolhida e com atrasos.",
    },
    "WAIT": {
        "en": "Pauses the script and watches the battle. Leaves early when a break condition is met, otherwise waits the full time.",
        "pt": "Pausa o script e observa a batalha. Sai antes quando uma condição de quebra é atendida; caso contrário espera o tempo total.",
    },
    "RECALC": {
        "en": "Re-reads the attack troop bar so the counts are current. Useful after deploying the clan castle or a siege machine.",
        "pt": "Relê a barra de tropas da batalha para atualizar as contagens. Útil após soltar o castelo de clã ou uma máquina de siege.",
    },
    "NOTE": {
        "en": "Comment line. The bot ignores it; use it to document the attack for yourself.",
        "pt": "Linha de comentário. O bot ignora; use para documentar o ataque.",
    },
    "RAW": {
        "en": "A line the editor does not model. It is preserved exactly as written.",
        "pt": "Uma linha que o editor não modela. É preservada exatamente como escrita.",
    },
}

# --------------------------------------------------------------------------- #
# Per-field labels and explanations
# --------------------------------------------------------------------------- #
FIELDS = {
    "make.vector": {
        "name": {"en": "Vector letter", "pt": "Letra do vetor"},
        "help": {
            "en": "Single letter A-Z that names the vector. DROP commands reference it by this letter.",
            "pt": "Letra única de A a Z que nomeia o vetor. Os comandos DROP referenciam o vetor por esta letra.",
        },
    },
    "make.side": {
        "name": {"en": "Side", "pt": "Lado"},
        "help": {
            "en": "Which edge of the base the vector is built on. Relative sides (FRONT-LEFT, etc.) rotate depending on the side the bot enters from.",
            "pt": "Qual borda da vila o vetor usa. Os lados relativos (FRONT-LEFT etc.) giram conforme o lado por onde o bot entra.",
        },
    },
    "make.points": {
        "name": {"en": "Drop points", "pt": "Pontos de soltura"},
        "help": {
            "en": "Number of points along the vector. Must be 1 or 5 when a building target is set.",
            "pt": "Quantidade de pontos ao longo do vetor. Deve ser 1 ou 5 quando um edifício-alvo é definido.",
        },
    },
    "make.add_tiles": {
        "name": {"en": "Add tiles", "pt": "Deslocar tiles"},
        "help": {
            "en": "Shifts the line away from the redline, in tiles (8 px each). Positive moves outside the base, negative moves inside.",
            "pt": "Desloca a linha a partir da redline, em tiles (8 px cada). Positivo move para fora da vila, negativo para dentro.",
        },
    },
    "make.versus": {
        "name": {"en": "Versus", "pt": "Sentido"},
        "help": {
            "en": "Order the points are used. INT-EXT = inside to outside, EXT-INT = outside to inside, IGNORE = no flip.",
            "pt": "Ordem em que os pontos são usados. INT-EXT = de dentro para fora, EXT-INT = de fora para dentro, IGNORE = não inverte.",
        },
    },
    "make.random_x": {
        "name": {"en": "Random X (px)", "pt": "Aleatório X (px)"},
        "help": {
            "en": "Random horizontal jitter added to each point so drops vary between attacks.",
            "pt": "Variação horizontal aleatória somada a cada ponto para variar as solturas entre ataques.",
        },
    },
    "make.random_y": {
        "name": {"en": "Random Y (px)", "pt": "Aleatório Y (px)"},
        "help": {
            "en": "Random vertical jitter added to each point so drops vary between attacks.",
            "pt": "Variação vertical aleatória somada a cada ponto para variar as solturas entre ataques.",
        },
    },
    "make.building": {
        "name": {"en": "Building target", "pt": "Edifício-alvo"},
        "help": {
            "en": "Optional defence to target. The bot finds it at runtime and builds the points around/near it (requires 1 or 5 points).",
            "pt": "Defesa opcional como alvo. O bot a encontra em tempo real e gera os pontos ao redor/perto dela (exige 1 ou 5 pontos).",
        },
    },
    "drop.vectors": {
        "name": {"en": "Vectors", "pt": "Vetores"},
        "help": {
            "en": "Vector(s) to use: 'A', a range 'A-B', or a list 'A,B,C' to alternate between them.",
            "pt": "Vetor(es) a usar: 'A', um intervalo 'A-B' ou uma lista 'A,B,C' para alternar entre eles.",
        },
    },
    "drop.index": {
        "name": {"en": "Point index", "pt": "Índice dos pontos"},
        "help": {
            "en": "Which points inside the vector, in order: '1', range '1-10', list '1,3,5'. The order controls the drop sequence.",
            "pt": "Quais pontos dentro do vetor, em ordem: '1', intervalo '1-10', lista '1,3,5'. A ordem controla a sequência.",
        },
    },
    "drop.quantity": {
        "name": {"en": "Quantity", "pt": "Quantidade"},
        "help": {
            "en": "How many of the unit to place per point. A range like '2-4' randomises it.",
            "pt": "Quantas unidades colocar por ponto. Um intervalo como '2-4' sorteia o valor.",
        },
    },
    "drop.unit": {
        "name": {"en": "Unit", "pt": "Unidade"},
        "help": {
            "en": "Unit short name (e.g. MeteorG, Heal, Queen, WallW). REMAIN dumps everything left; AnyS drops any siege.",
            "pt": "Nome curto da unidade (ex.: MeteorG, Heal, Queen, WallW). REMAIN solta tudo que sobrou; AnyS solta qualquer siege.",
        },
    },
    "drop.delay_points": {
        "name": {"en": "Delay between points (ms)", "pt": "Atraso entre pontos (ms)"},
        "help": {
            "en": "Delay in milliseconds between consecutive points. A range is allowed.",
            "pt": "Atraso em milissegundos entre pontos consecutivos. Aceita intervalo.",
        },
    },
    "drop.delay_change": {
        "name": {"en": "Delay between taps (ms)", "pt": "Atraso entre toques (ms)"},
        "help": {
            "en": "Extra delay between individual taps on the same point.",
            "pt": "Atraso extra entre toques individuais no mesmo ponto.",
        },
    },
    "drop.sleep_after": {
        "name": {"en": "Sleep after (ms)", "pt": "Pausa depois (ms)"},
        "help": {
            "en": "Sleep in milliseconds after this DROP finishes. A range is allowed.",
            "pt": "Pausa em milissegundos após este DROP terminar. Aceita intervalo.",
        },
    },
    "wait.duration": {
        "name": {"en": "Duration (ms)", "pt": "Duração (ms)"},
        "help": {
            "en": "Maximum wait time in milliseconds. A range is allowed.",
            "pt": "Tempo máximo de espera em milissegundos. Aceita intervalo.",
        },
    },
    "wait.conditions": {
        "name": {"en": "Break conditions", "pt": "Condições de quebra"},
        "help": {
            "en": "Optional conditions, comma separated: TH, SIEGE, TH+SIEGE, 50%, AQ, BK, GW, RC, DD, AQ+BK.",
            "pt": "Condições opcionais, separadas por vírgula: TH, SIEGE, TH+SIEGE, 50%, AQ, BK, GW, RC, DD, AQ+BK.",
        },
    },
    "note.text": {
        "name": {"en": "Text", "pt": "Texto"},
        "help": {
            "en": "Free text comment. Ignored by the bot.",
            "pt": "Comentário livre. Ignorado pelo bot.",
        },
    },
}


class Translator:
    def __init__(self, lang: str = "pt"):
        self.lang = lang if lang in LANGUAGES else "pt"

    # -- basic lookup ------------------------------------------------------ #
    def tr(self, key: str) -> str:
        entry = UI.get(key)
        if not entry:
            return key
        return entry.get(self.lang) or entry.get("en", key)

    def _pick(self, table: dict) -> str:
        if not isinstance(table, dict):
            return ""
        return table.get(self.lang) or table.get("en") or ""

    def command_name(self, kind: str) -> str:
        return self._pick(COMMAND_NAMES.get(kind, {}))

    def command_desc(self, kind: str) -> str:
        return self._pick(COMMAND_DESC.get(kind, {}))

    def field_name(self, key: str) -> str:
        return self._pick(FIELDS.get(key, {}).get("name", {}))

    def field_help(self, key: str) -> str:
        return self._pick(FIELDS.get(key, {}).get("help", {}))

    # -- structure helpers ------------------------------------------------- #
    def describe(self, command, index: int | None = None) -> dict:
        """Return title, description and parameter rows for a command."""
        if command is None:
            rows = [
                (self.command_name(kind), self.command_desc(kind))
                for kind in ("MAKE", "DROP", "WAIT", "RECALC", "NOTE")
            ]
            return {
                "title": self.tr("help_title"),
                "description": self.tr("help_none"),
                "line": None,
                "rows": rows,
            }

        kind = command.kind
        rows = []
        if isinstance(command, Make):
            rows = [
                ("make.vector", command.vector),
                ("make.side", command.side),
                ("make.points", str(command.points)),
                ("make.add_tiles", str(command.add_tiles)),
                ("make.versus", command.versus),
                ("make.random_x", str(command.random_x)),
                ("make.random_y", str(command.random_y)),
                ("make.building", command.building or self.tr("none")),
            ]
        elif isinstance(command, Drop):
            rows = [
                ("drop.vectors", command.vectors),
                ("drop.index", command.index),
                ("drop.quantity", command.quantity),
                ("drop.unit", command.unit),
                ("drop.delay_points", command.delay_points),
                ("drop.delay_change", command.delay_change),
                ("drop.sleep_after", command.sleep_after),
            ]
        elif isinstance(command, Wait):
            rows = [
                ("wait.duration", command.duration),
                ("wait.conditions", command.conditions or self.tr("none")),
            ]
        elif isinstance(command, Note):
            rows = [("note.text", command.text or self.tr("none"))]
        elif isinstance(command, Recalc):
            rows = []

        return {
            "title": self.command_name(kind),
            "description": self.command_desc(kind),
            "line": index,
            "rows": [
                (self.field_name(key), value, self.field_help(key))
                for key, value in rows
            ],
        }
