"""Motorcycle implementation."""

from vehicle_system.domain.vehicle import Vehicle


class Motorcycle(Vehicle):  # Substitution — usable wherever Vehicle is expected.
    wheels = 2

    def move(self) -> str:
        return f"{self.display_name} balances on {self.wheels} wheels"
