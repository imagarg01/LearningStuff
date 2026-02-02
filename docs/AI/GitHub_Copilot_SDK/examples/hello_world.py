import os
import asyncio
from dotenv import load_dotenv
from copilot import CopilotClient

# Load environment variables (GITHUB_TOKEN)
load_dotenv()

async def main():
    # Initialize the client
    # Expects GITHUB_TOKEN in env or can be passed explicitly
    client = CopilotClient({"log_level": "debug"})

    # Create a session
    try:
        session = await client.create_session()
    except RuntimeError as e:
        if "protocol version mismatch" in str(e):
            print(f"\n[!] Error: {e}")
            print("\n[i] Tip: The default 'copilot' binary might be outdated or incompatible.")
            print("    Try installing the standalone CLI via npm:")
            print("      npm install -g @githubnext/github-copilot-cli")
            print("    Then run with the explicit path:")
            print("      COPILOT_CLI_PATH=$(which github-copilot-cli) python hello_world.py")
            return
        elif "Client not connected" in str(e):
             print(f"\n[!] Connection Error: {e}")
             return
        else:
            raise e
    except TimeoutError as e:
        print(f"\n[!] Connection Timed Out: {e}")
        print("[i] Troubleshooting steps:")
        print("    1. Authentication is likely missing for the standalone CLI.")
        print("    2. Run this command to authenticate: 'github-copilot-cli auth'")
        print("    3. Then try running the script again.")
        return

    response_event = await session.send_and_wait({"prompt": "Hello, who are you?"})

    # Print the response
    if response_event and response_event.data and hasattr(response_event.data, 'content'):
        print(f"Copilot: {response_event.data.content}")
    else:
        print("Copilot: [No text response received]")

if __name__ == "__main__":
    asyncio.run(main())
