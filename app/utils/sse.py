
import json
from typing import Any


def format_sse(
    event: str,
    data: Any,
) -> str:
    payload = json.dumps(
        data,
        ensure_ascii=False,
        default=str,
    )

    return (
        f"event: {event}\n"
        f"data: {payload}\n\n"
    )
