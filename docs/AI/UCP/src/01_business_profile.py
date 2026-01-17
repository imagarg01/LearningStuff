"""
UCP Example 01: Business Profile
================================
Demonstrates UCP business profile generation for capability discovery.

A UCP profile declares what capabilities a business supports,
enabling AI agents to discover and configure themselves.
"""

import json
from dataclasses import dataclass, field, asdict
from typing import Optional
from datetime import datetime, timedelta


@dataclass
class Capability:
    """A UCP capability declaration."""
    name: str
    version: str
    spec: str
    schema: str
    endpoint: str


@dataclass
class Extension:
    """A capability extension."""
    name: str
    version: str
    extends: str
    spec: Optional[str] = None


@dataclass
class OAuth2Config:
    """OAuth 2.0 configuration."""
    authorization_endpoint: str
    token_endpoint: str
    scopes: list[str] = field(default_factory=list)


@dataclass
class Service:
    """A UCP service namespace."""
    namespace: str
    capabilities: list[Capability] = field(default_factory=list)
    extensions: list[Extension] = field(default_factory=list)


@dataclass
class UCPProfile:
    """A complete UCP business profile."""
    name: str
    version: str
    services: list[Service] = field(default_factory=list)
    transports: list[str] = field(default_factory=lambda: ["rest"])
    authentication: Optional[OAuth2Config] = None
    
    def to_json(self) -> str:
        """Convert profile to JSON."""
        return json.dumps(asdict(self), indent=2, default=str)
    
    def to_dict(self) -> dict:
        """Convert profile to dictionary."""
        return asdict(self)


class ProfileBuilder:
    """Builder for creating UCP business profiles."""
    
    BASE_URL = "https://ucp.dev"
    
    def __init__(self, name: str, base_endpoint: str):
        self.name = name
        self.base_endpoint = base_endpoint
        self.version = datetime.now().strftime("%Y-%m-%d")
        self.services: list[Service] = []
        self.transports = ["rest"]
        self.oauth: Optional[OAuth2Config] = None
    
    def add_checkout(self) -> "ProfileBuilder":
        """Add checkout capability."""
        shopping = self._get_or_create_service("dev.ucp.shopping")
        shopping.capabilities.append(Capability(
            name="dev.ucp.shopping.checkout",
            version=self.version,
            spec=f"{self.BASE_URL}/specification/checkout",
            schema=f"{self.BASE_URL}/schemas/shopping/checkout.json",
            endpoint=f"{self.base_endpoint}/checkout"
        ))
        return self
    
    def add_order(self) -> "ProfileBuilder":
        """Add order capability."""
        shopping = self._get_or_create_service("dev.ucp.shopping")
        shopping.capabilities.append(Capability(
            name="dev.ucp.shopping.order",
            version=self.version,
            spec=f"{self.BASE_URL}/specification/order",
            schema=f"{self.BASE_URL}/schemas/shopping/order.json",
            endpoint=f"{self.base_endpoint}/order"
        ))
        return self
    
    def add_identity_linking(self) -> "ProfileBuilder":
        """Add identity linking capability."""
        identity = self._get_or_create_service("dev.ucp.identity")
        identity.capabilities.append(Capability(
            name="dev.ucp.identity.linking",
            version=self.version,
            spec=f"{self.BASE_URL}/specification/identity-linking",
            schema=f"{self.BASE_URL}/schemas/identity/linking.json",
            endpoint=f"{self.base_endpoint}/identity"
        ))
        return self
    
    def add_fulfillment_extension(self) -> "ProfileBuilder":
        """Add fulfillment extension (extends checkout)."""
        shopping = self._get_or_create_service("dev.ucp.shopping")
        shopping.extensions.append(Extension(
            name="dev.ucp.shopping.fulfillment",
            version=self.version,
            extends="dev.ucp.shopping.checkout",
            spec=f"{self.BASE_URL}/specification/fulfillment"
        ))
        return self
    
    def add_discounts_extension(self) -> "ProfileBuilder":
        """Add discounts extension (extends checkout)."""
        shopping = self._get_or_create_service("dev.ucp.shopping")
        shopping.extensions.append(Extension(
            name="dev.ucp.shopping.discounts",
            version=self.version,
            extends="dev.ucp.shopping.checkout",
            spec=f"{self.BASE_URL}/specification/discounts"
        ))
        return self
    
    def with_mcp_transport(self) -> "ProfileBuilder":
        """Enable MCP transport."""
        if "mcp" not in self.transports:
            self.transports.append("mcp")
        return self
    
    def with_a2a_transport(self) -> "ProfileBuilder":
        """Enable A2A transport."""
        if "a2a" not in self.transports:
            self.transports.append("a2a")
        return self
    
    def with_oauth(self, auth_endpoint: str, token_endpoint: str, 
                   scopes: list[str] = None) -> "ProfileBuilder":
        """Configure OAuth 2.0 authentication."""
        self.oauth = OAuth2Config(
            authorization_endpoint=auth_endpoint,
            token_endpoint=token_endpoint,
            scopes=scopes or ["checkout.read", "checkout.write", "order.read"]
        )
        return self
    
    def build(self) -> UCPProfile:
        """Build the final profile."""
        return UCPProfile(
            name=self.name,
            version=self.version,
            services=self.services,
            transports=self.transports,
            authentication=self.oauth
        )
    
    def _get_or_create_service(self, namespace: str) -> Service:
        """Get existing service or create new one."""
        for service in self.services:
            if service.namespace == namespace:
                return service
        service = Service(namespace=namespace)
        self.services.append(service)
        return service


# =============================================================================
# Example Usage
# =============================================================================

def create_retail_profile():
    """Create a complete retail store profile."""
    
    profile = (ProfileBuilder("Example Store", "https://api.example.com/ucp")
        .add_checkout()
        .add_order()
        .add_identity_linking()
        .add_fulfillment_extension()
        .add_discounts_extension()
        .with_mcp_transport()
        .with_oauth(
            "https://example.com/oauth/authorize",
            "https://example.com/oauth/token"
        )
        .build()
    )
    
    return profile


def create_minimal_profile():
    """Create a minimal profile with just checkout."""
    
    profile = (ProfileBuilder("Simple Shop", "https://api.simpleshop.com/ucp")
        .add_checkout()
        .build()
    )
    
    return profile


if __name__ == "__main__":
    print("=" * 70)
    print("UCP Business Profile Examples")
    print("=" * 70)
    
    print("\n📦 Example 1: Complete Retail Profile")
    print("-" * 70)
    retail = create_retail_profile()
    print(retail.to_json())
    
    print("\n" + "=" * 70)
    
    print("\n🛒 Example 2: Minimal Checkout-Only Profile")
    print("-" * 70)
    minimal = create_minimal_profile()
    print(minimal.to_json())
    
    print("\n" + "=" * 70)
    print("\nProfiles should be served at: /.well-known/ucp-profile")
    print("Platforms will discover capabilities automatically!")
