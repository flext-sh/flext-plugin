# from flext-plugin/docs/security/sonarqube-triage.md:170
       39          """Discover Python plugins recursively in a directory."""
       40          discovered: MutableSequence[TDiscovery] = []
       41          try:
       42              items = tuple(path.iterdir())
>>>    43          except (OSError, PermissionError):
       44              logger.exception("Failed to discover directory %s", path)
       45              return discovered
       46          for item in items:
       47              if (
