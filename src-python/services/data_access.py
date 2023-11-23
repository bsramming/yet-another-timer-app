"""Data access service."""

import json

from pathlib import Path
from typing import List

from model.timer_collection import TimerCollection
from model.timer import Timer


class DataService:
    @classmethod
    def initialize(cls, data_path: Path) -> List[TimerCollection]:
        """Load any timer collection defined in given Path.

        data_path is the Path containing the json files to load."""

        timer_collections = []

        if data_path.exists():
            # TODO: Validation checks on this input JSON file.
            for _file in data_path.glob("*.json"):
                with _file.open() as tf:
                    _data = json.load(tf)

                timer_collection = TimerCollection(
                    name=_data["name"], repeat=_data["repeat"]
                )
                for _timer in _data["timers"]:
                    timer_collection.timers.append(
                        Timer(
                            description=_timer["description"],
                            duration=_timer["duration"],
                        )
                    )

                timer_collections.append(timer_collection)
        else:
            raise FileNotFoundError(f"Error: data path: {str(data_path)} not found.")

        return timer_collections
