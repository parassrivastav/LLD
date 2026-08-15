# Vehicle project: beginner's walkthrough

Read this file beside the `vehicle_system/` package. Classes are grouped into
folders by responsibility because OOP is about objects collaborating, not putting
everything inside one enormous class.

## 1. Class and object

A **class** is a blueprint. An **object** is one instance created from it.

```python
car = Car("KA01AB1234", "Tata", "Nexon", ElectricMotor())
```

- `Car` is the class.
- `car` is an object of that class.
- Calling `Car(...)` creates the object and invokes its `__init__` method.
- `isinstance(car, Car)` and `isinstance(car, Vehicle)` are both `True` because
  `Car` inherits from `Vehicle`.

## 2. Constructor and `self`

`__init__` initializes a newly created object:

```python
def __init__(self, registration: str, brand: str, model: str, engine: Engine):
    self.brand = brand
```

`self` means "this particular object." Therefore, `self.brand` belongs to the
object, while the parameter `brand` is only a temporary local name. Python passes
`self` automatically when we call an instance method.

The `Car` constructor uses:

```python
super().__init__(*args, **kwargs)
```

`super()` accesses the parent (`Vehicle`) implementation. This prevents `Car` from
duplicating all common initialization. `*args` forwards positional arguments and
`**kwargs` forwards keyword arguments.

Python does not overload constructors by defining several `__init__` methods.
Instead, it uses defaults, keyword arguments, and named alternative constructors:

```python
car = Car.from_string("KA01AB1234, Tata, Nexon, 2024", ElectricMotor())
```

## 3. Instance and class attributes

`self.brand`, `self.model`, and `self.year` are **instance attributes**. Each
vehicle object can have different values.

`Car.wheels` is a **class attribute**. It describes the class and is shared unless
an individual object overrides it. `ClassVar[int]` tells readers and type checkers
that the value belongs to the class.

## 4. Instance, class, and static methods

```python
car.start()                         # instance method: receives self
Car.from_string(data, engine)       # class method: receives cls
Vehicle.is_vintage(1990)            # static method: receives neither
```

- An **instance method** reads or changes one object.
- A **class method** works with the class and is useful as a named constructor.
- A **static method** is a related utility that needs no object/class state.

## 5. Encapsulation and properties

Encapsulation keeps an object's data and rules together. `_registration` begins
with `_` to say "internal implementation detail." Python trusts programmers rather
than making it absolutely private.

The public `registration` property controls access:

```python
@property
def registration(self) -> str:
    return self._registration

@registration.setter
def registration(self, value: str) -> None:
    # clean and validate before saving
```

Callers can still use natural attribute syntax:

```python
car.registration = "ka01ab1234"
print(car.registration)             # KA01AB1234
```

but invalid values cannot bypass the setter's rules.

## 6. Abstraction

`ABC` means **abstract base class**. It defines what related objects must be able
to do without dictating every implementation detail.

`Vehicle.move()` is marked `@abstractmethod`, so this fails:

```python
Vehicle(...)  # TypeError: abstract class cannot be instantiated
```

Concrete subclasses must implement `move()`. Similarly, every concrete `Engine`
must provide `start()`, `stop()`, and `energy_source`.

## 7. Inheritance and method overriding

```text
Vehicle
├── Car
├── Motorcycle
└── Aircraft
```

The child classes inherit common behavior such as `start`, `stop`, and `drive`.
Each child **overrides** `move()` with behavior appropriate to that vehicle.

Inheritance describes an **is-a** relationship: a `Car` is a `Vehicle`.

## 8. Polymorphism

Polymorphism means using the same operation with different object types:

```python
for vehicle in [car, motorcycle, aircraft]:
    print(vehicle.move())
```

Python selects the correct overridden `move()` at runtime. The loop does not need
`if type == Car` conditions, so adding another vehicle type does not change it.

## 9. Composition

A vehicle receives an engine object in its constructor:

```python
electric_car = Car(..., engine=ElectricMotor())
petrol_car = Car(..., engine=CombustionEngine("petrol"))
```

This is composition: a vehicle **has an** engine. The engine can be replaced
without creating combinations such as `ElectricCar`, `PetrolCar`,
`ElectricMotorcycle`, and `PetrolMotorcycle`.

Use inheritance for **is-a** relationships and composition for **has-a**
relationships.

