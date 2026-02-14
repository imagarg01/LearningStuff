package main

import (
	"fmt"
	"time"
)

// Mock Event Structure
type Event struct {
	UserID    string
	Type      string
	Amount    float64
	Timestamp time.Time
}

// StreamProcessor simulates Apache Flink or Kafka Streams
type StreamProcessor struct {
	WindowSize time.Duration
	StateStore map[string]float64 // Simulates internal Flink state
}

func NewStreamProcessor(window time.Duration) *StreamProcessor {
	return &StreamProcessor{
		WindowSize: window,
		StateStore: make(map[string]float64),
	}
}

// ProcessStream reads from the input channel and aggregates data
func (sp *StreamProcessor) ProcessStream(input <-chan Event, output chan<- string) {
	for event := range input {
		if event.Type == "Transaction" {
			// 1. Update State (Sliding Window Aggregation)
			// In real Flink, this handles out-of-order events and watermarks
			sp.StateStore[event.UserID] += event.Amount

			// 2. Emit Updated Metric to Read-Model
			// This would write to Redis/ScyllaDB
			updateMsg := fmt.Sprintf("User %s Total Spend: $%.2f", event.UserID, sp.StateStore[event.UserID])
			output <- updateMsg
		}
	}
}

func main() {
	// Channels simulating Kafka topics
	inputTopic := make(chan Event)
	readModelUpdateTopic := make(chan string)

	processor := NewStreamProcessor(30 * time.Hour) // Monthly spend window

	// Start Processor
	go processor.ProcessStream(inputTopic, readModelUpdateTopic)

	// Simulate incoming stream
	go func() {
		events := []Event{
			{"user_1", "Transaction", 50.00, time.Now()},
			{"user_1", "Transaction", 20.00, time.Now()},
			{"user_2", "Transaction", 100.00, time.Now()},
			{"user_1", "Transaction", 30.00, time.Now()},
		}
		for _, e := range events {
			inputTopic <- e
			time.Sleep(100 * time.Millisecond)
		}
		close(inputTopic)
	}()

	// Consume updates (Simulating Redis writer)
	for update := range readModelUpdateTopic {
		fmt.Println("[Read-Model Update]", update)
	}
}
