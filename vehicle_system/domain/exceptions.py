"""Vehicle-specific errors."""


class VehicleError(Exception):  # Custom exception — reports vehicle errors.
    """Base exception for vehicle domain errors."""


class InvalidVehicleError(VehicleError, ValueError):  # Multiple inheritance.
    """Raised when vehicle data violates a domain rule."""
