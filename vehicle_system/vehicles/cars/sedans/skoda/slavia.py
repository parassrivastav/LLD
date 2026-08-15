"""Concrete Skoda Slavia model."""

from vehicle_system.domain.engine import Engine
from vehicle_system.domain.exceptions import InvalidVehicleError
from vehicle_system.engines.combustion import CombustionEngine
from vehicle_system.vehicles.cars.sedans.sedan import Sedan


class SkodaSlavia(Sedan):  # Final class: Vehicle -> Car -> Sedan -> Slavia.
    wheels = 4
    boot_capacity_litres = 521
    fuel_tank_litres = 45
    ground_clearance_mm = 179
    safety_rating = 5

    VALID_TRANSMISSIONS = {"manual", "automatic"}

    def __init__(
        self,
        registration: str,
        engine: Engine | None = None,
        *,
        variant: str = "1.0 TSI Style",
        transmission: str = "manual",
        color: str = "Tornado Red",
        year: int = 2026,
        odometer_km: float = 0,
    ) -> None:
        normalized_transmission = transmission.strip().lower()
        if normalized_transmission not in self.VALID_TRANSMISSIONS:
            raise InvalidVehicleError("transmission must be manual or automatic")
        if not variant.strip():
            raise InvalidVehicleError("variant cannot be empty")
        if not color.strip():
            raise InvalidVehicleError("color cannot be empty")

        super().__init__(
            registration,
            "Skoda",
            "Slavia",
            engine or CombustionEngine("petrol"),
            year=year,
            odometer_km=odometer_km,
            seats=5,
            boot_capacity_litres=self.boot_capacity_litres,
        )
        self.variant = variant.strip()
        self.transmission = normalized_transmission
        self.color = color.strip()

    @property
    def specification(self) -> str:
        return f"{self.variant}, {self.transmission}, {self.color}"

    def move(self) -> str:
        return f"{self.display_name} {self.variant} drives as a premium sedan"
