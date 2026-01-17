"""
MCP Example 03: Resource Server
===============================
An MCP server providing resources (data that AI can read).

This example demonstrates:
1. File-based resources
2. Dynamic resources (database simulation)
3. Resource subscriptions
4. Multiple MIME types
"""

import json
import os
from dataclasses import dataclass, asdict
from typing import Optional
from pathlib import Path


@dataclass
class Resource:
    """An MCP resource definition."""
    uri: str
    name: str
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
    MCP server focused on resource management.
    
    Resource types:
    - file:// - Local files
    - config:// - Configuration data
    - db:// - Database queries
    - api:// - API responses
    """
    
    def __init__(self):
        self.name = "resource-demo-server"
        self.version = "1.0.0"
        self.subscriptions: set[str] = set()
        
        # Simulated data stores
        self._config = {
            "app": {
                "name": "Demo Application",
                "version": "2.0.0",
                "debug": False,
                "features": ["auth", "analytics", "export"]
            },
            "database": {
                "host": "localhost",
                "port": 5432,
                "name": "demo_db"
            }
        }
        
        self._database = {
            "users": [
                {"id": 1, "username": "alice", "role": "admin", "active": True},
                {"id": 2, "username": "bob", "role": "user", "active": True},
                {"id": 3, "username": "charlie", "role": "user", "active": False},
            ],
            "settings": [
                {"key": "theme", "value": "dark"},
                {"key": "language", "value": "en"},
                {"key": "notifications", "value": "true"},
            ]
        }
    
    def list_resources(self) -> list[dict]:
        """Return all available resources."""
        resources = [
            # Configuration resources
            Resource(
                uri="config://app",
                name="Application Config",
                mimeType="application/json",
                description="Main application configuration"
            ),
            Resource(
                uri="config://database",
                name="Database Config",
                mimeType="application/json",
                description="Database connection settings"
            ),
            
            # Database resources
            Resource(
                uri="db://users",
                name="Users Table",
                mimeType="application/json",
                description="All user records"
            ),
            Resource(
                uri="db://users/active",
                name="Active Users",
                mimeType="application/json",
                description="Only active user records"
            ),
            Resource(
                uri="db://settings",
                name="Settings",
                mimeType="application/json",
                description="Application settings"
            ),
            
            # API resources (simulated)
            Resource(
                uri="api://status",
                name="System Status",
                mimeType="application/json",
                description="Current system status"
            ),
            
            # Template resources
            Resource(
                uri="template://email/welcome",
                name="Welcome Email",
                mimeType="text/html",
                description="Welcome email template"
            ),
            Resource(
                uri="template://report/summary",
                name="Summary Report",
                mimeType="text/markdown",
                description="Summary report template"
            ),
        ]
        
        return [asdict(r) for r in resources]
    
    def read_resource(self, uri: str) -> dict:
        """Read a resource and return its contents."""
        
        if uri.startswith("config://"):
            return self._read_config(uri)
        elif uri.startswith("db://"):
            return self._read_database(uri)
        elif uri.startswith("api://"):
            return self._read_api(uri)
        elif uri.startswith("template://"):
            return self._read_template(uri)
        else:
            raise ValueError(f"Unknown resource URI: {uri}")
    
    def subscribe(self, uri: str) -> dict:
        """Subscribe to resource changes."""
        self.subscriptions.add(uri)
        return {"subscribed": True, "uri": uri}
    
    def unsubscribe(self, uri: str) -> dict:
        """Unsubscribe from resource changes."""
        self.subscriptions.discard(uri)
        return {"subscribed": False, "uri": uri}
    
    # Resource handlers
    
    def _read_config(self, uri: str) -> dict:
        """Read configuration resource."""
        key = uri.replace("config://", "")
        
        if key not in self._config:
            raise ValueError(f"Config not found: {key}")
        
        return asdict(ResourceContents(
            uri=uri,
            mimeType="application/json",
            text=json.dumps(self._config[key], indent=2)
        ))
    
    def _read_database(self, uri: str) -> dict:
        """Read database resource."""
        path = uri.replace("db://", "")
        parts = path.split("/")
        table = parts[0]
        
        if table not in self._database:
            raise ValueError(f"Table not found: {table}")
        
        data = self._database[table]
        
        # Apply filters
        if len(parts) > 1:
            filter_key = parts[1]
            if filter_key == "active":
                data = [r for r in data if r.get("active", True)]
        
        return asdict(ResourceContents(
            uri=uri,
            mimeType="application/json",
            text=json.dumps(data, indent=2)
        ))
    
    def _read_api(self, uri: str) -> dict:
        """Read API resource (simulated)."""
        endpoint = uri.replace("api://", "")
        
        if endpoint == "status":
            data = {
                "status": "healthy",
                "uptime_seconds": 86400,
                "version": "2.0.0",
                "services": {
                    "database": "connected",
                    "cache": "connected",
                    "queue": "connected"
                }
            }
        else:
            raise ValueError(f"Unknown API endpoint: {endpoint}")
        
        return asdict(ResourceContents(
            uri=uri,
            mimeType="application/json",
            text=json.dumps(data, indent=2)
        ))
    
    def _read_template(self, uri: str) -> dict:
        """Read template resource."""
        path = uri.replace("template://", "")
        
        templates = {
            "email/welcome": {
                "mimeType": "text/html",
                "content": """<!DOCTYPE html>
