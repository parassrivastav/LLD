"""Repository contract used by application services."""

from typing import Protocol

from vehicle_system.domain.vehicle import Vehicle


class VehicleRepository(Protocol):  # Interface — hides storage details.
    def save(self, vehicle: Vehicle) -> None: ...

    def get(self, registration: str) -> Vehicle | None: ...
