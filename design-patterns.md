# Design patterns in the Vehicle System

A design pattern is a reusable approach to a common software-design problem. It is
not a library or fixed piece of code. This project demonstrates the following
patterns and architectural patterns.

## 1. Strategy pattern

> Put interchangeable behavior behind a common interface.

`Engine` defines the common strategy:

```python
class Engine(ABC):
    @abstractmethod
    def start(self) -> str: ...

    @abstractmethod
    def stop(self) -> str: ...
```

The concrete strategies are:

```python
class CombustionEngine(Engine): ...
class ElectricMotor(Engine): ...
```

A vehicle delegates engine behavior to the selected strategy:

```python
class Vehicle:
    def __init__(self, ..., engine: Engine) -> None:
        self.engine = engine

    def start(self) -> str:
        return self.engine.start()
```

The strategy can be selected when constructing the vehicle:

```python
petrol_car = Car(..., engine=CombustionEngine("petrol"))
electric_car = Car(..., engine=ElectricMotor())
```

`Vehicle` does not need `if petrol` or `if electric` conditions.

## 2. Repository pattern

> Hide storage details behind a collection-like interface.

The repository contract defines what the application needs:

```python
class VehicleRepository(Protocol):
    def save(self, vehicle: Vehicle) -> None: ...
    def get(self, registration: str) -> Vehicle | None: ...
```

The current implementation stores vehicles in a dictionary:

```python
class InMemoryVehicleRepository:
    def save(self, vehicle: Vehicle) -> None:
        self._vehicles[vehicle.registration] = vehicle
```

A future database repository can implement the same contract. The service does not
need to know where or how vehicles are stored.

## 3. Dependency Injection pattern

> Give an object its dependencies instead of letting it create them.

`VehicleService` receives its repository through the constructor:

```python
class VehicleService:
    def __init__(self, repository: VehicleRepository) -> None:
        self._repository = repository
```

`main.py` supplies the concrete object:

```python
repository = InMemoryVehicleRepository()
service = VehicleService(repository)
```

`Vehicle` receives its engine in the same way. This makes implementations easy to
replace and makes unit testing simpler.

## 4. Factory-style named constructor

> Hide object-creation details behind a clearly named method.

`from_string()` creates a vehicle from formatted text:

```python
@classmethod
def from_string(cls, data: str, engine: Engine) -> Vehicle:
    registration, brand, model, year = (part.strip() for part in data.split(","))
    return cls(registration, brand, model, engine, year=int(year))
```

Usage:

```python
car = Car.from_string(
    "KA01AB1234, Tata, Nexon, 2024",
    ElectricMotor(),
)
```

This is a Python named-constructor/factory technique. It is simpler than a separate
factory class because creation currently has only one parsing rule.

## 5. Iterator pattern

> Access items one by one without exposing the internal collection.

The repository implements Python's iterator protocol:

```python
def __iter__(self) -> Iterator[Vehicle]:
    return iter(self._vehicles.values())
```

Callers can iterate naturally:

```python
for vehicle in repository:
    print(vehicle)
```

The caller does not access the internal `_vehicles` dictionary.

## 6. Service Layer pattern

> Keep application use cases in a service instead of UI or storage code.

`VehicleService` coordinates repository operations and application rules:

```python
def register(self, vehicle: Vehicle) -> None:
    if self._repository.get(vehicle.registration):
        raise VehicleError("vehicle is already registered")
    self._repository.save(vehicle)
```

The duplicate-registration rule is not placed in `main.py` or the repository.

## 7. Value Object pattern

> Represent a value using an immutable object compared by its data.

`ServiceRecord` is a frozen dataclass:

```python
@dataclass(frozen=True)
class ServiceRecord:
    registration: str
    description: str
    cost: float
```

It cannot be changed after creation. Two records with equal fields compare as equal.

## 8. Composition Root pattern

> Create and connect application dependencies in one known place.

`main.py` is the composition root:

```python
repository = InMemoryVehicleRepository()
service = VehicleService(repository)
slavia = SkodaSlavia("KA03SK2026")
```

The domain classes do not contain application setup code. Replacing a dependency
requires changing only this outer setup area.

## Pattern flow

```text
main.py (Composition Root)
   |
   +--> VehicleService (Service Layer)
   |         |
   |         +--> VehicleRepository (Repository)
   |                    |
   |                    +--> InMemoryVehicleRepository
   |
   +--> Vehicle
             |
             +--> Engine (Strategy)
                    ├── CombustionEngine
                    └── ElectricMotor
```

## Quick comparison

| Pattern | Problem it solves | Project example |
|---|---|---|
| Strategy | Change behavior without conditionals | Interchangeable engines |
| Repository | Hide persistence details | `VehicleRepository` |
| Dependency Injection | Remove hard-coded dependencies | Repository and engine injection |
| Named Constructor | Simplify special object creation | `Vehicle.from_string()` |
| Iterator | Traverse without exposing storage | Iterating the repository |
| Service Layer | Organize application use cases | `VehicleService` |
| Value Object | Represent immutable descriptive data | `ServiceRecord` |
| Composition Root | Assemble the application centrally | `main.py` |

## Features that are not patterns

The project also uses `ABC`, inheritance, polymorphism, properties, `Enum`, and type
annotations. These are language or OOP features. They help implement patterns, but
they are not design patterns by themselves.
