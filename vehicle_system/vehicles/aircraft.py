"""Aircraft implementation and focused flying interface."""

from typing import Protocol

from vehicle_system.domain.vehicle import Vehicle


class Flyable(Protocol):  # Interface — describes anything that can fly.
    def fly(self) -> str: ...


class Aircraft(Vehicle, Flyable):  # Implements both contracts.
    wheels = 3

    def move(self) -> str:
        return self.fly()

    def fly(self) -> str:
        return f"{self.display_name} flies through the air"
