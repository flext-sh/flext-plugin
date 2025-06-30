package entities

import (
	"time"

	"github.com/flext-sh/flext-plugin/pkg/domain"
	"github.com/flext-sh/flext-plugin/pkg/domain/valueobjects"
)

// PluginFactory provides factory methods for creating plugin entities
// Following go-ddd principles: Domain sets defaults, separate creation vs rehydration
type PluginFactory struct{}

// NewPluginFactory creates a new plugin factory
func NewPluginFactory() *PluginFactory {
	return &PluginFactory{}
}

// CreatePlugin creates a new plugin entity with validation (for new plugins)
func (f *PluginFactory) CreatePlugin(
	name valueobjects.PluginName,
	version valueobjects.PluginVersion,
	pluginType valueobjects.PluginType,
	entryPoint string,
	author string,
	license string,
) (*Plugin, error) {
	
	// Domain validation for creation
	if name.Value() == "" {
		return nil, domain.NewInvalidInputError("name", name.Value(), "plugin name cannot be empty")
	}
	
	if version.Value() == "" {
		return nil, domain.NewInvalidInputError("version", version.Value(), "plugin version cannot be empty")
	}
	
	if !pluginType.IsValid() {
		return nil, domain.NewInvalidInputError("plugin_type", pluginType.String(), "invalid plugin type")
	}
	
	if entryPoint == "" {
		return nil, domain.NewInvalidInputError("entry_point", entryPoint, "entry point cannot be empty")
	}
	
	if author == "" {
		return nil, domain.NewInvalidInputError("author", author, "author cannot be empty")
	}
	
	if license == "" {
		return nil, domain.NewInvalidInputError("license", license, "license cannot be empty")
	}
	
	// Create plugin with domain defaults
	plugin := &Plugin{
		PluginID:              domain.NewPluginID(),
		Name:                  name,
		Version:               version,
		PluginType:            pluginType,
		EntryPoint:            entryPoint,
		Author:                author,
		License:               license,
		Description:           "",
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
		MaxMemoryMB:           nil,
		CPUCores:              1,
		DiskSpaceMB:           100,
		Lifecycle:             valueobjects.PluginLifecycleUnregistered,
		Status:                valueobjects.PluginStatusUnknown,
		IsEnabled:             true,
		LoadedAt:              nil,
		LastUsedAt:            nil,
		LastHealthCheck:       nil,
		SupportsHotReload:     false,
		LastReloadedAt:        nil,
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

// RehydratePlugin creates a plugin from stored data without validation (for loading from storage)
func (f *PluginFactory) RehydratePlugin(
	pluginID domain.PluginID,
	name valueobjects.PluginName,
	version valueobjects.PluginVersion,
	description string,
	author string,
	license string,
	pluginType valueobjects.PluginType,
	capabilities []valueobjects.PluginCapability,
	entryPoint string,
	pythonVersion string,
	dependencies []string,
	configurationSchema map[string]interface{},
	defaultConfiguration map[string]interface{},
	currentConfiguration map[string]interface{},
	requiredPermissions []string,
	securityLevel string,
	trusted bool,
	minMemoryMB int,
	maxMemoryMB *int,
	cpuCores int,
	diskSpaceMB int,
	lifecycle valueobjects.PluginLifecycle,
	status valueobjects.PluginStatus,
	isEnabled bool,
	loadedAt *time.Time,
	lastUsedAt *time.Time,
	lastHealthCheck *time.Time,
	supportsHotReload bool,
	lastReloadedAt *time.Time,
	reloadCount int,
	totalExecutions int64,
	successfulExecutions int64,
	failedExecutions int64,
	averageExecutionMs float64,
	timestamps domain.PluginTimestamps,
) *Plugin {
	
	// No validation on rehydration - preserves historical data
	plugin := &Plugin{
		PluginID:              pluginID,
		Name:                  name,
		Version:               version,
		Description:           description,
		Author:                author,
		License:               license,
		PluginType:            pluginType,
		Capabilities:          capabilities,
		EntryPoint:            entryPoint,
		PythonVersion:         pythonVersion,
		Dependencies:          dependencies,
		ConfigurationSchema:   configurationSchema,
		DefaultConfiguration:  defaultConfiguration,
		CurrentConfiguration:  currentConfiguration,
		RequiredPermissions:   requiredPermissions,
		SecurityLevel:         securityLevel,
		Trusted:               trusted,
		MinMemoryMB:           minMemoryMB,
		MaxMemoryMB:           maxMemoryMB,
		CPUCores:              cpuCores,
		DiskSpaceMB:           diskSpaceMB,
		Lifecycle:             lifecycle,
		Status:                status,
		IsEnabled:             isEnabled,
		LoadedAt:              loadedAt,
		LastUsedAt:            lastUsedAt,
		LastHealthCheck:       lastHealthCheck,
		SupportsHotReload:     supportsHotReload,
		LastReloadedAt:        lastReloadedAt,
		ReloadCount:           reloadCount,
		TotalExecutions:       totalExecutions,
		SuccessfulExecutions:  successfulExecutions,
		FailedExecutions:      failedExecutions,
		AverageExecutionMs:    averageExecutionMs,
		Timestamps:            timestamps,
	}
	
	return plugin
}

// CreateBasicPlugin creates a plugin with minimal required information
func (f *PluginFactory) CreateBasicPlugin(
	name string,
	version string,
	pluginType string,
	entryPoint string,
	author string,
) (*Plugin, error) {
	
	// Create value objects with validation
	pluginName, err := valueobjects.NewPluginName(name)
	if err != nil {
		return nil, err
	}
	
	pluginVersion, err := valueobjects.NewPluginVersion(version)
	if err != nil {
		return nil, err
	}
	
	pluginTypeVO, err := valueobjects.NewPluginType(pluginType)
	if err != nil {
		return nil, err
	}
	
	// Use default license if not provided
	license := "MIT"
	if author == "" {
		author = "Unknown"
	}
	
	return f.CreatePlugin(pluginName, pluginVersion, pluginTypeVO, entryPoint, author, license)
}

// CreateExtractorPlugin creates a plugin with extractor-specific defaults
func (f *PluginFactory) CreateExtractorPlugin(
	name string,
	version string,
	entryPoint string,
	author string,
) (*Plugin, error) {
	
	plugin, err := f.CreateBasicPlugin(name, version, "extractor", entryPoint, author)
	if err != nil {
		return nil, err
	}
	
	// Add extractor-specific capabilities
	plugin.AddCapability(valueobjects.CapabilityDataExtraction)
	plugin.AddCapability(valueobjects.CapabilitySchemaInference)
	
	// Set extractor-specific defaults
	plugin.MinMemoryMB = 256
	plugin.DiskSpaceMB = 500
	
	return plugin, nil
}

// CreateLoaderPlugin creates a plugin with loader-specific defaults
func (f *PluginFactory) CreateLoaderPlugin(
	name string,
	version string,
	entryPoint string,
	author string,
) (*Plugin, error) {
	
	plugin, err := f.CreateBasicPlugin(name, version, "loader", entryPoint, author)
	if err != nil {
		return nil, err
	}
	
	// Add loader-specific capabilities
	plugin.AddCapability(valueobjects.CapabilityDataLoading)
	plugin.AddCapability(valueobjects.CapabilityDataValidation)
	
	// Set loader-specific defaults
	plugin.MinMemoryMB = 512
	plugin.DiskSpaceMB = 1000
	
	return plugin, nil
}

// CreateTransformerPlugin creates a plugin with transformer-specific defaults
func (f *PluginFactory) CreateTransformerPlugin(
	name string,
	version string,
	entryPoint string,
	author string,
) (*Plugin, error) {
	
	plugin, err := f.CreateBasicPlugin(name, version, "transformer", entryPoint, author)
	if err != nil {
		return nil, err
	}
	
	// Add transformer-specific capabilities
	plugin.AddCapability(valueobjects.CapabilityDataTransformation)
	plugin.AddCapability(valueobjects.CapabilityDataValidation)
	
	// Set transformer-specific defaults
	plugin.MinMemoryMB = 384
	plugin.DiskSpaceMB = 200
	
	return plugin, nil
}

// CreateMonitorPlugin creates a plugin with monitor-specific defaults
func (f *PluginFactory) CreateMonitorPlugin(
	name string,
	version string,
	entryPoint string,
	author string,
) (*Plugin, error) {
	
	plugin, err := f.CreateBasicPlugin(name, version, "monitor", entryPoint, author)
	if err != nil {
		return nil, err
	}
	
	// Add monitor-specific capabilities
	plugin.AddCapability(valueobjects.CapabilityHealthMonitoring)
	plugin.AddCapability(valueobjects.CapabilityPerformanceMonitoring)
	plugin.AddCapability(valueobjects.CapabilityErrorReporting)
	
	// Set monitor-specific defaults
	plugin.MinMemoryMB = 128
	plugin.DiskSpaceMB = 100
	
	return plugin, nil
}

// PluginExecutionFactory provides factory methods for creating plugin execution entities
type PluginExecutionFactory struct{}

// NewPluginExecutionFactory creates a new plugin execution factory
func NewPluginExecutionFactory() *PluginExecutionFactory {
	return &PluginExecutionFactory{}
}

// CreateExecution creates a new plugin execution entity with validation
func (f *PluginExecutionFactory) CreateExecution(
	pluginID domain.PluginID,
	triggeredBy string,
	triggerType string,
) (*PluginExecution, error) {
	
	// Domain validation for creation
	if pluginID.IsZero() {
		return nil, domain.NewInvalidInputError("plugin_id", pluginID.String(), "plugin ID cannot be empty")
	}
	
	if triggeredBy == "" {
		return nil, domain.NewInvalidInputError("triggered_by", triggeredBy, "triggered_by cannot be empty")
	}
	
	if triggerType == "" {
		return nil, domain.NewInvalidInputError("trigger_type", triggerType, "trigger_type cannot be empty")
	}
	
	// Create execution with domain defaults
	execution := &PluginExecution{
		ExecutionID:      domain.NewExecutionID(),
		PluginID:         pluginID,
		Status:           ExecutionStatusPending,
		TriggeredBy:      triggeredBy,
		TriggerType:      triggerType,
		Priority:         0,
		InputData:        make(map[string]interface{}),
		OutputData:       make(map[string]interface{}),
		ExecutionContext: make(map[string]interface{}),
		Environment:      "default",
		DurationMs:       0,
		TimeoutMs:        300000, // 5 minutes default
		MemoryUsageMB:    0,
		CPUTimeMs:        0,
		MaxMemoryMB:      512, // 512MB default limit
		Tags:             make(map[string]string),
		Metrics:          make(map[string]float64),
		RecordsProcessed: 0,
		RecordsSuccess:   0,
		RecordsError:     0,
		RetryCount:       0,
		MaxRetries:       3,
		Timestamps:       domain.NewPluginTimestamps(),
	}
	
	// Create execution result
	execution.Result = valueobjects.NewPluginExecutionResult(
		pluginID.String(),
		execution.ExecutionID.String(),
	)
	
	return execution, nil
}

// RehydrateExecution creates a plugin execution from stored data without validation
func (f *PluginExecutionFactory) RehydrateExecution(
	executionID domain.ExecutionID,
	pluginID domain.PluginID,
	status PluginExecutionStatus,
	triggeredBy string,
	triggerType string,
	priority int,
	inputData map[string]interface{},
	outputData map[string]interface{},
	errorMessage string,
	errorCode string,
	executionContext map[string]interface{},
	environment string,
	sessionID string,
	userID string,
	scheduledAt *time.Time,
	startedAt *time.Time,
	completedAt *time.Time,
	durationMs int64,
	timeoutMs int64,
	memoryUsageMB float64,
	cpuTimeMs float64,
	maxMemoryMB float64,
	traceID string,
	spanID string,
	tags map[string]string,
	metrics map[string]float64,
	recordsProcessed int64,
	recordsSuccess int64,
	recordsError int64,
	retryCount int,
	maxRetries int,
	result *valueobjects.PluginExecutionResult,
	timestamps domain.PluginTimestamps,
) *PluginExecution {
	
	// No validation on rehydration - preserves historical data
	execution := &PluginExecution{
		ExecutionID:      executionID,
		PluginID:         pluginID,
		Status:           status,
		TriggeredBy:      triggeredBy,
		TriggerType:      triggerType,
		Priority:         priority,
		InputData:        inputData,
		OutputData:       outputData,
		ErrorMessage:     errorMessage,
		ErrorCode:        errorCode,
		ExecutionContext: executionContext,
		Environment:      environment,
		SessionID:        sessionID,
		UserID:           userID,
		ScheduledAt:      scheduledAt,
		StartedAt:        startedAt,
		CompletedAt:      completedAt,
		DurationMs:       durationMs,
		TimeoutMs:        timeoutMs,
		MemoryUsageMB:    memoryUsageMB,
		CPUTimeMs:        cpuTimeMs,
		MaxMemoryMB:      maxMemoryMB,
		TraceID:          traceID,
		SpanID:           spanID,
		Tags:             tags,
		Metrics:          metrics,
		RecordsProcessed: recordsProcessed,
		RecordsSuccess:   recordsSuccess,
		RecordsError:     recordsError,
		RetryCount:       retryCount,
		MaxRetries:       maxRetries,
		Result:           result,
		Timestamps:       timestamps,
	}
	
	return execution
}

// CreateScheduledExecution creates a scheduled plugin execution
func (f *PluginExecutionFactory) CreateScheduledExecution(
	pluginID domain.PluginID,
	scheduledAt time.Time,
	triggeredBy string,
) (*PluginExecution, error) {
	
	execution, err := f.CreateExecution(pluginID, triggeredBy, "scheduled")
	if err != nil {
		return nil, err
	}
	
	execution.ScheduledAt = &scheduledAt
	execution.AddTag("trigger_type", "scheduled")
	execution.AddTag("scheduled_at", scheduledAt.Format(time.RFC3339))
	
	return execution, nil
}

// CreateManualExecution creates a manually triggered plugin execution
func (f *PluginExecutionFactory) CreateManualExecution(
	pluginID domain.PluginID,
	userID string,
	sessionID string,
) (*PluginExecution, error) {
	
	execution, err := f.CreateExecution(pluginID, userID, "manual")
	if err != nil {
		return nil, err
	}
	
	execution.UserID = userID
	execution.SessionID = sessionID
	execution.AddTag("trigger_type", "manual")
	execution.AddTag("user_id", userID)
	
	return execution, nil
}

// CreateAPIExecution creates an API-triggered plugin execution
func (f *PluginExecutionFactory) CreateAPIExecution(
	pluginID domain.PluginID,
	apiEndpoint string,
	requestID string,
) (*PluginExecution, error) {
	
	execution, err := f.CreateExecution(pluginID, apiEndpoint, "api")
	if err != nil {
		return nil, err
	}
	
	execution.AddTag("trigger_type", "api")
	execution.AddTag("api_endpoint", apiEndpoint)
	execution.AddTag("request_id", requestID)
	execution.SetContextData("api_endpoint", apiEndpoint)
	execution.SetContextData("request_id", requestID)
	
	return execution, nil
}

// CreateEventExecution creates an event-triggered plugin execution
func (f *PluginExecutionFactory) CreateEventExecution(
	pluginID domain.PluginID,
	eventType string,
	eventSource string,
) (*PluginExecution, error) {
	
	execution, err := f.CreateExecution(pluginID, eventSource, "event")
	if err != nil {
		return nil, err
	}
	
	execution.AddTag("trigger_type", "event")
	execution.AddTag("event_type", eventType)
	execution.AddTag("event_source", eventSource)
	execution.SetContextData("event_type", eventType)
	execution.SetContextData("event_source", eventSource)
	
	return execution, nil
}