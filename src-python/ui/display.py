"""Define the functions for getting UI display elements."""

from enum import Enum
from rich.console import Group
from rich.padding import Padding
from rich.panel import Panel
from rich.progress_bar import ProgressBar
from rich.style import Style
from rich.text import Text
from rich.tree import Tree

from model.timer_collection import TimerCollection
from model.timer import Timer

NUM_TO_WORD = {
    1: "one",
    2: "two",
    3: "three",
    4: "four",
    5: "five",
    6: "six",
    7: "seven",
    8: "eight",
    9: "nine",
}


class COMMANDS(Enum):
    List = 1
    Start = 2
    Create = 3
    Quit = 4


def get_commands_display() -> Tree:
    cmdList = []
    cmdList.append("List timers")
    cmdList.append("Start timer")
    cmdList.append("Create timer")
    cmdList.append("Quit")

    cmdTree = Tree(":clock10: Commands")

    for _idx, _cmd in enumerate(cmdList, start=1):
        cmdTree.add(f":{NUM_TO_WORD[_idx]}:  {_cmd}")

    return cmdTree


def get_collections_display(timer_collections: list[TimerCollection]) -> Tree:
    display = Tree("Timer Collections")
    header_style = Style(color="green", bold=True)
    for _idx, _timer_collection in enumerate(timer_collections, start=1):
        display.add(
            Group(
                Text(f"{_idx}.", style=header_style),
                Padding(get_timer_collection_display(_timer_collection), (1, 0, 0, 0)),
            )
        )

    return display


def get_timer_collection_display(timerCollection: TimerCollection) -> Panel:
    content = Group()
    repeat_msg = ":cross_mark: Timer does [b red]not[/] repeat."
    if timerCollection.repeat or timerCollection.repeat > 0:
        repeat_msg = f":repeat_button: Timer repeats"
        if not isinstance(timerCollection.repeat, bool):
            repeat_msg += f" for [b green]{timerCollection.repeat}[/] times."
        else:
            repeat_msg += " infinitely!"

    content.renderables.append(Padding(repeat_msg, (1, 0, 0, 0)))
    content.renderables.append(
        Padding(get_timers_display(timerCollection.timers), (1, 0, 0, 0))
    )

    return Panel(content, title=timerCollection.name, title_align="left", expand=False)


def get_timers_display(_timers: list[Timer]) -> Tree:
    timer_display = Tree(":clock1: Timers")

    for timer in _timers:
        timer_display.add(
            f"[b yellow]{timer.description}[/] for [b purple]{timer.duration}[/] seconds"
        )

    return timer_display


def gen_running_timer_display(timerCollection: TimerCollection) -> Panel:
    timer_panels = Group()
    # Create a Panel for each timer of the collection.
    for _timer in timerCollection.timers:
        timer_progress_bar = ProgressBar(
            total=_timer.duration, completed=_timer.remaining
        )
        timer_panel = Panel(
            timer_progress_bar,
            title=_timer.description,
            subtitle=Text(str(_timer.remaining)),
            title_align="right",
            subtitle_align="right",
        )

        timer_panels.renderables.append(Padding(timer_panel, (1, 0, 0, 0)))

    # Create a parent panel for the timer collection and add its timers to it.
    collection_panel = Panel(timer_panels, title=timerCollection.name)

    return collection_panel
