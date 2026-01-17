"""
Kafka Producer Example
"""

from kafka import KafkaProducer
import json
import time

def main():
    producer = KafkaProducer(
        bootstrap_servers=['localhost:9092'],
        value_serializer=lambda v: json.dumps(v).encode('utf-8'),
        key_serializer=lambda k: k.encode('utf-8') if k else None,
        acks='all'
    )
    
    # Send messages
    events = [
        {'user_id': 'user-1', 'action': 'login', 'timestamp': time.time()},
        {'user_id': 'user-2', 'action': 'purchase', 'timestamp': time.time()},
        {'user_id': 'user-1', 'action': 'logout', 'timestamp': time.time()},
    ]
    
    for event in events:
        future = producer.send(
            topic='user-events',
            key=event['user_id'],
            value=event
        )
        
        # Wait for confirmation
        record_metadata = future.get(timeout=10)
        print(f"Sent: {event}")
        print(f"  Partition: {record_metadata.partition}, Offset: {record_metadata.offset}")
        time.sleep(1)
    
    producer.flush()
    producer.close()
    print("Done!")

if __name__ == '__main__':
    main()
