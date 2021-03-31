import time
import typing

from dataclasses import dataclass


@dataclass
class Retry:
    max_reties: int
    delay_secs: float
    excetion: typing.Type[Exception]

    def execute(self, fn: typing.Callable):
        tries = 0
        while tries < self.max_reties:
            tries += 1
            try:
                return fn()
            except self.excetion as e:
                if tries < self.max_reties:
                    time.sleep(self.delay_secs)
                else:
                    raise e