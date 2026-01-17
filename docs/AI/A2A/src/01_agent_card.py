"""
A2A Example 01: Agent Card
==========================
Demonstrates generating and serving A2A Agent Cards.

This example shows:
1. AgentCard structure
2. Capability declaration
3. Skill definition
4. JSON serialization
"""

import json
from dataclasses import dataclass, field, asdict
from typing import Optional


@dataclass
class Skill:
    """A capability that an agent can perform."""
    id: str
    name: str
    description: str
    tags: list[str] = field(default_factory=list)
    inputModes: list[str] = field(default_factory=lambda: ["text"])
    outputModes: list[str] = field(default_factory=lambda: ["text"])
    examples: list[str] = field(default_factory=list)


@dataclass
class Capabilities:
    """Communication capabilities of an agent."""
    streaming: bool = False
    pushNotifications: bool = False
    stateTransitionHistory: bool = False


@dataclass
class OAuth2Config:
    """OAuth 2.0 configuration."""
    authorizationUrl: str
    tokenUrl: str
    scopes: dict[str, str] = field(default_factory=dict)


@dataclass
class Authentication:
    """Authentication configuration."""
    schemes: list[str] = field(default_factory=lambda: ["bearer"])
    oauth2: Optional[OAuth2Config] = None


@dataclass
class AgentCard:
    """An A2A Agent Card describing agent capabilities."""
    name: str
    description: str
    url: str
    version: str = "1.0.0"
    capabilities: Capabilities = field(default_factory=Capabilities)
    defaultInputModes: list[str] = field(default_factory=lambda: ["text"])
    defaultOutputModes: list[str] = field(default_factory=lambda: ["text"])
    skills: list[Skill] = field(default_factory=list)
    authentication: Optional[Authentication] = None
    
    def to_json(self, indent: int = 2) -> str:
        """Serialize to JSON."""
        data = asdict(self)
        # Remove None values
        data = {k: v for k, v in data.items() if v is not None}
        return json.dumps(data, indent=indent)
    
    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return asdict(self)


class AgentCardBuilder:
    """Fluent builder for Agent Cards."""
    
    def __init__(self, name: str, description: str, url: str):
        self.name = name
        self.description = description
        self.url = url
        self.version = "1.0.0"
        self.capabilities = Capabilities()
        self.skills: list[Skill] = []
        self.authentication: Optional[Authentication] = None
        self.input_modes = ["text"]
        self.output_modes = ["text"]
    
    def with_version(self, version: str) -> "AgentCardBuilder":
        self.version = version
        return self
    
    def with_streaming(self) -> "AgentCardBuilder":
        self.capabilities.streaming = True
        return self
    
    def with_push_notifications(self) -> "AgentCardBuilder":
        self.capabilities.pushNotifications = True
        return self
    
    def with_state_history(self) -> "AgentCardBuilder":
        self.capabilities.stateTransitionHistory = True
        return self
    
    def with_input_modes(self, modes: list[str]) -> "AgentCardBuilder":
        self.input_modes = modes
        return self
    
    def with_output_modes(self, modes: list[str]) -> "AgentCardBuilder":
        self.output_modes = modes
        return self
    
    def add_skill(self, skill: Skill) -> "AgentCardBuilder":
        self.skills.append(skill)
        return self
    
    def with_bearer_auth(self) -> "AgentCardBuilder":
        self.authentication = Authentication(schemes=["bearer"])
        return self
    
    def with_oauth2(self, auth_url: str, token_url: str, 
                   scopes: dict[str, str] = None) -> "AgentCardBuilder":
        self.authentication = Authentication(
            schemes=["oauth2"],
            oauth2=OAuth2Config(
                authorizationUrl=auth_url,
                tokenUrl=token_url,
                scopes=scopes or {}
            )
        )
        return self
    
    def build(self) -> AgentCard:
        return AgentCard(
            name=self.name,
            description=self.description,
            url=self.url,
            version=self.version,
            capabilities=self.capabilities,
            defaultInputModes=self.input_modes,
            defaultOutputModes=self.output_modes,
            skills=self.skills,
            authentication=self.authentication
        )


# =============================================================================
# Example Agent Cards
# =============================================================================

def create_travel_agent():
    """Create a travel planning agent card."""
    return (AgentCardBuilder(
            "Travel Planning Agent",
            "Helps users plan and book travel arrangements",
            "https://travel.example.com/a2a"
        )
        .with_version("2.0.0")
        .with_streaming()
        .with_push_notifications()
        .with_input_modes(["text", "file"])
        .with_output_modes(["text", "data", "file"])
        .add_skill(Skill(
            id="search_flights",
            name="Search Flights",
            description="Find available flights between cities",
            tags=["travel", "flights"],
            examples=["Find flights to Tokyo", "Search for cheap flights to Paris"]
        ))
        .add_skill(Skill(
            id="book_flight",
            name="Book Flight",
            description="Book a selected flight",
            tags=["travel", "booking"]
        ))
        .add_skill(Skill(
            id="create_itinerary",
            name="Create Itinerary",
            description="Build a complete trip plan with flights, hotels, and activities",
            tags=["travel", "planning"]
        ))
        .with_oauth2(
            "https://auth.travel.example.com/authorize",
            "https://auth.travel.example.com/token",
            {"agent:read": "Read travel data", "agent:write": "Book travel"}
        )
        .build()
    )


def create_simple_echo_agent():
    """Create a minimal echo agent card."""
    return AgentCard(
        name="Echo Agent",
        description="Echoes back messages for testing",
        url="https://echo.example.com/a2a",
        skills=[
            Skill(
                id="echo",
                name="Echo",
                description="Echo back the input message"
            )
        ]
    )


def create_research_agent():
    """Create a research assistant agent card."""
    return (AgentCardBuilder(
            "Research Assistant",
            "Helps with academic research tasks",
            "https://research.example.com/a2a"
        )
        .with_streaming()
        .with_state_history()
        .with_input_modes(["text", "file"])
        .with_output_modes(["text", "data", "file"])
        .add_skill(Skill(
            id="search_papers",
            name="Search Papers",
            description="Search academic databases for papers",
            tags=["research", "search"]
        ))
        .add_skill(Skill(
            id="summarize",
            name="Summarize Document",
            description="Create a summary of a research paper",
            tags=["research", "summarization"]
        ))
        .add_skill(Skill(
            id="extract_citations",
            name="Extract Citations",
            description="Extract and format citations from a paper",
            tags=["research", "citation"]
        ))
        .with_bearer_auth()
        .build()
    )


# =============================================================================
# Demo
# =============================================================================

def run_demo():
    """Demonstrate Agent Card generation."""
    
    print("=" * 70)
    print("A2A Agent Card Generator")
    print("=" * 70)
    
    # 1. Travel Agent
    print("\n✈️  Travel Planning Agent")
    print("-" * 50)
    travel = create_travel_agent()
    print(travel.to_json())
    
    # 2. Simple Echo
    print("\n" + "=" * 70)
    print("\n📢 Echo Agent (Minimal)")
    print("-" * 50)
    echo = create_simple_echo_agent()
    print(echo.to_json())
    
    # 3. Research Agent
    print("\n" + "=" * 70)
    print("\n📚 Research Assistant")
    print("-" * 50)
    research = create_research_agent()
    print(research.to_json())
    
    print("\n" + "=" * 70)
    print("Agent Cards should be served at: /.well-known/agent.json")
    print("=" * 70)


if __name__ == "__main__":
    run_demo()
