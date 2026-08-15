"""Car implementation."""

from typing import Any

from vehicle_system.domain.exceptions import InvalidVehicleError
from vehicle_system.domain.vehicle import Vehicle


class Car(Vehicle):  # Inheritance — Car gets Vehicle behavior.
    wheels = 4  # Overrides the parent's class variable.

    def __init__(self, *args: Any, seats: int = 5, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)  # Runs the parent constructor.
        if seats < 1:
            raise InvalidVehicleError("a car needs at least one seat")
        self.seats = seats

    def move(self) -> str:  # Overriding — Car defines its movement.
        return f"{self.display_name} drives on {self.wheels} wheels"
