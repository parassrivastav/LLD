import unittest

from vehicle import (
    Car,
    ElectricMotor,
    InMemoryVehicleRepository,
    InvalidVehicleError,
    Motorcycle,
    VehicleError,
    VehicleService,
)


class VehicleTests(unittest.TestCase):
    def setUp(self) -> None:
        self.car = Car("ka01ab1234", "Tata", "Nexon", ElectricMotor())

    def test_constructor_and_encapsulated_properties(self) -> None:
        self.assertEqual(self.car.registration, "KA01AB1234")
        self.assertEqual(self.car.state.value, "parked")
        with self.assertRaises(InvalidVehicleError):
            self.car.odometer_km = -1

    def test_alternative_constructor(self) -> None:
        car = Car.from_string("DL01AA0001, Mahindra, Thar, 2020", ElectricMotor())
        self.assertEqual((car.brand, car.year), ("Mahindra", 2020))

    def test_lifecycle_and_odometer(self) -> None:
        with self.assertRaises(VehicleError):
            self.car.drive(10)
        self.car.start()
        self.car.drive(12.5)
        self.assertEqual(self.car.odometer_km, 12.5)
        self.car.stop()

    def test_polymorphism(self) -> None:
        bike = Motorcycle("KA02AB1234", "Honda", "CB", ElectricMotor())
        report = VehicleService(InMemoryVehicleRepository()).movement_report(
            [self.car, bike]
        )
        self.assertIn("4 wheels", report[0])
        self.assertIn("2 wheels", report[1])

    def test_repository_and_duplicate_rule(self) -> None:
        repository = InMemoryVehicleRepository()
        service = VehicleService(repository)
        service.register(self.car)
        self.assertIs(repository.get("ka01ab1234"), self.car)
        with self.assertRaises(VehicleError):
            service.register(self.car)

    def test_equality_and_hash_use_registration(self) -> None:
        duplicate = Car("KA01AB1234", "Other", "Car", ElectricMotor())
        self.assertEqual(self.car, duplicate)
        self.assertEqual(len({self.car, duplicate}), 1)


if __name__ == "__main__":
    unittest.main()
