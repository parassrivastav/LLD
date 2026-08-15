"""Abstract vehicle containing behavior shared by all vehicle types."""

# Delays annotation evaluation — lets types refer to classes defined later.
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import ClassVar

from vehicle_system.domain.engine import Engine
from vehicle_system.domain.enums import VehicleState
from vehicle_system.domain.exceptions import InvalidVehicleError, VehicleError


class Vehicle(ABC):  # Abstract parent — shares code between vehicle types.
    wheels: ClassVar[int] = 0  # Class variable — shared by objects.
    vehicle_count: ClassVar[int] = 0

    def __init__(
        self,
        registration: str,  # Type annotation — expected input type.
        brand: str,
        model: str,
        engine: Engine,
        *,  # Keyword-only — call as year=2024.
        year: int = 2026,
        odometer_km: float = 0,
    ) -> None:  # -> None means this method returns nothing.
        self.registration = registration  # Calls the setter for validation.
        self.brand = brand  # `self` stores data in this object.
        self.model = model
        self.engine = engine  # Composition — Vehicle has an Engine.
        self.year = year
        self.odometer_km = odometer_km
        self._state = VehicleState.PARKED  # `_` marks internal data.
        type(self).vehicle_count += 1

    @property  # Getter — controls access to internal registration.
    def registration(self) -> str:
        return self._registration

    @registration.setter  # Setter — validates registration before storing it.
    def registration(self, value: str) -> None:
        cleaned = value.strip().upper()
        if not cleaned:
            raise InvalidVehicleError("registration cannot be empty")
        self._registration = cleaned

    @property
    def odometer_km(self) -> float:
        return self._odometer_km

    @odometer_km.setter
    def odometer_km(self, value: float) -> None:
        if value < 0:
            raise InvalidVehicleError("odometer cannot be negative")
        self._odometer_km = float(value)

    @property
    def state(self) -> VehicleState:
        return self._state

    @property
    def display_name(self) -> str:
        return f"{self.brand} {self.model}"

    @classmethod  # Alternative constructor — creates a vehicle from text.
    def from_string(cls, data: str, engine: Engine) -> Vehicle:
        registration, brand, model, year = (part.strip() for part in data.split(","))
        return cls(registration, brand, model, engine, year=int(year))

    @staticmethod  # Utility method — does not need `self` or `cls`.
    def is_vintage(year: int) -> bool:
        return 2026 - year >= 25

    def start(self) -> str:
        if self._state is VehicleState.RUNNING:
            return f"{self.display_name} is already running"
        self._state = VehicleState.RUNNING
        return self.engine.start()  # Delegates work to the composed Engine.

    def stop(self) -> str:
        if self._state is VehicleState.PARKED:
            return f"{self.display_name} is already parked"
        self._state = VehicleState.PARKED
        return self.engine.stop()

    def drive(self, distance_km: float) -> str:
        if self._state is not VehicleState.RUNNING:
            raise VehicleError("start the vehicle before driving")
        if distance_km <= 0:
            raise InvalidVehicleError("distance must be positive")
        self._odometer_km += distance_km
        return f"{self.display_name} travelled {distance_km:g} km"

    @abstractmethod
    def move(self) -> str:  # Subclasses must override this method.
        """Describe how this vehicle moves."""

    def __str__(self) -> str:  # Used by print(vehicle).
        return f"{self.display_name} ({self.registration})"

    def __repr__(self) -> str:  # Used for developer-friendly display.
        return (
            f"{type(self).__name__}(registration={self.registration!r}, "
            f"brand={self.brand!r}, model={self.model!r}, year={self.year!r})"
        )

    def __eq__(self, other: object) -> bool:  # Used by vehicle1 == vehicle2.
        if not isinstance(other, Vehicle):
            return NotImplemented
        return self.registration == other.registration

    def __hash__(self) -> int:  # Allows vehicles in sets and dictionary keys.
        return hash(self.registration)
