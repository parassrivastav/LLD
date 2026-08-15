# SOLID principles in the Vehicle System

SOLID is a set of five design principles that helps keep object-oriented code
easy to understand, extend, test, and maintain.

## S — Single Responsibility Principle (SRP)

> A class should have one main responsibility.

This project separates different jobs into different classes:

| Class | Responsibility |
|---|---|
| `Vehicle` | Vehicle state, lifecycle, and odometer rules |
| `Engine` | Engine behavior |
| `InMemoryVehicleRepository` | Storing and finding vehicles |
| `VehicleService` | Application rules such as registration |
| `ServiceRecord` | Holding service information |

For example, `Vehicle` does not save itself in a database:

```python
class Vehicle:
    def start(self): ...
    def stop(self): ...
    def drive(self, distance_km): ...
```

Storage is handled separately:

```python
class InMemoryVehicleRepository:
    def save(self, vehicle): ...
    def get(self, registration): ...
```

Therefore, changing storage does not require changing vehicle behavior.

## O — Open/Closed Principle (OCP)

> Code should be open for extension but closed for unnecessary modification.

`Vehicle` defines the common contract:

```python
class Vehicle(ABC):
    @abstractmethod
    def move(self) -> str:
        ...
```

New vehicle types extend it:

```python
class Motorcycle(Vehicle):
    def move(self) -> str:
        return "Motorcycle moves on two wheels"
```

`SkodaSlavia` was added without modifying `Vehicle` or `VehicleService`:

```text
Vehicle -> Car -> Sedan -> SkodaSlavia
```

The same applies to engines. `ElectricMotor` and `CombustionEngine` extend
`Engine`. Another engine can be added without changing the vehicle classes.

## L — Liskov Substitution Principle (LSP)

> A child object should work wherever its parent type is expected.

`movement_report()` accepts any collection of `Vehicle` objects:

```python
def movement_report(self, vehicles: Iterable[Vehicle]) -> list[str]:
    return [vehicle.move() for vehicle in vehicles]
```

It works with every valid subtype:

```python
service.movement_report([car, motorcycle, aircraft, slavia])
```

Each child provides `move()` and follows the parent contract. The service does not
need to check whether an object is a `Car`, `Aircraft`, or `SkodaSlavia`.

The tests also prove the inheritance chain:

```python
self.assertIsInstance(slavia, Sedan)
self.assertIsInstance(slavia, Car)
self.assertIsInstance(slavia, Vehicle)
```

## I — Interface Segregation Principle (ISP)

> A class should not be forced to implement methods it does not need.

Flying behavior has a small, focused interface:

```python
class Flyable(Protocol):
    def fly(self) -> str: ...
```

`Aircraft` implements it, but `Car` and `Motorcycle` do not need a meaningless
`fly()` method.

Storage also has its own focused interface:

```python
class VehicleRepository(Protocol):
    def save(self, vehicle: Vehicle) -> None: ...
    def get(self, registration: str) -> Vehicle | None: ...
```

The interface contains only the operations required by `VehicleService`.

## D — Dependency Inversion Principle (DIP)

> High-level code should depend on abstractions, not concrete implementations.

`VehicleService` depends on the `VehicleRepository` interface:

```python
class VehicleService:
    def __init__(self, repository: VehicleRepository) -> None:
        self._repository = repository
```

It does not create an `InMemoryVehicleRepository` itself. The dependency is passed
from `main.py`:

```python
repository = InMemoryVehicleRepository()
service = VehicleService(repository)
```

This is called **dependency injection**. A database repository can replace the
in-memory repository without changing `VehicleService`.

`Vehicle` follows the same principle by depending on the abstract `Engine`:

```python
def __init__(self, ..., engine: Engine) -> None:
    self.engine = engine
```

It can receive either implementation:

```python
petrol_car = SkodaSlavia("MH01SL2026", CombustionEngine("petrol"))
electric_demo = SkodaSlavia("MH02SL2026", ElectricMotor())
```

## Complete flow

```text
main.py
  |
  | creates and injects
  v
VehicleService ------> VehicleRepository
                            ^
                            |
                 InMemoryVehicleRepository

Vehicle -------------> Engine
  ^                      ^
  |                      |
SkodaSlavia       CombustionEngine / ElectricMotor
```

- SRP keeps each box focused on one job.
- OCP allows new implementations to be added.
- LSP lets child objects replace their parent types.
- ISP keeps interfaces small and relevant.
- DIP makes arrows point toward abstractions.

## Why this matters

With this design, you can add a `Truck`, `HydrogenEngine`, or database repository
without rewriting the existing service and domain logic. Each new part follows an
existing contract and can be tested independently.
