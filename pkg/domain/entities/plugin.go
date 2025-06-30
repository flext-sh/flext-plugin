package entities

import (
	"encoding/json"
	"fmt"
	"time"

	"github.com/flext-sh/flext-plugin/pkg/domain"
	"github.com/flext-sh/flext-plugin/pkg/domain/valueobjects"
)

// Plugin represents a plugin aggregate root in the domain
type Plugin struct {
	domain.PluginAggregateRoot

	// Identity and metadata
	PluginID    domain.PluginID             `json:"plugin_id"`
	Name        valueobjects.PluginName     `json:"name"`
	Version     valueobjects.PluginVersion  `json:"version"`
	Description string                      `json:"description"`
	Author      string                      `json:"author"`
	License     string                      `json:"license"`

	// Plugin classification
	PluginType    valueobjects.PluginType     `json:"plugin_type"`
	Capabilities  []valueobjects.PluginCapability `json:"capabilities"`
	
	// Technical specifications  
	EntryPoint     string   `json:"entry_point"`
	PythonVersion  string   `json:"python_version"`
	Dependencies   []string `json:"dependencies"`
	
	// Configuration
	ConfigurationSchema   map[string]interface{} `json:"configuration_schema"`
	DefaultConfiguration  map[string]interface{} `json:"default_configuration"`
	CurrentConfiguration  map[string]interface{} `json:"current_configuration"`
	
	// Security and permissions
	RequiredPermissions []string `json:"required_permissions"`
	SecurityLevel       string   `json:"security_level"`
	Trusted             bool     `json:"trusted"`
	
	// Resource requirements
	MinMemoryMB  int  `json:"min_memory_mb"`
	MaxMemoryMB  *int `json:"max_memory_mb,omitempty"`
	CPUCores     int  `json:"cpu_cores"`
	DiskSpaceMB  int  `json:"disk_space_mb"`
	
	// State management
	Lifecycle       valueobjects.PluginLifecycle `json:"lifecycle"`
	Status          valueobjects.PluginStatus    `json:"status"`
	IsEnabled       bool                         `json:"is_enabled"`
	LoadedAt        *time.Time                   `json:"loaded_at,omitempty"`
	LastUsedAt      *time.Time                   `json:"last_used_at,omitempty"`
	LastHealthCheck *time.Time                   `json:"last_health_check,omitempty"`
	
	// Hot reload support
	SupportsHotReload  bool      `json:"supports_hot_reload"`
	LastReloadedAt     *time.Time `json:"last_reloaded_at,omitempty"`
	ReloadCount        int       `json:"reload_count"`
	
	// Execution tracking
	TotalExecutions    int64     `json:"total_executions"`
	SuccessfulExecutions int64   `json:"successful_executions"`
	FailedExecutions   int64     `json:"failed_executions"`
	AverageExecutionMs float64   `json:"average_execution_ms"`
	
	// Metadata
	Timestamps domain.PluginTimestamps `json:"timestamps"`
}

// NewPlugin creates a new plugin with the provided metadata
func NewPlugin(
	name valueobjects.PluginName,
	version valueobjects.PluginVersion,
	pluginType valueobjects.PluginType,
	entryPoint string,
	author string,
	license string,
) (*Plugin, error) {
	
	// Validate required fields
	if name.Value() == "" {
		return nil, domain.NewInvalidInputError("name", name.Value(), "plugin name cannot be empty")
	}
	
	if version.Value() == "" {
		return nil, domain.NewInvalidInputError("version", version.Value(), "plugin version cannot be empty")
	}
	
	if entryPoint == "" {
		return nil, domain.NewInvalidInputError("entry_point", entryPoint, "plugin entry point cannot be empty")
	}
	
	plugin := &Plugin{
		PluginID:              domain.NewPluginID(),
		Name:                  name,
		Version:               version,
		PluginType:            pluginType,
		EntryPoint:            entryPoint,
		Author:                author,
		License:               license,
		PythonVersion:         ">=3.13",
		Dependencies:          make([]string, 0),
		Capabilities:          make([]valueobjects.PluginCapability, 0),
		ConfigurationSchema:   make(map[string]interface{}),
		DefaultConfiguration:  make(map[string]interface{}),
		CurrentConfiguration:  make(map[string]interface{}),
		RequiredPermissions:   make([]string, 0),
		SecurityLevel:         "standard",
		Trusted:               false,
		MinMemoryMB:           128,
		CPUCores:              1,
		DiskSpaceMB:           100,
		Lifecycle:             valueobjects.PluginLifecycleUnregistered,
		Status:                valueobjects.PluginStatusUnknown,
		IsEnabled:             true,
		SupportsHotReload:     false,
		ReloadCount:           0,
		TotalExecutions:       0,
		SuccessfulExecutions:  0,
		FailedExecutions:      0,
		AverageExecutionMs:    0.0,
		Timestamps:            domain.NewPluginTimestamps(),
	}
	
	// TODO: Add domain events when needed
	
	return plugin, nil
}

