#!/usr/bin/env python3
import argparse
import textwrap
from pathlib import Path

from angiosperm.pylib.readers import paragraphs_html


def main():
    args = parse_args()

    paragraphs = paragraphs_html.read(args.input_dir, args.pattern)

    for taxon, paragraph in paragraphs.items():
        print(taxon, "\n")
        print(paragraph, "\n")


def parse_args() -> argparse.Namespace:
    arg_parser = argparse.ArgumentParser(
        fromfile_prefix_chars="@",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=textwrap.dedent(
            """Find target paragraphs for gathering test data.""",
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
        "--pattern",
        help="""The paragraph's first sentence should contain this pattern.""",
    )

    args = arg_parser.parse_args()
    return args


if __name__ == "__main__":
    main()