## 10. Enum and state

`VehicleState` is an `Enum`, a fixed collection of named values. It prevents
inconsistent strings such as `"running"`, `"Running"`, and `"started"` from
representing the same state.

The lifecycle rules use that state:

```text
PARKED --start()--> RUNNING --stop()--> PARKED
```

Calling `drive()` while parked raises a domain error.

## 11. Exceptions

`VehicleError` is the project's general domain exception.
`InvalidVehicleError` is more specific and inherits from both `VehicleError` and
`ValueError`.

```python
try:
    car.drive(-10)
except InvalidVehicleError as error:
    print(error)
```

Raising an exception immediately stops an invalid operation. Catch it only where
the program can handle or report it meaningfully.

## 12. Protocol (interface)

A `Protocol` describes the methods an object must provide. It is Python's flexible
version of an interface:

```python
class VehicleRepository(Protocol):
    def save(self, vehicle: Vehicle) -> None: ...
```

`VehicleService` depends on this contract, not specifically on
`InMemoryVehicleRepository`. A database repository could replace it later without
changing the service. The `...` is an intentional empty placeholder.

## 13. Dataclass and immutability

`@dataclass` generates routine methods such as `__init__`, `__repr__`, and
`__eq__`. It is useful for classes whose main purpose is holding data.

`ServiceRecord` uses `frozen=True`, so it cannot be modified after construction.
That makes it an immutable value object.

## 14. Special (dunder) methods

Methods surrounded by double underscores connect a class to Python syntax:

| Method | Used by | Purpose here |
|---|---|---|
| `__init__` | `Car(...)` | Initialize an object |
| `__str__` | `str(car)`, `print(car)` | Friendly display |
| `__repr__` | `repr(car)` | Developer/debug display |
| `__eq__` | `car1 == car2` | Compare registrations |
| `__hash__` | `{car}`, dictionary keys | Hash by registration |
| `__len__` | `len(repository)` | Count saved vehicles |
| `__iter__` | `for vehicle in repository` | Iterate saved vehicles |

Equal objects must have equal hashes. That is why `__eq__` and `__hash__` both use
the registration number.

## 15. SOLID principles in this project

### S — Single Responsibility Principle

A class should have one reason to change.

- `Vehicle` handles vehicle state and movement rules.
- `InMemoryVehicleRepository` handles storage.
- `VehicleService` handles application use cases.
- `ServiceRecord` holds service data.

If storage changes to PostgreSQL, vehicle movement code should not change.

### O — Open/Closed Principle

Code should be open for extension but closed for unnecessary modification. A new
`HydrogenEngine(Engine)` or `Truck(Vehicle)` can be added without editing
`VehicleService`.

### L — Liskov Substitution Principle

A child object should work anywhere its parent is expected. `movement_report()`
accepts any `Vehicle`; `Car`, `Motorcycle`, and `Aircraft` all fulfill the `move()`
contract without surprising the caller.

### I — Interface Segregation Principle

Clients should not depend on methods they do not use. `Flyable` is deliberately
small, so a `Car` is not forced to implement a meaningless `fly()` method.
`VehicleRepository` contains only persistence operations required by its client.

### D — Dependency Inversion Principle

High-level logic should depend on abstractions. `VehicleService` accepts the
`VehicleRepository` protocol rather than constructing a particular database.
`Vehicle` similarly accepts the `Engine` abstraction. These dependencies are
injected through constructors, which also makes testing easy.

## 16. Run and experiment

```bash
python3 main.py
python3 -m unittest discover -s tests -v
```

Good exercises:

1. Add `Truck(Vehicle)` with six wheels and its own `move()` implementation.
2. Add `HydrogenEngine(Engine)` without editing `Vehicle`.
3. Write a test that rejects an empty registration.
4. Implement a file-based repository matching `VehicleRepository`.
5. Add a rule preventing `start()` when an engine has no energy.

## 17. Multi-level inheritance: Skoda Slavia

The concrete production-style example uses this chain:

```text
Vehicle -> Car -> Sedan -> SkodaSlavia
```

Constructing `SkodaSlavia` calls `Sedan.__init__`, then `Car.__init__`, and finally
`Vehicle.__init__` through `super()`. Each class initializes only the data it owns.
The Slavia inherits `start()`, `stop()`, and `drive()` while overriding `move()`.
