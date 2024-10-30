import sys
import subprocess


def launch_arm_none_eabi(bin="gcc"):
    argv = [f"arm-none-eabi-{bin}", *sys.argv[1:]]
    exit_code = subprocess.call(argv)
    sys.exit(exit_code)


def arm_none_eabi_gcc():
    launch_arm_none_eabi("gcc")


if __name__ == "__main__":
    launch_arm_none_eabi()
