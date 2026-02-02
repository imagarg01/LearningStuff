import os
import asyncio
from dotenv import load_dotenv
from copilot import CopilotClient, define_tool
from pydantic import BaseModel, Field

load_dotenv()

# --- 1. Tool Definition ---
class DeleteParams(BaseModel):
    filepath: str = Field(description="Path to file to delete")

@define_tool(description="Simulates deleting a file (safe mode).")
def delete_file(params: DeleteParams) -> str:
    """
    Simulates deleting a file (safe mode).
    """
    return f"SAFE MODE: Would have deleted {params.filepath}"

# --- 2. Hooks ---
# Hooks allow you to intercept and modify behavior at key lifecycle points.
def on_pre_tool_use(input_data, context):
    print(f"\n[Hook] Pre-tool execution: {input_data['toolName']} with args {input_data['toolArgs']}")
    # You can inspect args here. 
    # To deny execution, you would return specific denial objects (depends on SDK version).
    return None

def on_post_tool_use(input_data, context):
    print(f"[Hook] Post-tool execution. Result: {input_data['toolResult']}")
    return None

# --- 3. Permission Handler ---
# Called when the agent needs permission (e.g. to run a shell command or sensitive tool)
async def handle_permission(request, context):
    print(f"\n[Permission] Agent wants to: {request.get('kind')} for tool {request.get('toolCallId')}")
    # Auto-approve for this example. In a real app, you might prompt the user.
    return {"kind": "approved"}

# --- 4. User Input Handler ---
# Called when the agent explicitly asks the user for input via a tool/capability
async def handle_user_input(request, context):
    print(f"\n[Input Required] Copilot asks: {request.get('question')}")
    # Simulate user typing "Yes"
    return {"answer": "Yes, proceed", "wasFreeform": True}

async def main():
    client = CopilotClient()
    
    # Create a dummy file to attach
    with open("context_file.txt", "w") as f:
        f.write("This is a secret project codenamed 'Project Omega'.")

    # Initialize session with all advanced capabilities
    session = await client.create_session({
        "tools": [delete_file],
        "hooks": {
            "on_pre_tool_use": on_pre_tool_use,
            "on_post_tool_use": on_post_tool_use
        },
        "on_permission_request": handle_permission,
        "on_user_input_request": handle_user_input,
    })

    print("--- 1. File Attachment Example ---")
    # Attach the file so Copilot knows about 'Project Omega'
    await session.send_and_wait({
        "prompt": "What is the secret codename based on the attached file?",
        "attachments": [
            {"type": "file", "path": os.path.abspath("context_file.txt")}
        ]
    })
    # We expect Copilot to read the file and answer 'Project Omega'.
    messages = await session.get_messages()
    last_msg = messages[-1]
    content = getattr(last_msg.data, 'content', '')
    if content:
        print(f"Copilot: {content}")
    else:
        print(f"Copilot (No Content): {last_msg.data}")

    print("\n--- 2. Tool Hooks & Permissions Example ---")
    # This should trigger pre/post hooks and potentially permission checks
    await session.send_and_wait({
        "prompt": "Please delete the file 'old_logs.txt'."
    })
    
    # Clean up
    if os.path.exists("context_file.txt"):
        os.remove("context_file.txt")

if __name__ == "__main__":
    asyncio.run(main())
