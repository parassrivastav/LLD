import unittest

from vehicle_system import (
    Car,
    ElectricMotor,
    InMemoryVehicleRepository,
    VehicleError,
    VehicleService,
)


class RepositoryTests(unittest.TestCase):
    def test_save_find_and_reject_duplicate(self) -> None:
        repository = InMemoryVehicleRepository()
        service = VehicleService(repository)
        car = Car("KA01AB1234", "Tata", "Nexon", ElectricMotor())

        service.register(car)

        self.assertIs(repository.get("ka01ab1234"), car)
        self.assertEqual(len(repository), 1)
        with self.assertRaises(VehicleError):
            service.register(car)


if __name__ == "__main__":
    unittest.main()
