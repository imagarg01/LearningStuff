package main

import (
	"fmt"
	"time"
)

// SagaStep represents one microservice action in the transaction
type SagaStep struct {
	Name        string
	Action      func() error
	Compensate  func()
}

// SagaOrchestrator manages the distributed transaction
type SagaOrchestrator struct {
	steps []SagaStep
}

func (s *SagaOrchestrator) AddStep(step SagaStep) {
	s.steps = append(s.steps, step)
}

func (s *SagaOrchestrator) Execute() error {
	completedSteps := []SagaStep{}

	for _, step := range s.steps {
		fmt.Printf("[Saga] Executing: %s\n", step.Name)
		err := step.Action()
		
		if err != nil {
			fmt.Printf("[Saga] Error in %s! Starting Rollback...\n", step.Name)
			s.Rollback(completedSteps)
			return err
		}
		
		completedSteps = append(completedSteps, step)
	}
	
	fmt.Println("[Saga] Transaction Completed Successfully via Events!")
	return nil
}

func (s *SagaOrchestrator) Rollback(steps []SagaStep) {
	// Rollback in reverse order
	for i := len(steps) - 1; i >= 0; i-- {
		step := steps[i]
		fmt.Printf("[Saga] Compensating: %s\n", step.Name)
		step.Compensate()
	}
}

func main() {
	orchestrator := SagaOrchestrator{}

	// Step 1: Deduct Money (Ledger Service)
	orchestrator.AddStep(SagaStep{
		Name: "Deduct Funds",
		Action: func() error {
			fmt.Println(" -> Funds Deducted")
			return nil
		},
		Compensate: func() {
			fmt.Println(" -> Funds Refunded")
		},
	})

	// Step 2: Credit External Account (Payment Gateway)
	orchestrator.AddStep(SagaStep{
		Name: "Credit External Account",
		Action: func() error {
			// Simulate Failure
			fmt.Println(" -> Connection Timeout to Bank!")
			return fmt.Errorf("timeout")
		},
		Compensate: func() {
			fmt.Println(" -> (No Action Needed)")
		},
	})

	// Execute Transaction
	orchestrator.Execute()
}
