"""
UCP Example 02: Checkout Flow
=============================
Demonstrates a complete UCP checkout flow simulation.

This example shows how to:
1. Create a checkout session
2. Add items to the cart
3. Calculate totals (with tax)
4. Complete the purchase
"""

import json
from dataclasses import dataclass, field, asdict
from typing import Optional
from datetime import datetime, timedelta
import uuid


@dataclass
class CheckoutItem:
    """An item in the checkout cart."""
    id: str
    product_id: str
    name: str
    quantity: int
    unit_price: int  # in cents
    total: int = 0
    
    def __post_init__(self):
        self.total = self.quantity * self.unit_price


@dataclass
class TaxBreakdown:
    """Tax calculation breakdown."""
    name: str
    rate: float
    amount: int  # in cents


@dataclass
class Address:
    """Shipping/billing address."""
    name: str
    line1: str
    city: str
    state: str
    postal_code: str
    country: str


@dataclass
class CheckoutSession:
    """A UCP checkout session."""
    id: str
    status: str
    currency: str
    locale: str
    items: list[CheckoutItem] = field(default_factory=list)
    subtotal: int = 0
    tax: int = 0
    shipping: int = 0
    total: int = 0
    tax_breakdown: list[TaxBreakdown] = field(default_factory=list)
    shipping_address: Optional[Address] = None
    billing_address: Optional[Address] = None
    order_id: Optional[str] = None
    confirmation_number: Optional[str] = None
    created_at: str = ""
    expires_at: str = ""
    
    def __post_init__(self):
        if not self.created_at:
            self.created_at = datetime.now().isoformat()
        if not self.expires_at:
            self.expires_at = (datetime.now() + timedelta(hours=1)).isoformat()
    
    def to_json(self) -> str:
        """Convert to JSON response."""
        return json.dumps(asdict(self), indent=2, default=str)


class UCPCheckoutService:
    """
    Simulated UCP Checkout Service.
    
    In production, this would be a REST API.
    """
    
    # Simulated product catalog
    PRODUCTS = {
        "prod_shoe_001": {"name": "Running Shoes", "price": 9999},
        "prod_shirt_002": {"name": "Athletic T-Shirt", "price": 2999},
        "prod_socks_003": {"name": "Performance Socks (3-pack)", "price": 1499},
    }
    
    # Tax rates by state
    TAX_RATES = {
        "CA": [
            {"name": "CA State Tax", "rate": 0.0725},
            {"name": "SF Local Tax", "rate": 0.0125}
        ],
        "NY": [
            {"name": "NY State Tax", "rate": 0.08}
        ],
        "TX": [
            {"name": "TX State Tax", "rate": 0.0625}
        ]
    }
    
    def __init__(self):
        self.sessions: dict[str, CheckoutSession] = {}
    
    def create_checkout(self, currency: str = "USD", locale: str = "en-US") -> CheckoutSession:
        """
        Create a new checkout session.
        
        POST /checkout
        """
        session_id = f"checkout_{uuid.uuid4().hex[:12]}"
        session = CheckoutSession(
            id=session_id,
            status="open",
            currency=currency,
            locale=locale
        )
        self.sessions[session_id] = session
        return session
    
    def add_items(self, checkout_id: str, items: list[dict]) -> CheckoutSession:
        """
        Add items to checkout.
        
        POST /checkout/{id}/items
        """
        session = self.sessions.get(checkout_id)
        if not session:
            raise ValueError(f"Checkout {checkout_id} not found")
        
        for item_data in items:
            product_id = item_data["product_id"]
            quantity = item_data.get("quantity", 1)
            
            product = self.PRODUCTS.get(product_id)
            if not product:
                raise ValueError(f"Product {product_id} not found")
            
            item = CheckoutItem(
                id=f"item_{uuid.uuid4().hex[:8]}",
                product_id=product_id,
                name=product["name"],
                quantity=quantity,
                unit_price=product["price"]
            )
            session.items.append(item)
        
        session.subtotal = sum(item.total for item in session.items)
        return session
    
    def calculate(self, checkout_id: str, shipping_address: dict) -> CheckoutSession:
        """
        Calculate totals with tax and shipping.
        
        POST /checkout/{id}/calculate
        """
        session = self.sessions.get(checkout_id)
        if not session:
            raise ValueError(f"Checkout {checkout_id} not found")
        
        # Set shipping address
        session.shipping_address = Address(**shipping_address)
        
        # Calculate tax based on state
        state = shipping_address.get("state", "CA")
        tax_rates = self.TAX_RATES.get(state, self.TAX_RATES["CA"])
        
        session.tax_breakdown = []
        session.tax = 0
        
        for rate_info in tax_rates:
            tax_amount = int(session.subtotal * rate_info["rate"])
            session.tax_breakdown.append(TaxBreakdown(
                name=rate_info["name"],
                rate=rate_info["rate"],
                amount=tax_amount
            ))
            session.tax += tax_amount
        
        # Shipping calculation (simplified)
        if session.subtotal > 5000:  # Free shipping over $50
            session.shipping = 0
        else:
            session.shipping = 599
        
        session.total = session.subtotal + session.tax + session.shipping
        return session
    
    def complete(self, checkout_id: str, payment_token: str, 
                 billing_address: dict) -> CheckoutSession:
        """
        Complete the checkout.
        
        POST /checkout/{id}/complete
        """
        session = self.sessions.get(checkout_id)
        if not session:
            raise ValueError(f"Checkout {checkout_id} not found")
        
        # Set billing address
        session.billing_address = Address(**billing_address)
        
        # In production: validate payment_token with PSP
        # Simulate successful payment
        
        session.status = "completed"
        session.order_id = f"order_{uuid.uuid4().hex[:12]}"
        session.confirmation_number = f"ORD-{datetime.now().year}-{uuid.uuid4().hex[:6].upper()}"
        
        return session


