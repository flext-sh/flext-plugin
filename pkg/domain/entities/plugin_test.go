package entities

import (
	"testing"
	"time"

	"github.com/flext-sh/flext-plugin/pkg/domain/valueobjects"
	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/require"
)

func TestNewPlugin(t *testing.T) {
	t.Run("valid plugin creation", func(t *testing.T) {
		name, err := valueobjects.NewPluginName("test-plugin")
		require.NoError(t, err)
		
		version, err := valueobjects.NewPluginVersion("1.0.0")
		require.NoError(t, err)
		
		pluginType, err := valueobjects.NewPluginType("extractor")
		require.NoError(t, err)
		
		plugin, err := NewPlugin(name, version, pluginType, "test.main:Plugin", "Test Author", "MIT")
		
		assert.NoError(t, err)
		assert.NotNil(t, plugin)
		assert.Equal(t, "test-plugin", plugin.Name.Value())
		assert.Equal(t, "1.0.0", plugin.Version.Value())
		assert.Equal(t, valueobjects.PluginTypeExtractor, plugin.PluginType)
		assert.Equal(t, "test.main:Plugin", plugin.EntryPoint)
		assert.Equal(t, "Test Author", plugin.Author)
		assert.Equal(t, "MIT", plugin.License)
		assert.Equal(t, valueobjects.PluginLifecycleUnregistered, plugin.Lifecycle)
		assert.Equal(t, valueobjects.PluginStatusUnknown, plugin.Status)
		assert.True(t, plugin.IsEnabled)
		assert.False(t, plugin.SupportsHotReload)
		assert.False(t, plugin.PluginID.IsZero())
	})
	
	t.Run("empty name should fail", func(t *testing.T) {
		name, _ := valueobjects.NewPluginName("test-plugin")
		version, _ := valueobjects.NewPluginVersion("1.0.0")
		pluginType, _ := valueobjects.NewPluginType("extractor")
		
		// Test with empty entry point
		plugin, err := NewPlugin(name, version, pluginType, "", "Test Author", "MIT")
		
		assert.Error(t, err)
		assert.Nil(t, plugin)
		assert.Contains(t, err.Error(), "entry point cannot be empty")
	})
}

func TestPlugin_Lifecycle(t *testing.T) {
	// Create a test plugin
	name, _ := valueobjects.NewPluginName("test-plugin")
	version, _ := valueobjects.NewPluginVersion("1.0.0")
	pluginType, _ := valueobjects.NewPluginType("extractor")
	plugin, _ := NewPlugin(name, version, pluginType, "test.main:Plugin", "Test Author", "MIT")
	
	t.Run("register plugin", func(t *testing.T) {
		err := plugin.Register()
		assert.NoError(t, err)
		assert.Equal(t, valueobjects.PluginLifecycleRegistered, plugin.Lifecycle)
	})
	
	t.Run("load plugin", func(t *testing.T) {
		err := plugin.Load()
		assert.NoError(t, err)
		assert.Equal(t, valueobjects.PluginLifecycleLoaded, plugin.Lifecycle)
		assert.NotNil(t, plugin.LoadedAt)
	})
	
	t.Run("initialize plugin", func(t *testing.T) {
		err := plugin.Initialize()
		assert.NoError(t, err)
		assert.Equal(t, valueobjects.PluginLifecycleInitialized, plugin.Lifecycle)
		assert.Equal(t, valueobjects.PluginStatusHealthy, plugin.Status)
	})
	
	t.Run("activate plugin", func(t *testing.T) {
		err := plugin.Activate()
		assert.NoError(t, err)
		assert.Equal(t, valueobjects.PluginLifecycleActive, plugin.Lifecycle)
		assert.True(t, plugin.IsEnabled)
	})
	
	t.Run("suspend plugin", func(t *testing.T) {
		err := plugin.Suspend()
		assert.NoError(t, err)
		assert.Equal(t, valueobjects.PluginLifecycleSuspended, plugin.Lifecycle)
		assert.False(t, plugin.IsEnabled)
	})
	
	t.Run("reactivate plugin", func(t *testing.T) {
		err := plugin.Activate()
		assert.NoError(t, err)
		assert.Equal(t, valueobjects.PluginLifecycleActive, plugin.Lifecycle)
		assert.True(t, plugin.IsEnabled)
	})
	
	t.Run("unload plugin", func(t *testing.T) {
		err := plugin.Unload()
		assert.NoError(t, err)
		assert.Equal(t, valueobjects.PluginLifecycleUnloaded, plugin.Lifecycle)
		assert.Nil(t, plugin.LoadedAt)
	})
}

