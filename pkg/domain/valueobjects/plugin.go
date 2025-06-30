package valueobjects

import (
	"regexp"
	"strings"
	"time"

	"github.com/flext-sh/flext-plugin/pkg/domain"
)

// PluginType represents the functional category of a plugin
type PluginType string

const (
	// Data processing plugins
	PluginTypeExtractor   PluginType = "extractor"
	PluginTypeLoader      PluginType = "loader"
	PluginTypeTransformer PluginType = "transformer"
	PluginTypeValidator   PluginType = "validator"

	// Pipeline and orchestration plugins
	PluginTypeOrchestrator PluginType = "orchestrator"
	PluginTypeScheduler    PluginType = "scheduler"
	PluginTypeTrigger      PluginType = "trigger"

	// Monitoring and observability plugins
	PluginTypeMonitor PluginType = "monitor"
	PluginTypeAlerter PluginType = "alerter"
	PluginTypeLogger  PluginType = "logger"
	PluginTypeTracer  PluginType = "tracer"

	// Integration and connectivity plugins
	PluginTypeConnector PluginType = "connector"
	PluginTypeAdapter   PluginType = "adapter"
	PluginTypeBridge    PluginType = "bridge"

	// Security and compliance plugins
	PluginTypeAuthenticator PluginType = "authenticator"
	PluginTypeAuthorizer    PluginType = "authorizer"
	PluginTypeEncryptor     PluginType = "encryptor"
	PluginTypeAuditor       PluginType = "auditor"

	// Utility and extension plugins
	PluginTypeUtility   PluginType = "utility"
	PluginTypeExtension PluginType = "extension"
	PluginTypeFilter    PluginType = "filter"
	PluginTypeProcessor PluginType = "processor"
)

// ValidPluginTypes contains all valid plugin types
var ValidPluginTypes = map[PluginType]bool{
	PluginTypeExtractor:     true,
	PluginTypeLoader:        true,
	PluginTypeTransformer:   true,
	PluginTypeValidator:     true,
	PluginTypeOrchestrator:  true,
	PluginTypeScheduler:     true,
	PluginTypeTrigger:       true,
	PluginTypeMonitor:       true,
	PluginTypeAlerter:       true,
	PluginTypeLogger:        true,
	PluginTypeTracer:        true,
	PluginTypeConnector:     true,
	PluginTypeAdapter:       true,
	PluginTypeBridge:        true,
	PluginTypeAuthenticator: true,
	PluginTypeAuthorizer:    true,
	PluginTypeEncryptor:     true,
	PluginTypeAuditor:       true,
	PluginTypeUtility:       true,
	PluginTypeExtension:     true,
	PluginTypeFilter:        true,
	PluginTypeProcessor:     true,
}

// NewPluginType creates a new PluginType with validation
func NewPluginType(value string) (PluginType, error) {
	pluginType := PluginType(strings.ToLower(strings.TrimSpace(value)))
	
	if !ValidPluginTypes[pluginType] {
		return "", domain.NewInvalidInputError("plugin_type", value, "invalid plugin type")
	}
	
	return pluginType, nil
}

// String returns the string representation of the plugin type
func (pt PluginType) String() string {
	return string(pt)
}

// IsValid checks if the plugin type is valid
func (pt PluginType) IsValid() bool {
	return ValidPluginTypes[pt]
}

// PluginLifecycle represents the lifecycle state of a plugin
type PluginLifecycle string

const (
	PluginLifecycleUnregistered PluginLifecycle = "unregistered"
	PluginLifecycleRegistered   PluginLifecycle = "registered"
	PluginLifecycleLoaded       PluginLifecycle = "loaded"
	PluginLifecycleInitialized  PluginLifecycle = "initialized"
	PluginLifecycleActive       PluginLifecycle = "active"
	PluginLifecycleSuspended    PluginLifecycle = "suspended"
	PluginLifecycleError        PluginLifecycle = "error"
	PluginLifecycleUnloading    PluginLifecycle = "unloading"
	PluginLifecycleUnloaded     PluginLifecycle = "unloaded"
)

