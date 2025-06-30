package specifications

import (
	"strings"
	"time"

	"github.com/flext-sh/flext-plugin/pkg/domain"
	"github.com/flext-sh/flext-plugin/pkg/domain/entities"
	"github.com/flext-sh/flext-plugin/pkg/domain/valueobjects"
)

// PluginSpecification defines the interface for plugin business rules
type PluginSpecification interface {
	IsSatisfiedBy(plugin *entities.Plugin) bool
	GetErrorMessage() string
}

// PluginExecutionSpecification defines the interface for plugin execution business rules
type PluginExecutionSpecification interface {
	IsSatisfiedBy(execution *entities.PluginExecution) bool
	GetErrorMessage() string
}

// AndSpecification combines multiple specifications with AND logic
type AndSpecification struct {
	specs []PluginSpecification
}

// NewAndSpecification creates a new AND specification
func NewAndSpecification(specs ...PluginSpecification) *AndSpecification {
	return &AndSpecification{specs: specs}
}

// IsSatisfiedBy checks if all specifications are satisfied
func (s *AndSpecification) IsSatisfiedBy(plugin *entities.Plugin) bool {
	for _, spec := range s.specs {
		if !spec.IsSatisfiedBy(plugin) {
			return false
		}
	}
	return true
}

// GetErrorMessage returns combined error messages
func (s *AndSpecification) GetErrorMessage() string {
	var messages []string
	for _, spec := range s.specs {
		messages = append(messages, spec.GetErrorMessage())
	}
	return strings.Join(messages, "; ")
}

// OrSpecification combines multiple specifications with OR logic
type OrSpecification struct {
	specs []PluginSpecification
}

// NewOrSpecification creates a new OR specification
func NewOrSpecification(specs ...PluginSpecification) *OrSpecification {
	return &OrSpecification{specs: specs}
}

// IsSatisfiedBy checks if any specification is satisfied
func (s *OrSpecification) IsSatisfiedBy(plugin *entities.Plugin) bool {
	for _, spec := range s.specs {
		if spec.IsSatisfiedBy(plugin) {
			return true
		}
	}
	return false
}

// GetErrorMessage returns combined error messages
func (s *OrSpecification) GetErrorMessage() string {
	var messages []string
	for _, spec := range s.specs {
		messages = append(messages, spec.GetErrorMessage())
	}
	return "None of the following conditions are met: " + strings.Join(messages, "; ")
}

// NotSpecification negates a specification
type NotSpecification struct {
	spec PluginSpecification
}

// NewNotSpecification creates a new NOT specification
func NewNotSpecification(spec PluginSpecification) *NotSpecification {
	return &NotSpecification{spec: spec}
}

// IsSatisfiedBy checks if the specification is NOT satisfied
func (s *NotSpecification) IsSatisfiedBy(plugin *entities.Plugin) bool {
	return !s.spec.IsSatisfiedBy(plugin)
}

// GetErrorMessage returns negated error message
func (s *NotSpecification) GetErrorMessage() string {
	return "NOT (" + s.spec.GetErrorMessage() + ")"
}

// Plugin Specifications

// PluginCanExecuteSpecification checks if a plugin can be executed
type PluginCanExecuteSpecification struct{}

// NewPluginCanExecuteSpecification creates a new plugin can execute specification
func NewPluginCanExecuteSpecification() *PluginCanExecuteSpecification {
	return &PluginCanExecuteSpecification{}
}

// IsSatisfiedBy checks if the plugin can be executed
func (s *PluginCanExecuteSpecification) IsSatisfiedBy(plugin *entities.Plugin) bool {
	return plugin.CanExecute()
}

// GetErrorMessage returns the error message
func (s *PluginCanExecuteSpecification) GetErrorMessage() string {
	return "plugin cannot be executed (must be enabled, active, and healthy)"
}

// PluginIsEnabledSpecification checks if a plugin is enabled
type PluginIsEnabledSpecification struct{}

// NewPluginIsEnabledSpecification creates a new plugin is enabled specification
func NewPluginIsEnabledSpecification() *PluginIsEnabledSpecification {
	return &PluginIsEnabledSpecification{}
}

// IsSatisfiedBy checks if the plugin is enabled
func (s *PluginIsEnabledSpecification) IsSatisfiedBy(plugin *entities.Plugin) bool {
	return plugin.IsEnabled
}

