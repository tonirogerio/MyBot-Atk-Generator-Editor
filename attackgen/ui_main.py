"""PySide6 graphical editor for MyBot attack CSV scripts.

The editor is built around the same model/emit/validate core used by the CLI,
so anything you assemble here round-trips to a file the bot can execute.

Layout
------
- Left        : ordered command tree, property editor underneath
- Right top   : fixed size redline/vector preview with a show/hide legend
- Right middle: parameter help for the selected command (one language at a time)
- Bottom dock : validation (errors the bot would silently ignore show red)
- Right dock  : template gallery (examples only; double click to load)

A toolbar button switches the whole interface between English and Portuguese;
only one language is shown at a time.
"""

from __future__ import annotations

import sys
from pathlib import Path

# Allow running this file directly (e.g. Run in PyCharm) even when the working
# directory is not the project root, by putting attack-generator on sys.path.
if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from PySide6.QtCore import QPointF, Qt, Signal
from PySide6.QtGui import QAction, QBrush, QColor, QFont, QPainter, QPen, QPolygonF
from PySide6.QtWidgets import (
    QApplication,
    QCheckBox,
    QComboBox,
    QCompleter,
    QDialog,
    QDialogButtonBox,
    QDockWidget,
    QFileDialog,
    QFormLayout,
    QGroupBox,
    QHBoxLayout,
    QInputDialog,
    QLabel,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QMainWindow,
    QMenu,
    QMessageBox,
    QPushButton,
    QScrollArea,
    QSizePolicy,
    QSpinBox,
    QSplitter,
    QStyle,
    QTextEdit,
    QToolBar,
    QToolButton,
    QTreeWidget,
    QTreeWidgetItem,
    QVBoxLayout,
    QWidget,
    QWidgetAction,
)

from attackgen.emitter import write
from attackgen.geometry import building_anchor, diamond_corners, drop_points
from attackgen.i18n import Translator
from attackgen.model import Drop, Make, Note, Recalc, Script, Wait
from attackgen.parser import parse_file
from attackgen.schema import BUILDINGS, SIDES, UNITS, VERSUS, WAIT_CONDITIONS, TROOPS, SPELLS, HEROES, SIEGES, SPECIAL_UNITS
from attackgen.templates import get_all_templates, save_template
from attackgen.validate import validate

# CSV/Attack lives two folders above this package (attack-generator/attackgen).
_PROJECT_ROOT = Path(__file__).resolve().parents[2]
_DEFAULT_DIR = _PROJECT_ROOT / "CSV" / "Attack"

BRAND = "MyBot ATK GEN by Tony R0XX"

def _build_header_html(i18n: Translator) -> str:
    """Build header HTML with translated strings - only Tony R0XX in blue."""
    title = i18n.tr("app_title")
    subtitle = i18n.tr("app_subtitle")
    # Color only "Tony R0XX" in blue, rest in white
    main_part = "MyBot ATK GENERATOR - "
    author_part = "Tony R0XX"
    return (
        "<div style='font-size:19px; font-weight:800; letter-spacing:0.4px; color:#e6edf3;'>"
        f"{main_part}<span style='color:#58a6ff;'>{author_part}</span>"
        "</div>"
        f"<div style='color:#8b949e; font-size:11px; margin-top:2px;'>{subtitle}</div>"
    )

# Dark, modern theme applied to the whole application. This is Qt style
# sheets, i.e. CSS for widgets.
STYLESHEET = """
QMainWindow, QWidget { background-color: #0d1117; color: #e6edf3; font-size: 12px; }
QLabel { background: transparent; }

QMenuBar { background: #161b22; color: #e6edf3; border-bottom: 1px solid #21262d; }
QMenuBar::item { padding: 5px 12px; background: transparent; border-radius: 4px; }
QMenuBar::item:selected { background: #21262d; }
QMenu { background: #161b22; color: #e6edf3; border: 1px solid #30363d; padding: 4px; }
QMenu::item { padding: 6px 26px; border-radius: 4px; }
QMenu::item:selected { background: #1f6feb; }

QToolBar { background: #161b22; border: none; border-bottom: 1px solid #21262d; spacing: 6px; padding: 5px 8px; }

QPushButton, QToolButton {
    background: #21262d; color: #e6edf3; border: 1px solid #30363d;
    border-radius: 6px; padding: 6px 12px; font-weight: 600;
}
QPushButton:hover, QToolButton:hover { background: #30363d; border-color: #58a6ff; }
QPushButton:pressed, QToolButton:pressed { background: #1f6feb; border-color: #1f6feb; }
QPushButton:disabled { color: #6e7681; border-color: #21262d; }
QPushButton#accent { background: #1f6feb; border-color: #1f6feb; }
QPushButton#accent:hover { background: #2f81f7; }

QTreeWidget {
    background: #0d1117; alternate-background-color: #11161d;
    border: 1px solid #30363d; border-radius: 8px;
}
QTreeWidget::item { padding: 3px 4px; }
QTreeWidget::item:selected { background: #1f6feb; color: #ffffff; }
QHeaderView::section {
    background: #161b22; color: #8b949e; border: none;
    border-bottom: 1px solid #30363d; padding: 6px; font-weight: 600;
}

QLineEdit, QSpinBox, QComboBox, QTextEdit {
    background: #0d1117; color: #e6edf3; border: 1px solid #30363d;
    border-radius: 6px; padding: 5px 8px; selection-background-color: #1f6feb;
}
QLineEdit:focus, QSpinBox:focus, QComboBox:focus, QTextEdit:focus {
    border: 1px solid #58a6ff;
}
QComboBox::drop-down { border: none; width: 20px; }
QComboBox QAbstractItemView {
    background: #161b22; color: #e6edf3; border: 1px solid #30363d;
    selection-background-color: #1f6feb; outline: none;
}
QSpinBox::up-button, QSpinBox::down-button { width: 16px; background: #161b22; border: none; }

QGroupBox {
    border: 1px solid #30363d; border-radius: 8px;
    margin-top: 12px; padding-top: 10px; background: #0f141b;
}
QGroupBox::title { subcontrol-origin: margin; left: 12px; padding: 0 4px; color: #8b949e; }

QCheckBox { spacing: 6px; color: #e6edf3; }
QCheckBox::indicator {
    width: 16px; height: 16px; border: 1px solid #30363d;
    border-radius: 4px; background: #0d1117;
}
QCheckBox::indicator:checked { background: #1f6feb; border-color: #1f6feb; }

QScrollArea { border: none; background: transparent; }
QScrollBar:vertical { background: #0d1117; width: 12px; margin: 0; }
QScrollBar::handle:vertical { background: #30363d; border-radius: 6px; min-height: 24px; }
QScrollBar::handle:vertical:hover { background: #58a6ff; }
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0; }
QScrollBar:horizontal { background: #0d1117; height: 12px; margin: 0; }
QScrollBar::handle:horizontal { background: #30363d; border-radius: 6px; min-width: 24px; }
QScrollBar::handle:horizontal:hover { background: #58a6ff; }
QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal { width: 0; }

QDockWidget { color: #8b949e; }
QDockWidget::title { background: #161b22; padding: 7px; border: 1px solid #21262d; }
QListWidget {
    background: #0d1117; border: 1px solid #30363d; border-radius: 8px;
}
QListWidget::item { padding: 5px 6px; border-radius: 4px; }
QListWidget::item:selected { background: #1f6feb; color: #ffffff; }
QListWidget::item:hover { background: #161b22; }

QSplitter::handle { background: #161b22; }
QSplitter::handle:hover { background: #1f6feb; }
QStatusBar { background: #161b22; color: #8b949e; }
QScrollArea QWidget { background: transparent; }
"""

