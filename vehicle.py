"""Educational vehicle domain demonstrating Python OOP and SOLID principles."""

# Delays annotation evaluation — lets types refer to classes defined later.
from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from typing import ClassVar, Iterable, Iterator, Protocol


class VehicleError(Exception):  # Custom exception — reports vehicle errors.
    """Base exception for vehicle domain errors."""


class InvalidVehicleError(VehicleError, ValueError):  # Inherits both error types.
    """Raised when vehicle data violates a domain rule."""


class VehicleState(Enum):  # Enum — limits state to these fixed values.
    """Enum: a fixed set of allowed values, avoiding arbitrary state strings."""

    PARKED = "parked"
    RUNNING = "running"


class Engine(ABC):  # ABC — blueprint that cannot be used directly.
    """Abstraction implemented by any engine type (DIP and OCP)."""

    # Property — reads a method like an attribute: engine.energy_source.
    @property
    @abstractmethod
    def energy_source(self) -> str:
        """Return the source used to power this engine."""

    # Abstract method — every engine must provide its own start behavior.
    @abstractmethod
    def start(self) -> str:
        """Start the engine."""

    @abstractmethod
    def stop(self) -> str:
        """Stop the engine."""


class CombustionEngine(Engine):  # Inheritance — combustion engine is an Engine.
    def __init__(self, fuel: str = "petrol") -> None:
        self._fuel = fuel  # Instance variable — belongs to this engine object.

    @property
    def energy_source(self) -> str:
        return self._fuel

    def start(self) -> str:
        return f"{self._fuel.title()} engine started"

    def stop(self) -> str:
        return f"{self._fuel.title()} engine stopped"


class ElectricMotor(Engine):  # New engine type without changing Vehicle (OCP).
    @property
    def energy_source(self) -> str:
        return "electricity"

    def start(self) -> str:
        return "Electric motor ready"

    def stop(self) -> str:
        return "Electric motor switched off"


class Vehicle(ABC):  # Abstract parent — shares code between vehicle types.
    """Abstract base class shared by every vehicle.

    It deliberately owns only vehicle behavior (SRP). Persistence, printing, and
    servicing are separate collaborators.
    """

    # Class variables — values shared by all objects of the class.
    wheels: ClassVar[int] = 0
    vehicle_count: ClassVar[int] = 0

    def __init__(
        self,
        # Type annotations — show the expected input types.
        registration: str,
        brand: str,
        model: str,
        engine: Engine,
        *,  # Keyword-only — call as year=2024.
        year: int = 2026,
        odometer_km: float = 0,
    ) -> None:  # -> None means this method returns nothing.
        self.registration = registration  # Calls the setter for validation.
        self.brand = brand  # `self` stores data in this particular object.
        self.model = model
        self.engine = engine  # Composition — Vehicle has an Engine.
        self.year = year
        self.odometer_km = odometer_km
        self._state = VehicleState.PARKED  # `_` marks internal data.
        type(self).vehicle_count += 1  # Count objects of the concrete class.

    # Property and setter — control reading and updating registration.
    @property
    def registration(self) -> str:
        return self._registration  # Getter — returns the internal value.

    @registration.setter
    def registration(self, value: str) -> None:
        cleaned = value.strip().upper()  # Normalize before storing.
        if not cleaned:
            raise InvalidVehicleError("registration cannot be empty")  # Stop invalid data.
        self._registration = cleaned  # Setter — stores the checked value.

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

    # Class method — creates a Vehicle from one string.
    @classmethod
    def from_string(cls, data: str, engine: Engine) -> Vehicle:
        """Alternative constructor: 'registration,brand,model,year'."""
        registration, brand, model, year = (part.strip() for part in data.split(","))
        return cls(registration, brand, model, engine, year=int(year))

    # Static method — utility that needs no object (`self`).
    @staticmethod
    def is_vintage(year: int) -> bool:
        return 2026 - year >= 25

    def start(self) -> str:
        if self._state is VehicleState.RUNNING:
            return f"{self.display_name} is already running"
        self._state = VehicleState.RUNNING  # Change this object's state.
        return self.engine.start()  # Delegate work to the composed Engine.

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
        """Describe movement; subclasses provide polymorphic behavior."""

    # Dunder methods — define print, debug, equality, and set/dict behavior.
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


