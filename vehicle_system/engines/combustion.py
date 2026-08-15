"""Combustion engine implementation."""

from vehicle_system.domain.engine import Engine


class CombustionEngine(Engine):  # Inheritance — this is an Engine.
    def __init__(self, fuel: str = "petrol") -> None:
        self._fuel = fuel

    @property
    def energy_source(self) -> str:
        return self._fuel

    def start(self) -> str:
        return f"{self._fuel.title()} engine started"

    def stop(self) -> str:
        return f"{self._fuel.title()} engine stopped"