_PALETTE = (
    QColor(30, 144, 255),
    QColor(255, 140, 0),
    QColor(50, 205, 50),
    QColor(220, 20, 60),
    QColor(138, 43, 226),
    QColor(255, 165, 0),
    QColor(0, 191, 255),
    QColor(255, 69, 0),
    QColor(60, 179, 113),
    QColor(199, 21, 133),
    QColor(0, 128, 128),
    QColor(154, 205, 50),
)


def vector_color(letter: str) -> QColor:
    """Stable colour per vector letter so the legend and canvas always match."""
    letter = (letter or "A").strip().upper()
    index = ord(letter[0]) - ord("A") if letter else 0
    return _PALETTE[index % len(_PALETTE)] if index >= 0 else _PALETTE[0]


def _summary(command) -> str:
    """One line description shown in the tree's summary column."""
    if isinstance(command, Make):
        return (
            f"vector={command.vector}  side={command.side}  points={command.points}"
            f"  add={command.add_tiles}  vs={command.versus}"
            f"  bld={command.building or '-'}"
        )
    if isinstance(command, Drop):
        return (
            f"vector={command.vectors}  index={command.index}  qty={command.quantity}"
            f"  unit={command.unit}  delay={command.delay_points}"
            f"  sleep={command.sleep_after}"
        )
    if isinstance(command, Wait):
        return f"duration={command.duration}  conditions={command.conditions or '-'}"
    if isinstance(command, Recalc):
        return "re-read the attack troop bar"
    if isinstance(command, Note):
        return command.text[:80]
    return ""


class CommandItem(QTreeWidgetItem):
    """Tree row that keeps a reference to the command it represents."""

    def __init__(self, command, index: int):
        super().__init__()
        self.command = command
        self.index = index
        self.setText(0, f"{index + 1}")
        self.setText(1, command.kind)
        self.setText(2, _summary(command))

    def refresh(self, index: int) -> None:
        self.index = index
        self.setText(0, f"{index + 1}")
        self.setText(1, self.command.kind)
        self.setText(2, _summary(self.command))


class PropertyEditor(QWidget):
    """Form that edits the currently selected command in place."""

    changed = Signal()

    def __init__(self, i18n: Translator, parent=None):
        super().__init__(parent)
        self.i18n = i18n
        self._command = None
        outer = QVBoxLayout(self)
        self._form = QFormLayout()
        outer.addLayout(self._form)
        outer.addStretch()

    def set_command(self, command):
        self._command = command
        self._rebuild()

    def retranslate(self) -> None:
        self._rebuild()

    def _prefix(self) -> str | None:
        if isinstance(self._command, Make):
            return "make"
        if isinstance(self._command, Drop):
            return "drop"
        if isinstance(self._command, Wait):
            return "wait"
        if isinstance(self._command, Note):
            return "note"
        return None

    def _label(self, name: str) -> str:
        prefix = self._prefix()
        if prefix is None:
            return name
        return self.i18n.field_name(f"{prefix}.{name}")

    def _help(self, name: str) -> str:
        prefix = self._prefix()
        if prefix is None:
            return ""
        return self.i18n.field_help(f"{prefix}.{name}")

    def _clear(self) -> None:
        while self._form.rowCount():
            self._form.removeRow(0)

    def _rebuild(self) -> None:
        self._clear()
        command = self._command
        if command is None:
            self._form.addRow(QLabel(self.i18n.tr("help_none")))
            return

        if isinstance(command, Make):
            self._add_combo("vector", command.vector, [chr(c) for c in range(65, 91)])
            self._add_combo("side", command.side, SIDES)
            self._add_spin("points", command.points, 1, 20)
            self._add_spin("add_tiles", command.add_tiles, -40, 40)
            self._add_combo("versus", command.versus, VERSUS)
            self._add_spin("random_x", command.random_x, 0, 200)
            self._add_spin("random_y", command.random_y, 0, 200)
            self._add_combo("building", command.building, [""] + list(BUILDINGS))
        elif isinstance(command, Drop):
            # Vector selector - shows available vectors from MAKE commands
            vectors = self._get_available_vectors()
            if vectors:
                self._add_combo("vectors", command.vectors, vectors, editable=True)
            else:
                self._add_line("vectors", command.vectors)
            self._add_line("index", command.index)
            self._add_line("quantity", command.quantity)
            self._add_combo("unit", command.unit, self._unit_options(), editable=True)
            self._add_line("delay_points", command.delay_points)
            self._add_line("delay_change", command.delay_change)
            self._add_line("sleep_after", command.sleep_after)
        elif isinstance(command, Wait):
            self._add_line("duration", command.duration)
            self._add_combo(
                "conditions", command.conditions, [""] + list(WAIT_CONDITIONS), editable=True
            )
        elif isinstance(command, Note):
            edit = QLineEdit(command.text)
            edit.setToolTip(self._help("text"))
            edit.editingFinished.connect(lambda: self._set("text", edit.text()))
            self._form.addRow(self._label("text"), edit)
        elif isinstance(command, Recalc):
            self._form.addRow(QLabel("RECALC"))

    def _add_line(self, name: str, value: str) -> None:
        edit = QLineEdit(value)
        edit.setToolTip(self._help(name))
        edit.editingFinished.connect(lambda: self._set(name, edit.text()))
        self._form.addRow(self._label(name), edit)

    def _add_spin(self, name: str, value: int, minimum: int, maximum: int) -> None:
        spin = QSpinBox()
        spin.setRange(minimum, maximum)
        spin.setValue(value)
        spin.setToolTip(self._help(name))
        spin.valueChanged.connect(lambda v: self._set(name, v))
        self._form.addRow(self._label(name), spin)

    def _add_combo(
        self, name: str, value: str, options: list[str], editable: bool = False
    ) -> None:
        # Special handling for unit field: custom compact dropdown
        if name == "unit" and hasattr(self, '_unit_options') and options == self._unit_options():
            unit_widget = UnitComboWidget(value, options, self._help(name), self)
            unit_widget.valueChanged.connect(lambda v: self._set(name, v))
            self._form.addRow(self._label(name), unit_widget)
        else:
            combo = QComboBox()
            combo.addItems(options)
            combo.setEditable(editable)
            combo.setCurrentText(value)
            combo.setToolTip(self._help(name))
            combo.currentTextChanged.connect(lambda v: self._set(name, v))
            self._form.addRow(self._label(name), combo)

    def _set(self, name: str, value) -> None:
        if self._command is None:
            return
        setattr(self._command, name, value)
        self.changed.emit()

    def _unit_options(self) -> list[str]:
        """Flat list of all deployable units for DROP unit combo."""
        options = []
        # Troops
        for short, name, space in TROOPS:
            options.append(short)
        # Spells
        for short, name, space in SPELLS:
            options.append(short)
        # Heroes
        for short, name in HEROES:
            options.append(short)
        # Sieges
        for short, name in SIEGES:
            options.append(short)
        # Special
        for short in SPECIAL_UNITS:
            options.append(short)
        return options

    def _get_available_vectors(self) -> list[str]:
        """Get vector letters from MAKE commands in the script."""
        # We need access to the main window's script - this will be set externally
        if hasattr(self, '_main_script') and self._main_script:
            return [m.vector.strip().upper() for m in self._main_script.makes() if m.vector.strip()]
        return []


