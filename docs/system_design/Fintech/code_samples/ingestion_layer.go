package main

import (
	"fmt"
	"log"
	"time"
)

// EventType defines the type of event entering the system
type EventType string

const (
	TransactionInitiated EventType = "TransactionInitiated"
	ChatQueryReceived    EventType = "ChatQueryReceived"
)

// Event represents a standardized event structure (Avro/Protobuf schema compliant)
type Event struct {
	ID        string
	UserID    string
	Type      EventType
	Payload   map[string]interface{}
	Timestamp time.Time
}

// IngestionLayer simulates the API Gateway / BFF
type IngestionLayer struct {
	EventBus chan Event // Simulates Kafka Topic
}

func NewIngestionLayer(bus chan Event) *IngestionLayer {
	return &IngestionLayer{EventBus: bus}
}

// HandleRequest simulates receiving a fast HTTP/WebSocket request
// It validates and immediately transforms the request into an Event
func (i *IngestionLayer) HandleRequest(userID string, reqType EventType, data map[string]interface{}) {
	// 1. Validation (Fast)
	if userID == "" {
		log.Println("Error: Invalid UserID")
		return
	}

	// 2. Transformation (Request -> Event)
	event := Event{
		ID:        fmt.Sprintf("evt-%d", time.Now().UnixNano()),
		UserID:    userID,
		Type:      reqType,
		Payload:   data,
		Timestamp: time.Now(),
	}

	// 3. Emit to Event Bus (Async)
	// In a real system, this pushes to a Kafka Producer
	go func() {
		i.EventBus <- event
		fmt.Printf("[Ingestion] Emitted event %s for user %s\n", event.ID, event.UserID)
	}()
}

func main() {
	// Mock Event Bus (Kafka)
	kafkaTopic := make(chan Event, 100)

	gateway := NewIngestionLayer(kafkaTopic)

	// Simulate 100k RPS (scaled down for demo)
	for j := 0; j < 5; j++ {
		gateway.HandleRequest("user_123", TransactionInitiated, map[string]interface{}{"amount": 500.00})
		gateway.HandleRequest("user_123", ChatQueryReceived, map[string]interface{}{"query": "Can I afford this?"})
		time.Sleep(10 * time.Millisecond)
	}

	// Verify events in bus
	go func() {
		for msg := range kafkaTopic {
			fmt.Printf("[Kafka] Received: %v\n", msg)
		}
	}()

	time.Sleep(1 * time.Second)
}