# =============================================================================
# Example: Full Checkout Flow
# =============================================================================

def run_checkout_demo():
    """Demonstrate a complete checkout flow."""
    
    service = UCPCheckoutService()
    
    print("📦 Step 1: Create Checkout Session")
    print("-" * 50)
    session = service.create_checkout(currency="USD", locale="en-US")
    print(f"Created session: {session.id}")
    print(f"Status: {session.status}")
    print(f"Expires: {session.expires_at}")
    
    print("\n🛒 Step 2: Add Items to Cart")
    print("-" * 50)
    session = service.add_items(session.id, [
        {"product_id": "prod_shoe_001", "quantity": 1},
        {"product_id": "prod_shirt_002", "quantity": 2},
        {"product_id": "prod_socks_003", "quantity": 1}
    ])
    
    for item in session.items:
        print(f"  {item.name} x{item.quantity} = ${item.total/100:.2f}")
    print(f"  Subtotal: ${session.subtotal/100:.2f}")
    
    print("\n🧮 Step 3: Calculate Totals")
    print("-" * 50)
    session = service.calculate(session.id, {
        "name": "John Doe",
        "line1": "123 Main Street",
        "city": "San Francisco",
        "state": "CA",
        "postal_code": "94105",
        "country": "US"
    })
    
    print(f"  Subtotal: ${session.subtotal/100:.2f}")
    for tax in session.tax_breakdown:
        print(f"  {tax.name} ({tax.rate*100:.2f}%): ${tax.amount/100:.2f}")
    print(f"  Shipping: ${session.shipping/100:.2f}")
    print(f"  Total: ${session.total/100:.2f}")
    
    print("\n✅ Step 4: Complete Checkout")
    print("-" * 50)
    session = service.complete(
        session.id,
        payment_token="tok_visa_abc123",
        billing_address={
            "name": "John Doe",
            "line1": "123 Main Street",
            "city": "San Francisco",
            "state": "CA",
            "postal_code": "94105",
            "country": "US"
        }
    )
    
    print(f"  Status: {session.status}")
    print(f"  Order ID: {session.order_id}")
    print(f"  Confirmation: {session.confirmation_number}")
    
    return session


if __name__ == "__main__":
    print("=" * 70)
    print("UCP Checkout Flow Demo")
    print("=" * 70)
    print()
    
    session = run_checkout_demo()
    
    print("\n" + "=" * 70)
    print("📋 Final Session State (JSON)")
    print("=" * 70)
    print(session.to_json())
