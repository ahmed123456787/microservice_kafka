from confluent_kafka import Producer
import json


def produce_message(topic: str, key: str, value: dict):
    """
    Envoie un message à Kafka
    
    Args:
        topic: Nom du topic Kafka
        key: Clé du message
        value: Valeur du message (dict)
    """
    # Configuration du producer
    config = {
        'bootstrap.servers': 'kafka:9093',
        'client.id': 'python-producer'
    }
    
    # Créer le producer
    producer = Producer(config)
    
    try:
        # Convertir le message en JSON
        message_json = json.dumps(value).encode('utf-8')
        key_bytes = key.encode('utf-8')
        
        # Envoyer le message
        producer.produce(
            topic=topic,
            key=key_bytes,
            value=message_json
        )
        
        # Attendre l'envoi
        producer.flush()
        
    finally:
        producer.flush()


# Exemple d'utilisation
if __name__ == "__main__":
    produce_message(
        topic="user-events",
        key="user_123",
        value={"action": "login", "timestamp": "2024-01-15T10:30:00Z"}
    )