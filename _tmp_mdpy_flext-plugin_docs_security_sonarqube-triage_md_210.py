# from flext-plugin_docs/security/sonarqube-triage.md:210
      275              super().__init__()
      276              if container is not None:
      277                  self._container = container
      278              self._plugins = dict[str, FlextPluginPlatform.Plugin]()
>>>   279              self._executions = dict[str, FlextPluginPlatform.PluginExecution]()
      280              self._registry = FlextPluginPlatform.PluginRegistry.create()
      281              self._discovery = None
      282              self._loader = None
      283              self._executor = None
