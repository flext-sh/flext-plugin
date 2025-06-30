package ports

import (
	"context"

	"github.com/flext-sh/flext-plugin/pkg/domain"
	"github.com/flext-sh/flext-plugin/pkg/domain/entities"
	"github.com/flext-sh/flext-plugin/pkg/domain/valueobjects"
)

// PluginRepository defines the contract for plugin persistence
// Following go-ddd principles: Find vs Get semantics, soft deletion, read after write
type PluginRepository interface {
	// Get methods - must return value or error
	GetByID(ctx context.Context, id domain.PluginID) (*entities.Plugin, error)
	GetByName(ctx context.Context, name valueobjects.PluginName) (*entities.Plugin, error)
	GetByNameAndVersion(ctx context.Context, name valueobjects.PluginName, version valueobjects.PluginVersion) (*entities.Plugin, error)

	// Find methods - can return nil without error
	FindByID(ctx context.Context, id domain.PluginID) (*entities.Plugin, error)
	FindByName(ctx context.Context, name valueobjects.PluginName) (*entities.Plugin, error)
	FindByType(ctx context.Context, pluginType valueobjects.PluginType) ([]*entities.Plugin, error)
	FindByCapability(ctx context.Context, capability valueobjects.PluginCapability) ([]*entities.Plugin, error)
	FindByAuthor(ctx context.Context, author string) ([]*entities.Plugin, error)
	FindByLifecycle(ctx context.Context, lifecycle valueobjects.PluginLifecycle) ([]*entities.Plugin, error)
	FindByStatus(ctx context.Context, status valueobjects.PluginStatus) ([]*entities.Plugin, error)
	
	// Query methods
	FindAll(ctx context.Context, limit, offset int) ([]*entities.Plugin, error)
	FindEnabled(ctx context.Context) ([]*entities.Plugin, error)
	FindDisabled(ctx context.Context) ([]*entities.Plugin, error)
	FindActive(ctx context.Context) ([]*entities.Plugin, error)
	FindLoaded(ctx context.Context) ([]*entities.Plugin, error)
	FindWithHotReload(ctx context.Context) ([]*entities.Plugin, error)
	
	// Search methods
	Search(ctx context.Context, query string, limit, offset int) ([]*entities.Plugin, error)
	SearchByTags(ctx context.Context, tags []string) ([]*entities.Plugin, error)
	
	// Existence checks
	ExistsByID(ctx context.Context, id domain.PluginID) (bool, error)
	ExistsByName(ctx context.Context, name valueobjects.PluginName) (bool, error)
	ExistsByNameAndVersion(ctx context.Context, name valueobjects.PluginName, version valueobjects.PluginVersion) (bool, error)
	
	// Write operations - follow read after write pattern
	Save(ctx context.Context, plugin *entities.Plugin) (*entities.Plugin, error)
	Update(ctx context.Context, plugin *entities.Plugin) (*entities.Plugin, error)
	
	// Soft deletion - preserves history
	Delete(ctx context.Context, id domain.PluginID) error
	SoftDelete(ctx context.Context, id domain.PluginID) error
	
	// State management
	UpdateLifecycle(ctx context.Context, id domain.PluginID, lifecycle valueobjects.PluginLifecycle) error
	UpdateStatus(ctx context.Context, id domain.PluginID, status valueobjects.PluginStatus) error
	UpdateConfiguration(ctx context.Context, id domain.PluginID, config map[string]interface{}) error
	
	// Metrics and analytics
	GetTotalCount(ctx context.Context) (int64, error)
	GetCountByType(ctx context.Context, pluginType valueobjects.PluginType) (int64, error)
	GetCountByStatus(ctx context.Context, status valueobjects.PluginStatus) (int64, error)
	GetMostUsed(ctx context.Context, limit int) ([]*entities.Plugin, error)
	GetLeastUsed(ctx context.Context, limit int) ([]*entities.Plugin, error)
	
	// Batch operations
	SaveBatch(ctx context.Context, plugins []*entities.Plugin) ([]*entities.Plugin, error)
	UpdateBatch(ctx context.Context, plugins []*entities.Plugin) ([]*entities.Plugin, error)
	DeleteBatch(ctx context.Context, ids []domain.PluginID) error
}

