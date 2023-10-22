from typing import Annotated

from pydantic import UrlConstraints
from pydantic_core import Url


SQLiteDsn = Annotated[
    Url,
    UrlConstraints(
        allowed_schemes=["sqlite+aiosqlite", "sqlite"],
    ),
]
