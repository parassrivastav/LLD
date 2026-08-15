"""Electric motor implementation."""

from vehicle_system.domain.engine import Engine


class ElectricMotor(Engine):  # Extension — added without changing Vehicle.
    @property
    def energy_source(self) -> str:
        return "electricity"

    def start(self) -> str:
        return "Electric motor ready"

    def stop(self) -> str:
        return "Electric motor switched off"
