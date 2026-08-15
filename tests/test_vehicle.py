import unittest

from vehicle_system import Car, ElectricMotor, InvalidVehicleError, VehicleError


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

    def test_equality_and_hash_use_registration(self) -> None:
        duplicate = Car("KA01AB1234", "Other", "Car", ElectricMotor())
        self.assertEqual(self.car, duplicate)
        self.assertEqual(len({self.car, duplicate}), 1)


if __name__ == "__main__":
    unittest.main()
