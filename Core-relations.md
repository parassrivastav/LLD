# Core object relationships

This project demonstrates four common relationships between classes:

```text
Association  = uses-a
Aggregation  = has-a, but both can exist independently
Composition  = owns-a, and creates/controls the part
Inheritance  = is-a
```

## 1. Association

> One object uses another object without owning it.

`VehicleService.movement_report()` temporarily uses vehicle objects:

```python
def movement_report(self, vehicles: Iterable[Vehicle]) -> list[str]:
    return [vehicle.move() for vehicle in vehicles]
```

The service receives the vehicles, calls `move()`, and returns a report. It does not
store, create, or destroy them.

```text
VehicleService ---- uses ----> Vehicle
```

This is association because both objects exist independently and only collaborate
during the method call.

## 2. Aggregation

> One object contains other objects, but those objects can exist independently.

`InMemoryVehicleRepository` stores vehicle objects:

```python
class InMemoryVehicleRepository:
    def __init__(self) -> None:
        self._vehicles: dict[str, Vehicle] = {}

    def save(self, vehicle: Vehicle) -> None:
        self._vehicles[vehicle.registration] = vehicle
```

The vehicle is created before it is given to the repository:

```python
slavia = SkodaSlavia("MH01SL2026")
repository.save(slavia)
```

Removing the repository does not conceptually remove the Slavia object held by the
caller. The vehicle has its own independent lifecycle.

```text
InMemoryVehicleRepository ◇---- Vehicle
```

The empty diamond (`◇`) represents aggregation.

Constructor injection is another aggregation example:

```python
repository = InMemoryVehicleRepository()
service = VehicleService(repository)
```

The repository is created outside the service and can exist without it.

## 3. Composition

> One object owns a part and creates or controls that part.

By default, `SkodaSlavia` creates its own engine when no engine is supplied:

```python
engine or CombustionEngine("petrol")
```

Used like this:

```python
slavia = SkodaSlavia("MH01SL2026")
```

the Slavia creates and contains its default engine. This demonstrates composition:

```text
SkodaSlavia ◆---- CombustionEngine
```

The filled diamond (`◆`) represents composition.

The design also allows an engine to be supplied:

```python
engine = CombustionEngine("petrol")
slavia = SkodaSlavia("MH01SL2026", engine)
```

In that case, the engine was created independently, so the relationship behaves
more like aggregation. Python does not enforce object ownership; the way objects are
created and managed determines the relationship.

## 4. Inheritance

> A child class is a specialized form of its parent class.

The Slavia uses multi-level inheritance:

```text
Vehicle
   ↑
  Car
   ↑
 Sedan
   ↑
SkodaSlavia
```

The classes declare that relationship directly:

```python
class Car(Vehicle):
    ...

class Sedan(Car):
    ...

class SkodaSlavia(Sedan):
    ...
```

`SkodaSlavia` inherits:

- `start()`, `stop()`, and `drive()` from `Vehicle`.
- `seats` from `Car`.
- `boot_capacity_litres` and `open_boot()` from `Sedan`.
- Its own variant, transmission, color, and `move()` behavior.

The test proves the complete relationship:

```python
self.assertIsInstance(slavia, SkodaSlavia)
self.assertIsInstance(slavia, Sedan)
self.assertIsInstance(slavia, Car)
self.assertIsInstance(slavia, Vehicle)
```

## Quick comparison

| Relationship | Simple meaning | Example in this project |
|---|---|---|
| Association | Uses another object temporarily | Service uses vehicles for a report |
| Aggregation | Contains independent objects | Repository stores vehicles |
| Composition | Owns or creates a part | Slavia creates its default engine |
| Inheritance | Child **is a** parent type | Slavia is a Sedan, Car, and Vehicle |

The most important difference is ownership. Association only uses an object,
aggregation contains an independent object, composition owns a part, and
inheritance creates a parent-child type relationship.