func TestPlugin_CapabilityManagement(t *testing.T) {
	// Create a test plugin
	name, _ := valueobjects.NewPluginName("test-plugin")
	version, _ := valueobjects.NewPluginVersion("1.0.0")
	pluginType, _ := valueobjects.NewPluginType("extractor")
	plugin, _ := NewPlugin(name, version, pluginType, "test.main:Plugin", "Test Author", "MIT")
	
	t.Run("add capability", func(t *testing.T) {
		capability := valueobjects.CapabilityDataExtraction
		err := plugin.AddCapability(capability)
		assert.NoError(t, err)
		assert.True(t, plugin.HasCapability(capability))
		assert.Len(t, plugin.Capabilities, 1)
	})
	
	t.Run("add duplicate capability should fail", func(t *testing.T) {
		capability := valueobjects.CapabilityDataExtraction
		err := plugin.AddCapability(capability)
		assert.Error(t, err)
		assert.Contains(t, err.Error(), "already exists")
		assert.Len(t, plugin.Capabilities, 1) // Should still be 1
	})
	
	t.Run("add second capability", func(t *testing.T) {
		capability := valueobjects.CapabilitySchemaInference
		err := plugin.AddCapability(capability)
		assert.NoError(t, err)
		assert.True(t, plugin.HasCapability(capability))
		assert.Len(t, plugin.Capabilities, 2)
	})
	
	t.Run("remove capability", func(t *testing.T) {
		capability := valueobjects.CapabilityDataExtraction
		err := plugin.RemoveCapability(capability)
		assert.NoError(t, err)
		assert.False(t, plugin.HasCapability(capability))
		assert.Len(t, plugin.Capabilities, 1)
	})
	
	t.Run("remove non-existent capability should fail", func(t *testing.T) {
		capability := valueobjects.CapabilityDataExtraction // Already removed
		err := plugin.RemoveCapability(capability)
		assert.Error(t, err)
		assert.Contains(t, err.Error(), "not found")
	})
}

func TestPlugin_ConfigurationManagement(t *testing.T) {
	// Create a test plugin
	name, _ := valueobjects.NewPluginName("test-plugin")
	version, _ := valueobjects.NewPluginVersion("1.0.0")
	pluginType, _ := valueobjects.NewPluginType("extractor")
	plugin, _ := NewPlugin(name, version, pluginType, "test.main:Plugin", "Test Author", "MIT")
	
	t.Run("set configuration", func(t *testing.T) {
		config := map[string]interface{}{
			"host": "localhost",
			"port": 5432,
			"enabled": true,
		}
		
		err := plugin.SetConfiguration(config)
		assert.NoError(t, err)
		
		retrievedConfig := plugin.GetConfiguration()
		assert.Equal(t, config, retrievedConfig)
	})
	
	t.Run("set configuration value", func(t *testing.T) {
		err := plugin.SetConfigurationValue("timeout", 30)
		assert.NoError(t, err)
		
		value, exists := plugin.GetConfigurationValue("timeout")
		assert.True(t, exists)
		assert.Equal(t, 30, value)
	})
	
	t.Run("get non-existent configuration value", func(t *testing.T) {
		value, exists := plugin.GetConfigurationValue("non-existent")
		assert.False(t, exists)
		assert.Nil(t, value)
	})
}