class Car(Vehicle):  # Inheritance — Car gets Vehicle's common behavior.
    wheels = 4  # Override the parent's class variable.

    def __init__(self, *args: object, seats: int = 5, **kwargs: object) -> None:
        # super() — reuses the parent Vehicle constructor.
        super().__init__(*args, **kwargs)  # Run Vehicle.__init__ first.
        if seats < 1:
            raise InvalidVehicleError("a car needs at least one seat")
        self.seats = seats

    def move(self) -> str:  # Overriding — Car provides its own movement.
        return f"{self.display_name} drives on {self.wheels} wheels"


class Motorcycle(Vehicle):  # Another Vehicle subtype (LSP).
    wheels = 2

    def move(self) -> str:
        return f"{self.display_name} balances on {self.wheels} wheels"


class Flyable(Protocol):
    """Small client-specific interface (ISP)."""

    # Protocol — interface for anything that can fly.
    def fly(self) -> str: ...


class Aircraft(Vehicle, Flyable):  # Implements both Vehicle and Flyable contracts.
    wheels = 3

    def move(self) -> str:
        return self.fly()

    def fly(self) -> str:
        return f"{self.display_name} flies through the air"


class VehicleRepository(Protocol):
    """Persistence abstraction; high-level services do not depend on a DB."""

    def save(self, vehicle: Vehicle) -> None: ...

    def get(self, registration: str) -> Vehicle | None: ...


class InMemoryVehicleRepository:  # Stores vehicles in memory, not a database.
    def __init__(self) -> None:
        self._vehicles: dict[str, Vehicle] = {}  # registration -> vehicle

    def save(self, vehicle: Vehicle) -> None:
        self._vehicles[vehicle.registration] = vehicle  # Save using a unique key.

    def get(self, registration: str) -> Vehicle | None:
        return self._vehicles.get(registration.strip().upper())

    def __len__(self) -> int:
        return len(self._vehicles)

    def __iter__(self) -> Iterator[Vehicle]:
        return iter(self._vehicles.values())


class VehicleService:  # Service — contains application rules, not storage.
    """High-level use case depending on abstractions (DIP)."""

    def __init__(self, repository: VehicleRepository) -> None:
        self._repository = repository  # Dependency injection (DIP).

    def register(self, vehicle: Vehicle) -> None:
        if self._repository.get(vehicle.registration):
            raise VehicleError(f"{vehicle.registration} is already registered")
        self._repository.save(vehicle)

    def movement_report(self, vehicles: Iterable[Vehicle]) -> list[str]:
        """Works with every valid subtype (polymorphism and LSP)."""
        return [vehicle.move() for vehicle in vehicles]  # Same call, different behavior.


# Frozen dataclass — creates boilerplate methods and prevents field changes.
@dataclass(frozen=True)
class ServiceRecord:
    """Immutable value object composed with a vehicle when needed."""

    registration: str
    description: str
    cost: float


def main() -> None:
    repository = InMemoryVehicleRepository()  # Create the low-level dependency.
    service = VehicleService(repository)  # Inject it into the high-level service.

    car = Car.from_string("KA01AB1234, Tata, Nexon, 2024", ElectricMotor())
    bike = Motorcycle("KA02XY9876", "Royal Enfield", "Classic", CombustionEngine())
    plane = Aircraft("VT-DEMO", "Cessna", "172", CombustionEngine("aviation fuel"))

    for vehicle in (car, bike, plane):  # Polymorphism — one loop, three types.
        service.register(vehicle)
        print(vehicle)
        print(" ", vehicle.start())
        print(" ", vehicle.move())
        print(" ", vehicle.stop())

    print("Movement report:", service.movement_report(repository))


if __name__ == "__main__":
    main()
