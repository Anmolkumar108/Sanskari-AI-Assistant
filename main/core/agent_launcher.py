import subprocess
import sys
import os


class AgentLauncher:

    def __init__(self):
        self.process = None

    def start(self):

        if self.process is not None:
            return

        project_root = os.path.dirname(
            os.path.dirname(os.path.dirname(__file__))
        )

        self.process = subprocess.Popen(
            [
                sys.executable,
                "-m",
                "main.agent",
                "console"
            ],
            cwd=project_root
        )

    def stop(self):

        if self.process:

            self.process.kill()

            self.process = None