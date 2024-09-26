#!/usr/bin/env python3
import argparse
import textwrap
from pathlib import Path

from angiosperm.pylib import log
from angiosperm.pylib.readers import family_html
from angiosperm.pylib.writers import html_writer


def main():
    log.started()
    args = parse_args()

    pages = family_html.read(args.input_dir)

    if args.html_file:
        html_writer.write(pages, args.html_file)

    log.finished()


def parse_args() -> argparse.Namespace:
    arg_parser = argparse.ArgumentParser(
        fromfile_prefix_chars="@",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=textwrap.dedent(
            """
            Extract floral trait information from "The Families of Angiosperms"
            web pages.
            """,
        ),
    )

    arg_parser.add_argument(
        "--input-dir",
        type=Path,
        required=True,
        metavar="PATH",
        help="""Directory containing the input treatment HTML files.""",
    )

    arg_parser.add_argument(
        "--html-file",
        type=Path,
        metavar="PATH",
        help="""Output formatted trait data to this HTML file.""",
    )

    args = arg_parser.parse_args()
    return args


if __name__ == "__main__":
    main()
