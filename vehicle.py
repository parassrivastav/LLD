"""Educational vehicle domain demonstrating Python OOP and SOLID principles."""

# Keep type annotations as descriptions instead of evaluating them immediately.
# This lets a method mention classes that are still being defined below.
from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from typing import ClassVar, Iterable, Iterator, Protocol


class VehicleError(Exception):
    """Base exception for vehicle domain errors."""


class InvalidVehicleError(VehicleError, ValueError):
    """Raised when vehicle data violates a domain rule."""


class VehicleState(Enum):
    """Enum: a fixed set of allowed values, avoiding arbitrary state strings."""

    PARKED = "parked"
    RUNNING = "running"


class Engine(ABC):
    """Abstraction implemented by any engine type (DIP and OCP)."""

    # @property lets callers write `engine.energy_source` instead of calling
    # `engine.energy_source()`, while the implementation remains a method.
    @property
    @abstractmethod
    def energy_source(self) -> str:
        """Return the source used to power this engine."""

    # @abstractmethod forces each concrete Engine subclass to implement this.
    # `-> str` is a return-type annotation: this method should return text.
    @abstractmethod
    def start(self) -> str:
        """Start the engine."""

    @abstractmethod
    def stop(self) -> str:
        """Stop the engine."""


class CombustionEngine(Engine):
    def __init__(self, fuel: str = "petrol") -> None:
        self._fuel = fuel

    @property
    def energy_source(self) -> str:
        return self._fuel

    def start(self) -> str:
        return f"{self._fuel.title()} engine started"

    def stop(self) -> str:
        return f"{self._fuel.title()} engine stopped"


class ElectricMotor(Engine):
    @property
    def energy_source(self) -> str:
        return "electricity"

    def start(self) -> str:
        return "Electric motor ready"

    def stop(self) -> str:
        return "Electric motor switched off"


class Vehicle(ABC):
    """Abstract base class shared by every vehicle.

    It deliberately owns only vehicle behavior (SRP). Persistence, printing, and
    servicing are separate collaborators.
    """

    # `: ClassVar[int]` is a type annotation. It says this integer belongs to
    # the class and is shared, rather than being unique to each object.
    wheels: ClassVar[int] = 0
    vehicle_count: ClassVar[int] = 0

    def __init__(
        self,
        # `: str` and `: Engine` document the expected argument types.
        registration: str,
        brand: str,
        model: str,
        engine: Engine,
        *,  # Arguments after * must be supplied by name, e.g. year=2024.
        year: int = 2026,
        odometer_km: float = 0,
    ) -> None:  # Constructors modify the object and do not return a value.
        self.registration = registration
        self.brand = brand
        self.model = model
        self.engine = engine
        self.year = year
        self.odometer_km = odometer_km
        self._state = VehicleState.PARKED
        type(self).vehicle_count += 1

    # Together, @property and @registration.setter provide controlled access
    # to `_registration`; assignments are cleaned and validated in one place.
    @property
    def registration(self) -> str:
        return self._registration

    @registration.setter
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

    # @classmethod receives the class as `cls`. It is commonly used for a
    # named/alternative constructor. Python does not overload constructors.
    @classmethod
    def from_string(cls, data: str, engine: Engine) -> Vehicle:
        """Alternative constructor: 'registration,brand,model,year'."""
        registration, brand, model, year = (part.strip() for part in data.split(","))
        return cls(registration, brand, model, engine, year=int(year))

    # @staticmethod belongs conceptually to Vehicle but needs no `self` or
    # `cls`, because this calculation does not use an object or class state.
    @staticmethod
    def is_vintage(year: int) -> bool:
        return 2026 - year >= 25

    def start(self) -> str:
        if self._state is VehicleState.RUNNING:
            return f"{self.display_name} is already running"
        self._state = VehicleState.RUNNING
        return self.engine.start()

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
    def move(self) -> str:
        """Describe movement; subclasses provide polymorphic behavior."""

    # Double-underscore (`dunder`) methods integrate our class with Python.
    # str(vehicle), repr(vehicle), ==, and set/dict hashing call these methods.
    def __str__(self) -> str:
        return f"{self.display_name} ({self.registration})"

    def __repr__(self) -> str:
        return (
            f"{type(self).__name__}(registration={self.registration!r}, "
            f"brand={self.brand!r}, model={self.model!r}, year={self.year!r})"
        )

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Vehicle):
            return NotImplemented
        return self.registration == other.registration

    def __hash__(self) -> int:
        return hash(self.registration)