func TestPlugin_ExecutionTracking(t *testing.T) {
	t.Run("record successful execution", func(t *testing.T) {
		// Create a fresh test plugin for each test
		name, _ := valueobjects.NewPluginName("test-plugin-exec1")
		version, _ := valueobjects.NewPluginVersion("1.0.0")
		pluginType, _ := valueobjects.NewPluginType("extractor")
		plugin, _ := NewPlugin(name, version, pluginType, "test.main:Plugin", "Test Author", "MIT")
		
		initialTotal := plugin.TotalExecutions
		initialSuccessful := plugin.SuccessfulExecutions
		
		plugin.RecordExecution(true, 1000) // 1 second
		
		assert.Equal(t, initialTotal+1, plugin.TotalExecutions)
		assert.Equal(t, initialSuccessful+1, plugin.SuccessfulExecutions)
		assert.Equal(t, float64(1000), plugin.AverageExecutionMs)
		assert.NotNil(t, plugin.LastUsedAt)
	})
	
	t.Run("record failed execution", func(t *testing.T) {
		// Create a fresh test plugin for each test
		name, _ := valueobjects.NewPluginName("test-plugin-exec2")
		version, _ := valueobjects.NewPluginVersion("1.0.0")
		pluginType, _ := valueobjects.NewPluginType("extractor")
		plugin, _ := NewPlugin(name, version, pluginType, "test.main:Plugin", "Test Author", "MIT")
		
		// Record one successful execution first
		plugin.RecordExecution(true, 1000) // 1 second
		
		initialTotal := plugin.TotalExecutions
		initialFailed := plugin.FailedExecutions
		
		plugin.RecordExecution(false, 500) // 0.5 seconds
		
		assert.Equal(t, initialTotal+1, plugin.TotalExecutions)
		assert.Equal(t, initialFailed+1, plugin.FailedExecutions)
		
		// Average should be (1000 + 500) / 2 = 750
		assert.Equal(t, float64(750), plugin.AverageExecutionMs)
	})
	
	t.Run("get success rate", func(t *testing.T) {
		// Create a fresh test plugin for each test
		name, _ := valueobjects.NewPluginName("test-plugin-exec3")
		version, _ := valueobjects.NewPluginVersion("1.0.0")
		pluginType, _ := valueobjects.NewPluginType("extractor")
		plugin, _ := NewPlugin(name, version, pluginType, "test.main:Plugin", "Test Author", "MIT")
		
		// Record 1 successful and 1 failed execution
		plugin.RecordExecution(true, 1000)
		plugin.RecordExecution(false, 500)
		
		successRate := plugin.GetSuccessRate()
		assert.Equal(t, float64(50), successRate) // 50%
	})
}

func TestPlugin_HotReload(t *testing.T) {
	// Create a test plugin
	name, _ := valueobjects.NewPluginName("test-plugin")
	version, _ := valueobjects.NewPluginVersion("1.0.0")
	pluginType, _ := valueobjects.NewPluginType("extractor")
	plugin, _ := NewPlugin(name, version, pluginType, "test.main:Plugin", "Test Author", "MIT")
	
	// Add hot reload capability and activate plugin
	plugin.AddCapability(valueobjects.CapabilityHotReload)
	plugin.Register()
	plugin.Load()
	plugin.Initialize()
	plugin.Activate()
	
	t.Run("enable hot reload", func(t *testing.T) {
		err := plugin.EnableHotReload()
		assert.NoError(t, err)
		assert.True(t, plugin.SupportsHotReload)
	})
	
	t.Run("enable hot reload without capability should fail", func(t *testing.T) {
		// Create plugin without hot reload capability
		name2, _ := valueobjects.NewPluginName("test-plugin-2")
		plugin2, _ := NewPlugin(name2, version, pluginType, "test.main:Plugin", "Test Author", "MIT")
		
		err := plugin2.EnableHotReload()
		assert.Error(t, err)
		assert.Contains(t, err.Error(), "does not support hot reload capability")
	})
	
	t.Run("perform hot reload", func(t *testing.T) {
		initialReloadCount := plugin.ReloadCount
		
		err := plugin.PerformHotReload()
		assert.NoError(t, err)
		assert.Equal(t, initialReloadCount+1, plugin.ReloadCount)
		assert.NotNil(t, plugin.LastReloadedAt)
	})
	
	t.Run("perform hot reload on inactive plugin should fail", func(t *testing.T) {
		plugin.Suspend()
		
		err := plugin.PerformHotReload()
		assert.Error(t, err)
		assert.Contains(t, err.Error(), "must be active")
	})
	
	t.Run("disable hot reload", func(t *testing.T) {
		plugin.Activate() // Reactivate for this test
		plugin.DisableHotReload()
		assert.False(t, plugin.SupportsHotReload)
	})
}

