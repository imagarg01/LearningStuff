"""
RabbitMQ Consumer Example
"""

import pika
import json

def callback(ch, method, properties, body):
    message = json.loads(body)
    print(f"Received: {message}")
    print(f"  Routing key: {method.routing_key}")
    
    # Process message
    try:
        process_order(message)
        ch.basic_ack(delivery_tag=method.delivery_tag)
        print("  ✓ Acknowledged")
    except Exception as e:
        print(f"  ✗ Error: {e}")
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)

def process_order(order):
    """Process the order (simulate work)."""
    print(f"  Processing order {order['id']}...")

def main():
    # Connect
    connection = pika.BlockingConnection(
        pika.ConnectionParameters('localhost')
    )
    channel = connection.channel()
    
    # Declare exchange
    channel.exchange_declare(
        exchange='orders',
        exchange_type='topic',
        durable=True
    )
    
    # Declare queue
    channel.queue_declare(queue='order_processor', durable=True)
    
    # Bind with pattern
    channel.queue_bind(
        exchange='orders',
        queue='order_processor',
        routing_key='order.created.*'  # All regions
    )
    
    # Prefetch
    channel.basic_qos(prefetch_count=1)
    
    # Start consuming
    channel.basic_consume(
        queue='order_processor',
        on_message_callback=callback,
        auto_ack=False
    )
    
    print("Waiting for messages... Press CTRL+C to exit")
    channel.start_consuming()

if __name__ == '__main__':
    main()
