"""High level helpers for collecting roulette numbers from Betfair."""

from __future__ import annotations

import contextlib
import time
from dataclasses import dataclass
from typing import Iterable, Iterator, List, Sequence

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager


BETFAIR_ROULETTE_URL = "https://casino.betfair.com/pt-br/c/roleta"
NUMBER_CLASS_NAME = "number"


@dataclass
class CaptureConfig:
    """Configuration values for the capture loop."""

    limit: int = 8
    delay_seconds: float = 5.0
    initial_wait_seconds: float = 5.0


def create_driver() -> webdriver.Chrome:
    """Instantiate a Chrome WebDriver using ``webdriver-manager``.

    Returns
    -------
    webdriver.Chrome
        The ready-to-use Chrome driver.
    """

    service = Service(ChromeDriverManager().install())
    return webdriver.Chrome(service=service)


def _extract_numbers(elements: Sequence) -> List[str]:
    """Extract up to ``CaptureConfig.limit`` numbers from the given elements."""

    numbers: List[str] = []
    for element in elements:
        number = element.text.strip()
        if not number:
            continue
        numbers.append(number)
    return numbers


def capture_numbers(
    driver: webdriver.Chrome,
    config: CaptureConfig | None = None,
) -> Iterator[List[str]]:
    """Continuously capture roulette numbers from Betfair.

    Parameters
    ----------
    driver:
        An instance of :class:`webdriver.Chrome`.
    config:
        Optional :class:`CaptureConfig` containing loop settings.

    Yields
    ------
    list[str]
        A list containing the most recent roulette numbers.
    """

    cfg = config or CaptureConfig()

    driver.get(BETFAIR_ROULETTE_URL)
    time.sleep(cfg.initial_wait_seconds)

    while True:
        with contextlib.suppress(Exception):
            elements = driver.find_elements(By.CLASS_NAME, NUMBER_CLASS_NAME)
            limited_elements = elements[: cfg.limit]
            numbers = _extract_numbers(limited_elements)
            if numbers:
                yield numbers

        time.sleep(cfg.delay_seconds)


def capture_numbers_once(
    driver: webdriver.Chrome,
    limit: int = 8,
    initial_wait_seconds: float = 5.0,
) -> List[str]:
    """Capture roulette numbers once, returning the latest results."""

    driver.get(BETFAIR_ROULETTE_URL)
    time.sleep(initial_wait_seconds)
    elements = driver.find_elements(By.CLASS_NAME, NUMBER_CLASS_NAME)
    limited_elements = elements[:limit]
    return _extract_numbers(limited_elements)
