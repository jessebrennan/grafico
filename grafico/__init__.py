import os


class Config:

    @property
    def project_root(self):
        return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


config = Config()
