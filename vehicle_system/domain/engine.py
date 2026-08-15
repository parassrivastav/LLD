"""Engine abstraction used by vehicles."""

from abc import ABC, abstractmethod


class Engine(ABC):  # ABC — blueprint that cannot be used directly.
    """Contract implemented by every engine type."""

    @property  # Property — accessed as engine.energy_source.
    @abstractmethod
    def energy_source(self) -> str:
        """Return the source used to power this engine."""

    @abstractmethod  # Every engine must provide its own start behavior.
    def start(self) -> str:
        """Start the engine."""

    @abstractmethod
    def stop(self) -> str:
        """Stop the engine."""
