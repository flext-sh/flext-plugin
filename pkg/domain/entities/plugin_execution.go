package entities

import (
	"encoding/json"
	"time"

	"github.com/flext-sh/flext-plugin/pkg/domain"
	"github.com/flext-sh/flext-plugin/pkg/domain/valueobjects"
)

// PluginExecutionStatus represents the status of a plugin execution
type PluginExecutionStatus string

const (
	ExecutionStatusPending   PluginExecutionStatus = "pending"
	ExecutionStatusRunning   PluginExecutionStatus = "running"
	ExecutionStatusCompleted PluginExecutionStatus = "completed"
	ExecutionStatusFailed    PluginExecutionStatus = "failed"
	ExecutionStatusCancelled PluginExecutionStatus = "cancelled"
	ExecutionStatusTimeout   PluginExecutionStatus = "timeout"
)

// PluginExecution represents a plugin execution entity
type PluginExecution struct {
	domain.PluginEntity

	// Identity
	ExecutionID domain.ExecutionID `json:"execution_id"`
	PluginID    domain.PluginID    `json:"plugin_id"`
	
	// Execution metadata
	Status        PluginExecutionStatus `json:"status"`
	TriggeredBy   string               `json:"triggered_by"`
	TriggerType   string               `json:"trigger_type"`
	Priority      int                  `json:"priority"`
	
	// Input and output
	InputData     map[string]interface{} `json:"input_data"`
	OutputData    map[string]interface{} `json:"output_data"`
	ErrorMessage  string                 `json:"error_message,omitempty"`
	ErrorCode     string                 `json:"error_code,omitempty"`
	
	// Execution context
	ExecutionContext map[string]interface{} `json:"execution_context"`
	Environment      string                 `json:"environment"`
	SessionID        string                 `json:"session_id,omitempty"`
	UserID           string                 `json:"user_id,omitempty"`
	
	// Timing information
	ScheduledAt  *time.Time `json:"scheduled_at,omitempty"`
	StartedAt    *time.Time `json:"started_at,omitempty"`
	CompletedAt  *time.Time `json:"completed_at,omitempty"`
	DurationMs   int64      `json:"duration_ms"`
	TimeoutMs    int64      `json:"timeout_ms"`
	
	// Resource usage
	MemoryUsageMB  float64 `json:"memory_usage_mb"`
	CPUTimeMs      float64 `json:"cpu_time_ms"`
	MaxMemoryMB    float64 `json:"max_memory_mb"`
	
	// Tracing and monitoring
	TraceID      string            `json:"trace_id,omitempty"`
	SpanID       string            `json:"span_id,omitempty"`
	Tags         map[string]string `json:"tags"`
	Metrics      map[string]float64 `json:"metrics"`
	
	// Result metadata
	RecordsProcessed int64   `json:"records_processed"`
	RecordsSuccess   int64   `json:"records_success"`
	RecordsError     int64   `json:"records_error"`
	RetryCount       int     `json:"retry_count"`
	MaxRetries       int     `json:"max_retries"`
	
	// Execution result
	Result *valueobjects.PluginExecutionResult `json:"result,omitempty"`
	
	// Timestamps
	Timestamps domain.PluginTimestamps `json:"timestamps"`
}

// NewPluginExecution creates a new plugin execution
func NewPluginExecution(
	pluginID domain.PluginID,
	triggeredBy string,
	triggerType string,
) *PluginExecution {
	
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
	
	return execution
}

// Start starts the plugin execution
func (pe *PluginExecution) Start() error {
	if pe.Status != ExecutionStatusPending {
		return domain.NewLifecycleError(
			pe.PluginID.String(),
			string(pe.Status),
			string(ExecutionStatusRunning),
			"execution must be pending to start",
		)
	}
	
	now := time.Now()
	pe.Status = ExecutionStatusRunning
	pe.StartedAt = &now
	pe.Timestamps.MarkUpdated()
	
	// Add context data to result
	pe.Result.AddContextData("started_at", now)
	pe.Result.AddContextData("triggered_by", pe.TriggeredBy)
	pe.Result.AddContextData("trigger_type", pe.TriggerType)
	
	return nil
}

// Complete completes the plugin execution successfully
func (pe *PluginExecution) Complete(outputData map[string]interface{}) error {
	if pe.Status != ExecutionStatusRunning {
		return domain.NewLifecycleError(
			pe.PluginID.String(),
			string(pe.Status),
			string(ExecutionStatusCompleted),
			"execution must be running to complete",
		)
	}
	
	now := time.Now()
	pe.Status = ExecutionStatusCompleted
	pe.CompletedAt = &now
	pe.OutputData = outputData
	
	// Calculate duration
	if pe.StartedAt != nil {
		pe.DurationMs = now.Sub(*pe.StartedAt).Milliseconds()
	}
	
	pe.Timestamps.MarkUpdated()
	
	// Mark result as completed
	pe.Result.MarkCompleted(outputData, nil)
	
	return nil
}

