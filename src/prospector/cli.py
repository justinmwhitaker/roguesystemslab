from __future__ import annotations

import argparse

from .config import RunConfig
from .pipeline import dry_run


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="prospector", description="Prospector CLI scaffold")
    sub = parser.add_subparsers(dest="command", required=True)

    run_parser = sub.add_parser("run", help="Run a dry-run pipeline and write CSV")
    run_parser.add_argument("--product", required=True, help="Product description")
    run_parser.add_argument("--icp", required=True, help="ICP definition")
    run_parser.add_argument("--filters", required=True, help="Prospect filters")
    run_parser.add_argument("--max-prospects", type=int, default=50, help="Maximum prospects to output")
    run_parser.add_argument("--out", default="prospects.csv", help="Output CSV path")
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "run":
        config = RunConfig(product=args.product, icp=args.icp, filters=args.filters, max_prospects=args.max_prospects)
        written = dry_run(config, args.out)
        print(f"Dry run complete. Wrote {written}")


if __name__ == "__main__":
    main()