// GetErrorMessage returns the error message
func (s *PluginIsEnabledSpecification) GetErrorMessage() string {
	return "plugin is not enabled"
}

// PluginIsActiveSpecification checks if a plugin is in active lifecycle state
type PluginIsActiveSpecification struct{}

// NewPluginIsActiveSpecification creates a new plugin is active specification
func NewPluginIsActiveSpecification() *PluginIsActiveSpecification {
	return &PluginIsActiveSpecification{}
}

// IsSatisfiedBy checks if the plugin is in active state
func (s *PluginIsActiveSpecification) IsSatisfiedBy(plugin *entities.Plugin) bool {
	return plugin.Lifecycle == valueobjects.PluginLifecycleActive
}

// GetErrorMessage returns the error message
func (s *PluginIsActiveSpecification) GetErrorMessage() string {
	return "plugin is not in active lifecycle state"
}

// PluginIsHealthySpecification checks if a plugin is healthy
type PluginIsHealthySpecification struct{}

// NewPluginIsHealthySpecification creates a new plugin is healthy specification
func NewPluginIsHealthySpecification() *PluginIsHealthySpecification {
	return &PluginIsHealthySpecification{}
}

// IsSatisfiedBy checks if the plugin is healthy
func (s *PluginIsHealthySpecification) IsSatisfiedBy(plugin *entities.Plugin) bool {
	return plugin.Status == valueobjects.PluginStatusHealthy || 
		   plugin.Status == valueobjects.PluginStatusDegraded
}

// GetErrorMessage returns the error message
func (s *PluginIsHealthySpecification) GetErrorMessage() string {
	return "plugin is not healthy"
}

// PluginHasCapabilitySpecification checks if a plugin has a specific capability
type PluginHasCapabilitySpecification struct {
	capability valueobjects.PluginCapability
}

// NewPluginHasCapabilitySpecification creates a new plugin has capability specification
func NewPluginHasCapabilitySpecification(capability valueobjects.PluginCapability) *PluginHasCapabilitySpecification {
	return &PluginHasCapabilitySpecification{capability: capability}
}

// IsSatisfiedBy checks if the plugin has the required capability
func (s *PluginHasCapabilitySpecification) IsSatisfiedBy(plugin *entities.Plugin) bool {
	return plugin.HasCapability(s.capability)
}

// GetErrorMessage returns the error message
func (s *PluginHasCapabilitySpecification) GetErrorMessage() string {
	return "plugin does not have required capability: " + s.capability.String()
}

// PluginSupportsHotReloadSpecification checks if a plugin supports hot reload
type PluginSupportsHotReloadSpecification struct{}

// NewPluginSupportsHotReloadSpecification creates a new plugin supports hot reload specification
func NewPluginSupportsHotReloadSpecification() *PluginSupportsHotReloadSpecification {
	return &PluginSupportsHotReloadSpecification{}
}

// IsSatisfiedBy checks if the plugin supports hot reload
func (s *PluginSupportsHotReloadSpecification) IsSatisfiedBy(plugin *entities.Plugin) bool {
	return plugin.SupportsHotReload
}

// GetErrorMessage returns the error message
func (s *PluginSupportsHotReloadSpecification) GetErrorMessage() string {
	return "plugin does not support hot reload"
}

// PluginIsTrustedSpecification checks if a plugin is trusted
type PluginIsTrustedSpecification struct{}

// NewPluginIsTrustedSpecification creates a new plugin is trusted specification
func NewPluginIsTrustedSpecification() *PluginIsTrustedSpecification {
	return &PluginIsTrustedSpecification{}
}

// IsSatisfiedBy checks if the plugin is trusted
func (s *PluginIsTrustedSpecification) IsSatisfiedBy(plugin *entities.Plugin) bool {
	return plugin.Trusted
}

// GetErrorMessage returns the error message
func (s *PluginIsTrustedSpecification) GetErrorMessage() string {
	return "plugin is not trusted"
}

// PluginMeetsResourceRequirementsSpecification checks if a plugin meets resource requirements
type PluginMeetsResourceRequirementsSpecification struct {
	availableMemoryMB int
	availableCPUCores int
	availableDiskMB   int
}

