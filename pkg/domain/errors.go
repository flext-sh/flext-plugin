package domain

import (
	"errors"
	"fmt"
)

// Plugin-specific domain errors following go-ddd principles
var (
	ErrPluginNotFound         = errors.New("plugin not found")
	ErrPluginAlreadyExists    = errors.New("plugin already exists")
	ErrPluginInvalidInput     = errors.New("plugin invalid input")
	ErrPluginBusinessRule     = errors.New("plugin business rule violation")
	ErrPluginConcurrency      = errors.New("plugin concurrency conflict")
	ErrPluginValidation       = errors.New("plugin validation failed")
	ErrPluginLoad             = errors.New("plugin load failed")
	ErrPluginExecution        = errors.New("plugin execution failed")
	ErrPluginDependency       = errors.New("plugin dependency failed")
	ErrPluginSecurity         = errors.New("plugin security violation")
	ErrPluginConfiguration    = errors.New("plugin configuration error")
	ErrPluginLifecycle        = errors.New("plugin lifecycle error")
	ErrPluginResource         = errors.New("plugin resource error")
	ErrPluginPermission       = errors.New("plugin permission denied")
	ErrPluginTimeout          = errors.New("plugin operation timeout")
	ErrPluginHotReload        = errors.New("plugin hot reload failed")
)

// PluginDomainError provides structured error information for plugin operations
type PluginDomainError struct {
	Type     error
	Message  string
	Field    string
	Value    interface{}
	PluginID string
	Details  map[string]interface{}
}

// Error implements the error interface
func (e *PluginDomainError) Error() string {
	if e.PluginID != "" {
		return fmt.Sprintf("[Plugin %s] %s: %s", e.PluginID, e.Type.Error(), e.Message)
	}
	return fmt.Sprintf("%s: %s", e.Type.Error(), e.Message)
}

// Unwrap returns the underlying error type for errors.Is() compatibility
func (e *PluginDomainError) Unwrap() error {
	return e.Type
}

// IsNotFound checks if the error is a not found error
func (e *PluginDomainError) IsNotFound() bool {
	return errors.Is(e.Type, ErrPluginNotFound)
}

// IsAlreadyExists checks if the error is an already exists error
func (e *PluginDomainError) IsAlreadyExists() bool {
	return errors.Is(e.Type, ErrPluginAlreadyExists)
}

// IsValidation checks if the error is a validation error
func (e *PluginDomainError) IsValidation() bool {
	return errors.Is(e.Type, ErrPluginValidation) || errors.Is(e.Type, ErrPluginInvalidInput)
}

// IsBusinessRule checks if the error is a business rule violation
func (e *PluginDomainError) IsBusinessRule() bool {
	return errors.Is(e.Type, ErrPluginBusinessRule)
}

// IsSecurity checks if the error is a security violation
func (e *PluginDomainError) IsSecurity() bool {
	return errors.Is(e.Type, ErrPluginSecurity) || errors.Is(e.Type, ErrPluginPermission)
}

// Helper functions for creating structured domain errors

// NewPluginNotFoundError creates a new plugin not found error
func NewPluginNotFoundError(pluginID string) *PluginDomainError {
	return &PluginDomainError{
		Type:     ErrPluginNotFound,
		Message:  fmt.Sprintf("plugin with ID '%s' not found", pluginID),
		PluginID: pluginID,
	}
}

// NewPluginAlreadyExistsError creates a new plugin already exists error
func NewPluginAlreadyExistsError(pluginID string) *PluginDomainError {
	return &PluginDomainError{
		Type:     ErrPluginAlreadyExists,
		Message:  fmt.Sprintf("plugin with ID '%s' already exists", pluginID),
		PluginID: pluginID,
	}
}

// NewInvalidInputError creates a new invalid input error with field context
func NewInvalidInputError(field string, value interface{}, message string) *PluginDomainError {
	return &PluginDomainError{
		Type:    ErrPluginInvalidInput,
		Message: message,
		Field:   field,
		Value:   value,
	}
}

// NewBusinessRuleError creates a new business rule violation error
func NewBusinessRuleError(message string) *PluginDomainError {
	return &PluginDomainError{
		Type:    ErrPluginBusinessRule,
		Message: message,
	}
}

// NewValidationError creates a new validation error with detailed failures
func NewValidationError(pluginID string, failures []string) *PluginDomainError {
	return &PluginDomainError{
		Type:     ErrPluginValidation,
		Message:  fmt.Sprintf("plugin validation failed: %v", failures),
		PluginID: pluginID,
		Details:  map[string]interface{}{"validation_failures": failures},
	}
}

// NewLoadError creates a new plugin load error
func NewLoadError(pluginID string, message string, cause error) *PluginDomainError {
	details := make(map[string]interface{})
	if cause != nil {
		details["cause"] = cause.Error()
	}
	return &PluginDomainError{
		Type:     ErrPluginLoad,
		Message:  message,
		PluginID: pluginID,
		Details:  details,
	}
}

