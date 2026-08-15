# Vehicle OOP and SOLID example

This small Python project is a study example, not a claim that every real vehicle
system should use the same model. Run it with:

For a concept-by-concept explanation with examples, read
[`LEARNING_GUIDE.md`](LEARNING_GUIDE.md) alongside the source code.

For a principle-by-principle explanation of the design, read
[`SOLID.md`](SOLID.md).

For association, aggregation, composition, and inheritance, read
[`Core-relations.md`](Core-relations.md).

For the reusable design patterns used in the project, read
[`design-patterns.md`](design-patterns.md).

```bash
python3 main.py
python3 -m unittest discover -s tests -v
```

## Project structure

```text
vehicle_system/
├── domain/         # Core abstractions, state, errors, and value objects
├── engines/        # Concrete Engine implementations
├── vehicles/
│   └── cars/
│       └── sedans/
│           └── skoda/
│               └── slavia.py
├── repositories/   # Persistence interface and implementations
└── services/       # Application use cases
tests/              # Tests grouped by responsibility
main.py             # Composition root and runnable demo
```

The concrete Slavia example has a clear specialization chain:

```text
Vehicle -> Car -> Sedan -> SkodaSlavia
```

- `Vehicle` owns registration, engine, lifecycle, and odometer behavior.
- `Car` adds seats.
- `Sedan` adds body style and boot capacity.
- `SkodaSlavia` fixes the brand/model and adds Slavia specifications.

## How this project demonstrates OOP

### 1. Class and object

A class is a design. An object is a real instance created from that design.

```python
slavia = SkodaSlavia("MH01SL2026")
```

`SkodaSlavia` is the class and `slavia` is the object.

### 2. Constructor

`__init__()` initializes an object. Each class initializes only its own data:

- `Vehicle` initializes registration, brand, model, engine, and odometer.
- `Car` initializes seats.
- `Sedan` initializes boot capacity.
- `SkodaSlavia` initializes variant, transmission, and color.

Each constructor uses `super()` to call its parent constructor:

```python
super().__init__(*args, **kwargs)
```

### 3. Abstraction

`Vehicle` and `Engine` inherit from `ABC`, so they represent incomplete designs:

```python
class Vehicle(ABC):
    @abstractmethod
    def move(self) -> str:
        ...
```

Every concrete vehicle must provide `move()`. `Vehicle` cannot be instantiated
directly because it contains an abstract method.

### 4. Inheritance

Child classes reuse and specialize parent behavior:

```text
Vehicle -> Car -> Sedan -> SkodaSlavia
```

Therefore, a `SkodaSlavia` object receives `start()`, `stop()`, and `drive()` from
`Vehicle`, seats from `Car`, and boot behavior from `Sedan`.

### 5. Encapsulation

Internal values use a leading underscore:

```python
self._registration = cleaned
self._state = VehicleState.PARKED
```

Properties control how those values are accessed and changed:

```python
@registration.setter
def registration(self, value: str) -> None:
    # Clean and validate before storing.
```

This prevents an empty registration or negative odometer from entering the object.

### 6. Polymorphism

Different vehicle objects respond differently to the same `move()` call:

```python
for vehicle in (car, bike, plane, slavia):
    print(vehicle.move())
```

Python automatically calls the correct implementation for each object.

### 7. Method overriding

The parent declares `move()`, and children replace it with specific behavior:

```python
class SkodaSlavia(Sedan):
    def move(self) -> str:
        return "Skoda Slavia drives as a premium sedan"
```

This is why polymorphism works.

### 8. Composition

A vehicle **has an** engine instead of being an engine:

```python
self.engine = engine
```

The engine is supplied through the constructor, so the same vehicle design can use
a different `Engine` implementation without changing `Vehicle`.

### 9. Class and instance attributes

Instance attributes can differ for every object:

```python
self.color = color
```

Class attributes describe values shared by the class:

```python
class SkodaSlavia(Sedan):
    wheels = 4
    fuel_tank_litres = 45
```

### 10. Types of methods

- Instance method: receives `self` and works with one object, such as `start()`.
- Class method: receives `cls`; `from_string()` is an alternative constructor.
- Static method: receives neither; `is_vintage()` is a related utility.

### 11. Interfaces with Protocol

`VehicleRepository` is a small interface describing required storage operations:

```python
class VehicleRepository(Protocol):
    def save(self, vehicle: Vehicle) -> None: ...
```

`VehicleService` can use any repository that follows this interface.

### 12. Special methods

Python calls these methods through its normal syntax:

| Method | Usage |
|---|---|
| `__init__` | Creates and initializes an object |
| `__str__` | `print(vehicle)` |
| `__repr__` | Developer/debug display |
| `__eq__` | `vehicle1 == vehicle2` |
| `__hash__` | Allows objects in sets and dictionary keys |
| `__len__` | `len(repository)` |
| `__iter__` | `for vehicle in repository` |

### 13. Association between objects

`VehicleService` receives and works with a repository. They are separate objects
that collaborate without inheriting from each other.

### 14. Immutable value object

`ServiceRecord` uses a frozen dataclass:

```python
@dataclass(frozen=True)
class ServiceRecord:
    ...
```

Python creates common methods automatically, and its values cannot change after
the object is created.

Python does not support constructor overloading by signature. It uses default and
keyword arguments or named class methods such as `from_string()` instead. Python
also has no truly private fields; a leading underscore marks internal data, while
properties provide controlled access.

Python does not support constructor overloading by signature. Idiomatic Python uses
default/keyword arguments and named class methods such as `from_string()` instead.
Python also has no truly private fields; a leading underscore communicates protected
internal state, while properties provide controlled access.

## Reading the type annotations

Annotations are optional labels that document expected types. They help readers,
editors, and type-checking tools, but Python normally does not enforce them while the
program runs.

```python
def drive(distance_km: float) -> str:
```

- `distance_km: float` says the argument should be a number.
- `-> str` says the method should return text.
- `-> None` means the method returns no useful value.
- `Vehicle | None` means either a `Vehicle` or no result (`None`).
- `list[str]` means a list containing strings.
- `ClassVar[int]` identifies a class-level integer shared by objects.

Decorators beginning with `@` are different from type annotations. A decorator
changes or describes method/class behavior: examples include `@property`,
`@classmethod`, `@staticmethod`, `@abstractmethod`, and `@dataclass`.

## SOLID mapping

| Principle | Where it appears |
|---|---|
| Single Responsibility | Vehicle behavior, persistence, and use cases live in separate classes. |
| Open/Closed | New `Engine` or `Vehicle` implementations can be added without modifying services. |
| Liskov Substitution | Each concrete vehicle can be passed to `movement_report()`. |
| Interface Segregation | Focused `Flyable` and `VehicleRepository` protocols avoid broad interfaces. |
| Dependency Inversion | `VehicleService` uses the repository protocol; `Vehicle` uses the engine abstraction. |

The `tests/` directory verifies constructors, inheritance, validation, lifecycle,
polymorphism, persistence, equality, and error handling automatically.
