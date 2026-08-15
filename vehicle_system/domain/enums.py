"""Fixed values used by the domain."""

from enum import Enum


class VehicleState(Enum):  # Enum — limits state to these fixed values.
    PARKED = "parked"
    RUNNING = "running"