<html>
<head><title>Welcome!</title></head>
<body>
    <h1>Welcome to Our Platform!</h1>
    <p>Hello {{username}},</p>
    <p>Thank you for joining us.</p>
</body>
</html>"""
            },
            "report/summary": {
                "mimeType": "text/markdown",
                "content": """# Summary Report

## Overview
Generated on: {{date}}

## Metrics
- Total Users: {{user_count}}
- Active Sessions: {{session_count}}

## Recommendations
1. Review inactive accounts
2. Optimize database queries
"""
            }
        }
        
        if path not in templates:
            raise ValueError(f"Template not found: {path}")
        
        template = templates[path]
        return asdict(ResourceContents(
            uri=uri,
            mimeType=template["mimeType"],
            text=template["content"]
        ))


# =============================================================================
# Demo
# =============================================================================

def run_demo():
    """Demonstrate the resource server."""
    
    server = ResourceServer()
    
    print("=" * 70)
    print("MCP Resource Server Demo")
    print("=" * 70)
    
    # List all resources
    print("\n📚 Available Resources:")
    print("-" * 50)
    for resource in server.list_resources():
        print(f"  [{resource['mimeType']:20}] {resource['uri']}")
        print(f"                         └─ {resource.get('description', '')}")
    
    # Read resources
    print("\n" + "=" * 70)
    print("📖 Reading Resources")
    print("=" * 70)
    
    # 1. Config
    print("\n[config://app]")
    result = server.read_resource("config://app")
    print(result["text"])
    
    # 2. Database - all users
    print("\n[db://users]")
    result = server.read_resource("db://users")
    print(result["text"])
    
    # 3. Database - active users only
    print("\n[db://users/active]")
    result = server.read_resource("db://users/active")
    print(result["text"])
    
    # 4. API status
    print("\n[api://status]")
    result = server.read_resource("api://status")
    print(result["text"])
    
    # 5. Template
    print("\n[template://report/summary]")
    result = server.read_resource("template://report/summary")
    print(result["text"])
    
    # Subscriptions
    print("\n" + "=" * 70)
    print("🔔 Resource Subscriptions")
    print("=" * 70)
    
    print("\nSubscribing to config://app...")
    result = server.subscribe("config://app")
    print(f"  → {result}")
    
    print(f"\nActive subscriptions: {server.subscriptions}")
    
    print("\n" + "=" * 70)
    print("✅ Resource demo complete!")


if __name__ == "__main__":
    run_demo()
