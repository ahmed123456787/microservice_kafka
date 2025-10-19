from confluent_kafka import Consumer, KafkaException
import sys

def consume_messages():
    # Configure the consumer
    consumer = Consumer({
        'bootstrap.servers': 'localhost:9092',
        'group.id': 'test-consumer-group',
        'auto.offset.reset': 'earliest'  # Start from beginning
    })
    
    # Subscribe to the topic
    consumer.subscribe(['notifications'])
    
    print("Waiting for messages... Press Ctrl+C to exit")
    
    try:
        while True:
            # Poll for messages
            msg = consumer.poll(timeout=1.0)
            
            if msg is None:
                continue
            if msg.error():
                print(f"Consumer error: {msg.error()}")
                continue
                
            # Print the message
            print(f"Key: {msg.key().decode('utf-8') if msg.key() else None}")
            print(f"Value: {msg.value().decode('utf-8')}")
            print(f"Topic: {msg.topic()}")
            print(f"Partition: {msg.partition()}")
            print(f"Offset: {msg.offset()}")
            print("-" * 50)
            
    except KeyboardInterrupt:
        print("Stopping consumer...")
    finally:
        consumer.close()

if __name__ == "__main__":
    consume_messages()