// ValidPluginLifecycles contains all valid plugin lifecycle states
var ValidPluginLifecycles = map[PluginLifecycle]bool{
	PluginLifecycleUnregistered: true,
	PluginLifecycleRegistered:   true,
	PluginLifecycleLoaded:       true,
	PluginLifecycleInitialized:  true,
	PluginLifecycleActive:       true,
	PluginLifecycleSuspended:    true,
	PluginLifecycleError:        true,
	PluginLifecycleUnloading:    true,
	PluginLifecycleUnloaded:     true,
}

// NewPluginLifecycle creates a new PluginLifecycle with validation
func NewPluginLifecycle(value string) (PluginLifecycle, error) {
	lifecycle := PluginLifecycle(strings.ToLower(strings.TrimSpace(value)))
	
	if !ValidPluginLifecycles[lifecycle] {
		return "", domain.NewInvalidInputError("plugin_lifecycle", value, "invalid plugin lifecycle state")
	}
	
	return lifecycle, nil
}

// String returns the string representation of the plugin lifecycle
func (pl PluginLifecycle) String() string {
	return string(pl)
}

// IsValid checks if the plugin lifecycle state is valid
func (pl PluginLifecycle) IsValid() bool {
	return ValidPluginLifecycles[pl]
}

// CanTransitionTo checks if transition to another state is valid
func (pl PluginLifecycle) CanTransitionTo(target PluginLifecycle) bool {
	// Define valid state transitions
	validTransitions := map[PluginLifecycle][]PluginLifecycle{
		PluginLifecycleUnregistered: {PluginLifecycleRegistered},
		PluginLifecycleRegistered:   {PluginLifecycleLoaded, PluginLifecycleError},
		PluginLifecycleLoaded:       {PluginLifecycleInitialized, PluginLifecycleError, PluginLifecycleUnloading},
		PluginLifecycleInitialized:  {PluginLifecycleActive, PluginLifecycleError, PluginLifecycleUnloading},
		PluginLifecycleActive:       {PluginLifecycleSuspended, PluginLifecycleError, PluginLifecycleUnloading},
		PluginLifecycleSuspended:    {PluginLifecycleActive, PluginLifecycleError, PluginLifecycleUnloading},
		PluginLifecycleError:        {PluginLifecycleLoaded, PluginLifecycleUnloading},
		PluginLifecycleUnloading:    {PluginLifecycleUnloaded, PluginLifecycleError},
		PluginLifecycleUnloaded:     {PluginLifecycleRegistered},
	}
	
	allowedTargets, exists := validTransitions[pl]
	if !exists {
		return false
	}
	
	for _, allowed := range allowedTargets {
		if allowed == target {
			return true
		}
	}
	
	return false
}

// PluginStatus represents the operational status of a plugin
type PluginStatus string

const (
	PluginStatusHealthy   PluginStatus = "healthy"
	PluginStatusDegraded  PluginStatus = "degraded"
	PluginStatusUnhealthy PluginStatus = "unhealthy"
	PluginStatusUnknown   PluginStatus = "unknown"
)

// ValidPluginStatuses contains all valid plugin statuses
var ValidPluginStatuses = map[PluginStatus]bool{
	PluginStatusHealthy:   true,
	PluginStatusDegraded:  true,
	PluginStatusUnhealthy: true,
	PluginStatusUnknown:   true,
}

// NewPluginStatus creates a new PluginStatus with validation
func NewPluginStatus(value string) (PluginStatus, error) {
	status := PluginStatus(strings.ToLower(strings.TrimSpace(value)))
	
	if !ValidPluginStatuses[status] {
		return "", domain.NewInvalidInputError("plugin_status", value, "invalid plugin status")
	}
	
	return status, nil
}

// String returns the string representation of the plugin status
func (ps PluginStatus) String() string {
	return string(ps)
}

// IsValid checks if the plugin status is valid
func (ps PluginStatus) IsValid() bool {
	return ValidPluginStatuses[ps]
}

// PluginName represents a validated plugin name
type PluginName struct {
	value string
}

// pluginNamePattern defines the valid format for plugin names
var pluginNamePattern = regexp.MustCompile(`^[a-z0-9][a-z0-9-]*[a-z0-9]$`)