class UnitComboWidget(QWidget):
    """Custom compact dropdown for unit selection with search and categorized list."""
    
    valueChanged = Signal(str)
    
    def __init__(self, current_value: str, all_options: list[str], tooltip: str, parent=None):
        super().__init__(parent)
        self.all_options = [opt for opt in all_options if not opt.startswith("---")]
        self.current_value = current_value
        
        # Main layout - button that opens the menu
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        self.button = QToolButton()
        self.button.setText(current_value)
        self.button.setToolTip(tooltip)
        self.button.setPopupMode(QToolButton.InstantPopup)
        self.button.setFixedHeight(26)
        self.button.setMinimumWidth(120)
        self.button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.button.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.button.setArrowType(Qt.DownArrow)
        
        # Create menu with list widget
        self.menu = QMenu(self)
        self.menu.setMinimumWidth(180)
        self.menu.setMaximumWidth(220)
        
        # Search box at top of menu
        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText("Buscar...")
        self.search_box.setFixedHeight(24)
        self.search_box.textChanged.connect(self._filter_list)
        
        search_action = QWidgetAction(self.menu)
        search_action.setDefaultWidget(self.search_box)
        self.menu.addAction(search_action)
        self.menu.addSeparator()
        
        # List widget for options
        self.list_widget = QListWidget()
        self.list_widget.setMaximumHeight(300)  # Compact max height
        self.list_widget.setMinimumWidth(160)
        self.list_widget.setFrameShape(QListWidget.NoFrame)
        self.list_widget.itemClicked.connect(self._on_item_clicked)
        self.list_widget.setVerticalScrollMode(QListWidget.ScrollPerPixel)
        
        list_action = QWidgetAction(self.menu)
        list_action.setDefaultWidget(self.list_widget)
        self.menu.addAction(list_action)
        
        self.button.setMenu(self.menu)
        
        # Populate list
        self._populate_list("")
        
        # Set current value
        self._set_current_display(current_value)
        
        layout.addWidget(self.button)
    
    def _populate_list(self, filter_text: str):
        """Populate the list widget with filtered options."""
        self.list_widget.clear()
        filter_lower = filter_text.lower()
        
        # Categorized sections
        categories = [
            ("Tropas", TROOPS),
            ("Feitiços", SPELLS),
            ("Heróis", HEROES),
            ("Sieges", SIEGES),
            ("Especiais", [(s, s, 0) for s in SPECIAL_UNITS]),
        ]
        
        for cat_name, cat_data in categories:
            # Add category header
            header_item = QListWidgetItem(f"── {cat_name} ──")
            header_item.setFlags(Qt.NoItemFlags)
            header_item.setBackground(QColor(30, 38, 48))
            header_item.setForeground(QColor(139, 148, 158))
            font = header_item.font()
            font.setBold(True)
            header_item.setFont(font)
            self.list_widget.addItem(header_item)
            
            for entry in cat_data:
                if len(entry) == 3:
                    short, name, space = entry
                else:
                    short, name = entry
                    space = 0
                
                if filter_lower and filter_lower not in short.lower() and filter_lower not in name.lower():
                    continue
                
                item = QListWidgetItem(f"{short}  —  {name}")
                item.setData(Qt.UserRole, short)
                item.setToolTip(f"{name} (espaço: {space})" if space else name)
                self.list_widget.addItem(item)
                
                # Select current value
                if short == self.current_value:
                    self.list_widget.setCurrentItem(item)
    
    def _filter_list(self, text: str):
        self._populate_list(text)
    
    def _on_item_clicked(self, item: QListWidgetItem):
        short = item.data(Qt.UserRole)
        if short:
            self.current_value = short
            self._set_current_display(short)
            self.menu.hide()
            self.valueChanged.emit(short)
    
    def _set_current_display(self, value: str):
        self.button.setText(value)
        self.current_value = value