// NewPluginMeetsResourceRequirementsSpecification creates a new resource requirements specification
func NewPluginMeetsResourceRequirementsSpecification(memoryMB, cpuCores, diskMB int) *PluginMeetsResourceRequirementsSpecification {
	return &PluginMeetsResourceRequirementsSpecification{
		availableMemoryMB: memoryMB,
		availableCPUCores: cpuCores,
		availableDiskMB:   diskMB,
	}
}

// IsSatisfiedBy checks if the plugin meets resource requirements
func (s *PluginMeetsResourceRequirementsSpecification) IsSatisfiedBy(plugin *entities.Plugin) bool {
	return plugin.MinMemoryMB <= s.availableMemoryMB &&
		   plugin.CPUCores <= s.availableCPUCores &&
		   plugin.DiskSpaceMB <= s.availableDiskMB
}

// GetErrorMessage returns the error message
func (s *PluginMeetsResourceRequirementsSpecification) GetErrorMessage() string {
	return "plugin resource requirements exceed available resources"
}

// PluginCanBeHotReloadedSpecification checks if a plugin can be hot reloaded
type PluginCanBeHotReloadedSpecification struct{}

// NewPluginCanBeHotReloadedSpecification creates a new plugin can be hot reloaded specification
func NewPluginCanBeHotReloadedSpecification() *PluginCanBeHotReloadedSpecification {
	return &PluginCanBeHotReloadedSpecification{}
}

// IsSatisfiedBy checks if the plugin can be hot reloaded
func (s *PluginCanBeHotReloadedSpecification) IsSatisfiedBy(plugin *entities.Plugin) bool {
	return plugin.SupportsHotReload && 
		   plugin.Lifecycle == valueobjects.PluginLifecycleActive &&
		   plugin.IsEnabled
}

// GetErrorMessage returns the error message
func (s *PluginCanBeHotReloadedSpecification) GetErrorMessage() string {
	return "plugin cannot be hot reloaded (must support hot reload, be active, and enabled)"
}

// PluginCanBeUnloadedSpecification checks if a plugin can be unloaded
type PluginCanBeUnloadedSpecification struct{}

// NewPluginCanBeUnloadedSpecification creates a new plugin can be unloaded specification
func NewPluginCanBeUnloadedSpecification() *PluginCanBeUnloadedSpecification {
	return &PluginCanBeUnloadedSpecification{}
}

// IsSatisfiedBy checks if the plugin can be unloaded
func (s *PluginCanBeUnloadedSpecification) IsSatisfiedBy(plugin *entities.Plugin) bool {
	// Plugin can be unloaded if it's not in unloaded state and not in error state during unloading
	return plugin.Lifecycle != valueobjects.PluginLifecycleUnloaded &&
		   plugin.Lifecycle != valueobjects.PluginLifecycleUnloading
}

// GetErrorMessage returns the error message
func (s *PluginCanBeUnloadedSpecification) GetErrorMessage() string {
	return "plugin cannot be unloaded (already unloaded or currently unloading)"
}

// PluginHasValidConfigurationSpecification checks if a plugin has valid configuration
type PluginHasValidConfigurationSpecification struct{}

// NewPluginHasValidConfigurationSpecification creates a new plugin has valid configuration specification
func NewPluginHasValidConfigurationSpecification() *PluginHasValidConfigurationSpecification {
	return &PluginHasValidConfigurationSpecification{}
}

// IsSatisfiedBy checks if the plugin has valid configuration
func (s *PluginHasValidConfigurationSpecification) IsSatisfiedBy(plugin *entities.Plugin) bool {
	// Basic validation - can be enhanced with schema validation
	if plugin.CurrentConfiguration == nil {
		return len(plugin.ConfigurationSchema) == 0 // No config required
	}
	
	// TODO: Implement schema validation
	return true
}

// GetErrorMessage returns the error message
func (s *PluginHasValidConfigurationSpecification) GetErrorMessage() string {
	return "plugin configuration is invalid"
}

// Plugin Execution Specifications

// ExecutionAndSpecification combines multiple execution specifications with AND logic
type ExecutionAndSpecification struct {
	specs []PluginExecutionSpecification
}

// NewExecutionAndSpecification creates a new execution AND specification
func NewExecutionAndSpecification(specs ...PluginExecutionSpecification) *ExecutionAndSpecification {
	return &ExecutionAndSpecification{specs: specs}
}

