"""
Main CLI entry point for Yet Another Timer App.
"""
from pathlib import Path
from rich.console import Group
from rich.panel import Panel
from rich.live import Live
from rich.padding import Padding
from rich.progress_bar import ProgressBar
from rich.text import Text

from model.timer_collection import TimerCollection
from services.data_access import DataService


def gen_timer_collection_ui(timerCollection: TimerCollection) -> Panel:
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


if __name__ == "__main__":
    # TODO: Replace this temp code with better CLI options & flow.
    timer_collections = DataService.initialize(Path("./data"))

    with Live(gen_timer_collection_ui(timer_collections[1])) as live:
        for _ in timer_collections[1].run():
            live.update(gen_timer_collection_ui(timer_collections[1]))

    #### EXAMPLE TIMER....

    # myTimer = Timer("Timer 1", 10)
    # countDownBar = ProgressBar(total=myTimer.duration, completed=myTimer.remaining)

    # def gen_count_down() -> Panel:
    #     count_down_group = Group(countDownBar)
    #     count_down_panel = Panel(count_down_group, title="Timer 1", title_align="right", subtitle=Text(str(countDownBar.completed)), subtitle_align="right")
    #     return count_down_panel

    # with Live(gen_count_down()) as live:
    #     for x in myTimer.run():
    #     # while countDownBar.completed > 0:
    #         # time.sleep(1)
    #         countDownBar.completed = myTimer.remaining
    #         live.update(gen_count_down())

    # print(ProgressBar(total=30, completed=30.0))
