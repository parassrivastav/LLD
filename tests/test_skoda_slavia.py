import unittest

from vehicle_system import (
    Car,
    ElectricMotor,
    InvalidVehicleError,
    Sedan,
    SkodaSlavia,
    Vehicle,
)


class SkodaSlaviaTests(unittest.TestCase):
    def test_complete_inheritance_chain(self) -> None:
        slavia = SkodaSlavia("MH01SL2026")

        self.assertIsInstance(slavia, SkodaSlavia)
        self.assertIsInstance(slavia, Sedan)
        self.assertIsInstance(slavia, Car)
        self.assertIsInstance(slavia, Vehicle)

    def test_model_defaults_and_inherited_behavior(self) -> None:
        slavia = SkodaSlavia("MH01SL2026")

        self.assertEqual(slavia.display_name, "Skoda Slavia")
        self.assertEqual(slavia.seats, 5)
        self.assertEqual(slavia.boot_capacity_litres, 521)
        self.assertEqual(slavia.engine.energy_source, "petrol")
        self.assertIn("521-litre", slavia.open_boot())

        slavia.start()
        slavia.drive(25)
        self.assertEqual(slavia.odometer_km, 25)

    def test_configuration_and_engine_injection(self) -> None:
        slavia = SkodaSlavia(
            "MH02SL2026",
            ElectricMotor(),
            variant="1.5 TSI Prestige",
            transmission="AUTOMATIC",
            color="Carbon Steel",
        )

        self.assertEqual(slavia.engine.energy_source, "electricity")
        self.assertEqual(slavia.transmission, "automatic")
        self.assertIn("1.5 TSI Prestige", slavia.move())

    def test_rejects_invalid_configuration(self) -> None:
        with self.assertRaises(InvalidVehicleError):
            SkodaSlavia("MH03SL2026", transmission="CVT")


if __name__ == "__main__":
    unittest.main()