// IsSatisfiedBy checks if all execution specifications are satisfied
func (s *ExecutionAndSpecification) IsSatisfiedBy(execution *entities.PluginExecution) bool {
	for _, spec := range s.specs {
		if !spec.IsSatisfiedBy(execution) {
			return false
		}
	}
	return true
}

// GetErrorMessage returns combined error messages
func (s *ExecutionAndSpecification) GetErrorMessage() string {
	var messages []string
	for _, spec := range s.specs {
		messages = append(messages, spec.GetErrorMessage())
	}
	return strings.Join(messages, "; ")
}

// ExecutionCanBeStartedSpecification checks if an execution can be started
type ExecutionCanBeStartedSpecification struct{}

// NewExecutionCanBeStartedSpecification creates a new execution can be started specification
func NewExecutionCanBeStartedSpecification() *ExecutionCanBeStartedSpecification {
	return &ExecutionCanBeStartedSpecification{}
}

// IsSatisfiedBy checks if the execution can be started
func (s *ExecutionCanBeStartedSpecification) IsSatisfiedBy(execution *entities.PluginExecution) bool {
	return execution.Status == entities.ExecutionStatusPending
}

// GetErrorMessage returns the error message
func (s *ExecutionCanBeStartedSpecification) GetErrorMessage() string {
	return "execution cannot be started (must be in pending status)"
}

// ExecutionCanBeCompletedSpecification checks if an execution can be completed
type ExecutionCanBeCompletedSpecification struct{}

// NewExecutionCanBeCompletedSpecification creates a new execution can be completed specification
func NewExecutionCanBeCompletedSpecification() *ExecutionCanBeCompletedSpecification {
	return &ExecutionCanBeCompletedSpecification{}
}

// IsSatisfiedBy checks if the execution can be completed
func (s *ExecutionCanBeCompletedSpecification) IsSatisfiedBy(execution *entities.PluginExecution) bool {
	return execution.Status == entities.ExecutionStatusRunning
}

// GetErrorMessage returns the error message
func (s *ExecutionCanBeCompletedSpecification) GetErrorMessage() string {
	return "execution cannot be completed (must be in running status)"
}

// ExecutionCanBeCancelledSpecification checks if an execution can be cancelled
type ExecutionCanBeCancelledSpecification struct{}

// NewExecutionCanBeCancelledSpecification creates a new execution can be cancelled specification
func NewExecutionCanBeCancelledSpecification() *ExecutionCanBeCancelledSpecification {
	return &ExecutionCanBeCancelledSpecification{}
}

// IsSatisfiedBy checks if the execution can be cancelled
func (s *ExecutionCanBeCancelledSpecification) IsSatisfiedBy(execution *entities.PluginExecution) bool {
	return execution.Status == entities.ExecutionStatusPending ||
		   execution.Status == entities.ExecutionStatusRunning
}

// GetErrorMessage returns the error message
func (s *ExecutionCanBeCancelledSpecification) GetErrorMessage() string {
	return "execution cannot be cancelled (must be pending or running)"
}

// ExecutionCanBeRetriedSpecification checks if an execution can be retried
type ExecutionCanBeRetriedSpecification struct{}

// NewExecutionCanBeRetriedSpecification creates a new execution can be retried specification
func NewExecutionCanBeRetriedSpecification() *ExecutionCanBeRetriedSpecification {
	return &ExecutionCanBeRetriedSpecification{}
}

// IsSatisfiedBy checks if the execution can be retried
func (s *ExecutionCanBeRetriedSpecification) IsSatisfiedBy(execution *entities.PluginExecution) bool {
	return (execution.Status == entities.ExecutionStatusFailed ||
		    execution.Status == entities.ExecutionStatusCancelled ||
		    execution.Status == entities.ExecutionStatusTimeout) &&
		   execution.RetryCount < execution.MaxRetries
}

// GetErrorMessage returns the error message
func (s *ExecutionCanBeRetriedSpecification) GetErrorMessage() string {
	return "execution cannot be retried (must be failed/cancelled/timeout and under retry limit)"
}

// ExecutionIsWithinTimeoutSpecification checks if an execution is within timeout
type ExecutionIsWithinTimeoutSpecification struct{}