// Register transitions the plugin to registered state
func (p *Plugin) Register() error {
	if !p.Lifecycle.CanTransitionTo(valueobjects.PluginLifecycleRegistered) {
		return domain.NewLifecycleError(
			p.PluginID.String(),
			p.Lifecycle.String(),
			valueobjects.PluginLifecycleRegistered.String(),
			"cannot transition to registered state",
		)
	}
	
	p.Lifecycle = valueobjects.PluginLifecycleRegistered
	p.Timestamps.MarkUpdated()
	
	
	return nil
}

// Load transitions the plugin to loaded state
func (p *Plugin) Load() error {
	if !p.Lifecycle.CanTransitionTo(valueobjects.PluginLifecycleLoaded) {
		return domain.NewLifecycleError(
			p.PluginID.String(),
			p.Lifecycle.String(),
			valueobjects.PluginLifecycleLoaded.String(),
			"cannot transition to loaded state",
		)
	}
	
	now := time.Now()
	p.Lifecycle = valueobjects.PluginLifecycleLoaded
	p.LoadedAt = &now
	p.Timestamps.MarkLoaded()
	
	
	return nil
}

// Initialize transitions the plugin to initialized state
func (p *Plugin) Initialize() error {
	if !p.Lifecycle.CanTransitionTo(valueobjects.PluginLifecycleInitialized) {
		return domain.NewLifecycleError(
			p.PluginID.String(),
			p.Lifecycle.String(),
			valueobjects.PluginLifecycleInitialized.String(),
			"cannot transition to initialized state",
		)
	}
	
	p.Lifecycle = valueobjects.PluginLifecycleInitialized
	p.Status = valueobjects.PluginStatusHealthy
	p.Timestamps.MarkUpdated()
	
	
	return nil
}

// Activate transitions the plugin to active state
func (p *Plugin) Activate() error {
	if !p.Lifecycle.CanTransitionTo(valueobjects.PluginLifecycleActive) {
		return domain.NewLifecycleError(
			p.PluginID.String(),
			p.Lifecycle.String(),
			valueobjects.PluginLifecycleActive.String(),
			"cannot transition to active state",
		)
	}
	
	p.Lifecycle = valueobjects.PluginLifecycleActive
	p.IsEnabled = true
	p.Timestamps.MarkUpdated()
	
	
	return nil
}

// Suspend transitions the plugin to suspended state
func (p *Plugin) Suspend() error {
	if !p.Lifecycle.CanTransitionTo(valueobjects.PluginLifecycleSuspended) {
		return domain.NewLifecycleError(
			p.PluginID.String(),
			p.Lifecycle.String(),
			valueobjects.PluginLifecycleSuspended.String(),
			"cannot transition to suspended state",
		)
	}
	
	p.Lifecycle = valueobjects.PluginLifecycleSuspended
	p.IsEnabled = false
	p.Timestamps.MarkUpdated()
	
	
	return nil
}

// MarkError transitions the plugin to error state
func (p *Plugin) MarkError(errorMessage string) error {
	p.Lifecycle = valueobjects.PluginLifecycleError
	p.Status = valueobjects.PluginStatusUnhealthy
	p.Timestamps.MarkUpdated()
	
	
	return nil
}

// Unload transitions the plugin to unloading then unloaded state
func (p *Plugin) Unload() error {
	// First transition to unloading
	if !p.Lifecycle.CanTransitionTo(valueobjects.PluginLifecycleUnloading) {
		return domain.NewLifecycleError(
			p.PluginID.String(),
			p.Lifecycle.String(),
			valueobjects.PluginLifecycleUnloading.String(),
			"cannot transition to unloading state",
		)
	}
	
	p.Lifecycle = valueobjects.PluginLifecycleUnloading
	
	// Perform unloading operations here...
	
	// Then transition to unloaded
	p.Lifecycle = valueobjects.PluginLifecycleUnloaded
	p.Timestamps.MarkUnloaded()
	p.LoadedAt = nil
	
	
	return nil
}

