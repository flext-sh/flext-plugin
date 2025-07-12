# Logging Migration Report for flext-plugin

## Summary

Total files with logging imports: 14

## Files to Migrate

- `src/flx_plugin/core/discovery.py:11` - `import logging`
- `src/flx_plugin/core/loader.py:9` - `import logging`
- `src/flx_plugin/core/manager.py:10` - `import logging`
- `src/flx_plugin/hot_reload/reloader.py:9` - `import logging`
- `src/flx_plugin/hot_reload/rollback.py:8` - `import logging`
- `src/flx_plugin/hot_reload/state_manager.py:9` - `import logging`
- `src/flx_plugin/hot_reload/watcher.py:11` - `import logging`
- `src/flext_plugin/core/discovery.py:11` - `import logging`
- `src/flext_plugin/core/loader.py:9` - `import logging`
- `src/flext_plugin/core/manager.py:10` - `import logging`
- `src/flext_plugin/hot_reload/reloader.py:9` - `import logging`
- `src/flext_plugin/hot_reload/rollback.py:8` - `import logging`
- `src/flext_plugin/hot_reload/state_manager.py:9` - `import logging`
- `src/flext_plugin/hot_reload/watcher.py:11` - `import logging`

## Migration Steps

1. Replace logging imports:

   ```python
   # Old
   import logging
   logger = logging.getLogger(__name__)

   # New
   from flext_observability.logging import get_logger
   logger = get_logger(__name__)
   ```

2. Add setup_logging to your main entry point:

   ```python
   from flext_observability import setup_logging

   setup_logging(
       service_name="flext-plugin",
       log_level="INFO",
       json_logs=True
   )
   ```

3. Update logging calls to use structured format:

   ```python
   # Old
   logger.info("Processing %s items", count)

   # New
   logger.info("Processing items", count=count)
   ```

See `examples/logging_migration.py` for a complete example.