// PluginExecutionRepository defines the contract for plugin execution persistence
type PluginExecutionRepository interface {
	// Get methods - must return value or error
	GetByID(ctx context.Context, id domain.ExecutionID) (*entities.PluginExecution, error)
	GetByPluginAndExecution(ctx context.Context, pluginID domain.PluginID, executionID domain.ExecutionID) (*entities.PluginExecution, error)
	
	// Find methods - can return nil without error
	FindByID(ctx context.Context, id domain.ExecutionID) (*entities.PluginExecution, error)
	FindByPluginID(ctx context.Context, pluginID domain.PluginID, limit, offset int) ([]*entities.PluginExecution, error)
	FindByStatus(ctx context.Context, status entities.PluginExecutionStatus) ([]*entities.PluginExecution, error)
	FindByTriggeredBy(ctx context.Context, triggeredBy string) ([]*entities.PluginExecution, error)
	FindByTriggerType(ctx context.Context, triggerType string) ([]*entities.PluginExecution, error)
	FindByEnvironment(ctx context.Context, environment string) ([]*entities.PluginExecution, error)
	FindByUserID(ctx context.Context, userID string) ([]*entities.PluginExecution, error)
	
	// Query methods
	FindAll(ctx context.Context, limit, offset int) ([]*entities.PluginExecution, error)
	FindRunning(ctx context.Context) ([]*entities.PluginExecution, error)
	FindCompleted(ctx context.Context, limit, offset int) ([]*entities.PluginExecution, error)
	FindFailed(ctx context.Context, limit, offset int) ([]*entities.PluginExecution, error)
	FindPending(ctx context.Context) ([]*entities.PluginExecution, error)
	FindTimedOut(ctx context.Context) ([]*entities.PluginExecution, error)
	FindCancelled(ctx context.Context, limit, offset int) ([]*entities.PluginExecution, error)
	
	// Time-based queries
	FindByDateRange(ctx context.Context, start, end string) ([]*entities.PluginExecution, error)
	FindRecent(ctx context.Context, hours int, limit int) ([]*entities.PluginExecution, error)
	FindLongRunning(ctx context.Context, thresholdMs int64) ([]*entities.PluginExecution, error)
	
	// Search methods
	Search(ctx context.Context, query string, limit, offset int) ([]*entities.PluginExecution, error)
	SearchByTraceID(ctx context.Context, traceID string) ([]*entities.PluginExecution, error)
	SearchByTags(ctx context.Context, tags map[string]string) ([]*entities.PluginExecution, error)
	
	// Existence checks
	ExistsByID(ctx context.Context, id domain.ExecutionID) (bool, error)
	ExistsByPluginAndExecution(ctx context.Context, pluginID domain.PluginID, executionID domain.ExecutionID) (bool, error)
	
	// Write operations - follow read after write pattern
	Save(ctx context.Context, execution *entities.PluginExecution) (*entities.PluginExecution, error)
	Update(ctx context.Context, execution *entities.PluginExecution) (*entities.PluginExecution, error)
	
	// Soft deletion - preserves execution history
	Delete(ctx context.Context, id domain.ExecutionID) error
	SoftDelete(ctx context.Context, id domain.ExecutionID) error
	
	// State management
	UpdateStatus(ctx context.Context, id domain.ExecutionID, status entities.PluginExecutionStatus) error
	UpdateResourceUsage(ctx context.Context, id domain.ExecutionID, memoryMB, cpuTimeMs float64) error
	UpdateMetrics(ctx context.Context, id domain.ExecutionID, metrics map[string]float64) error
	AddTags(ctx context.Context, id domain.ExecutionID, tags map[string]string) error
	
	// Execution management
	GetNextExecutionNumber(ctx context.Context, pluginID domain.PluginID) (int64, error)
	MarkStarted(ctx context.Context, id domain.ExecutionID) error
	MarkCompleted(ctx context.Context, id domain.ExecutionID, outputData map[string]interface{}) error
	MarkFailed(ctx context.Context, id domain.ExecutionID, errorMessage, errorCode string) error
	MarkCancelled(ctx context.Context, id domain.ExecutionID, reason string) error
	MarkTimedOut(ctx context.Context, id domain.ExecutionID) error
	
	// Metrics and analytics
	GetTotalCount(ctx context.Context) (int64, error)
	GetCountByPlugin(ctx context.Context, pluginID domain.PluginID) (int64, error)
	GetCountByStatus(ctx context.Context, status entities.PluginExecutionStatus) (int64, error)
	GetSuccessRate(ctx context.Context, pluginID domain.PluginID) (float64, error)
	GetAverageExecutionTime(ctx context.Context, pluginID domain.PluginID) (float64, error)
	GetExecutionStats(ctx context.Context, pluginID domain.PluginID) (map[string]interface{}, error)
	
	// Cleanup and maintenance
	DeleteOldExecutions(ctx context.Context, olderThanDays int) (int64, error)
	DeleteByPlugin(ctx context.Context, pluginID domain.PluginID) error
	ArchiveExecutions(ctx context.Context, olderThanDays int) (int64, error)
	
	// Batch operations
	SaveBatch(ctx context.Context, executions []*entities.PluginExecution) ([]*entities.PluginExecution, error)
	UpdateBatch(ctx context.Context, executions []*entities.PluginExecution) ([]*entities.PluginExecution, error)
	DeleteBatch(ctx context.Context, ids []domain.ExecutionID) error
}