// AddCapability adds a capability to the plugin
func (p *Plugin) AddCapability(capability valueobjects.PluginCapability) error {
	// Check if capability already exists
	for _, existing := range p.Capabilities {
		if existing == capability {
			return domain.NewBusinessRuleError(fmt.Sprintf("capability '%s' already exists", capability.String()))
		}
	}
	
	p.Capabilities = append(p.Capabilities, capability)
	p.Timestamps.MarkUpdated()
	
	return nil
}

// RemoveCapability removes a capability from the plugin
func (p *Plugin) RemoveCapability(capability valueobjects.PluginCapability) error {
	for i, existing := range p.Capabilities {
		if existing == capability {
			// Remove capability by shifting slice
			p.Capabilities = append(p.Capabilities[:i], p.Capabilities[i+1:]...)
			p.Timestamps.MarkUpdated()
			return nil
		}
	}
	
	return domain.NewBusinessRuleError(fmt.Sprintf("capability '%s' not found", capability.String()))
}

// HasCapability checks if the plugin has a specific capability
func (p *Plugin) HasCapability(capability valueobjects.PluginCapability) bool {
	for _, existing := range p.Capabilities {
		if existing == capability {
			return true
		}
	}
	return false
}

// SetConfiguration updates the plugin's current configuration
func (p *Plugin) SetConfiguration(config map[string]interface{}) error {
	// Validate configuration against schema if available
	if len(p.ConfigurationSchema) > 0 {
		if err := p.validateConfiguration(config); err != nil {
			return domain.NewConfigurationError(p.PluginID.String(), "", err.Error())
		}
	}
	
	p.CurrentConfiguration = config
	p.Timestamps.MarkUpdated()
	
	
	return nil
}

// GetConfiguration returns a copy of the current configuration
func (p *Plugin) GetConfiguration() map[string]interface{} {
	config := make(map[string]interface{})
	for k, v := range p.CurrentConfiguration {
		config[k] = v
	}
	return config
}

// SetConfigurationValue sets a specific configuration value
func (p *Plugin) SetConfigurationValue(key string, value interface{}) error {
	if p.CurrentConfiguration == nil {
		p.CurrentConfiguration = make(map[string]interface{})
	}
	
	p.CurrentConfiguration[key] = value
	p.Timestamps.MarkUpdated()
	
	return nil
}

// GetConfigurationValue gets a specific configuration value
func (p *Plugin) GetConfigurationValue(key string) (interface{}, bool) {
	value, exists := p.CurrentConfiguration[key]
	return value, exists
}

// CanExecute checks if the plugin can be executed
func (p *Plugin) CanExecute() bool {
	return p.IsEnabled &&
		(p.Lifecycle == valueobjects.PluginLifecycleActive) &&
		(p.Status == valueobjects.PluginStatusHealthy || p.Status == valueobjects.PluginStatusDegraded)
}

// MarkUsed updates the last used timestamp
func (p *Plugin) MarkUsed() {
	now := time.Now()
	p.LastUsedAt = &now
	p.Timestamps.MarkUsed()
}

// RecordExecution records the result of a plugin execution
func (p *Plugin) RecordExecution(success bool, durationMs int64) {
	p.TotalExecutions++
	
	if success {
		p.SuccessfulExecutions++
	} else {
		p.FailedExecutions++
	}
	
	// Update average execution time
	if p.TotalExecutions > 0 {
		totalTime := p.AverageExecutionMs * float64(p.TotalExecutions-1)
		p.AverageExecutionMs = (totalTime + float64(durationMs)) / float64(p.TotalExecutions)
	}
	
	p.MarkUsed()
}

// GetSuccessRate returns the success rate of plugin executions
func (p *Plugin) GetSuccessRate() float64 {
	if p.TotalExecutions == 0 {
		return 0.0
	}
	return float64(p.SuccessfulExecutions) / float64(p.TotalExecutions) * 100.0
}

// UpdateHealthStatus updates the plugin's health status
func (p *Plugin) UpdateHealthStatus(status valueobjects.PluginStatus) {
	if p.Status != status {
		p.Status = status
		now := time.Now()
		p.LastHealthCheck = &now
		p.Timestamps.MarkUpdated()
	}
}

