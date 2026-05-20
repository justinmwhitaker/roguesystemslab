from __future__ import annotations

import argparse

from .config import RunConfig
from .pipeline import dry_run


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="prospector", description="Prospector CLI scaffold")
    sub = parser.add_subparsers(dest="command")

    run_parser = sub.add_parser("run", help="Run a dry-run pipeline and write CSV")
    run_parser.add_argument("--product", required=True, help="Product description")
    run_parser.add_argument("--icp", required=True, help="ICP definition")
    run_parser.add_argument("--filters", required=True, help="Prospect filters")
    run_parser.add_argument("--max-prospects", type=int, default=50, help="Maximum prospects to output")
    run_parser.add_argument("--out", default="prospects.csv", help="Output CSV path")
    run_parser.add_argument("--target-company-size", default="", help="Target company size")
    run_parser.add_argument("--sources", default="web,linkedin", help="Comma-separated sources (web,linkedin)")
    run_parser.add_argument("--lookback-days", type=int, default=30, help="Lookback window in days (1-180)")
    return parser


def _ask_non_empty(question: str, input_fn=input) -> str:
    while True:
        value = input_fn(question).strip()
        if value:
            return value
        print("Please enter a value.")


def _ask_int(question: str, minimum: int, maximum: int, input_fn=input) -> int:
    while True:
        raw = input_fn(question).strip()
        try:
            value = int(raw)
        except ValueError:
            print("Please enter a whole number.")
            continue
        if minimum <= value <= maximum:
            return value
        print(f"Please enter a number between {minimum} and {maximum}.")


def _ask_sources(question: str, input_fn=input) -> tuple[str, ...]:
    allowed = {"web", "linkedin"}
    while True:
        raw = input_fn(question).strip().lower()
        selected = tuple(s.strip() for s in raw.split(",") if s.strip())
        if selected and set(selected).issubset(allowed):
            return selected
        print("Please choose from: web, linkedin (comma-separated).")


def prompt_for_run_config(input_fn=input) -> RunConfig:
    print("Prospector interactive setup")
    product = _ask_non_empty("1) What product are we looking for prospects for? ", input_fn)
    target_client = _ask_non_empty("2) What is the target client? ", input_fn)
    target_company_size = _ask_non_empty("3) What is the target company size? ", input_fn)
    sources = _ask_sources("4) Where should Prospect look? (Web, LinkedIn) ", input_fn)
    max_prospects = _ask_int("5) How many prospects do I want returned? ", 1, 10_000, input_fn)
    lookback_days = _ask_int("6) How many days should be searched? (1-180 days) ", 1, 180, input_fn)

    return RunConfig(
        product=product,
        icp=target_client,
        filters=f"company_size={target_company_size}",
        max_prospects=max_prospects,
        target_company_size=target_company_size,
        sources=sources,
        lookback_days=lookback_days,
    )


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "run":
        sources = tuple(s.strip().lower() for s in args.sources.split(",") if s.strip())
        config = RunConfig(
            product=args.product,
            icp=args.icp,
            filters=args.filters,
            max_prospects=args.max_prospects,
            target_company_size=args.target_company_size,
            sources=sources,
            lookback_days=args.lookback_days,
        )
        written = dry_run(config, args.out)
        print(f"Dry run complete. Wrote {written}")
        return

    config = prompt_for_run_config()
    written = dry_run(config, "prospects.csv")
    print(f"Interactive run complete. Wrote {written}")


if __name__ == "__main__":
    main()
