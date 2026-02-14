package main

import (
	"fmt"
	"sync"
	"time"
)

// --- Database Layers ---

// WriteDB simulates PostgreSQL (Transactional, Slower)
type WriteDB struct {
	data map[string]float64
	mu   sync.Mutex
}

func (db *WriteDB) UpdateBalance(userID string, amount float64) {
	db.mu.Lock()
	defer db.mu.Unlock()
	time.Sleep(50 * time.Millisecond) // Simulate DB latency
	db.data[userID] += amount
	fmt.Printf("[WriteDB] Updated %s (Slow)\n", userID)
}

// ReadCache simulates Redis (Read-Model, Fast)
type ReadCache struct {
	data map[string]float64
	mu   sync.RWMutex
}

func (rc *ReadCache) Set(userID string, balance float64) {
	rc.mu.Lock()
	defer rc.mu.Unlock()
	rc.data[userID] = balance
	fmt.Printf("[ReadCache] Updated %s (Fast)\n", userID)
}

func (rc *ReadCache) Get(userID string) float64 {
	rc.mu.RLock()
	defer rc.mu.RUnlock()
	return rc.data[userID]
}

// --- CQRS Handler ---

// EventHandler consumes events from Kafka and updates the Read Model
func EventHandler(eventChannel <-chan string, writeDB *WriteDB, readCache *ReadCache) {
	for userID := range eventChannel {
		// In a real system, the event contains the data.
		// Here we simulate fetching the latest state from WriteDB or the event payload
		// and updating the cache.
		
		// For CQRS, the event usually carries the change. 
		// Let's assume the event triggers a "Materialized View" refresh
		
		// 1. Ideally, payload has the new state. 
		// If not, we might check WriteDB (but that adds load).
		// Best Practice: Event carries the delta or new state.
		
		newBalance := 100.00 // simplified
		readCache.Set(userID, newBalance)
	}
}

func main() {
	writeDB := &WriteDB{data: make(map[string]float64)}
	readCache := &ReadCache{data: make(map[string]float64)}
	eventBus := make(chan string)

	// Start Async Event Consumer (CQRS Updater)
	go EventHandler(eventBus, writeDB, readCache)

	// Simulation: User Transaction
	userID := "u1"
	
	// Command Side: Write to DB + Emit Event
	fmt.Println("--- Transaction Started ---")
	writeDB.UpdateBalance(userID, 100.0)
	eventBus <- userID // Emit event
	
	time.Sleep(100 * time.Millisecond) // Wait for async propagation

	// Query Side: Client reads from Cache
	balance := readCache.Get(userID)
	fmt.Printf("--- Client Query ---\nUser Balance: $%.2f (from Cache)\n", balance)
}
