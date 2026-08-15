"""Vehicle application service."""

from collections.abc import Iterable

from vehicle_system.domain.exceptions import VehicleError
from vehicle_system.domain.vehicle import Vehicle
from vehicle_system.repositories.interface import VehicleRepository


class VehicleService:  # Keeps application rules separate from storage.
    def __init__(self, repository: VehicleRepository) -> None:
        self._repository = repository  # Dependency injection (DIP).

    def register(self, vehicle: Vehicle) -> None:
        if self._repository.get(vehicle.registration):
            raise VehicleError(f"{vehicle.registration} is already registered")
        self._repository.save(vehicle)

    def movement_report(self, vehicles: Iterable[Vehicle]) -> list[str]:
        return [vehicle.move() for vehicle in vehicles]  # Runtime polymorphism.
