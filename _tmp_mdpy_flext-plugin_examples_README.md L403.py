# from flext-plugin/examples/README.md:403
from __future__ import annotations

try:
    result = operation()
    if result.success:
        return result.value
    else:
        logger.error(f"Operation failed: {result.error}")
        return None
except Exception as e:
    logger.error(f"Unexpected error: {e}")
    return r[bool].fail(f"Unexpected error: {e}")