// PluginDiscoveryPort defines the contract for plugin discovery services
type PluginDiscoveryPort interface {
	// Discovery operations
	DiscoverPlugins(ctx context.Context, directories []string) ([]*entities.Plugin, error)
	DiscoverPluginInDirectory(ctx context.Context, directory string) ([]*entities.Plugin, error)
	DiscoverPluginByPath(ctx context.Context, path string) (*entities.Plugin, error)
	
	// Validation
	ValidatePluginStructure(ctx context.Context, path string) error
	ValidatePluginMetadata(ctx context.Context, metadata map[string]interface{}) error
	ValidatePluginDependencies(ctx context.Context, dependencies []string) error
	
	// Metadata extraction
	ExtractMetadata(ctx context.Context, path string) (map[string]interface{}, error)
	ExtractCapabilities(ctx context.Context, path string) ([]valueobjects.PluginCapability, error)
	ExtractConfigurationSchema(ctx context.Context, path string) (map[string]interface{}, error)
	
	// Registry operations
	RegisterPlugin(ctx context.Context, plugin *entities.Plugin) error
	UnregisterPlugin(ctx context.Context, pluginID domain.PluginID) error
	UpdatePluginRegistry(ctx context.Context, plugin *entities.Plugin) error
}

// PluginLoaderPort defines the contract for plugin loading services
type PluginLoaderPort interface {
	// Loading operations
	LoadPlugin(ctx context.Context, plugin *entities.Plugin) error
	UnloadPlugin(ctx context.Context, pluginID domain.PluginID) error
	ReloadPlugin(ctx context.Context, pluginID domain.PluginID) error
	
	// Lifecycle management
	InitializePlugin(ctx context.Context, pluginID domain.PluginID) error
	StartPlugin(ctx context.Context, pluginID domain.PluginID) error
	StopPlugin(ctx context.Context, pluginID domain.PluginID) error
	SuspendPlugin(ctx context.Context, pluginID domain.PluginID) error
	ResumePlugin(ctx context.Context, pluginID domain.PluginID) error
	
	// Hot reload support
	SupportsHotReload(ctx context.Context, pluginID domain.PluginID) (bool, error)
	PerformHotReload(ctx context.Context, pluginID domain.PluginID) error
	
	// Health checks
	CheckPluginHealth(ctx context.Context, pluginID domain.PluginID) (map[string]interface{}, error)
	GetPluginStatus(ctx context.Context, pluginID domain.PluginID) (valueobjects.PluginStatus, error)
	
	// Resource management
	GetResourceUsage(ctx context.Context, pluginID domain.PluginID) (map[string]interface{}, error)
	SetResourceLimits(ctx context.Context, pluginID domain.PluginID, limits map[string]interface{}) error
	
	// Configuration management
	ApplyConfiguration(ctx context.Context, pluginID domain.PluginID, config map[string]interface{}) error
	ValidateConfiguration(ctx context.Context, pluginID domain.PluginID, config map[string]interface{}) error
}

