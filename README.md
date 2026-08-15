# Vehicle OOP and SOLID example

This small Python project is a study example, not a claim that every real vehicle
system should use the same model. Run it with:

For a concept-by-concept explanation with examples, read
[`LEARNING_GUIDE.md`](LEARNING_GUIDE.md) alongside the source code.

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

## OOP and class features

- `Vehicle` is an abstract base class; `Car`, `Motorcycle`, and `Aircraft`
  demonstrate inheritance and method overriding.
- Calling `move()` through `Vehicle` references demonstrates runtime polymorphism.
- Validated properties and `_state` encapsulate mutable state.
- A vehicle *has an* `Engine`: composition is preferred over engine inheritance.
- `__init__`, `super()`, keyword-only/default arguments, `from_string()` as an
  alternative class constructor, `staticmethod`, class attributes, and instance
  attributes demonstrate construction and class mechanics.
- `__str__`, `__repr__`, `__eq__`, and `__hash__` demonstrate Python's data model.
- `ServiceRecord` shows an immutable data/value class, `VehicleState` an enum,
  and custom exceptions domain-specific error handling.

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

`test_vehicle.py` exercises validation, lifecycle, alternate construction,
polymorphism, persistence, equality, and errors.
