from .module import Module


class SSHTunnel(Periodic):

    def stand(self):
        super().stand()
        self.info("SSHT module starting")

    def sense(self):
        self.info("SSHT sensing")
