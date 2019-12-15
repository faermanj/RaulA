import time
import threading
import logging
import datetime
import os
import random
from pathlib import Path
from .module import Module


class NonSense(Exception):
    pass


class Periodic(Module):
    MIN_DELAY = 0.01
    MAX_DELAY = 3600
    MAX_VARIANCE = 0.05
    DEF_FREQUENCY = 10
    DEF_MIN_DELAY = 5
    DEF_MAX_DELAY = 60

    thread = None

    step_logger = logging.getLogger('raula.step')
    logger = logging.getLogger('raula.periodic')

    def stand(self):
        super().stand()
        delay = round(self.delay(), 4)
        hz = round(1 / delay, 4)
        self.logger.info(
            "Standing module [{}] at [{}]Hz = [{}]s delay".format(self.name, hz, delay))
        self.get_thread().start()
    
    def skid(self):
        self.logger.info("Skidding module [{}]".format(self.name))
        self.agent.set_default("running","0")

    def join(self):
        try:
            worker = self.get_thread()
            if (worker.is_alive()):
                worker.join()
        except KeyboardInterrupt:
            self.debug("KeyboardInterrupt on Periodic[{}].join()".format(self.name))
            self.skid()
            
    def default_delay(self):
        return (Periodic.DEF_MIN_DELAY, Periodic.DEF_MAX_DELAY, Periodic.DEF_FREQUENCY)
        

    def delay(self):
        (min_delay, max_delay, frequency)  = self.default_delay()
    
        min_delay = self.get_float("min_delay", min_delay)
        max_delay = self.get_float("max_delay", max_delay)
        frequency = self.get_float("frequency", frequency)
        
        frequency = max(frequency, Periodic.MIN_DELAY)
        frequency = min(frequency, Periodic.MAX_DELAY)

        noise = random.random() * Periodic.MAX_VARIANCE
        frequency = frequency * (1.0 - noise)
        frequency = round(frequency, 4)
        assert frequency > 0.0
        return frequency

    def backoff(self):
        return 100 * self.delay()

    def step(self):
        self.step_logger.debug("Stepping [{}]".format(self.name))
        ts_before = datetime.datetime.now()
        value = self.sense(timestamp=ts_before)
        ts_after = datetime.datetime.now()
        return {
            "before": str(ts_before),
            "value": value,
            "after": str(ts_after)
        }

    def is_running(self):
        global_running = self.agent.get_default("running") == "1"
        is_running = global_running
        return is_running

    def run(self):
        while(self.is_running()):
            try:
                time.sleep(self.delay())
                if(self.is_working()):
                    footprint = self.step()
                    self.agent.ingest(self, footprint)
                else:
                    backoff = self.backoff()
                    self.logger.warning(
                        "Module [{}] not working. Backing off for  [{}]".format(self.name, backoff))
                    time.sleep(backoff)
            except KeyboardInterrupt:
                print("KeybardInterrupt from Periodic.run()")
                self.logger.info("Module [{}] interrupted".format(self.name))
                break
        self.logger.info("Module [{}] ended".format(self.name))

    def get_thread(self):
        if (not self.thread):
            self.thread = threading.Thread(target=self.run, daemon=True)
        return self.thread

    def get_data_path(self):
        raula_data = Path(self.agent.get_default("raula_data"))
        return raula_data

    def get_log_path(self):
        raula_log = Path(self.agent.get_default("raula_log"))
        return raula_log

    def get_module_path(self):
        data_path = self.get_data_path() / self.name
        return data_path

    def get_module_log_path(self):
        data_path = self.get_log_path() / self.name
        return data_path

    def mk_filename(self, ts, prefix, ext):
        data_path = self.get_module_path()
        data_path / (ts.strftime("%Y/%m/%d/%H/%M"))
        if(not data_path.exists()):
            self.logger.debug("Creating path [{}]".format(str(data_path)))
            data_path.mkdir(parents=True, exist_ok=True)
        file_ts = ts.strftime("%Y%m%d%H%M%S%f")
        data_file = data_path / '{}_{}.{}'.format(prefix, file_ts, ext)
        picture_file = str(data_file)
        return picture_file

    # Abstract Methods

    def is_working(self):
        return True

    def sense(self):
        raise NonSense
