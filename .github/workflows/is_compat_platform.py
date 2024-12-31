import sys
import platform as p


def compatible(semver: str) -> bool:
    # Expected tag in format v1.2.3
    version_major = int(semver[1:].split('.')[0])
    macOS_arm = 'darwin' in p.system().lower() and 'arm' in p.processor().lower()
    return (not macOS_arm or (macOS_arm and version_major >= 12))


def main():
    # Take a single command line argument, the tag name
    if len(sys.argv) == 2:
        print("true" if compatible(sys.argv[1]) else "false")
    else:
        raise ValueError("Need the tag version as a single argument.")


if __name__ == "__main__":
    main()
