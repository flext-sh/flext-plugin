# from flext-plugin/docs/standards/python-module-organization.md:274
# Singer ETL plugin types (Meltano integration)
from __future__ import annotations

PluginType.TAP  # Data extraction from sources
PluginType.TARGET  # Data loading to destinations
PluginType.TRANSFORM  # DBT-based transformations

# Architecture plugin types
PluginType.SERVICE  # Microservice components
PluginType.MIDDLEWARE  # Request/response processing
PluginType.EXTENSION  # Platform extensions

# Integration plugin types
PluginType.API  # REST/GraphQL endpoints
PluginType.DATABASE  # Database connectivity
PluginType.AUTHENTICATION  # Auth providers and strategies

# Utility plugin types
PluginType.UTILITY  # General-purpose utilities
PluginType.TOOL  # Development and REDACTED_LDAP_BIND_PASSWORD tools
PluginType.PROCESSOR  # Data processing components```
______________________________________________________________________

## 📦 **Import Patterns & Best Practices**

### **Recommended Import Styles**

#### **1. Primary Pattern (Recommended for Ecosystem)**

