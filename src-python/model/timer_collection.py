"""
TimerCollection Class definition.
"""

from dataclasses import dataclass, field
from typing import List

from .timer import Timer


@dataclass
class TimerCollection:
    """Class for grouping together multiple timers."""

    name: str
    """Name of the timer collection."""

    repeat: bool | int = False
    """Used to repeat the set of timers once all have completed.

    Value of False or 0 will not repeat the timers.
    True will continuously repeat.
    Positive integer will repeat that many times."""

    timers: List[Timer] = field(default_factory=list)
    """List of timers that make up this collection."""

    def run(self):
        """Run a timer collection. Timers are ran sequentially.

        Will run through it's list of timers and repeat if specified.
        """

        for _timer in self.timers:
            for _ in _timer.run():
                yield
