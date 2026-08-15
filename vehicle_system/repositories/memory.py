"""In-memory repository used by the demo and tests."""

from collections.abc import Iterator

from vehicle_system.domain.vehicle import Vehicle


class InMemoryVehicleRepository:  # Stores objects without a database.
    def __init__(self) -> None:
        self._vehicles: dict[str, Vehicle] = {}  # registration -> vehicle

    def save(self, vehicle: Vehicle) -> None:
        self._vehicles[vehicle.registration] = vehicle

    def get(self, registration: str) -> Vehicle | None:
        return self._vehicles.get(registration.strip().upper())

    def __len__(self) -> int:
        return len(self._vehicles)

    def __iter__(self) -> Iterator[Vehicle]:
        return iter(self._vehicles.values())
