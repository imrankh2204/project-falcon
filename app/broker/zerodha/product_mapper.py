"""
Maps Falcon product types to Kite product types.
"""

from __future__ import annotations

from app.live.product_type import ProductType


class ProductMapper:
    """
    Translate Falcon product types into Kite values.
    """

    _MAP: dict[ProductType, str] = {
        ProductType.MIS: "MIS",
        ProductType.NRML: "NRML",
        ProductType.CNC: "CNC",
    }

    @classmethod
    def to_kite(
        cls,
        product_type: ProductType,
    ) -> str:
        """
        Convert Falcon product type into Kite product type.
        """

        if not isinstance(
            product_type,
            ProductType,
        ):
            raise TypeError(
                "product_type must be a ProductType."
            )

        return cls._MAP[product_type]