// Fail marks the plugin execution as failed
func (pe *PluginExecution) Fail(errorMessage, errorCode string, err error) error {
	if pe.Status == ExecutionStatusCompleted {
		return domain.NewLifecycleError(
			pe.PluginID.String(),
			string(pe.Status),
			string(ExecutionStatusFailed),
			"cannot fail a completed execution",
		)
	}
	
	now := time.Now()
	pe.Status = ExecutionStatusFailed
	pe.CompletedAt = &now
	pe.ErrorMessage = errorMessage
	pe.ErrorCode = errorCode
	
	// Calculate duration
	if pe.StartedAt != nil {
		pe.DurationMs = now.Sub(*pe.StartedAt).Milliseconds()
	}
	
	pe.Timestamps.MarkUpdated()
	
	// Mark result as failed
	pe.Result.MarkCompleted(nil, err)
	
	return nil
}

// Cancel cancels the plugin execution
func (pe *PluginExecution) Cancel(reason string) error {
	if pe.Status == ExecutionStatusCompleted || pe.Status == ExecutionStatusFailed {
		return domain.NewLifecycleError(
			pe.PluginID.String(),
			string(pe.Status),
			string(ExecutionStatusCancelled),
			"cannot cancel a completed or failed execution",
		)
	}
	
	now := time.Now()
	pe.Status = ExecutionStatusCancelled
	pe.CompletedAt = &now
	pe.ErrorMessage = reason
	pe.ErrorCode = "CANCELLED"
	
	// Calculate duration
	if pe.StartedAt != nil {
		pe.DurationMs = now.Sub(*pe.StartedAt).Milliseconds()
	}
	
	pe.Timestamps.MarkUpdated()
	
	// Mark result as cancelled
	pe.Result.MarkCompleted(nil, domain.NewExecutionError(
		pe.PluginID.String(),
		pe.ExecutionID.String(),
		reason,
		nil,
	))
	
	return nil
}

// Timeout marks the plugin execution as timed out
func (pe *PluginExecution) Timeout() error {
	if pe.Status == ExecutionStatusCompleted || pe.Status == ExecutionStatusFailed {
		return domain.NewLifecycleError(
			pe.PluginID.String(),
			string(pe.Status),
			string(ExecutionStatusTimeout),
			"cannot timeout a completed or failed execution",
		)
	}
	
	now := time.Now()
	pe.Status = ExecutionStatusTimeout
	pe.CompletedAt = &now
	pe.ErrorMessage = "execution timed out"
	pe.ErrorCode = "TIMEOUT"
	
	// Calculate duration
	if pe.StartedAt != nil {
		pe.DurationMs = now.Sub(*pe.StartedAt).Milliseconds()
	}
	
	pe.Timestamps.MarkUpdated()
	
	// Mark result as timed out
	pe.Result.MarkCompleted(nil, domain.NewTimeoutError(
		pe.PluginID.String(),
		"plugin execution",
		time.Duration(pe.TimeoutMs*int64(time.Millisecond)).String(),
	))
	
	return nil
}

// Retry increments the retry count and resets the execution
func (pe *PluginExecution) Retry() error {
	if pe.RetryCount >= pe.MaxRetries {
		return domain.NewBusinessRuleError("maximum retry count exceeded")
	}
	
	pe.RetryCount++
	pe.Status = ExecutionStatusPending
	pe.StartedAt = nil
	pe.CompletedAt = nil
	pe.ErrorMessage = ""
	pe.ErrorCode = ""
	pe.Timestamps.MarkUpdated()
	
	// Create new execution result for retry
	pe.Result = valueobjects.NewPluginExecutionResult(
		pe.PluginID.String(),
		pe.ExecutionID.String(),
	)
	pe.Result.AddContextData("retry_count", pe.RetryCount)
	
	return nil
}

// SetInputData sets the input data for the execution
func (pe *PluginExecution) SetInputData(key string, value interface{}) {
	if pe.InputData == nil {
		pe.InputData = make(map[string]interface{})
	}
	pe.InputData[key] = value
	pe.Timestamps.MarkUpdated()
}

// GetInputData gets input data value by key
func (pe *PluginExecution) GetInputData(key string) (interface{}, bool) {
	value, exists := pe.InputData[key]
	return value, exists
}

// SetOutputData sets the output data for the execution
func (pe *PluginExecution) SetOutputData(key string, value interface{}) {
	if pe.OutputData == nil {
		pe.OutputData = make(map[string]interface{})
	}
	pe.OutputData[key] = value
	pe.Timestamps.MarkUpdated()
}

// GetOutputData gets output data value by key
func (pe *PluginExecution) GetOutputData(key string) (interface{}, bool) {
	value, exists := pe.OutputData[key]
	return value, exists
}

// SetContextData sets execution context data
func (pe *PluginExecution) SetContextData(key string, value interface{}) {
	if pe.ExecutionContext == nil {
		pe.ExecutionContext = make(map[string]interface{})
	}
	pe.ExecutionContext[key] = value
	pe.Result.AddContextData(key, value)
	pe.Timestamps.MarkUpdated()
}

