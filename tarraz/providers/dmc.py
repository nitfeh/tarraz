from typing import Optional, List, TYPE_CHECKING

from .provider import ColorProvider

if TYPE_CHECKING:
    from tarraz.models import Color


class DMCProvider(ColorProvider):
    def __init__(
        self,
        data_path: Optional[str] = None,
        colors: Optional[List["Color"]] = None,
    ) -> None:
        if not data_path and not colors:
            data_path = "tarraz/assets/dmc.json"

        super().__init__(data_path=data_path, colors=colors)
