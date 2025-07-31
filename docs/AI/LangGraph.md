# LangGraph

- LangGraph persists context for long-running workflows.

- LangGraph models agent workflows as directed graphs. There are three main components:

  - **Nodes**: Represent tasks or actions in the workflow.
  - **Edges**: Define the relationships and flow between nodes.
  - **Context**: Stores information that persists across nodes, allowing for stateful workflows.

  In short: nodes do the work, edges tell what to do next.

- LangGraph's underlying graph algorithm used message passing to define a general program. A **super-step** can be considered a single iteration of the algorithm, where each node processes its input and produces output.

  - Nodes that run in parallel are part of same super-step.
  - Nodes that run sequentially are part of different super-steps.

- At the start of graph execution, all nodes begin in an **_inactive_** state. As the graph executes, nodes transition to **_active_**.
  The graph execution terminates when all nodes are **_inactive_** and no message are in transit.

## State

It consists **schema** of the graph as welll as **reducer** functions that define how the state is updated.
The scheme of the State will be the input schema to all Nodes and Edges in the graph can be either a TypedDict or a Pydantic model. All Nodes will emit
updates to the State which are then applied using the specified reducer functions.

- Node can write to any state channel in the graph. The graph state is the union of the state channels defined at initialization.
- Reducers are key to understanding how the state is updated. They are functions that take the current state and the new data emitted by a node, and return the updated state.