class PreviewCanvas(QWidget):
    """Drawing of the reference redline and the MAKE vectors.
    
    Expands to fill available space. Minimum size ensures usability.
    Supports Zoom (wheel) and Pan (middle/right drag)."""

    pointClicked = Signal(str, int)  # vector letter, point index (1-based)
    mouseCoords = Signal(float, float) # canvas coordinates

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(600, 450)  # Minimum usable size
        self._script: Script | None = None
        self._visible: set[str] | None = None
        self._highlight: set[str] = set()
        self._point_radius = 10  # hit radius in screen pixels
        self.setMouseTracking(True)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        # Zoom & Pan state
        self._zoom = 1.0
        self._pan = QPointF(0.0, 0.0)
        self._dragging = False
        self._drag_start = QPointF(0.0, 0.0)

    def set_script(self, script: Script) -> None:
        self._script = script
        self.update()

    def set_visible(self, letters: set[str] | None) -> None:
        self._visible = letters
        self.update()

    def set_highlight(self, letters: set[str]) -> None:
        self._highlight = {l.upper() for l in letters}
        self.update()

    def reset_view(self) -> None:
        self._zoom = 1.0
        self._pan = QPointF(0.0, 0.0)
        self.update()

    def wheelEvent(self, event) -> None:  # noqa: N802
        factor = 1.15
        if event.angleDelta().y() < 0:
            factor = 1.0 / factor
        
        old_zoom = self._zoom
        new_zoom = max(0.5, min(5.0, old_zoom * factor))
        
        # Zoom toward mouse position
        pos = event.position()
        self._pan = pos - (pos - self._pan) * (new_zoom / old_zoom)
        self._zoom = new_zoom
        self.update()

    def mousePressEvent(self, event) -> None:  # noqa: N802
        if event.button() in (Qt.MiddleButton, Qt.RightButton):
            self._dragging = True
            self._drag_start = event.position() - self._pan
            return
            
        if event.button() != Qt.LeftButton or not self._script:
            return
            
        pos = event.position()
        to_screen = self._mapper()

        # Check each vector's points
        for make in self._script.makes():
            letter = make.vector.strip().upper()
            if self._visible is not None and letter not in self._visible:
                continue
            points = [to_screen(p) for p in drop_points(make.side, make.points, make.add_tiles)]
            for idx, pt in enumerate(points, start=1):
                dx = pos.x() - pt.x()
                dy = pos.y() - pt.y()
                if dx * dx + dy * dy <= self._point_radius * self._point_radius:
                    self.pointClicked.emit(letter, idx)
                    return

        super().mousePressEvent(event)

    def mouseMoveEvent(self, event) -> None:  # noqa: N802
        if self._dragging:
            self._pan = event.position() - self._drag_start
            self.update()
            return
            
        # Emit coordinates in map space (860x732 base)
        pos = event.position()
        width, height = self.width(), self.height()
        base_scale_x = width / 860.0
        base_scale_y = height / 732.0
        
        map_x = (pos.x() - self._pan.x()) / (base_scale_x * self._zoom)
        map_y = (pos.y() - self._pan.y()) / (base_scale_y * self._zoom)
        self.mouseCoords.emit(map_x, map_y)
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event) -> None:  # noqa: N802
        if event.button() in (Qt.MiddleButton, Qt.RightButton):
            self._dragging = False
            return
        super().mouseReleaseEvent(event)

    def _mapper(self):
        width, height = self.width(), self.height()
        base_scale_x = width / 860.0
        base_scale_y = height / 732.0

        def to_screen(point) -> QPointF:
            x = point.x * base_scale_x * self._zoom + self._pan.x()
            y = point.y * base_scale_y * self._zoom + self._pan.y()
            return QPointF(x, y)

        return to_screen

    def paintEvent(self, event) -> None:  # noqa: N802 (Qt naming)
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.fillRect(self.rect(), QColor(13, 17, 23))

        # Subtle grid for a modern, technical look.
        painter.setPen(QPen(QColor(27, 36, 48), 1))
        step = 32
        for x in range(0, self.width(), step):
            painter.drawLine(x, 0, x, self.height())
        for y in range(0, self.height(), step):
            painter.drawLine(0, y, self.width(), y)

        to_screen = self._mapper()
        corners = diamond_corners()
        polygon = [to_screen(corners[key]) for key in ("top", "right", "bottom", "left")]
        painter.setPen(QPen(QColor(229, 83, 75), 2, Qt.DashLine))
        painter.drawPolygon(QPolygonF(polygon))

        if not self._script:
            painter.setPen(QColor(110, 118, 129))
            painter.drawText(self.rect(), Qt.AlignCenter, "..")
            return

        dim = bool(self._highlight)
        for make in self._script.makes():
            letter = make.vector.strip().upper()
            if self._visible is not None and letter not in self._visible:
                continue

            base = vector_color(letter)
            if dim and letter not in self._highlight:
                color = QColor(base)
                color.setAlpha(60)
            else:
                color = base

            points = [to_screen(p) for p in drop_points(make.side, make.points, make.add_tiles)]
            if len(points) >= 2:
                painter.setPen(QPen(color, 3 if (dim and letter in self._highlight) else 2))
                for a, b in zip(points, points[1:]):
                    painter.drawLine(a, b)

            painter.setFont(QFont("Consolas", 11))
            painter.setPen(QPen(color))
            for step, point in enumerate(points, start=1):
                painter.setBrush(QBrush(color))
                painter.drawEllipse(point, 5, 5)
                # Opposite side from vector name (which is at +6, +14 from middle)
                painter.drawText(point + QPointF(-24, -16), f"{make.vector}{step}")

            if points:
                painter.setFont(QFont("Consolas", 11, QFont.Bold))
                mid = points[len(points) // 2]
                painter.drawText(mid + QPointF(6, 14), make.vector)

        for make in self._script.makes():
            if not make.building:
                continue
            letter = make.vector.strip().upper()
            if self._visible is not None and letter not in self._visible:
                continue
            anchor = to_screen(building_anchor(make.building))
            painter.setBrush(QBrush(QColor(255, 90, 90, 200)))
            painter.setPen(QPen(QColor(160, 0, 0), 2))
            painter.drawEllipse(anchor, 7, 7)
            painter.setFont(QFont("Consolas", 7))
            painter.drawText(anchor + QPointF(10, 4), make.building)

    def mousePressEvent(self, event) -> None:  # noqa: N802
        if event.button() != Qt.LeftButton or not self._script:
            return
        pos = event.position()
        to_screen = self._mapper()

        # Check each vector's points
        for make in self._script.makes():
            letter = make.vector.strip().upper()
            if self._visible is not None and letter not in self._visible:
                continue
            points = [to_screen(p) for p in drop_points(make.side, make.points, make.add_tiles)]
            for idx, pt in enumerate(points, start=1):
                dx = pos.x() - pt.x()
                dy = pos.y() - pt.y()
                if dx * dx + dy * dy <= self._point_radius * self._point_radius:
                    self.pointClicked.emit(letter, idx)
                    return

        super().mousePressEvent(event)


class VectorLegend(QGroupBox):
    """Show / hide each vector so overlapping lines can be separated.
    
    Can be used in vertical mode (dock) or horizontal mode (toolbar above canvas)."""

    visibilityChanged = Signal()

    def __init__(self, i18n: Translator, horizontal: bool = False, parent=None):
        super().__init__(parent)
        self.i18n = i18n
        self.horizontal = horizontal
        self._checks: dict[str, QCheckBox] = {}
        self._infos: dict[str, str] = {}

        outer = QHBoxLayout(self) if horizontal else QVBoxLayout(self)
        outer.setContentsMargins(4, 2, 4, 2)
        outer.setSpacing(4)

        if horizontal:
            # Ultra-compact horizontal: just one row of checkboxes with color swatches
            self._btn_show = QPushButton()
            self._btn_hide = QPushButton()
            self._btn_show.setToolTip(self.i18n.tr("legend_show_all"))
            self._btn_hide.setToolTip(self.i18n.tr("legend_hide_all"))
            self._btn_show.setMaximumWidth(60)
            self._btn_hide.setMaximumWidth(60)
            self._btn_show.clicked.connect(lambda: self._set_all(True))
            self._btn_hide.clicked.connect(lambda: self._set_all(False))
            outer.addWidget(self._btn_show)
            outer.addWidget(self._btn_hide)
            outer.addSpacing(6)

            # Direct horizontal layout - NO scroll area, just flows naturally
            self._rows = QHBoxLayout()
            self._rows.setContentsMargins(0, 0, 0, 0)
            self._rows.setSpacing(8)
            outer.addLayout(self._rows, 1)
        else:
            # Original vertical layout for dock
            buttons = QHBoxLayout()
            self._btn_show = QPushButton()
            self._btn_hide = QPushButton()
            self._btn_show.clicked.connect(lambda: self._set_all(True))
            self._btn_hide.clicked.connect(lambda: self._set_all(False))
            buttons.addWidget(self._btn_show)
            buttons.addWidget(self._btn_hide)
            buttons.addStretch()
            outer.addLayout(buttons)

            self._scroll = QScrollArea()
            self._scroll.setWidgetResizable(True)
            self._container = QWidget()
            self._rows = QVBoxLayout(self._container)
            self._rows.addStretch()
            self._scroll.setWidget(self._container)
            outer.addWidget(self._scroll)

            self._empty = QLabel()
            self._empty.setWordWrap(True)
            outer.addWidget(self._empty)

        self.retranslate()
        self.set_makes([])

    def retranslate(self) -> None:
        if self.horizontal:
            self.setTitle("")  # no title in horizontal mode
            self._btn_show.setText("☑")
            self._btn_hide.setText("☐")
            self._btn_show.setToolTip(self.i18n.tr("legend_show_all"))
            self._btn_hide.setToolTip(self.i18n.tr("legend_hide_all"))
        else:
            self.setTitle(self.i18n.tr("legend_title"))
            self._btn_show.setText(self.i18n.tr("legend_show_all"))
            self._btn_hide.setText(self.i18n.tr("legend_hide_all"))
            self._empty.setText(self.i18n.tr("legend_empty"))

    def set_makes(self, makes) -> None:
        previous = None
        if self._checks:
            previous = {letter for letter, check in self._checks.items() if check.isChecked()}

        # Clear existing rows.
        while self._rows.count():
            item = self._rows.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()
        self._checks.clear()
        self._infos.clear()

        seen: dict[str, object] = {}
        order: list[str] = []
        for make in makes:
            letter = make.vector.strip().upper()
            if not letter or letter in seen:
                continue
            seen[letter] = make
            order.append(letter)

        if not order:
            if not self.horizontal:
                self._empty.show()
                self._rows.addStretch()
            return

        if not self.horizontal:
            self._empty.hide()

        for letter in order:
            make = seen[letter]
            info = f"  {make.side}  ({make.points})"
            self._infos[letter] = info

            row = QWidget()
            row_layout = QHBoxLayout(row)
            row_layout.setContentsMargins(2, 0, 2, 0)
            row_layout.setSpacing(4)

            swatch = QLabel()
            swatch.setFixedSize(12, 12)
            color = vector_color(letter).name()
            swatch.setStyleSheet(f"background:{color}; border:1px solid #333; border-radius:2px;")
            row_layout.addWidget(swatch)

            check = QCheckBox(f"{letter}")
            checked = True if previous is None else (letter in previous)
            check.setChecked(checked)
            check.stateChanged.connect(lambda _state=0: self.visibilityChanged.emit())
            row_layout.addWidget(check)

            self._checks[letter] = check
            self._rows.addWidget(row)

        if self.horizontal:
            self._rows.addStretch()

    def _set_all(self, checked: bool) -> None:
        for check in self._checks.values():
            check.setChecked(checked)
        self.visibilityChanged.emit()

    def visible_letters(self) -> set[str] | None:
        if not self._checks:
            return None
        return {letter for letter, check in self._checks.items() if check.isChecked()}


class TemplateDialog(QDialog):
    """Dialog for selecting a template with categories, import/export."""
    
    def __init__(self, i18n: Translator, parent=None):
        super().__init__(parent)
        self.i18n = i18n
        self.setWindowTitle(i18n.tr("action_template"))
        self.resize(450, 500)
        self.selected: str | None = None
        
        layout = QVBoxLayout(self)
        
        # Toolbar
        toolbar = QHBoxLayout()
        
        # Category filter
        self._category_combo = QComboBox()
        self._category_combo.addItem("Todas")
        self._category_combo.addItems(["Ataque Aéreo", "Híbrido", "Farm", "Guerra", "Push", "Outros"])
        self._category_combo.currentTextChanged.connect(self._filter_by_category)
        toolbar.addWidget(QLabel("Categoria:"))
        toolbar.addWidget(self._category_combo)
        toolbar.addStretch()
        
        # Import/Export buttons
        btn_import = QPushButton("Importar...")
        btn_import.clicked.connect(self._import_template)
        btn_export = QPushButton("Exportar...")
        btn_export.clicked.connect(self._export_template)
        toolbar.addWidget(btn_import)
        toolbar.addWidget(btn_export)
        
        layout.addLayout(toolbar)
        
        # Template list
        self._list = QListWidget()
        self._all_templates = get_all_templates()
        self._populate_list()
        self._list.itemDoubleClicked.connect(lambda _: self.accept())
        layout.addWidget(self._list)
        
        # Info label
        self._info_label = QLabel("Selecione um modelo para ver detalhes")
        self._info_label.setWordWrap(True)
        self._info_label.setStyleSheet("color: #8b949e; font-size: 11px; padding: 4px;")
        layout.addWidget(self._info_label)
        self._list.currentItemChanged.connect(self._update_info)
        
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    def _populate_list(self):
        self._list.clear()
        category = self._category_combo.currentText()
        for name, builder in sorted(self._all_templates.items()):
            # For now, all templates go in "Outros" unless we have metadata
            # In a real implementation, templates would have category metadata
            if category == "Todas" or category == "Outros":
                self._list.addItem(name)

    def _filter_by_category(self, category: str):
        self._populate_list()

    def _update_info(self, current, _previous):
        if current:
            name = current.text()
            builder = self._all_templates.get(name)
            if builder:
                # Create a temporary script to inspect
                script = builder(name)
                cmd_counts = {}
                for cmd in script.commands:
                    cmd_counts[cmd.kind] = cmd_counts.get(cmd.kind, 0) + 1
                info = f"<b>{name}</b><br>"
                info += f"Comandos: {len(script.commands)}<br>"
                for kind, count in cmd_counts.items():
                    info += f"  {kind}: {count}<br>"
                self._info_label.setText(info)

    def _import_template(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "Importar Modelo", "", "JSON (*.json);;ZIP (*.zip)"
        )
        if path:
            try:
                if path.endswith('.zip'):
                    import zipfile
                    with zipfile.ZipFile(path, 'r') as zf:
                        zf.extractall(Path(__file__).resolve().parents[1] / "templates")
                else:
                    import shutil
                    dest = Path(__file__).resolve().parents[1] / "templates" / Path(path).name
                    shutil.copy2(path, dest)
                self._all_templates = get_all_templates()
                self._populate_list()
                QMessageBox.information(self, "Sucesso", "Modelo importado com sucesso!")
            except Exception as e:
                QMessageBox.critical(self, "Erro", f"Falha ao importar: {e}")

    def _export_template(self):
        item = self._list.currentItem()
        if not item:
            QMessageBox.warning(self, "Aviso", "Selecione um modelo para exportar.")
            return
        name = item.text()
        path, _ = QFileDialog.getSaveFileName(
            self, "Exportar Modelo", f"{name}.json", "JSON (*.json);;ZIP (*.zip)"
        )
        if path:
            try:
                import json
                builder = self._all_templates[name]
                script = builder(name)
                data = {
                    "name": name,
                    "commands": [
                        {
                            "kind": c.kind,
                            "vector": getattr(c, "vector", ""),
                            "side": getattr(c, "side", ""),
                            "points": getattr(c, "points", 0),
                            "add_tiles": getattr(c, "add_tiles", 0),
                            "versus": getattr(c, "versus", ""),
                            "random_x": getattr(c, "random_x", 0),
                            "random_y": getattr(c, "random_y", 0),
                            "building": getattr(c, "building", ""),
                            "vectors": getattr(c, "vectors", ""),
                            "index": getattr(c, "index", ""),
                            "quantity": getattr(c, "quantity", ""),
                            "unit": getattr(c, "unit", ""),
                            "delay_points": getattr(c, "delay_points", ""),
                            "delay_change": getattr(c, "delay_change", ""),
                            "sleep_after": getattr(c, "sleep_after", ""),
                            "duration": getattr(c, "duration", 0),
                            "conditions": getattr(c, "conditions", ""),
                            "text": getattr(c, "text", ""),
                        }
                        for c in script.commands
                    ]
                }
                if path.endswith('.zip'):
                    import zipfile
                    with zipfile.ZipFile(path, 'w') as zf:
                        zf.writestr(f"{name}.json", json.dumps(data, indent=2))
                else:
                    with open(path, 'w', encoding='utf-8') as f:
                        json.dump(data, f, indent=2, ensure_ascii=False)
                QMessageBox.information(self, "Sucesso", "Modelo exportado com sucesso!")
            except Exception as e:
                QMessageBox.critical(self, "Erro", f"Falha ao exportar: {e}")

    def accept(self) -> None:
        item = self._list.currentItem()
        if item:
            self.selected = item.text()
            super().accept()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.i18n = Translator("pt")
        self.resize(1360, 900)

        # Window icon (works in dev and PyInstaller bundle)
        self._set_window_icon()

        self.script = Script(name="NewAttack")
        self.current_file: Path | None = None
        self._current = None
        self._selected_index: int | None = None
        
        # Undo/Redo stack
        self._undo_stack: list[Script] = []
        self._redo_stack: list[Script] = []
        self._max_undo = 50

        self._build_toolbar()
        self._build_central()
        self._build_docks()
        self._build_menu()

        self.retranslate()
        self._rebuild_tree()
        self._refresh_validation()

    def _set_window_icon(self) -> None:
        """Set window icon for title bar and taskbar."""
        from PySide6.QtGui import QIcon
        import sys
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        if hasattr(sys, '_MEIPASS'):
            icon_path = Path(sys._MEIPASS) / "icon.ico"
        else:
            icon_path = Path(__file__).resolve().parents[1] / "icon.ico"
        if icon_path.exists():
            self.setWindowIcon(QIcon(str(icon_path)))

    # ------------------------------------------------------------------ UI ---
    def _build_toolbar(self) -> None:
        toolbar = QToolBar()
        toolbar.setMovable(False)
        
        # Undo/Redo
        self._act_undo = QAction(self, shortcut="Ctrl+Z", triggered=self._undo)
        self._act_redo = QAction(self, shortcut="Ctrl+Y", triggered=self._redo)
        toolbar.addAction(self._act_undo)
        toolbar.addAction(self._act_redo)
        toolbar.addSeparator()
        
        # Copy/Paste
        self._act_copy = QAction(self, shortcut="Ctrl+C", triggered=self._copy_commands)
        self._act_paste = QAction(self, shortcut="Ctrl+V", triggered=self._paste_commands)
        self._act_duplicate = QAction(self, shortcut="Ctrl+D", triggered=self._duplicate_commands)
        toolbar.addAction(self._act_copy)
        toolbar.addAction(self._act_paste)
        toolbar.addAction(self._act_duplicate)
        toolbar.addSeparator()
        
        # Canvas controls
        self._act_reset_view = QAction(self, shortcut="Home", triggered=self._reset_canvas_view)
        toolbar.addAction(self._act_reset_view)
        toolbar.addSeparator()
        
        self._language_button = QPushButton()
        self._language_button.clicked.connect(self._toggle_language)
        toolbar.addWidget(self._language_button)
        self.addToolBar(toolbar)
        
        # Update undo/redo enabled state
        self._update_undo_redo_actions()

    def _build_central(self) -> None:
        # Main horizontal splitter: Left (tree) | Center (canvas + horizontal legend) | Right (templates + props)
        splitter = QSplitter(Qt.Horizontal)

        # ========== LEFT: Command tree + buttons ==========
        left = QWidget()
        left_layout = QVBoxLayout(left)
        left_layout.setContentsMargins(0, 0, 0, 0)
        self.tree = QTreeWidget()
        self.tree.setColumnWidth(0, 44)
        self.tree.setColumnWidth(1, 96)
        self.tree.currentItemChanged.connect(self._on_select)
        left_layout.addWidget(self.tree)

        self._buttons: dict[str, QPushButton] = {}
        add_row = QHBoxLayout()
        for key, factory in (
            ("btn_make", lambda: Make()),
            ("btn_drop", lambda: Drop()),
            ("btn_wait", lambda: Wait()),
            ("btn_note", lambda: Note()),
            ("btn_recalc", lambda: Recalc()),
        ):
            button = QPushButton()
            button.clicked.connect(lambda _=False, f=factory: self._add_command(f()))
            button.setToolTip(self.i18n.tr(f"{key}_tooltip"))
            self._buttons[key] = button
            add_row.addWidget(button)
        left_layout.addLayout(add_row)

        order_row = QHBoxLayout()
        for key, slot in (
            ("btn_delete", self._delete_selected),
            ("btn_up", lambda: self._move_selected(-1)),
            ("btn_down", lambda: self._move_selected(1)),
        ):
            button = QPushButton()
            button.clicked.connect(slot)
            button.setToolTip(self.i18n.tr(f"{key}_tooltip"))
            self._buttons[key] = button
            order_row.addWidget(button)
        left_layout.addLayout(order_row)

        splitter.addWidget(left)

        # ========== CENTER: Canvas with horizontal legend on top ==========
        center = QWidget()
        center_layout = QVBoxLayout(center)
        center_layout.setContentsMargins(0, 0, 0, 0)
        center_layout.setSpacing(0)

        # Horizontal legend toolbar above canvas
        self.legend = VectorLegend(self.i18n, horizontal=True)
        self.legend.visibilityChanged.connect(self._apply_visibility)
        center_layout.addWidget(self.legend)

        # Canvas - takes all remaining space
        self.preview = PreviewCanvas()
        self.preview.pointClicked.connect(self._on_canvas_point_clicked)
        center_layout.addWidget(self.preview, 1)

        splitter.addWidget(center)

        # ========== RIGHT: Vertical split - Templates (top) / Properties (bottom) ==========
        right_splitter = QSplitter(Qt.Vertical)

        # Templates panel (top)
        self._dock_templates_widget = QWidget()
        templates_layout = QVBoxLayout(self._dock_templates_widget)
        templates_layout.setContentsMargins(0, 0, 0, 0)
        
        templates_header = QLabel()
        templates_header.setObjectName("panelHeader")
        templates_layout.addWidget(templates_header)
        
        self.template_list = QListWidget()
        self.template_list.itemDoubleClicked.connect(lambda item: self._load_template(item.text()))
        self.template_list.setContextMenuPolicy(Qt.CustomContextMenu)
        self.template_list.customContextMenuRequested.connect(self._show_template_context_menu)
        templates_layout.addWidget(self.template_list, 1)
        
        right_splitter.addWidget(self._dock_templates_widget)

        # Properties panel (bottom) - was below canvas before
        self.props = PropertyEditor(self.i18n)
        self.props._main_script = self.script  # Reference for vector selector
        self.props.changed.connect(self._on_property_changed)
        props_scroll = QScrollArea()
        props_scroll.setWidgetResizable(True)
        props_scroll.setWidget(self.props)
        right_splitter.addWidget(props_scroll)

        right_splitter.setSizes([300, 500])
        splitter.addWidget(right_splitter)

        # Final sizes: Left=340, Center=650, Right=300
        splitter.setSizes([340, 650, 300])

        # Top header with brand
        self.header = QLabel(_build_header_html(self.i18n))
        self.header.setTextFormat(Qt.RichText)
        self.header.setObjectName("brandHeader")

        container = QWidget()
        container_layout = QVBoxLayout(container)
        container_layout.setContentsMargins(10, 8, 10, 8)
        container_layout.setSpacing(8)
        container_layout.addWidget(self.header)
        container_layout.addWidget(splitter, 1)
        self.setCentralWidget(container)

    def _build_docks(self) -> None:
        self._dock_validation = QDockWidget()
        self.validation_list = QListWidget()
        self._dock_validation.setWidget(self.validation_list)
        self.addDockWidget(Qt.BottomDockWidgetArea, self._dock_validation)

    def _build_menu(self) -> None:
        menu = self.menuBar()

        self._menu_file = menu.addMenu("")
        self._menu_edit = menu.addMenu("")
        self._menu_help = menu.addMenu("")

        self._act = {
            "new": QAction(self, shortcut="Ctrl+N", triggered=self._new_script),
            "open": QAction(self, shortcut="Ctrl+O", triggered=self._open_file),
            "save": QAction(self, shortcut="Ctrl+S", triggered=self._save_file),
            "save_as": QAction(self, shortcut="Ctrl+Shift+S", triggered=self._save_file_as),
            "export": QAction(self, triggered=self._save_file_as),
            "save_template": QAction(self, shortcut="Ctrl+M", triggered=self._save_as_template),
            "exit": QAction(self, triggered=self.close),
            "template": QAction(self, shortcut="Ctrl+T", triggered=self._new_from_template),
            "validate": QAction(self, shortcut="F7", triggered=self._refresh_validation),
            "units": QAction(self, triggered=self._show_shortnames),
        }

        for key in ("new", "open", "save", "save_as"):
            self._menu_file.addAction(self._act[key])
        self._menu_file.addSeparator()
        self._menu_file.addAction(self._act["export"])
        self._menu_file.addSeparator()
        self._menu_file.addAction(self._act["save_template"])
        self._menu_file.addSeparator()
        self._menu_file.addAction(self._act["exit"])

        self._menu_edit.addAction(self._act["template"])
        self._menu_edit.addAction(self._act["validate"])

        self._menu_help.addAction(self._act["units"])

    # --------------------------------------------------------- language -----
    def _toggle_language(self) -> None:
        self.i18n.lang = "en" if self.i18n.lang == "pt" else "pt"
        self.retranslate()

    def retranslate(self) -> None:
        self.setWindowTitle(self.i18n.tr("app_title"))
        self._language_button.setText(self.i18n.lang.upper())
        self._language_button.setObjectName("accent")
        self._language_button.setToolTip(
            "Mudar para English" if self.i18n.lang == "pt" else "Switch to Português (BR)"
        )

        # Update header with translated strings
        self.header.setText(_build_header_html(self.i18n))

        self._menu_file.setTitle(self.i18n.tr("menu_file"))
        self._menu_edit.setTitle(self.i18n.tr("menu_edit"))
        self._menu_help.setTitle(self.i18n.tr("menu_help"))

        for key, action in self._act.items():
            action.setText(self.i18n.tr(f"action_{key}"))

        # Update toolbar actions
        self._act_undo.setText(self.i18n.tr("action_undo"))
        self._act_redo.setText(self.i18n.tr("action_redo"))
        self._act_copy.setText(self.i18n.tr("action_copy"))
        self._act_paste.setText(self.i18n.tr("action_paste"))
        self._act_duplicate.setText(self.i18n.tr("action_duplicate"))
        self._act_reset_view.setText(self.i18n.tr("action_reset_view"))

        self.tree.setHeaderLabels(
            [self.i18n.tr("tree_num"), self.i18n.tr("tree_command"), self.i18n.tr("tree_summary")]
        )
        for key, button in self._buttons.items():
            button.setText(self.i18n.tr(key))
            button.setToolTip(self.i18n.tr(f"{key}_tooltip"))
        self._dock_validation.setWindowTitle(self.i18n.tr("dock_validation"))

        # Update templates panel header
        if hasattr(self, '_dock_templates_widget'):
            header = self._dock_templates_widget.findChild(QLabel, "panelHeader")
            if header:
                header.setText(self.i18n.tr("dock_templates"))

        self.legend.retranslate()
        self.props.retranslate()
        self._refresh_template_list(self.template_list)

        self._refresh_validation()

    # ------------------------------------------------------------- actions ---
    def _new_script(self) -> None:
        self.script = Script(name="NewAttack")
        self.current_file = None
        self._rebuild_tree()
        self._refresh_validation()

    def _new_from_template(self) -> None:
        dialog = TemplateDialog(self.i18n, self)
        if dialog.exec() and dialog.selected:
            self._load_template(dialog.selected)

    def _refresh_template_list(self, list_widget: QListWidget) -> None:
        list_widget.clear()
        for name in sorted(get_all_templates()):
            list_widget.addItem(name)

    def _show_template_context_menu(self, pos) -> None:
        """Show context menu for template list (right-click)."""
        item = self.template_list.itemAt(pos)
        if not item:
            return
        
        template_name = item.text()
        menu = QMenu(self)
        
        # Load template
        act_load = menu.addAction("Carregar modelo")
        act_load.triggered.connect(lambda: self._load_template(template_name))
        
        menu.addSeparator()
        
        # Open containing folder
        act_open_folder = menu.addAction("Abrir pasta de modelos")
        act_open_folder.triggered.connect(self._open_templates_folder)
        
        # Rename template
        act_rename = menu.addAction("Renomear...")
        act_rename.triggered.connect(lambda: self._rename_template(template_name))
        
        # Delete template
        act_delete = menu.addAction("Excluir modelo")
        act_delete.setIcon(self.style().standardIcon(QStyle.SP_TrashIcon))
        act_delete.triggered.connect(lambda: self._delete_template(template_name))
        
        menu.exec(self.template_list.mapToGlobal(pos))

    def _open_templates_folder(self) -> None:
        """Open the templates folder in file explorer."""
        import subprocess
        from pathlib import Path
        templates_dir = Path(__file__).resolve().parents[1] / "templates"
        templates_dir.mkdir(parents=True, exist_ok=True)
        subprocess.run(["explorer", str(templates_dir)], shell=True)

    def _rename_template(self, old_name: str) -> None:
        """Rename a user template."""
        new_name, ok = QInputDialog.getText(
            self, "Renomear modelo", "Novo nome:", text=old_name
        )
        if not ok or not new_name.strip() or new_name.strip() == old_name:
            return
        
        templates_dir = Path(__file__).resolve().parents[1] / "templates"
        old_path = templates_dir / f"{old_name}.json"
        new_path = templates_dir / f"{new_name.strip()}.json"
        
        if not old_path.exists():
            QMessageBox.warning(self, "Erro", "Modelo não encontrado.")
            return
        if new_path.exists():
            QMessageBox.warning(self, "Erro", "Já existe modelo com esse nome.")
            return
        
        old_path.rename(new_path)
        self._refresh_template_list(self.template_list)
        self.statusBar().showMessage(f"Modelo renomeado para '{new_name.strip()}'", 4000)

    def _delete_template(self, name: str) -> None:
        """Delete a user template."""
        # Prevent deleting built-in templates
        builtin = {"Meteor Mayhem", "Electro Dragon Loons", "Queen Charge Hybrid"}
        if name in builtin:
            QMessageBox.information(self, "Não permitido", "Modelos padrão não podem ser excluídos.")
            return
        
        reply = QMessageBox.question(
            self, "Excluir modelo",
            f"Excluir o modelo '{name}' permanentemente?",
            QMessageBox.Yes | QMessageBox.No
        )
        if reply != QMessageBox.Yes:
            return
        
        templates_dir = Path(__file__).resolve().parents[1] / "templates"
        path = templates_dir / f"{name}.json"
        if path.exists():
            path.unlink()
            self._refresh_template_list(self.template_list)
            self.statusBar().showMessage(f"Modelo '{name}' excluído", 4000)

    def _load_template(self, name: str) -> None:
        builder = get_all_templates()[name]
        self.script = builder(name)
        self.current_file = None
        self._rebuild_tree()
        self._refresh_validation()

    def _open_file(self) -> None:
        path, _ = QFileDialog.getOpenFileName(
            self, self.i18n.tr("action_open"), str(_DEFAULT_DIR), "CSV (*.csv)"
        )
        if path:
            self._load_file(Path(path))

    def _load_file(self, path: Path) -> None:
        try:
            self.script = parse_file(str(path))
            self.script.name = path.stem
            self.current_file = path
        except Exception as error:  # noqa: BLE001 - surface any parse failure
            QMessageBox.critical(self, self.i18n.tr("action_open"), str(error))
            return
        self._rebuild_tree()
        self._refresh_validation()

    def _save_file(self) -> None:
        if self.current_file is None:
            self._save_file_as()
            return
        write(self.script, str(self.current_file))
        self.statusBar().showMessage(f"Saved {self.current_file}", 4000)

    def _save_file_as(self) -> None:
        _DEFAULT_DIR.mkdir(parents=True, exist_ok=True)
        suggested = str(_DEFAULT_DIR / f"{self.script.name}.csv")
        path, _ = QFileDialog.getSaveFileName(
            self, self.i18n.tr("action_save_as"), suggested, "CSV (*.csv)"
        )
        if not path:
            return
        self.current_file = Path(path)
        self.script.name = self.current_file.stem
        write(self.script, str(self.current_file))
        self.statusBar().showMessage(f"Saved {self.current_file}", 4000)

    def _save_as_template(self) -> None:
        name, ok = QInputDialog.getText(self, self.i18n.tr("action_save_template"), "Template name:", text=self.script.name)
        if not ok or not name.strip():
            return
        save_template(name.strip(), self.script)
        self._refresh_template_list(self.template_list)
        self.statusBar().showMessage(f"Template '{name}' saved", 4000)

    # ------------------------------------------------------------ editing ---
    def _add_command(self, command) -> None:
        self._push_undo()
        self.script.commands.append(command)
        self._rebuild_tree()
        last = self.tree.topLevelItem(len(self.script.commands) - 1)
        if last:
            self.tree.setCurrentItem(last)
        self._refresh_validation()

    def _delete_selected(self) -> None:
        item = self.tree.currentItem()
        if not isinstance(item, CommandItem):
            return
        self._push_undo()
        self.script.commands.pop(item.index)
        self._rebuild_tree()
        self._refresh_validation()

    def _move_selected(self, offset: int) -> None:
        item = self.tree.currentItem()
        if not isinstance(item, CommandItem):
            return
        target = item.index + offset
        if not 0 <= target < len(self.script.commands):
            return
        self._push_undo()
        commands = self.script.commands
        commands[item.index], commands[target] = commands[target], commands[item.index]
        self._rebuild_tree()
        moved = self.tree.topLevelItem(target)
        if moved:
            self.tree.setCurrentItem(moved)
        self._refresh_validation()

    def _on_select(self, current, _previous) -> None:
        if isinstance(current, CommandItem):
            self._current = current.command
            self._selected_index = current.index
        else:
            self._current = None
            self._selected_index = None
        self.props.set_command(self._current)
        self.preview.set_highlight(self._highlight_for(self._current))

    def _highlight_for(self, command) -> set[str]:
        if isinstance(command, Make):
            return {command.vector.strip().upper()}
        if isinstance(command, Drop):
            letters: set[str] = set()
            for chunk in command.vectors.replace(";", ",").split(","):
                for part in chunk.split("-"):
                    part = part.strip().upper()
                    if part:
                        letters.add(part)
            return letters
        return set()

    def _on_command_edited(self) -> None:
        item = self.tree.currentItem()
        if isinstance(item, CommandItem):
            item.refresh(item.index)
        self.legend.set_makes(self.script.makes())
        self._apply_visibility()
        self.preview.set_script(self.script)
        self.preview.set_highlight(self._highlight_for(self._current))
        self._refresh_validation()

    def _on_canvas_point_clicked(self, vector: str, point_idx: int) -> None:
        """Called when user clicks a drop point on the canvas."""
        msg = f"Vetor {vector}, ponto {point_idx}"
        self.statusBar().showMessage(msg, 5000)
        # If a DROP is selected, offer to update its vector/index
        item = self.tree.currentItem()
        if isinstance(item, CommandItem) and item.command.kind == "DROP":
            drop = item.command
            reply = QMessageBox.question(
                self,
                "Atualizar DROP",
                f"Atualizar este DROP para vetor '{vector}', ponto {point_idx}?\n\n"
                f"Atual: vetores={drop.vectors}, índice={drop.index}",
                QMessageBox.Yes | QMessageBox.No,
            )
            if reply == QMessageBox.Yes:
                self._push_undo()
                drop.vectors = vector
                drop.index = str(point_idx)
                self._on_command_edited()

    def _on_property_changed(self) -> None:
        """Called when a property is edited - push undo on first change."""
        if not hasattr(self, '_editing_command'):
            self._editing_command = None
        if self._editing_command != self._current:
            self._push_undo()
            self._editing_command = self._current
        self._on_command_edited()

    def _apply_visibility(self) -> None:
        self.preview.set_visible(self.legend.visible_letters())

    # ------------------------------------------------------ undo/redo -----
    def _push_undo(self) -> None:
        """Save current script state to undo stack."""
        import copy
        self._undo_stack.append(copy.deepcopy(self.script))
        if len(self._undo_stack) > self._max_undo:
            self._undo_stack.pop(0)
        self._redo_stack.clear()
        self._update_undo_redo_actions()

    def _undo(self) -> None:
        if not self._undo_stack:
            return
        import copy
        # Save current selection
        selected_idx = self._selected_index
        self._redo_stack.append(copy.deepcopy(self.script))
        self.script = self._undo_stack.pop()
        self._rebuild_tree()
        self._update_undo_redo_actions()
        # Restore selection if valid
        if selected_idx is not None and selected_idx < len(self.script.commands):
            self.tree.setCurrentItem(self.tree.topLevelItem(selected_idx))
        self.statusBar().showMessage(self.i18n.tr("status_undo"), 2000)

    def _redo(self) -> None:
        if not self._redo_stack:
            return
        import copy
        # Save current selection
        selected_idx = self._selected_index
        self._undo_stack.append(copy.deepcopy(self.script))
        self.script = self._redo_stack.pop()
        self._rebuild_tree()
        self._update_undo_redo_actions()
        # Restore selection if valid
        if selected_idx is not None and selected_idx < len(self.script.commands):
            self.tree.setCurrentItem(self.tree.topLevelItem(selected_idx))
        self.statusBar().showMessage(self.i18n.tr("status_redo"), 2000)

    def _update_undo_redo_actions(self) -> None:
        self._act_undo.setEnabled(len(self._undo_stack) > 0)
        self._act_redo.setEnabled(len(self._redo_stack) > 0)

    # -------------------------------------------------------- copy/paste --
    def _copy_commands(self) -> None:
        items = self.tree.selectedItems()
        if not items:
            return
        import copy
        self._clipboard = [copy.deepcopy(item.command) for item in items if isinstance(item, CommandItem)]
        self._act_paste.setEnabled(len(self._clipboard) > 0)
        self.statusBar().showMessage(f"{len(self._clipboard)} comando(s) copiado(s)", 2000)

    def _paste_commands(self) -> None:
        if not hasattr(self, '_clipboard') or not self._clipboard:
            return
        import copy
        self._push_undo()
        insert_idx = len(self.script.commands)
        current = self.tree.currentItem()
        if isinstance(current, CommandItem):
            insert_idx = current.index + 1
        for cmd in self._clipboard:
            self.script.commands.insert(insert_idx, copy.deepcopy(cmd))
            insert_idx += 1
        self._rebuild_tree()
        self.statusBar().showMessage(f"{len(self._clipboard)} comando(s) colado(s)", 2000)

    def _duplicate_commands(self) -> None:
        items = self.tree.selectedItems()
        if not items:
            return
        import copy
        self._push_undo()
        insert_idx = len(self.script.commands)
        current = self.tree.currentItem()
        if isinstance(current, CommandItem):
            insert_idx = current.index + 1
        for item in items:
            if isinstance(item, CommandItem):
                self.script.commands.insert(insert_idx, copy.deepcopy(item.command))
                insert_idx += 1
        self._rebuild_tree()
        self.statusBar().showMessage(f"{len(items)} comando(s) duplicado(s)", 2000)

    def _reset_canvas_view(self) -> None:
        self.preview.reset_view()
        self.statusBar().showMessage("Visão do canvas resetada", 2000)

    # ------------------------------------------------------------ refresh ---
    def _rebuild_tree(self) -> None:
        self.tree.clear()
        for index, command in enumerate(self.script.commands):
            self.tree.addTopLevelItem(CommandItem(command, index))
        self.legend.set_makes(self.script.makes())
        self.preview.set_script(self.script)
        self._apply_visibility()
        self._current = None
        self._selected_index = None
        # Update property editor's script reference for vector selector
        if hasattr(self, 'props'):
            self.props._main_script = self.script

    def _refresh_validation(self) -> None:
        self.validation_list.clear()
        problems = validate(self.script)
        
        # Build map of command index -> list of problems
        prob_by_idx = {}
        for problem in problems:
            idx = problem.index  # Problem uses 'index' field
            if idx >= 0:
                prob_by_idx.setdefault(idx, []).append(problem)
        
        # Update tree items with validation status
        for i in range(self.tree.topLevelItemCount()):
            item = self.tree.topLevelItem(i)
            if isinstance(item, CommandItem):
                idx = item.index
                if idx in prob_by_idx:
                    # Has errors/warnings
                    item.setIcon(1, self.style().standardIcon(QStyle.SP_MessageBoxCritical))
                    item.setToolTip(2, "\n".join(str(p) for p in prob_by_idx[idx]))
                else:
                    # OK
                    item.setIcon(1, self.style().standardIcon(QStyle.SP_DialogApplyButton))
                    item.setToolTip(2, "")
        
        if not problems:
            item = QListWidgetItem(self.i18n.tr("validation_ok"))
            item.setForeground(QColor(0, 140, 0))
            self.validation_list.addItem(item)
            return
        for problem in problems:
            item = QListWidgetItem(str(problem))
            item.setForeground(
                QColor(200, 0, 0) if problem.severity == "error" else QColor(180, 120, 0)
            )
            self.validation_list.addItem(item)

    def _show_shortnames(self) -> None:
        dialog = QDialog(self)
        dialog.setWindowTitle(self.i18n.tr("action_units"))
        dialog.resize(520, 640)
        layout = QVBoxLayout(dialog)

        text = QTextEdit()
        text.setReadOnly(True)
        text.setFont(QFont("Consolas", 9))
        lines = []
        for kind, title in (
            ("troop", "TROOPS"),
            ("spell", "SPELLS"),
            ("hero", "HEROES"),
            ("siege", "SIEGE MACHINES"),
            ("special", "SPECIAL"),
        ):
            lines.append(f"=== {title} ===")
            for short in sorted(UNITS):
                info = UNITS[short]
                if info["kind"] != kind:
                    continue
                space = f"  ({info['space']})" if info["space"] else ""
                lines.append(f"  {short:<10} {info['name']}{space}")
            lines.append("")
        text.setPlainText("\n".join(lines))
        layout.addWidget(text)

        buttons = QDialogButtonBox(QDialogButtonBox.Close)
        buttons.rejected.connect(dialog.reject)
        layout.addWidget(buttons)
        dialog.exec()


def main() -> None:
    app = QApplication(sys.argv)
    app.setApplicationName(BRAND)
    app.setStyle("Fusion")
    app.setFont(QFont("Segoe UI", 9))
    app.setStyleSheet(STYLESHEET)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
