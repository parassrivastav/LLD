"""Composition root: creates dependencies and runs the demonstration."""

from vehicle_system import (
    Aircraft,
    Car,
    CombustionEngine,
    ElectricMotor,
    InMemoryVehicleRepository,
    Motorcycle,
    VehicleService,
)


def main() -> None:
    repository = InMemoryVehicleRepository()  # Create concrete dependency.
    service = VehicleService(repository)  # Inject dependency into service.

    car = Car.from_string("KA01AB1234, Tata, Nexon, 2024", ElectricMotor())
    bike = Motorcycle("KA02XY9876", "Royal Enfield", "Classic", CombustionEngine())
    plane = Aircraft("VT-DEMO", "Cessna", "172", CombustionEngine("aviation fuel"))

    for vehicle in (car, bike, plane):  # Same logic works for every subtype.
        service.register(vehicle)
        print(vehicle)
        print(" ", vehicle.start())
        print(" ", vehicle.move())
        print(" ", vehicle.stop())

    print("Movement report:", service.movement_report(repository))


if __name__ == "__main__":  # Runs only when executing `python3 main.py`.
    main()
