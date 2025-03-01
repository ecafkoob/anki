# Copyright: Ankitects Pty Ltd and contributors
# License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html

from typing import Optional

from anki.decks import DEFAULT_DECK_ID, DeckId
from aqt import AnkiQt
from aqt.qt import *
from aqt.utils import HelpPage, shortcut, tr


class DeckChooser(QHBoxLayout):
    def __init__(
        self,
        mw: AnkiQt,
        widget: QWidget,
        label: bool = True,
        starting_deck_id: Optional[DeckId] = None,
    ) -> None:
        QHBoxLayout.__init__(self)
        self._widget = widget  # type: ignore
        self.mw = mw
        self._setup_ui(show_label=label)

        self._selected_deck_id = DeckId(0)
        # default to current deck if starting id not provided
        if starting_deck_id is None:
            starting_deck_id = DeckId(self.mw.col.get_config("curDeck", default=1) or 1)
        self.selected_deck_id = starting_deck_id

    def _setup_ui(self, show_label: bool) -> None:
        self.setContentsMargins(0, 0, 0, 0)
        self.setSpacing(8)

        # text label before button?
        if show_label:
            self.deckLabel = QLabel(tr.decks_deck())
            self.addWidget(self.deckLabel)

        # decks box
        self.deck = QPushButton()
        qconnect(self.deck.clicked, self.choose_deck)
        self.deck.setAutoDefault(False)
        self.deck.setToolTip(shortcut(tr.qt_misc_target_deck_ctrlandd()))
        qconnect(
            QShortcut(QKeySequence("Ctrl+D"), self._widget).activated, self.choose_deck
        )
        sizePolicy = QSizePolicy(QSizePolicy.Policy(7), QSizePolicy.Policy(0))
        self.deck.setSizePolicy(sizePolicy)
        self.addWidget(self.deck)

        self._widget.setLayout(self)

    def selected_deck_name(self) -> str:
        return (
            self.mw.col.decks.name_if_exists(self.selected_deck_id) or "missing default"
        )

    @property
    def selected_deck_id(self) -> DeckId:
        self._ensure_selected_deck_valid()

        return self._selected_deck_id

    @selected_deck_id.setter
    def selected_deck_id(self, id: DeckId) -> None:
        if id != self._selected_deck_id:
            self._selected_deck_id = id
            self._ensure_selected_deck_valid()
            self._update_button_label()

    def _ensure_selected_deck_valid(self) -> None:
        deck = self.mw.col.decks.get(self._selected_deck_id, default=False)
        if not deck or deck["dyn"]:
            self.selected_deck_id = DEFAULT_DECK_ID

    def _update_button_label(self) -> None:
        self.deck.setText(self.selected_deck_name().replace("&", "&&"))

    def show(self) -> None:
        self._widget.show()  # type: ignore

    def hide(self) -> None:
        self._widget.hide()  # type: ignore

    def choose_deck(self) -> None:
        from aqt.studydeck import StudyDeck

        current = self.selected_deck_name()
        ret = StudyDeck(
            self.mw,
            current=current,
            accept=tr.actions_choose(),
            title=tr.qt_misc_choose_deck(),
            help=HelpPage.EDITING,
            cancel=False,
            parent=self._widget,
            geomKey="selectDeck",
        )
        if ret.name:
            self.selected_deck_id = self.mw.col.decks.by_name(ret.name)["id"]

    # legacy

    onDeckChange = choose_deck
    deckName = selected_deck_name

    def selectedId(self) -> DeckId:
        return self.selected_deck_id

    def cleanup(self) -> None:
        pass