// EnableHotReload enables hot reload capability for the plugin
func (p *Plugin) EnableHotReload() error {
	if !p.HasCapability(valueobjects.CapabilityHotReload) {
		return domain.NewBusinessRuleError("plugin does not support hot reload capability")
	}
	
	p.SupportsHotReload = true
	p.Timestamps.MarkUpdated()
	
	
	return nil
}

// DisableHotReload disables hot reload capability for the plugin
func (p *Plugin) DisableHotReload() {
	p.SupportsHotReload = false
	p.Timestamps.MarkUpdated()
	
}

// PerformHotReload performs a hot reload of the plugin
func (p *Plugin) PerformHotReload() error {
	if !p.SupportsHotReload {
		return domain.NewHotReloadError(p.PluginID.String(), "plugin does not support hot reload", nil)
	}
	
	if p.Lifecycle != valueobjects.PluginLifecycleActive {
		return domain.NewHotReloadError(p.PluginID.String(), "plugin must be active to perform hot reload", nil)
	}
	
	now := time.Now()
	p.LastReloadedAt = &now
	p.ReloadCount++
	p.Timestamps.MarkUpdated()
	
	
	return nil
}

// AddDependency adds a dependency to the plugin
func (p *Plugin) AddDependency(dependency string) error {
	// Check if dependency already exists
	for _, existing := range p.Dependencies {
		if existing == dependency {
			return domain.NewBusinessRuleError(fmt.Sprintf("dependency '%s' already exists", dependency))
		}
	}
	
	p.Dependencies = append(p.Dependencies, dependency)
	p.Timestamps.MarkUpdated()
	
	return nil
}

// RemoveDependency removes a dependency from the plugin
func (p *Plugin) RemoveDependency(dependency string) error {
	for i, existing := range p.Dependencies {
		if existing == dependency {
			// Remove dependency by shifting slice
			p.Dependencies = append(p.Dependencies[:i], p.Dependencies[i+1:]...)
			p.Timestamps.MarkUpdated()
			return nil
		}
	}
	
	return domain.NewBusinessRuleError(fmt.Sprintf("dependency '%s' not found", dependency))
}

// HasDependency checks if the plugin has a specific dependency
func (p *Plugin) HasDependency(dependency string) bool {
	for _, existing := range p.Dependencies {
		if existing == dependency {
			return true
		}
	}
	return false
}

// SetResourceLimits sets the resource limits for the plugin
func (p *Plugin) SetResourceLimits(minMemoryMB, maxMemoryMB, cpuCores, diskSpaceMB int) error {
	if minMemoryMB <= 0 {
		return domain.NewInvalidInputError("min_memory_mb", minMemoryMB, "minimum memory must be positive")
	}
	
	if maxMemoryMB > 0 && maxMemoryMB < minMemoryMB {
		return domain.NewInvalidInputError("max_memory_mb", maxMemoryMB, "maximum memory must be greater than minimum memory")
	}
	
	if cpuCores <= 0 {
		return domain.NewInvalidInputError("cpu_cores", cpuCores, "CPU cores must be positive")
	}
	
	if diskSpaceMB <= 0 {
		return domain.NewInvalidInputError("disk_space_mb", diskSpaceMB, "disk space must be positive")
	}
	
	p.MinMemoryMB = minMemoryMB
	if maxMemoryMB > 0 {
		p.MaxMemoryMB = &maxMemoryMB
	}
	p.CPUCores = cpuCores
	p.DiskSpaceMB = diskSpaceMB
	p.Timestamps.MarkUpdated()
	
	return nil
}

// validateConfiguration validates configuration against the schema
func (p *Plugin) validateConfiguration(config map[string]interface{}) error {
	// Basic validation - can be enhanced with JSON schema validation
	if config == nil {
		return fmt.Errorf("configuration cannot be nil")
	}
	
	// TODO: Implement JSON schema validation
	// For now, just check that required fields exist in schema
	
	return nil
}

// ToJSON serializes the plugin to JSON
func (p *Plugin) ToJSON() ([]byte, error) {
	return json.Marshal(p)
}

// FromJSON deserializes the plugin from JSON  
func (p *Plugin) FromJSON(data []byte) error {
	return json.Unmarshal(data, p)
}