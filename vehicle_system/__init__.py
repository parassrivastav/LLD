"""Public API for the vehicle system package."""

from vehicle_system.domain.engine import Engine
from vehicle_system.domain.enums import VehicleState
from vehicle_system.domain.exceptions import InvalidVehicleError, VehicleError
from vehicle_system.domain.service_record import ServiceRecord
from vehicle_system.domain.vehicle import Vehicle
from vehicle_system.engines.combustion import CombustionEngine
from vehicle_system.engines.electric import ElectricMotor
from vehicle_system.repositories.memory import InMemoryVehicleRepository
from vehicle_system.services.vehicle_service import VehicleService
from vehicle_system.vehicles.aircraft import Aircraft
from vehicle_system.vehicles.cars.car import Car
from vehicle_system.vehicles.cars.sedans.sedan import Sedan
from vehicle_system.vehicles.cars.sedans.skoda.slavia import SkodaSlavia
from vehicle_system.vehicles.motorcycle import Motorcycle

__all__ = [
    "Aircraft",
    "Car",
    "CombustionEngine",
    "ElectricMotor",
    "Engine",
    "InMemoryVehicleRepository",
    "InvalidVehicleError",
    "Motorcycle",
    "ServiceRecord",
    "Sedan",
    "SkodaSlavia",
    "Vehicle",
    "VehicleError",
    "VehicleService",
    "VehicleState",
]