// NewExecutionError creates a new plugin execution error
func NewExecutionError(pluginID string, executionID string, message string, cause error) *PluginDomainError {
	details := map[string]interface{}{
		"execution_id": executionID,
	}
	if cause != nil {
		details["cause"] = cause.Error()
	}
	return &PluginDomainError{
		Type:     ErrPluginExecution,
		Message:  message,
		PluginID: pluginID,
		Details:  details,
	}
}

// NewDependencyError creates a new plugin dependency error
func NewDependencyError(pluginID string, missingDependencies []string) *PluginDomainError {
	return &PluginDomainError{
		Type:     ErrPluginDependency,
		Message:  fmt.Sprintf("missing dependencies: %v", missingDependencies),
		PluginID: pluginID,
		Details:  map[string]interface{}{"missing_dependencies": missingDependencies},
	}
}

// NewSecurityError creates a new plugin security violation error
func NewSecurityError(pluginID string, violations []string) *PluginDomainError {
	return &PluginDomainError{
		Type:     ErrPluginSecurity,
		Message:  fmt.Sprintf("security violations: %v", violations),
		PluginID: pluginID,
		Details:  map[string]interface{}{"security_violations": violations},
	}
}

// NewConfigurationError creates a new plugin configuration error
func NewConfigurationError(pluginID string, field string, message string) *PluginDomainError {
	return &PluginDomainError{
		Type:     ErrPluginConfiguration,
		Message:  message,
		Field:    field,
		PluginID: pluginID,
	}
}

// NewLifecycleError creates a new plugin lifecycle error
func NewLifecycleError(pluginID string, currentState string, targetState string, message string) *PluginDomainError {
	return &PluginDomainError{
		Type:     ErrPluginLifecycle,
		Message:  message,
		PluginID: pluginID,
		Details: map[string]interface{}{
			"current_state": currentState,
			"target_state":  targetState,
		},
	}
}

// NewResourceError creates a new plugin resource error
func NewResourceError(pluginID string, resource string, message string) *PluginDomainError {
	return &PluginDomainError{
		Type:     ErrPluginResource,
		Message:  message,
		PluginID: pluginID,
		Details:  map[string]interface{}{"resource": resource},
	}
}

// NewPermissionError creates a new plugin permission denied error
func NewPermissionError(pluginID string, permission string) *PluginDomainError {
	return &PluginDomainError{
		Type:     ErrPluginPermission,
		Message:  fmt.Sprintf("permission denied: %s", permission),
		PluginID: pluginID,
		Details:  map[string]interface{}{"required_permission": permission},
	}
}

// NewTimeoutError creates a new plugin timeout error
func NewTimeoutError(pluginID string, operation string, timeout string) *PluginDomainError {
	return &PluginDomainError{
		Type:     ErrPluginTimeout,
		Message:  fmt.Sprintf("operation '%s' timed out after %s", operation, timeout),
		PluginID: pluginID,
		Details: map[string]interface{}{
			"operation": operation,
			"timeout":   timeout,
		},
	}
}

// NewHotReloadError creates a new plugin hot reload error
func NewHotReloadError(pluginID string, message string, cause error) *PluginDomainError {
	details := make(map[string]interface{})
	if cause != nil {
		details["cause"] = cause.Error()
	}
	return &PluginDomainError{
		Type:     ErrPluginHotReload,
		Message:  message,
		PluginID: pluginID,
		Details:  details,
	}
}

// Helper functions for error checking

// IsPluginNotFound checks if an error is a plugin not found error
func IsPluginNotFound(err error) bool {
	var domainErr *PluginDomainError
	if errors.As(err, &domainErr) {
		return domainErr.IsNotFound()
	}
	return errors.Is(err, ErrPluginNotFound)
}

// IsPluginAlreadyExists checks if an error is a plugin already exists error
func IsPluginAlreadyExists(err error) bool {
	var domainErr *PluginDomainError
	if errors.As(err, &domainErr) {
		return domainErr.IsAlreadyExists()
	}
	return errors.Is(err, ErrPluginAlreadyExists)
}

// IsPluginValidation checks if an error is a plugin validation error
func IsPluginValidation(err error) bool {
	var domainErr *PluginDomainError
	if errors.As(err, &domainErr) {
		return domainErr.IsValidation()
	}
	return errors.Is(err, ErrPluginValidation) || errors.Is(err, ErrPluginInvalidInput)
}

// IsPluginBusinessRule checks if an error is a plugin business rule violation
func IsPluginBusinessRule(err error) bool {
	var domainErr *PluginDomainError
	if errors.As(err, &domainErr) {
		return domainErr.IsBusinessRule()
	}
	return errors.Is(err, ErrPluginBusinessRule)
}

// IsPluginSecurity checks if an error is a plugin security violation
func IsPluginSecurity(err error) bool {
	var domainErr *PluginDomainError
	if errors.As(err, &domainErr) {
		return domainErr.IsSecurity()
	}
	return errors.Is(err, ErrPluginSecurity) || errors.Is(err, ErrPluginPermission)
}