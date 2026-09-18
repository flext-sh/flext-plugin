# from flext-plugin_docs/security/sonarqube-triage.md:250
       56              "subprocess",
       57              "os.system",
       58          ]
       59          Discovery: ClassVar[type[FlextPluginDiscovery]]
>>>    60          Platform: ClassVar[type[FlextPluginPlatform]]
       61
       62          @classmethod
       63          def discover_plugins(
       64              cls, directory: Path | str
