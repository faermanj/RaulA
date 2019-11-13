from .sensor import Sensor
import random


class Heartbeats(Sensor):
    beats = ["<3",
             "♱♡‿♡♰",
             "♡＾▽＾♡",
             "✿♥‿♥✿",
             "♡ඩ⌔ඩ♡",
             "༼♥ل͜♥༽",
             "(✿ ♥‿♥)"]

    def sense(self, timestamp):
        self.debug("Heart beating")
        hb_string = random.choice(self.beats)
        hb_int = int(random.random() * 100)
        hb_float = random.random()
        return {
            "hb_string": hb_string,
            "hb_int": hb_int,
            "hb_float": hb_float
        }