// GetContextData gets execution context data by key
func (pe *PluginExecution) GetContextData(key string) (interface{}, bool) {
	value, exists := pe.ExecutionContext[key]
	return value, exists
}

// AddTag adds a tag to the execution
func (pe *PluginExecution) AddTag(key, value string) {
	if pe.Tags == nil {
		pe.Tags = make(map[string]string)
	}
	pe.Tags[key] = value
	pe.Timestamps.MarkUpdated()
}

// GetTag gets a tag value by key
func (pe *PluginExecution) GetTag(key string) (string, bool) {
	value, exists := pe.Tags[key]
	return value, exists
}

// SetMetric sets a metric value
func (pe *PluginExecution) SetMetric(key string, value float64) {
	if pe.Metrics == nil {
		pe.Metrics = make(map[string]float64)
	}
	pe.Metrics[key] = value
	pe.Timestamps.MarkUpdated()
}

// GetMetric gets a metric value by key
func (pe *PluginExecution) GetMetric(key string) (float64, bool) {
	value, exists := pe.Metrics[key]
	return value, exists
}

// UpdateResourceUsage updates the resource usage metrics
func (pe *PluginExecution) UpdateResourceUsage(memoryMB, cpuTimeMs float64) {
	pe.MemoryUsageMB = memoryMB
	pe.CPUTimeMs = cpuTimeMs
	
	// Update peak memory usage
	if memoryMB > pe.MaxMemoryMB {
		pe.MaxMemoryMB = memoryMB
	}
	
	// Update result resource usage
	pe.Result.SetResourceUsage(memoryMB, cpuTimeMs)
	
	pe.Timestamps.MarkUpdated()
}

// SetTracing sets the distributed tracing information
func (pe *PluginExecution) SetTracing(traceID, spanID string) {
	pe.TraceID = traceID
	pe.SpanID = spanID
	pe.Result.SetTracing(traceID, spanID)
	pe.Timestamps.MarkUpdated()
}

// UpdateRecordMetrics updates the record processing metrics
func (pe *PluginExecution) UpdateRecordMetrics(processed, success, error int64) {
	pe.RecordsProcessed = processed
	pe.RecordsSuccess = success
	pe.RecordsError = error
	
	// Add metrics to result context
	pe.Result.AddContextData("records_processed", processed)
	pe.Result.AddContextData("records_success", success)
	pe.Result.AddContextData("records_error", error)
	
	pe.Timestamps.MarkUpdated()
}

// GetSuccessRate returns the success rate of record processing
func (pe *PluginExecution) GetSuccessRate() float64 {
	if pe.RecordsProcessed == 0 {
		return 0.0
	}
	return float64(pe.RecordsSuccess) / float64(pe.RecordsProcessed) * 100.0
}

// IsCompleted checks if the execution is in a terminal state
func (pe *PluginExecution) IsCompleted() bool {
	return pe.Status == ExecutionStatusCompleted ||
		pe.Status == ExecutionStatusFailed ||
		pe.Status == ExecutionStatusCancelled ||
		pe.Status == ExecutionStatusTimeout
}

// IsRunning checks if the execution is currently running
func (pe *PluginExecution) IsRunning() bool {
	return pe.Status == ExecutionStatusRunning
}

// IsSuccessful checks if the execution completed successfully
func (pe *PluginExecution) IsSuccessful() bool {
	return pe.Status == ExecutionStatusCompleted
}

// HasTimedOut checks if the execution should be considered timed out
func (pe *PluginExecution) HasTimedOut() bool {
	if pe.StartedAt == nil || pe.TimeoutMs <= 0 {
		return false
	}
	
	elapsed := time.Since(*pe.StartedAt).Milliseconds()
	return elapsed > pe.TimeoutMs
}

// GetElapsedTime returns the elapsed execution time
func (pe *PluginExecution) GetElapsedTime() time.Duration {
	if pe.StartedAt == nil {
		return 0
	}
	
	if pe.CompletedAt != nil {
		return pe.CompletedAt.Sub(*pe.StartedAt)
	}
	
	return time.Since(*pe.StartedAt)
}

// SetTimeout sets the execution timeout
func (pe *PluginExecution) SetTimeout(timeoutMs int64) {
	pe.TimeoutMs = timeoutMs
	pe.Timestamps.MarkUpdated()
}

// SetPriority sets the execution priority
func (pe *PluginExecution) SetPriority(priority int) {
	pe.Priority = priority
	pe.Timestamps.MarkUpdated()
}

// ToJSON serializes the execution to JSON
func (pe *PluginExecution) ToJSON() ([]byte, error) {
	return json.Marshal(pe)
}

// FromJSON deserializes the execution from JSON
func (pe *PluginExecution) FromJSON(data []byte) error {
	return json.Unmarshal(data, pe)
}