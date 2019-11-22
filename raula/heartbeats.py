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
        hb_string = self.get_config("hb_string", random.choice(self.beats))
        hb_int = self.get_int("hb_int", random.random() * 100)
        hb_float = self.get_float("hb_float", random.random())
        result = {
            "hb_string": hb_string,
            "hb_int": hb_int,
            "hb_float": hb_float
        }
        self.debug(result)
        return result 
