import operator

from aiogram_dialog.widgets.kbd import ScrollingGroup, Select
from aiogram_dialog.widgets.text import Format

SCROLLING_HEIGHT = 6


def paginated_history():
    return ScrollingGroup(
        Select(
            Format("{item[0]}"),
            id="s_scroll_history",
            item_id_getter=operator.itemgetter(1),
            items="history",
        ),
        id="history_ids",
        width=1,
        height=SCROLLING_HEIGHT,
    )