// PluginExecutorPort defines the contract for plugin execution services
type PluginExecutorPort interface {
	// Execution operations
	ExecutePlugin(ctx context.Context, execution *entities.PluginExecution) (*valueobjects.PluginExecutionResult, error)
	ExecutePluginAsync(ctx context.Context, execution *entities.PluginExecution) (chan *valueobjects.PluginExecutionResult, error)
	CancelExecution(ctx context.Context, executionID domain.ExecutionID) error
	
	// Execution management
	CreateExecution(ctx context.Context, pluginID domain.PluginID, input map[string]interface{}, context map[string]interface{}) (*entities.PluginExecution, error)
	ScheduleExecution(ctx context.Context, pluginID domain.PluginID, scheduledAt string, input map[string]interface{}) (*entities.PluginExecution, error)
	RetryExecution(ctx context.Context, executionID domain.ExecutionID) (*entities.PluginExecution, error)
	
	// Monitoring
	GetExecutionStatus(ctx context.Context, executionID domain.ExecutionID) (entities.PluginExecutionStatus, error)
	GetExecutionResult(ctx context.Context, executionID domain.ExecutionID) (*valueobjects.PluginExecutionResult, error)
	GetExecutionLogs(ctx context.Context, executionID domain.ExecutionID) ([]string, error)
	GetExecutionMetrics(ctx context.Context, executionID domain.ExecutionID) (map[string]interface{}, error)
	
	// Resource monitoring
	MonitorResourceUsage(ctx context.Context, executionID domain.ExecutionID) error
	GetResourceUsage(ctx context.Context, executionID domain.ExecutionID) (map[string]interface{}, error)
	
	// Timeout management
	SetExecutionTimeout(ctx context.Context, executionID domain.ExecutionID, timeoutMs int64) error
	CheckExecutionTimeout(ctx context.Context, executionID domain.ExecutionID) (bool, error)
}

// PluginManagerPort defines the contract for high-level plugin management
type PluginManagerPort interface {
	// Plugin lifecycle
	RegisterPlugin(ctx context.Context, pluginPath string) (*entities.Plugin, error)
	InstallPlugin(ctx context.Context, pluginID domain.PluginID) error
	UninstallPlugin(ctx context.Context, pluginID domain.PluginID) error
	EnablePlugin(ctx context.Context, pluginID domain.PluginID) error
	DisablePlugin(ctx context.Context, pluginID domain.PluginID) error
	
	// Plugin discovery and management
	ListPlugins(ctx context.Context) ([]*entities.Plugin, error)
	GetPlugin(ctx context.Context, pluginID domain.PluginID) (*entities.Plugin, error)
	SearchPlugins(ctx context.Context, query string) ([]*entities.Plugin, error)
	
	// Plugin execution
	ExecutePlugin(ctx context.Context, pluginID domain.PluginID, input map[string]interface{}) (*valueobjects.PluginExecutionResult, error)
	GetExecutions(ctx context.Context, pluginID domain.PluginID) ([]*entities.PluginExecution, error)
	
	// Configuration management
	GetPluginConfiguration(ctx context.Context, pluginID domain.PluginID) (map[string]interface{}, error)
	SetPluginConfiguration(ctx context.Context, pluginID domain.PluginID, config map[string]interface{}) error
	
	// Health and monitoring
	CheckPluginHealth(ctx context.Context, pluginID domain.PluginID) (valueobjects.PluginStatus, error)
	GetPluginMetrics(ctx context.Context, pluginID domain.PluginID) (map[string]interface{}, error)
	
	// Hot reload
	ReloadPlugin(ctx context.Context, pluginID domain.PluginID) error
	EnableHotReload(ctx context.Context, pluginID domain.PluginID) error
	DisableHotReload(ctx context.Context, pluginID domain.PluginID) error
}

