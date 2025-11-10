"""Command line interface for continuously capturing roulette numbers."""

from __future__ import annotations

import argparse
from contextlib import suppress

from .collector import CaptureConfig, capture_numbers, create_driver


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Capture and display roulette results from Betfair."
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=8,
        help="Maximum quantity of numbers to display per iteration (default: 8).",
    )
    parser.add_argument(
        "--delay",
        type=float,
        default=5.0,
        help="Delay in seconds between captures (default: 5).",
    )
    parser.add_argument(
        "--initial-wait",
        type=float,
        default=5.0,
        help="Initial wait time before the first capture (default: 5).",
    )
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    config = CaptureConfig(
        limit=args.limit,
        delay_seconds=args.delay,
        initial_wait_seconds=args.initial_wait,
    )

    driver = create_driver()
    try:
        for numbers in capture_numbers(driver, config=config):
            print("Últimos números:", numbers)
    except KeyboardInterrupt:
        print("\nEncerrado pelo usuário.")
    finally:
        with suppress(Exception):
            driver.quit()


if __name__ == "__main__":
    main()
