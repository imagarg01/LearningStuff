"""
MCP Example 02: Advanced Tools, Structured Outputs, MRTR & Tasks Extension
==========================================================================
Demonstrates all 2026-07-28 MCP tool and execution capabilities:
1. JSON Schema 2020-12 `inputSchema` and `outputSchema` (`structuredContent`)
2. Tool `annotations` (`readOnlyHint`, `destructiveHint`, `idempotentHint`, `openWorldHint`) & `icons`
3. Self-Correcting Tool Execution Errors (`isError: True`, SEP-1303)
4. Multi Round-Trip Requests (MRTR) (`resultType: "input_required"`, `requestState`, `elicitation/create`)
5. Asynchronous Durable Tasks Extension (`io.modelcontextprotocol/tasks`: `tasks/get`, `tasks/result`, `tasks/cancel`)
"""

import base64
import json
from dataclasses import dataclass, asdict
from datetime import datetime
from typing import Any, Optional


@dataclass
class Tool:
    """MCP 2026-07-28 tool definition with outputSchema, annotations, and icons."""
    name: str
    title: str
    description: str
    inputSchema: dict
    outputSchema: Optional[dict] = None
    annotations: Optional[dict] = None
    icons: Optional[list[dict]] = None


class ToolServer:
    """
    MCP server demonstrating advanced 2026-07-28 tool capabilities:
    - Structured outputs (`outputSchema` + `structuredContent`)
    - Semantic validation errors (`isError: True`) for LLM self-correction
    - Stateless Multi Round-Trip Requests (MRTR) for human-in-the-loop elicitation
    - Durable Tasks extension (`io.modelcontextprotocol/tasks`)
    """

    def __init__(self, instance_id: str = "instance-A"):
        self.name = "enterprise-tool-server"
        self.version = "2.0.0"
        self.instance_id = instance_id
        self.tasks: dict[str, dict] = {}
        self._register_all_tools()

    def _register_all_tools(self):
        self.tools: dict[str, Tool] = {}

        # 1. Tool with outputSchema, structuredContent, annotations, and icons
        self.tools["analyze_text"] = Tool(
            name="analyze_text",
            title="Analyze Text Metrics",
            description="Analyze text and return typed statistics matching outputSchema",
            icons=[{"src": "https://example.com/icons/analytics.svg", "mimeType": "image/svg+xml"}],
            inputSchema={
                "$schema": "https://json-schema.org/draft/2020-12/schema",
                "type": "object",
                "properties": {
                    "text": {"type": "string", "description": "Text to analyze"}
                },
                "required": ["text"]
            },
            outputSchema={
                "$schema": "https://json-schema.org/draft/2020-12/schema",
                "type": "object",
                "properties": {
                    "character_count": {"type": "integer"},
                    "word_count": {"type": "integer"},
                    "line_count": {"type": "integer"},
                    "has_numbers": {"type": "boolean"}
                },
                "required": ["character_count", "word_count", "line_count", "has_numbers"]
            },
            annotations={
                "title": "Analyze Text Metrics",
                "readOnlyHint": True,
                "destructiveHint": False,
                "idempotentHint": True,
                "openWorldHint": False
            }
        )

        # 2. Tool demonstrating SEP-1303 self-correcting validation error (isError: True)
        self.tools["query_orders_by_date"] = Tool(
            name="query_orders_by_date",
            title="Query Orders by ISO Date",
            description="Query orders for a specific ISO date (YYYY-MM-DD)",
            inputSchema={
                "$schema": "https://json-schema.org/draft/2020-12/schema",
                "type": "object",
                "properties": {
                    "date": {"type": "string", "description": "Date in strict YYYY-MM-DD format"}
                },
                "required": ["date"]
            },
            outputSchema={
                "$schema": "https://json-schema.org/draft/2020-12/schema",
                "type": "object",
                "properties": {
                    "date": {"type": "string"},
                    "orders": {"type": "array"}
                },
                "required": ["date", "orders"]
            },
            annotations={
                "readOnlyHint": True,
                "destructiveHint": False,
                "idempotentHint": True,
                "openWorldHint": False
            }
        )

        # 3. High-risk destructive tool requiring MRTR Elicitation (human approval)
        self.tools["delete_production_records"] = Tool(
            name="delete_production_records",
            title="Delete Production Archive",
            description="Permanently delete archived records (Requires human approval via MRTR)",
            inputSchema={
                "$schema": "https://json-schema.org/draft/2020-12/schema",
                "type": "object",
                "properties": {
                    "table": {"type": "string"},
                    "count": {"type": "integer"}
                },
                "required": ["table", "count"]
            },
            annotations={
                "readOnlyHint": False,
                "destructiveHint": True,
                "idempotentHint": True,
                "openWorldHint": False
            }
        )

        # 4. Long-running async operation using Tasks Extension (io.modelcontextprotocol/tasks)
        self.tools["run_batch_migration"] = Tool(
            name="run_batch_migration",
            title="Run Async Database Migration",
            description="Starts a long-running migration job and returns a durable Task handle",
            inputSchema={
                "$schema": "https://json-schema.org/draft/2020-12/schema",
                "type": "object",
                "properties": {
                    "environment": {"type": "string", "enum": ["staging", "production"]}
                },
                "required": ["environment"]
            },
            annotations={
                "readOnlyHint": False,
                "destructiveHint": False,
                "idempotentHint": True,
                "openWorldHint": False
            }
        )

    def list_tools(self) -> dict:
        """Return tools catalog with cacheable ttlMs."""
        cleaned = []
        for tool in self.tools.values():
            d = {k: v for k, v in asdict(tool).items() if v is not None}
            cleaned.append(d)
        return {"tools": cleaned, "ttlMs": 3600000, "cacheScope": "public"}

    def call_tool(self, params: dict) -> dict:
        """Dispatch a tool call supporting structuredContent, SEP-1303 errors, MRTR, and Tasks."""
        name = params.get("name")
        args = params.get("arguments", {})

        if name == "analyze_text":
            return self._handle_analyze_text(args)
        elif name == "query_orders_by_date":
            return self._handle_query_orders(args)
        elif name == "delete_production_records":
            return self._handle_delete_records_mrtr(params)
        elif name == "run_batch_migration":
            return self._handle_start_task(args)
        else:
            return {
                "content": [{"type": "text", "text": f"Unknown tool: {name}"}],
                "isError": True
            }

    # -------------------------------------------------------------------------
    # 1. Structured Output Handler (outputSchema + structuredContent)
    # -------------------------------------------------------------------------
    def _handle_analyze_text(self, args: dict) -> dict:
        text = args["text"]
        structured = {
            "character_count": len(text),
            "word_count": len(text.split()),
            "line_count": len(text.splitlines()) or 1,
            "has_numbers": any(c.isdigit() for c in text),
        }
        return {
            "content": [
                {
                    "type": "text",
                    "text": f"Analyzed {structured['word_count']} words ({structured['character_count']} chars)."
                }
            ],
            "structuredContent": structured,
            "isError": False
        }

    # -------------------------------------------------------------------------
    # 2. SEP-1303 Self-Correcting Validation Error Handler (isError: True)
    # -------------------------------------------------------------------------
    def _handle_query_orders(self, args: dict) -> dict:
        date_str = args.get("date", "")
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            # SEP-1303: Return a tool execution error (isError: True) with semantic guidance
            # instead of raising a JSON-RPC protocol exception so the LLM can self-correct!
            return {
                "content": [
                    {
                        "type": "text",
                        "text": (
                            f"Validation Error: Invalid date '{date_str}'. "
                            "Expected strict ISO-8601 format 'YYYY-MM-DD' (e.g., '2026-10-31'). "
                            "Please re-invoke query_orders_by_date with a formatted date."
                        )
                    }
                ],
                "isError": True
            }

        orders = [
            {"orderId": "ord_501", "amount": 129.99, "status": "shipped"},
            {"orderId": "ord_502", "amount": 49.50, "status": "delivered"},
        ]
        return {
            "content": [{"type": "text", "text": f"Found {len(orders)} orders for {date_str}."}],
            "structuredContent": {"date": date_str, "orders": orders},
            "isError": False
        }

    # -------------------------------------------------------------------------
    # 3. Multi Round-Trip Request (MRTR) Handler (input_required + requestState)
    # -------------------------------------------------------------------------
    def _handle_delete_records_mrtr(self, params: dict) -> dict:
        args = params.get("arguments", {})

        # Round-Trip 1: No user inputResponses yet -> return input_required + opaque requestState
        if "inputResponses" not in params:
            state_payload = json.dumps({
                "table": args["table"],
                "count": args["count"],
                "origin_instance": self.instance_id
            })
            request_state_token = base64.urlsafe_b64encode(state_payload.encode()).decode()

            return {
                "resultType": "input_required",
                "requestState": request_state_token,
                "inputRequests": {
                    "confirm_deletion": {
                        "method": "elicitation/create",
                        "params": {
                            "mode": "form",
                            "message": (
                                f"Are you sure you want to permanently delete {args['count']} "
                                f"records from '{args['table']}'?"
                            ),
                            "requestedSchema": {
                                "type": "object",
                                "properties": {
                                    "approved": {"type": "boolean", "description": "Confirm deletion"}
                                },
                                "required": ["approved"]
                            }
                        }
                    }
                }
            }

        # Round-Trip 2: Client retried with echoed requestState and inputResponses
        # Note: Even a completely different stateless server instance (Instance B) can decode requestState!
        decoded_state = json.loads(base64.urlsafe_b64decode(params["requestState"].encode()).decode())
        approval = (
            params["inputResponses"]
            .get("confirm_deletion", {})
            .get("content", {})
            .get("approved", False)
        )

        if not approval:
            return {
                "content": [{"type": "text", "text": "Deletion aborted by user."}],
                "isError": False
            }

        return {
            "content": [
                {
                    "type": "text",
                    "text": (
                        f"[Executed on {self.instance_id}; state initiated on {decoded_state['origin_instance']}] "
                        f"Successfully deleted {decoded_state['count']} records from '{decoded_state['table']}'."
                    )
                }
            ],
            "isError": False
        }

    # -------------------------------------------------------------------------
    # 4. Tasks Extension Handler (io.modelcontextprotocol/tasks)
    # -------------------------------------------------------------------------
    def _handle_start_task(self, args: dict) -> dict:
        task_id = "task_mig_2026"
        self.tasks[task_id] = {
            "taskId": task_id,
            "status": "working",
            "environment": args["environment"],
            "ttlMs": 3600000,
            "pollIntervalMs": 1000
        }
        return {
            "resultType": "task",
            "task": {
                "taskId": task_id,
                "status": "working",
                "ttlMs": 3600000,
                "pollIntervalMs": 1000
            }
        }

    def get_task_status(self, task_id: str) -> dict:
        """Simulate tasks/get polling transition from working -> completed."""
        task = self.tasks[task_id]
        task["status"] = "completed"
        return {
            "taskId": task_id,
            "status": task["status"],
            "result": {
                "content": [
                    {
                        "type": "text",
                        "text": f"Migration in '{task['environment']}' completed: 14 tables updated."
                    }
                ],
                "isError": False
            }
        }


