# from flext-plugin/examples/README.md:422
from __future__ import annotations


def cleanup(self) -> p.Result[bool]:
    """Cleanup with error handling."""
    try:
        if hasattr(self, "_connection") and self._connection:
            self._connection.close()

        if hasattr(self, "_temp_files"):
            for file_path in self._temp_files:
                os.unlink(file_path)

        return r[bool].ok(True)
    except Exception as e:
        return r[bool].fail(f"Cleanup failed: {e}")
