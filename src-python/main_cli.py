"""
Main CLI entry point for Yet Another Timer App.
"""

from pathlib import Path
from rich import print
from rich.console import Console
from rich.live import Live
from rich.panel import Panel
from rich.prompt import Prompt, IntPrompt
from rich.tree import Tree

from services.data_access import DataService
from ui.display import COMMANDS, NUM_TO_WORD
import ui.display as ui


if __name__ == "__main__":
    # TODO: Replace this temp code with better CLI options & flow.
    timer_collections = DataService.initialize(Path("./data"))
    console = Console()

    cmdTree = ui.get_commands_display()

    cmd = None
    while cmd != COMMANDS.Quit.value:
        print(cmdTree)
        cmd = IntPrompt.ask(
            f"Select command",
            choices=list(map(str, range(1, len(cmdTree.children) + 1))),
        )

        if cmd == COMMANDS.List.value:
            print(ui.get_collections_display(timer_collections))

        elif cmd == COMMANDS.Start.value:
            _select_tree = Tree("Select a timer collection to start")
            for _idx, _tc in enumerate(timer_collections, start=1):
                _select_tree.add(f":{NUM_TO_WORD[_idx]}:  {_tc.name}")
            print(_select_tree)
            # TODO: add option to NOT select a timer and get back to menu
            selected_timer = IntPrompt.ask(
                f"Select timer",
                choices=list(map(str, range(1, len(_select_tree.children) + 1))),
            )
            console.clear()
            selected_timer_collection = timer_collections[selected_timer - 1]
            # TODO: Add timer repeat logic
            with Live(ui.gen_running_timer_display(selected_timer_collection)) as live:
                for _ in selected_timer_collection.run():
                    live.update(ui.gen_running_timer_display(selected_timer_collection))

        elif cmd == COMMANDS.Create.value:
            print(
                Panel(":construction: Under construction :construction:", expand=False)
            )

        if cmd != COMMANDS.Quit.value:
            Prompt.ask("Press any key to go back to the main menu")
            console.clear()
