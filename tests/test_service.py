import unittest

from vehicle_system import (
    Car,
    ElectricMotor,
    InMemoryVehicleRepository,
    Motorcycle,
    VehicleService,
)


class VehicleServiceTests(unittest.TestCase):
    def test_polymorphic_movement_report(self) -> None:
        car = Car("KA01AB1234", "Tata", "Nexon", ElectricMotor())
        bike = Motorcycle("KA02AB1234", "Honda", "CB", ElectricMotor())
        service = VehicleService(InMemoryVehicleRepository())

        report = service.movement_report([car, bike])

        self.assertIn("4 wheels", report[0])
        self.assertIn("2 wheels", report[1])


if __name__ == "__main__":
    unittest.main()
