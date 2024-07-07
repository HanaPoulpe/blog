#!/usr/bin/env python
import os
import pathlib
import sys

import dotenv

dotenv.load_dotenv(pathlib.Path(__file__).parent.joinpath(".env"))


def main(argv: list[str] | None = None) -> None:
    argv = argv or sys.argv

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "blog.settings")

    from configurations.management import execute_from_command_line

    execute_from_command_line(argv)


if __name__ == "__main__":
    main()
