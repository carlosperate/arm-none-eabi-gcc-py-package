executable_launcher = """
import os
import sys
import subprocess


def launch_{bin_short}():
    argv = [
        os.path.join(
            os.path.abspath(os.path.dirname(__file__)),
            "{gcc_folder}",
            "bin",
            "{bin}"
        ),
        *sys.argv[1:]
    ]
    exit_code = subprocess.call(argv)
    sys.exit(exit_code)


if __name__ == "__main__":
    launch_{bin_short}()
"""