func TestPlugin_CanExecute(t *testing.T) {
	// Create a test plugin
	name, _ := valueobjects.NewPluginName("test-plugin")
	version, _ := valueobjects.NewPluginVersion("1.0.0")
	pluginType, _ := valueobjects.NewPluginType("extractor")
	plugin, _ := NewPlugin(name, version, pluginType, "test.main:Plugin", "Test Author", "MIT")
	
	t.Run("unregistered plugin cannot execute", func(t *testing.T) {
		assert.False(t, plugin.CanExecute())
	})
	
	t.Run("registered but not active plugin cannot execute", func(t *testing.T) {
		plugin.Register()
		plugin.Load()
		plugin.Initialize()
		assert.False(t, plugin.CanExecute())
	})
	
	t.Run("active and healthy plugin can execute", func(t *testing.T) {
		plugin.Activate()
		assert.True(t, plugin.CanExecute())
	})
	
	t.Run("disabled plugin cannot execute", func(t *testing.T) {
		plugin.IsEnabled = false
		assert.False(t, plugin.CanExecute())
	})
	
	t.Run("unhealthy plugin cannot execute", func(t *testing.T) {
		plugin.IsEnabled = true
		plugin.Status = valueobjects.PluginStatusUnhealthy
		assert.False(t, plugin.CanExecute())
	})
	
	t.Run("degraded plugin can execute", func(t *testing.T) {
		plugin.Status = valueobjects.PluginStatusDegraded
		assert.True(t, plugin.CanExecute())
	})
}

func TestPlugin_ResourceLimits(t *testing.T) {
	// Create a test plugin
	name, _ := valueobjects.NewPluginName("test-plugin")
	version, _ := valueobjects.NewPluginVersion("1.0.0")
	pluginType, _ := valueobjects.NewPluginType("extractor")
	plugin, _ := NewPlugin(name, version, pluginType, "test.main:Plugin", "Test Author", "MIT")
	
	t.Run("set valid resource limits", func(t *testing.T) {
		err := plugin.SetResourceLimits(256, 512, 2, 1000)
		assert.NoError(t, err)
		assert.Equal(t, 256, plugin.MinMemoryMB)
		assert.NotNil(t, plugin.MaxMemoryMB)
		assert.Equal(t, 512, *plugin.MaxMemoryMB)
		assert.Equal(t, 2, plugin.CPUCores)
		assert.Equal(t, 1000, plugin.DiskSpaceMB)
	})
	
	t.Run("set invalid resource limits should fail", func(t *testing.T) {
		// Min memory <= 0
		err := plugin.SetResourceLimits(0, 512, 2, 1000)
		assert.Error(t, err)
		assert.Contains(t, err.Error(), "minimum memory must be positive")
		
		// Max memory < min memory
		err = plugin.SetResourceLimits(256, 128, 2, 1000)
		assert.Error(t, err)
		assert.Contains(t, err.Error(), "maximum memory must be greater than minimum memory")
		
		// CPU cores <= 0
		err = plugin.SetResourceLimits(256, 512, 0, 1000)
		assert.Error(t, err)
		assert.Contains(t, err.Error(), "CPU cores must be positive")
		
		// Disk space <= 0
		err = plugin.SetResourceLimits(256, 512, 2, 0)
		assert.Error(t, err)
		assert.Contains(t, err.Error(), "disk space must be positive")
	})
}

