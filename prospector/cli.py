from __future__ import annotations

import argparse
from collections.abc import Callable, Sequence
from pathlib import Path

from .config import RunConfig
from .pipeline import dry_run


DEFAULT_OUTPUT_PATH = "prospects.csv"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="prospector",
        description="Run Prospector interactively by default, or use `prospector run` for scripted runs.",
    )
    sub = parser.add_subparsers(dest="command")

    run_parser = sub.add_parser("run", help="Run Prospector non-interactively and write CSV")
    run_parser.add_argument("--product", required=True, help="Product description")
    run_parser.add_argument("--icp", required=True, help="ICP definition")
    run_parser.add_argument("--filters", required=True, help="Prospect filters")
    run_parser.add_argument("--max-prospects", type=int, default=50, help="Maximum prospects to output")
    run_parser.add_argument("--out", default=DEFAULT_OUTPUT_PATH, help="Output CSV path")
    run_parser.add_argument("--target-company-size", default="", help="Target company size")
    run_parser.add_argument("--sources", default="web,linkedin", help="Comma-separated sources (web,linkedin)")
    run_parser.add_argument("--lookback-days", type=int, default=30, help="Lookback window in days (1-180)")
    return parser


def _ask_non_empty(question: str, input_fn: Callable[[str], str] = input) -> str:
    while True:
        value = input_fn(question).strip()
        if value:
            return value
        print("Please enter a value.")


def _ask_int(question: str, minimum: int, maximum: int, input_fn: Callable[[str], str] = input) -> int:
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


def _parse_sources(raw: str) -> tuple[str, ...]:
    allowed = {"web", "linkedin"}
    selected = tuple(s.strip().lower() for s in raw.split(",") if s.strip())
    if not selected or not set(selected).issubset(allowed):
        raise ValueError("sources must be one or more of: web, linkedin")
    return selected


def _ask_sources(question: str, input_fn: Callable[[str], str] = input) -> tuple[str, ...]:
    while True:
        raw = input_fn(question).strip()
        try:
            return _parse_sources(raw)
        except ValueError:
            print("Please choose from: web, linkedin (comma-separated).")


def prompt_for_run_config(input_fn: Callable[[str], str] = input) -> RunConfig:
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


def run_interactive(
    input_fn: Callable[[str], str] = input,
    out_path: str = DEFAULT_OUTPUT_PATH,
    run_fn: Callable[[RunConfig, str], Path] = dry_run,
) -> Path:
    config = prompt_for_run_config(input_fn)
    written = run_fn(config, out_path)
    print(f"Interactive run complete. Wrote {written}")
    return written


def run_from_args(args: argparse.Namespace, run_fn: Callable[[RunConfig, str], Path] = dry_run) -> Path:
    config = RunConfig(
        product=args.product,
        icp=args.icp,
        filters=args.filters,
        max_prospects=args.max_prospects,
        target_company_size=args.target_company_size,
        sources=_parse_sources(args.sources),
        lookback_days=args.lookback_days,
    )
    written = run_fn(config, args.out)
    print(f"Run complete. Wrote {written}")
    return written


def main(argv: Sequence[str] | None = None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "run":
        run_from_args(args)
        return

    run_interactive()


if __name__ == "__main__":
    main()
