"""Base class for sedan cars."""

from typing import Any

from vehicle_system.domain.exceptions import InvalidVehicleError
from vehicle_system.vehicles.cars.car import Car


class Sedan(Car):  # Inheritance chain: Vehicle -> Car -> Sedan.
    body_style = "sedan"

    def __init__(
        self,
        *args: Any,
        boot_capacity_litres: int,
        **kwargs: Any,
    ) -> None:
        super().__init__(*args, **kwargs)  # Calls Car, then Vehicle constructor.
        if boot_capacity_litres <= 0:
            raise InvalidVehicleError("boot capacity must be positive")
        self.boot_capacity_litres = boot_capacity_litres

    def open_boot(self) -> str:
        return f"Opened the {self.boot_capacity_litres}-litre boot"

    def move(self) -> str:  # Sedan-specific override of Car.move().
        return f"{self.display_name} sedan drives on {self.wheels} wheels"
