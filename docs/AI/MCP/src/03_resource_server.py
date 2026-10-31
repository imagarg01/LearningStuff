"""
MCP Example 03: Resource Server, URI Templates & Cacheable Catalogs
===================================================================
Demonstrates MCP resource capabilities (2026-07-28):
1. Static resources (`resources/list`) with `ttlMs` and `cacheScope`
2. Dynamic RFC 6570 Resource Templates (`resources/templates/list`)
3. Reading text & binary (`blob`) resources (`resources/read`)
4. Lightweight `resource_link` references returned from tools
"""

import json
from dataclasses import dataclass, asdict
from typing import Optional


@dataclass
class Resource:
    """An MCP static resource definition."""
    uri: str
    name: str
    title: str
    mimeType: str
    description: Optional[str] = None


@dataclass
class ResourceTemplate:
    """An MCP RFC 6570 dynamic URI template definition."""
    uriTemplate: str
    name: str
    title: str
    mimeType: str
    description: Optional[str] = None


@dataclass
class ResourceContents:
    """Resource content response."""
    uri: str
    mimeType: str
    text: Optional[str] = None
    blob: Optional[str] = None  # Base64 for binary


class ResourceServer:
    """
    MCP server focused on static resources, RFC 6570 URI templates, and ttlMs caching.
    """

    def __init__(self):
        self.name = "resource-demo-server"
        self.version = "2.0.0"

        self._config = {
            "app": {
                "name": "Demo Enterprise App",
                "version": "2.0.0",
                "stateless": True,
                "features": ["oauth2.1", "mrtr", "skills-sep-2640", "otel-sep-414"]
            }
        }

        self._users = {
            "1": {"id": "1", "username": "alice", "role": "admin", "department": "engineering"},
            "2": {"id": "2", "username": "bob", "role": "analyst", "department": "finance"},
        }

    def list_resources(self) -> dict:
        """Return static resources with 2026-07-28 ttlMs caching metadata."""
        resources = [
            Resource(
                uri="config://app",
                name="app_config",
                title="Application Configuration",
                mimeType="application/json",
                description="Main stateless application configuration"
            ),
            Resource(
                uri="api://status",
                name="system_status",
                title="Live System Health",
                mimeType="application/json",
                description="Current cluster health status"
            ),
        ]
        return {
            "resources": [asdict(r) for r in resources],
            "ttlMs": 600000,
            "cacheScope": "public"
        }

    def list_resource_templates(self) -> dict:
        """Return RFC 6570 parameterized URI templates (resources/templates/list)."""
        templates = [
            ResourceTemplate(
                uriTemplate="db://users/{userId}/profile",
                name="user_profile_by_id",
                title="User Profile by ID",
                mimeType="application/json",
                description="Fetch a specific user's profile record by userId"
            )
        ]
        return {
            "resourceTemplates": [asdict(t) for t in templates],
            "ttlMs": 3600000,
            "cacheScope": "public"
        }

    def read_resource(self, uri: str) -> dict:
        """Read a static or template-resolved resource URI."""
        if uri == "config://app":
            return asdict(ResourceContents(
                uri=uri,
                mimeType="application/json",
                text=json.dumps(self._config["app"], indent=2)
            ))
        elif uri == "api://status":
            return asdict(ResourceContents(
                uri=uri,
                mimeType="application/json",
                text=json.dumps({"status": "healthy", "protocolVersion": "2026-07-28"}, indent=2)
            ))
        elif uri.startswith("db://users/") and uri.endswith("/profile"):
            user_id = uri.split("/")[3]
            user = self._users.get(user_id)
            if not user:
                raise ValueError(f"User not found: {user_id}")
            return asdict(ResourceContents(
                uri=uri,
                mimeType="application/json",
                text=json.dumps(user, indent=2)
            ))
        else:
            raise ValueError(f"Unknown resource URI: {uri}")

    def create_resource_link_result(self, user_id: str) -> dict:
        """Demonstrate returning a lightweight `resource_link` from a tool call."""
        user = self._users.get(user_id)
        return {
            "content": [
                {
                    "type": "text",
                    "text": f"Found user '{user['username']}'. Read the linked resource for full profile."
                },
                {
                    "type": "resource_link",
                    "uri": f"db://users/{user_id}/profile",
                    "name": f"Profile: {user['username']}",
                    "mimeType": "application/json"
                }
            ],
            "isError": False
        }


def run_demo():
    """Demonstrate the 2026-07-28 resource server."""
    server = ResourceServer()

    print("=" * 70)
    print("MCP Example 03: Resources, URI Templates & Resource Links (2026-07-28)")
    print("=" * 70)

    # 1. List static resources (with ttlMs)
    print("\n📚 1. Request: resources/list (with ttlMs caching)")
    print("-" * 55)
    print(json.dumps(server.list_resources(), indent=2))

    # 2. List RFC 6570 resource templates
    print("\n🧩 2. Request: resources/templates/list (RFC 6570 URI Templates)")
    print("-" * 55)
    print(json.dumps(server.list_resource_templates(), indent=2))

    # 3. Read a parameterized URI template instance
    print("\n📖 3. Request: resources/read (db://users/1/profile)")
    print("-" * 55)
    print(json.dumps(server.read_resource("db://users/1/profile"), indent=2))

    # 4. Demonstrate resource_link content type
    print("\n🔗 4. Tool Result with `resource_link` Pointer")
    print("-" * 55)
    print(json.dumps(server.create_resource_link_result("2"), indent=2))

    print("\n" + "=" * 70)
    print("✅ Resource demo complete!")


if __name__ == "__main__":
    run_demo()
