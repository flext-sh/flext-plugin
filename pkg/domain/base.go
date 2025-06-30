package domain

import (
	"time"

	"github.com/flext-sh/flext-core/pkg/domain"
	"github.com/google/uuid"
)

// PluginBaseModel provides common fields and behavior for all plugin domain objects
type PluginBaseModel struct {
	domain.DomainBaseModel
}

// PluginEntity represents an identifiable plugin domain entity
type PluginEntity struct {
	domain.DomainEntity
}

// PluginAggregateRoot represents a plugin aggregate root with domain events
type PluginAggregateRoot struct {
	domain.DomainAggregateRoot
}

// PluginID represents a unique plugin identifier
type PluginID uuid.UUID

// NewPluginID creates a new plugin ID
func NewPluginID() PluginID {
	return PluginID(uuid.New())
}

// ParsePluginID parses a string into a PluginID
func ParsePluginID(s string) (PluginID, error) {
	id, err := uuid.Parse(s)
	if err != nil {
		return PluginID{}, NewInvalidInputError("plugin_id", s, "invalid UUID format")
	}
	return PluginID(id), nil
}

// String returns the string representation of the plugin ID
func (id PluginID) String() string {
	return uuid.UUID(id).String()
}

// IsZero returns true if the ID is the zero UUID
func (id PluginID) IsZero() bool {
	return uuid.UUID(id) == uuid.Nil
}

// ExecutionID represents a unique plugin execution identifier
type ExecutionID uuid.UUID

// NewExecutionID creates a new execution ID
func NewExecutionID() ExecutionID {
	return ExecutionID(uuid.New())
}

// ParseExecutionID parses a string into an ExecutionID
func ParseExecutionID(s string) (ExecutionID, error) {
	id, err := uuid.Parse(s)
	if err != nil {
		return ExecutionID{}, NewInvalidInputError("execution_id", s, "invalid UUID format")
	}
	return ExecutionID(id), nil
}

// String returns the string representation of the execution ID
func (id ExecutionID) String() string {
	return uuid.UUID(id).String()
}

// IsZero returns true if the ID is the zero UUID
func (id ExecutionID) IsZero() bool {
	return uuid.UUID(id) == uuid.Nil
}

// DomainEvent represents a plugin domain event
type PluginDomainEvent struct {
	domain.DomainEvent
	PluginID    PluginID  `json:"plugin_id"`
	ExecutionID *ExecutionID `json:"execution_id,omitempty"`
}

// NewPluginDomainEvent creates a new plugin domain event
func NewPluginDomainEvent(eventType string, pluginID PluginID, data map[string]interface{}) *PluginDomainEvent {
	baseEvent := domain.NewDomainEvent(domain.EntityID(pluginID), eventType, data)
	return &PluginDomainEvent{
		DomainEvent: baseEvent,
		PluginID:    pluginID,
	}
}

// NewPluginExecutionEvent creates a new plugin execution domain event
func NewPluginExecutionEvent(eventType string, pluginID PluginID, executionID ExecutionID, data map[string]interface{}) *PluginDomainEvent {
	baseEvent := domain.NewDomainEvent(domain.EntityID(pluginID), eventType, data)
	return &PluginDomainEvent{
		DomainEvent: baseEvent,
		PluginID:    pluginID,
		ExecutionID: &executionID,
	}
}

// PluginTimestamps provides standard timestamps for plugin entities
type PluginTimestamps struct {
	CreatedAt   time.Time  `json:"created_at"`
	UpdatedAt   *time.Time `json:"updated_at,omitempty"`
	LoadedAt    *time.Time `json:"loaded_at,omitempty"`
	UnloadedAt  *time.Time `json:"unloaded_at,omitempty"`
	LastUsedAt  *time.Time `json:"last_used_at,omitempty"`
}

// NewPluginTimestamps creates new plugin timestamps with created_at set to now
func NewPluginTimestamps() PluginTimestamps {
	now := time.Now()
	return PluginTimestamps{
		CreatedAt: now,
	}
}

// MarkUpdated sets the updated_at timestamp to now
func (t *PluginTimestamps) MarkUpdated() {
	now := time.Now()
	t.UpdatedAt = &now
}

// MarkLoaded sets the loaded_at timestamp to now
func (t *PluginTimestamps) MarkLoaded() {
	now := time.Now()
	t.LoadedAt = &now
}

// MarkUnloaded sets the unloaded_at timestamp to now
func (t *PluginTimestamps) MarkUnloaded() {
	now := time.Now()
	t.UnloadedAt = &now
}

// MarkUsed sets the last_used_at timestamp to now
func (t *PluginTimestamps) MarkUsed() {
	now := time.Now()
	t.LastUsedAt = &now
}