func TestPlugin_DependencyManagement(t *testing.T) {
	// Create a test plugin
	name, _ := valueobjects.NewPluginName("test-plugin")
	version, _ := valueobjects.NewPluginVersion("1.0.0")
	pluginType, _ := valueobjects.NewPluginType("extractor")
	plugin, _ := NewPlugin(name, version, pluginType, "test.main:Plugin", "Test Author", "MIT")
	
	t.Run("add dependency", func(t *testing.T) {
		err := plugin.AddDependency("requests>=2.25.0")
		assert.NoError(t, err)
		assert.True(t, plugin.HasDependency("requests>=2.25.0"))
		assert.Len(t, plugin.Dependencies, 1)
	})
	
	t.Run("add duplicate dependency should fail", func(t *testing.T) {
		err := plugin.AddDependency("requests>=2.25.0")
		assert.Error(t, err)
		assert.Contains(t, err.Error(), "already exists")
		assert.Len(t, plugin.Dependencies, 1) // Should still be 1
	})
	
	t.Run("add second dependency", func(t *testing.T) {
		err := plugin.AddDependency("pandas>=1.0.0")
		assert.NoError(t, err)
		assert.True(t, plugin.HasDependency("pandas>=1.0.0"))
		assert.Len(t, plugin.Dependencies, 2)
	})
	
	t.Run("remove dependency", func(t *testing.T) {
		err := plugin.RemoveDependency("requests>=2.25.0")
		assert.NoError(t, err)
		assert.False(t, plugin.HasDependency("requests>=2.25.0"))
		assert.Len(t, plugin.Dependencies, 1)
	})
	
	t.Run("remove non-existent dependency should fail", func(t *testing.T) {
		err := plugin.RemoveDependency("requests>=2.25.0") // Already removed
		assert.Error(t, err)
		assert.Contains(t, err.Error(), "not found")
	})
}

func TestPlugin_HealthStatus(t *testing.T) {
	// Create a test plugin
	name, _ := valueobjects.NewPluginName("test-plugin")
	version, _ := valueobjects.NewPluginVersion("1.0.0")
	pluginType, _ := valueobjects.NewPluginType("extractor")
	plugin, _ := NewPlugin(name, version, pluginType, "test.main:Plugin", "Test Author", "MIT")
	
	t.Run("update health status", func(t *testing.T) {
		initialStatus := plugin.Status
		
		plugin.UpdateHealthStatus(valueobjects.PluginStatusHealthy)
		
		assert.Equal(t, valueobjects.PluginStatusHealthy, plugin.Status)
		assert.NotEqual(t, initialStatus, plugin.Status)
		assert.NotNil(t, plugin.LastHealthCheck)
	})
	
	t.Run("update to same status", func(t *testing.T) {
		oldLastHealthCheck := plugin.LastHealthCheck
		time.Sleep(1 * time.Millisecond) // Ensure time difference
		
		plugin.UpdateHealthStatus(valueobjects.PluginStatusHealthy)
		
		// Should not update LastHealthCheck when status is the same
		assert.Equal(t, oldLastHealthCheck, plugin.LastHealthCheck)
	})
}

func TestPlugin_ErrorHandling(t *testing.T) {
	// Create a test plugin
	name, _ := valueobjects.NewPluginName("test-plugin")
	version, _ := valueobjects.NewPluginVersion("1.0.0")
	pluginType, _ := valueobjects.NewPluginType("extractor")
	plugin, _ := NewPlugin(name, version, pluginType, "test.main:Plugin", "Test Author", "MIT")
	
	t.Run("mark plugin error", func(t *testing.T) {
		plugin.Register()
		plugin.Load()
		plugin.Initialize()
		plugin.Activate()
		
		err := plugin.MarkError("Test error message")
		assert.NoError(t, err)
		assert.Equal(t, valueobjects.PluginLifecycleError, plugin.Lifecycle)
		assert.Equal(t, valueobjects.PluginStatusUnhealthy, plugin.Status)
	})
}