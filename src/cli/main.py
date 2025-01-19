import argparse

from . import _commands as commands


def main() -> None:
    # Quick fix before moving long term to click
    parser = argparse.ArgumentParser()
    parser.add_argument("--command", choices=dir(commands), required=True)

    args = parser.parse_args()
    command_name = args.command

    command = getattr(commands, command_name)
    command()
