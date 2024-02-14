from typing import List, Optional

from tarraz.colors import DMC_COLORS
from tarraz.models import Color
from tarraz.providers import ColorProvider


class DMCProvider(ColorProvider):
    def __init__(
        self,
        data_path: Optional[str] = None,
        colors: Optional[List["Color"]] = None,
    ) -> None:
        if not data_path and not colors:
            colors = Color.create(DMC_COLORS)

        super().__init__(data_path=data_path, colors=colors)