class Car(Vehicle):
    wheels = 4

    def __init__(self, *args: object, seats: int = 5, **kwargs: object) -> None:
        # *args collects positional arguments; **kwargs collects named ones.
        # super() delegates the common initialization to Vehicle.__init__.
        super().__init__(*args, **kwargs)
        if seats < 1:
            raise InvalidVehicleError("a car needs at least one seat")
        self.seats = seats

    def move(self) -> str:
        return f"{self.display_name} drives on {self.wheels} wheels"


class Motorcycle(Vehicle):
    wheels = 2

    def move(self) -> str:
        return f"{self.display_name} balances on {self.wheels} wheels"


class Flyable(Protocol):
    """Small client-specific interface (ISP)."""

    # Protocol describes an interface. Any object with a compatible `fly`
    # method can be treated as Flyable without explicitly inheriting from it.
    def fly(self) -> str: ...


class Aircraft(Vehicle):
    wheels = 3

    def move(self) -> str:
        return self.fly()

    def fly(self) -> str:
        return f"{self.display_name} flies through the air"


class VehicleRepository(Protocol):
    """Persistence abstraction; high-level services do not depend on a DB."""

    def save(self, vehicle: Vehicle) -> None: ...

    def get(self, registration: str) -> Vehicle | None: ...


class InMemoryVehicleRepository:
    def __init__(self) -> None:
        self._vehicles: dict[str, Vehicle] = {}

    def save(self, vehicle: Vehicle) -> None:
        self._vehicles[vehicle.registration] = vehicle

    def get(self, registration: str) -> Vehicle | None:
        return self._vehicles.get(registration.strip().upper())

    def __len__(self) -> int:
        return len(self._vehicles)

    def __iter__(self) -> Iterator[Vehicle]:
        return iter(self._vehicles.values())


class VehicleService:
    """High-level use case depending on abstractions (DIP)."""

    def __init__(self, repository: VehicleRepository) -> None:
        self._repository = repository

    def register(self, vehicle: Vehicle) -> None:
        if self._repository.get(vehicle.registration):
            raise VehicleError(f"{vehicle.registration} is already registered")
        self._repository.save(vehicle)

    def movement_report(self, vehicles: Iterable[Vehicle]) -> list[str]:
        """Works with every valid subtype (polymorphism and LSP)."""
        return [vehicle.move() for vehicle in vehicles]


# @dataclass automatically creates constructor/equality/display methods.
# frozen=True prevents fields changing after a ServiceRecord is constructed.
@dataclass(frozen=True)
class ServiceRecord:
    """Immutable value object composed with a vehicle when needed."""

    registration: str
    description: str
    cost: float


def main() -> None:
    repository = InMemoryVehicleRepository()
    service = VehicleService(repository)

    car = Car.from_string("KA01AB1234, Tata, Nexon, 2024", ElectricMotor())
    bike = Motorcycle("KA02XY9876", "Royal Enfield", "Classic", CombustionEngine())
    plane = Aircraft("VT-DEMO", "Cessna", "172", CombustionEngine("aviation fuel"))

    for vehicle in (car, bike, plane):
        service.register(vehicle)
        print(vehicle)
        print(" ", vehicle.start())
        print(" ", vehicle.move())
        print(" ", vehicle.stop())

    print("Movement report:", service.movement_report(repository))


if __name__ == "__main__":
    main()