// NewPluginName creates a new PluginName with validation
func NewPluginName(name string) (PluginName, error) {
	name = strings.TrimSpace(name)
	
	if len(name) == 0 {
		return PluginName{}, domain.NewInvalidInputError("name", name, "plugin name cannot be empty")
	}
	
	if len(name) < 3 {
		return PluginName{}, domain.NewInvalidInputError("name", name, "plugin name must be at least 3 characters")
	}
	
	if len(name) > 100 {
		return PluginName{}, domain.NewInvalidInputError("name", name, "plugin name cannot exceed 100 characters")
	}
	
	if !pluginNamePattern.MatchString(name) {
		return PluginName{}, domain.NewInvalidInputError("name", name, "plugin name must contain only lowercase letters, numbers, and hyphens, and cannot start or end with a hyphen")
	}
	
	// Additional business rules
	if strings.Contains(name, "--") {
		return PluginName{}, domain.NewInvalidInputError("name", name, "plugin name cannot contain consecutive hyphens")
	}
	
	// Reserved names
	reservedNames := map[string]bool{
		"flext": true, "core": true, "system": true, "REDACTED_LDAP_BIND_PASSWORD": true,
		"root": true, "user": true, "config": true, "test": true,
	}
	
	if reservedNames[name] {
		return PluginName{}, domain.NewInvalidInputError("name", name, "plugin name is reserved")
	}
	
	return PluginName{value: name}, nil
}

// Value returns the string value of the plugin name
func (pn PluginName) Value() string {
	return pn.value
}

// String returns the string representation of the plugin name
func (pn PluginName) String() string {
	return pn.value
}

// PluginVersion represents a semantic version
type PluginVersion struct {
	value string
}

// semanticVersionPattern defines the valid format for semantic versions
var semanticVersionPattern = regexp.MustCompile(`^(\d+)\.(\d+)\.(\d+)(?:-([a-zA-Z0-9\-\.]+))?(?:\+([a-zA-Z0-9\-\.]+))?$`)

// NewPluginVersion creates a new PluginVersion with validation
func NewPluginVersion(version string) (PluginVersion, error) {
	version = strings.TrimSpace(version)
	
	if len(version) == 0 {
		return PluginVersion{}, domain.NewInvalidInputError("version", version, "plugin version cannot be empty")
	}
	
	if !semanticVersionPattern.MatchString(version) {
		return PluginVersion{}, domain.NewInvalidInputError("version", version, "plugin version must follow semantic versioning (e.g., 1.0.0, 1.0.0-alpha, 1.0.0+build)")
	}
	
	return PluginVersion{value: version}, nil
}

// Value returns the string value of the plugin version
func (pv PluginVersion) Value() string {
	return pv.value
}

// String returns the string representation of the plugin version
func (pv PluginVersion) String() string {
	return pv.value
}

// PluginCapability represents a specific capability of a plugin
type PluginCapability string

const (
	// Data processing capabilities
	CapabilityDataExtraction     PluginCapability = "data_extraction"
	CapabilityDataLoading        PluginCapability = "data_loading"
	CapabilityDataTransformation PluginCapability = "data_transformation"
	CapabilityDataValidation     PluginCapability = "data_validation"

	// Schema and metadata capabilities
	CapabilitySchemaInference    PluginCapability = "schema_inference"
	CapabilitySchemaValidation   PluginCapability = "schema_validation"
	CapabilityMetadataExtraction PluginCapability = "metadata_extraction"

	// Synchronization capabilities
	CapabilityIncrementalSync PluginCapability = "incremental_sync"
	CapabilityFullSync        PluginCapability = "full_sync"
	CapabilityRealTimeSync    PluginCapability = "real_time_sync"

	// Pipeline capabilities
	CapabilityPipelineOrchestration PluginCapability = "pipeline_orchestration"
	CapabilityTaskScheduling        PluginCapability = "task_scheduling"
	CapabilityDependencyManagement  PluginCapability = "dependency_management"

	// Monitoring capabilities
	CapabilityHealthMonitoring      PluginCapability = "health_monitoring"
	CapabilityPerformanceMonitoring PluginCapability = "performance_monitoring"
	CapabilityErrorReporting        PluginCapability = "error_reporting"

	// Hot reload capability
	CapabilityHotReload PluginCapability = "hot_reload"
)

