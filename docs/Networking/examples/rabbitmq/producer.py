"""
RabbitMQ Producer Example
"""

import pika
import json
import time

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
    
    # Send messages
    orders = [
        {'id': 1, 'product': 'Laptop', 'region': 'us'},
        {'id': 2, 'product': 'Phone', 'region': 'eu'},
        {'id': 3, 'product': 'Tablet', 'region': 'us'},
    ]
    
    for order in orders:
        routing_key = f"order.created.{order['region']}"
        
        channel.basic_publish(
            exchange='orders',
            routing_key=routing_key,
            body=json.dumps(order),
            properties=pika.BasicProperties(
                delivery_mode=2,  # Persistent
                content_type='application/json'
            )
        )
        print(f"Sent: {order} with key: {routing_key}")
        time.sleep(1)
    
    connection.close()
    print("Done!")

if __name__ == '__main__':
    main()
