"""
Timer class definition.
"""
import time
from dataclasses import dataclass


@dataclass
class Timer:
    """Class for working with timers."""

    description: str
    """Text to describe the timer."""

    duration: int
    """Duration of the timer in seconds."""

    is_running: bool = False
    """Flag if the timer is running or not."""

    remaining: int = None
    """Time, in seconds, remaining on the timer when is_running."""

    def __post_init__(self):
        """Default remaining time to given duration when a Timer is created."""
        self.remaining = self.duration

    def run(self):
        self.is_running = True
        self.remaining = self.duration

        while self.remaining > 0:
            self.remaining -= 1
            time.sleep(1)
            yield

        self.is_running = False