# =============================================================================
# Demo
# =============================================================================

def run_demo():
    """Demonstrate all 2026-07-28 tool capabilities."""
    instance_a = ToolServer(instance_id="server-instance-A")
    instance_b = ToolServer(instance_id="server-instance-B")

    print("=" * 70)
    print("MCP Example 02: Structured Outputs, SEP-1303, MRTR & Tasks Extension")
    print("=" * 70)

    # 1. Structured Output (outputSchema + structuredContent)
    print("\n1️⃣  Structured Tool Output (outputSchema + structuredContent)")
    print("-" * 60)
    res = instance_a.call_tool({
        "name": "analyze_text",
        "arguments": {"text": "MCP 2026-07-28 supports JSON Schema 2020-12!"}
    })
    print(json.dumps(res, indent=2))

    # 2. SEP-1303 Failing Forward & LLM Self-Correction Loop
    print("\n2️⃣  SEP-1303 Self-Correcting Validation Error (isError: True)")
    print("-" * 60)
    bad_res = instance_a.call_tool({
        "name": "query_orders_by_date",
        "arguments": {"date": "10/31/2026"}  # Wrong format
    })
    print("❌ First Attempt (Invalid Format -> Returns isError: True):")
    print(json.dumps(bad_res, indent=2))

    fixed_res = instance_a.call_tool({
        "name": "query_orders_by_date",
        "arguments": {"date": "2026-10-31"}  # LLM self-corrects to ISO format
    })
    print("\n✅ Second Attempt (LLM Self-Corrected to YYYY-MM-DD):")
    print(json.dumps(fixed_res, indent=2))

    # 3. Stateless Multi Round-Trip Request (MRTR) across Load-Balanced Instances
    print("\n3️⃣  Multi Round-Trip Request (MRTR) Across Load-Balanced Instances")
    print("-" * 60)
    mrtr_step1 = instance_a.call_tool({
        "name": "delete_production_records",
        "arguments": {"table": "user_logs_archived", "count": 1420}
    })
    print("⏸️  Round-Trip 1 (Instance A responds with input_required + requestState):")
    print(json.dumps(mrtr_step1, indent=2))

    print("\n▶️  Round-Trip 2 (Client retries with inputResponses -> Routed to Instance B!):")
    mrtr_step2 = instance_b.call_tool({
        "name": "delete_production_records",
        "arguments": {"table": "user_logs_archived", "count": 1420},
        "requestState": mrtr_step1["requestState"],
        "inputResponses": {
            "confirm_deletion": {
                "action": "accept",
                "content": {"approved": True}
            }
        }
    })
    print(json.dumps(mrtr_step2, indent=2))

    # 4. Tasks Extension (io.modelcontextprotocol/tasks)
    print("\n4️⃣  Asynchronous Tasks Extension (io.modelcontextprotocol/tasks)")
    print("-" * 60)
    task_start = instance_a.call_tool({
        "name": "run_batch_migration",
        "arguments": {"environment": "staging"}
    })
    print("⏳ Initial Tool Call Returns Task Handle immediately:")
    print(json.dumps(task_start, indent=2))

    task_id = task_start["task"]["taskId"]
    task_done = instance_a.get_task_status(task_id)
    print("\n📊 Polling via tasks/get Returns Completed Result:")
    print(json.dumps(task_done, indent=2))

    print("\n" + "=" * 70)
    print("✅ Advanced Tool Server demo complete!")


if __name__ == "__main__":
    run_demo()
