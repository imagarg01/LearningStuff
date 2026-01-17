"""
Kafka Consumer Example
"""

from kafka import KafkaConsumer
import json

def main():
    consumer = KafkaConsumer(
        'user-events',
        bootstrap_servers=['localhost:9092'],
        group_id='event-processor',
        auto_offset_reset='earliest',
        enable_auto_commit=False,
        value_deserializer=lambda v: json.loads(v.decode('utf-8'))
    )
    
    print("Waiting for messages... Press CTRL+C to exit")
    
    try:
        for message in consumer:
            print(f"Received:")
            print(f"  Topic: {message.topic}")
            print(f"  Partition: {message.partition}")
            print(f"  Offset: {message.offset}")
            print(f"  Key: {message.key}")
            print(f"  Value: {message.value}")
            
            # Process message
            process_event(message.value)
            
            # Commit offset
            consumer.commit()
            print("  ✓ Committed")
            print()
    except KeyboardInterrupt:
        pass
    finally:
        consumer.close()

def process_event(event):
    """Process the event."""
    print(f"  Processing: {event['action']} by {event['user_id']}")

if __name__ == '__main__':
    main()
