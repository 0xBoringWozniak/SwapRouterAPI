from abc import ABC, abstractmethod


class Connector(ABC):
    """
    Dex connector interface. All connectors must implement this interface.

    Args:
        ABC: abstract base class

    Raises:
        NotImplementedError: if method is not implemented
    """
    @abstractmethod
    def get_amount_out(self, amount_in: float) -> float:
        """
        Get amount out for given amount in in pool.

        Args:
            amount_in (float): amount in of token

        Raises:
            NotImplementedError: if method is not implemented

        Returns:
            float: amount out of token
        """
        raise NotImplementedError