// HotReloadPort defines the contract for hot reload functionality
type HotReloadPort interface {
	// Hot reload management
	EnableHotReload(ctx context.Context, pluginID domain.PluginID) error
	DisableHotReload(ctx context.Context, pluginID domain.PluginID) error
	IsHotReloadEnabled(ctx context.Context, pluginID domain.PluginID) (bool, error)
	
	// File watching
	StartWatching(ctx context.Context, pluginID domain.PluginID, paths []string) error
	StopWatching(ctx context.Context, pluginID domain.PluginID) error
	GetWatchedPaths(ctx context.Context, pluginID domain.PluginID) ([]string, error)
	
	// Reload operations
	ReloadPlugin(ctx context.Context, pluginID domain.PluginID) error
	ReloadPluginWithBackup(ctx context.Context, pluginID domain.PluginID) error
	RollbackReload(ctx context.Context, pluginID domain.PluginID) error
	
	// State management
	PreserveState(ctx context.Context, pluginID domain.PluginID) error
	RestoreState(ctx context.Context, pluginID domain.PluginID) error
	ClearState(ctx context.Context, pluginID domain.PluginID) error
	
	// Validation
	ValidateBeforeReload(ctx context.Context, pluginID domain.PluginID) error
	CheckReloadCompatibility(ctx context.Context, pluginID domain.PluginID) error
	
	// Events
	OnFileChanged(ctx context.Context, pluginID domain.PluginID, filePath string) error
	OnReloadStarted(ctx context.Context, pluginID domain.PluginID) error
	OnReloadCompleted(ctx context.Context, pluginID domain.PluginID) error
	OnReloadFailed(ctx context.Context, pluginID domain.PluginID, err error) error
}

// EventBusPort defines the contract for plugin event publishing
type EventBusPort interface {
	// Event publishing
	Publish(ctx context.Context, event *domain.PluginDomainEvent) error
	PublishBatch(ctx context.Context, events []*domain.PluginDomainEvent) error
	
	// Event subscription
	Subscribe(ctx context.Context, eventType string, handler func(*domain.PluginDomainEvent) error) error
	Unsubscribe(ctx context.Context, eventType string) error
	
	// Event filtering
	SubscribeToPlugin(ctx context.Context, pluginID domain.PluginID, handler func(*domain.PluginDomainEvent) error) error
	SubscribeToExecution(ctx context.Context, executionID domain.ExecutionID, handler func(*domain.PluginDomainEvent) error) error
}

// LoggingPort defines the contract for plugin logging
type LoggingPort interface {
	// Logging methods
	Debug(ctx context.Context, message string, fields map[string]interface{})
	Info(ctx context.Context, message string, fields map[string]interface{})
	Warn(ctx context.Context, message string, fields map[string]interface{})
	Error(ctx context.Context, message string, err error, fields map[string]interface{})
	
	// Plugin-specific logging
	LogPluginEvent(ctx context.Context, pluginID domain.PluginID, level string, message string, fields map[string]interface{})
	LogExecutionEvent(ctx context.Context, executionID domain.ExecutionID, level string, message string, fields map[string]interface{})
	
	// Log retrieval
	GetPluginLogs(ctx context.Context, pluginID domain.PluginID, limit int) ([]map[string]interface{}, error)
	GetExecutionLogs(ctx context.Context, executionID domain.ExecutionID, limit int) ([]map[string]interface{}, error)
}