# from flext-plugin/docs/security/sonarqube-triage.md:40
       55      postgres_plugin = FlextPluginModels.Plugin.Entity(
       56          name="docker-postgres-connector",
       57          plugin_version="1.0.0",
       58          description="PostgreSQL database connector for Docker environment",
>>>    59          author="FLEXT Team",
       60          plugin_type=FlextPluginConstants.Plugin.Type.DATABASE.value,
       61          is_enabled=True,
       62          metadata={"dependencies": ["psycopg2-binary"]},
       63      )