// NewExecutionIsWithinTimeoutSpecification creates a new execution is within timeout specification
func NewExecutionIsWithinTimeoutSpecification() *ExecutionIsWithinTimeoutSpecification {
	return &ExecutionIsWithinTimeoutSpecification{}
}

// IsSatisfiedBy checks if the execution is within timeout
func (s *ExecutionIsWithinTimeoutSpecification) IsSatisfiedBy(execution *entities.PluginExecution) bool {
	return !execution.HasTimedOut()
}

// GetErrorMessage returns the error message
func (s *ExecutionIsWithinTimeoutSpecification) GetErrorMessage() string {
	return "execution has exceeded timeout limit"
}

// ExecutionHasValidInputSpecification checks if an execution has valid input
type ExecutionHasValidInputSpecification struct{}

// NewExecutionHasValidInputSpecification creates a new execution has valid input specification
func NewExecutionHasValidInputSpecification() *ExecutionHasValidInputSpecification {
	return &ExecutionHasValidInputSpecification{}
}

// IsSatisfiedBy checks if the execution has valid input
func (s *ExecutionHasValidInputSpecification) IsSatisfiedBy(execution *entities.PluginExecution) bool {
	// Basic validation - can be enhanced with schema validation
	return execution.InputData != nil
}

// GetErrorMessage returns the error message
func (s *ExecutionHasValidInputSpecification) GetErrorMessage() string {
	return "execution input data is invalid"
}

// Business Rule Validators

// ValidatePluginCanExecute validates if a plugin can execute
func ValidatePluginCanExecute(plugin *entities.Plugin) error {
	spec := NewAndSpecification(
		NewPluginIsEnabledSpecification(),
		NewPluginIsActiveSpecification(),
		NewPluginIsHealthySpecification(),
	)
	
	if !spec.IsSatisfiedBy(plugin) {
		return domain.NewBusinessRuleError(spec.GetErrorMessage())
	}
	
	return nil
}

// ValidatePluginCanBeHotReloaded validates if a plugin can be hot reloaded
func ValidatePluginCanBeHotReloaded(plugin *entities.Plugin) error {
	spec := NewPluginCanBeHotReloadedSpecification()
	
	if !spec.IsSatisfiedBy(plugin) {
		return domain.NewBusinessRuleError(spec.GetErrorMessage())
	}
	
	return nil
}

// ValidatePluginResourceRequirements validates plugin resource requirements
func ValidatePluginResourceRequirements(plugin *entities.Plugin, availableMemoryMB, availableCPUCores, availableDiskMB int) error {
	spec := NewPluginMeetsResourceRequirementsSpecification(availableMemoryMB, availableCPUCores, availableDiskMB)
	
	if !spec.IsSatisfiedBy(plugin) {
		return domain.NewResourceError(
			plugin.PluginID.String(),
			"memory/cpu/disk",
			spec.GetErrorMessage(),
		)
	}
	
	return nil
}

// ValidateExecutionCanStart validates if an execution can be started
func ValidateExecutionCanStart(execution *entities.PluginExecution) error {
	spec := NewExecutionAndSpecification(
		NewExecutionCanBeStartedSpecification(),
		NewExecutionHasValidInputSpecification(),
	)
	
	if !spec.IsSatisfiedBy(execution) {
		return domain.NewBusinessRuleError(spec.GetErrorMessage())
	}
	
	return nil
}

// ValidateExecutionCanBeRetried validates if an execution can be retried
func ValidateExecutionCanBeRetried(execution *entities.PluginExecution) error {
	spec := NewExecutionCanBeRetriedSpecification()
	
	if !spec.IsSatisfiedBy(execution) {
		return domain.NewBusinessRuleError(spec.GetErrorMessage())
	}
	
	return nil
}

// ValidateExecutionTimeout validates execution timeout
func ValidateExecutionTimeout(execution *entities.PluginExecution) error {
	spec := NewExecutionIsWithinTimeoutSpecification()
	
	if !spec.IsSatisfiedBy(execution) {
		return domain.NewTimeoutError(
			execution.PluginID.String(),
			"plugin execution",
			time.Duration(execution.TimeoutMs*int64(time.Millisecond)).String(),
		)
	}
	
	return nil
}