// ValidPluginCapabilities contains all valid plugin capabilities
var ValidPluginCapabilities = map[PluginCapability]bool{
	CapabilityDataExtraction:        true,
	CapabilityDataLoading:           true,
	CapabilityDataTransformation:    true,
	CapabilityDataValidation:        true,
	CapabilitySchemaInference:       true,
	CapabilitySchemaValidation:      true,
	CapabilityMetadataExtraction:    true,
	CapabilityIncrementalSync:       true,
	CapabilityFullSync:              true,
	CapabilityRealTimeSync:          true,
	CapabilityPipelineOrchestration: true,
	CapabilityTaskScheduling:        true,
	CapabilityDependencyManagement:  true,
	CapabilityHealthMonitoring:      true,
	CapabilityPerformanceMonitoring: true,
	CapabilityErrorReporting:        true,
	CapabilityHotReload:             true,
}

// NewPluginCapability creates a new PluginCapability with validation
func NewPluginCapability(value string) (PluginCapability, error) {
	capability := PluginCapability(strings.ToLower(strings.TrimSpace(value)))
	
	if !ValidPluginCapabilities[capability] {
		return "", domain.NewInvalidInputError("capability", value, "invalid plugin capability")
	}
	
	return capability, nil
}

// String returns the string representation of the plugin capability
func (pc PluginCapability) String() string {
	return string(pc)
}

// IsValid checks if the plugin capability is valid
func (pc PluginCapability) IsValid() bool {
	return ValidPluginCapabilities[pc]
}

// PluginExecutionResult represents the result of a plugin execution
type PluginExecutionResult struct {
	Success       bool                   `json:"success"`
	Result        interface{}            `json:"result,omitempty"`
	Error         string                 `json:"error,omitempty"`
	PluginID      string                 `json:"plugin_id"`
	ExecutionID   string                 `json:"execution_id"`
	StartTime     time.Time              `json:"start_time"`
	EndTime       *time.Time             `json:"end_time,omitempty"`
	DurationMs    *int64                 `json:"duration_ms,omitempty"`
	Context       map[string]interface{} `json:"execution_context,omitempty"`
	TraceID       string                 `json:"trace_id,omitempty"`
	SpanID        string                 `json:"span_id,omitempty"`
	MemoryUsageMB *float64               `json:"memory_usage_mb,omitempty"`
	CPUTimeMs     *float64               `json:"cpu_time_ms,omitempty"`
}

// NewPluginExecutionResult creates a new plugin execution result
func NewPluginExecutionResult(pluginID, executionID string) *PluginExecutionResult {
	return &PluginExecutionResult{
		PluginID:    pluginID,
		ExecutionID: executionID,
		StartTime:   time.Now(),
		Context:     make(map[string]interface{}),
	}
}

// MarkCompleted marks the execution as completed with optional result or error
func (per *PluginExecutionResult) MarkCompleted(result interface{}, err error) {
	now := time.Now()
	per.EndTime = &now
	
	duration := now.Sub(per.StartTime).Milliseconds()
	per.DurationMs = &duration
	
	if err != nil {
		per.Success = false
		per.Error = err.Error()
	} else {
		per.Success = true
		per.Result = result
	}
}

// SetResourceUsage sets the resource usage metrics
func (per *PluginExecutionResult) SetResourceUsage(memoryMB, cpuTimeMs float64) {
	per.MemoryUsageMB = &memoryMB
	per.CPUTimeMs = &cpuTimeMs
}

// SetTracing sets the distributed tracing information
func (per *PluginExecutionResult) SetTracing(traceID, spanID string) {
	per.TraceID = traceID
	per.SpanID = spanID
}

// AddContextData adds data to the execution context
func (per *PluginExecutionResult) AddContextData(key string, value interface{}) {
	if per.Context == nil {
		per.Context = make(map[string]interface{})
	}
	per.Context[key] = value
}

// GetDuration returns the execution duration in milliseconds
func (per *PluginExecutionResult) GetDuration() int64 {
	if per.DurationMs != nil {
		return *per.DurationMs
	}
	
	if per.EndTime != nil {
		return per.EndTime.Sub(per.StartTime).Milliseconds()
	}
	
	return time.Since(per.StartTime).Milliseconds()
}