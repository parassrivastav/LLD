"""Value objects related to vehicle servicing."""

from dataclasses import dataclass


@dataclass(frozen=True)  # Generates boilerplate and prevents field changes.
class ServiceRecord:
    registration: str
    description: str
    cost: float
