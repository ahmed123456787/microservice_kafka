from confluent_kafka.experimental.aio import AIOProducer


async def produce_message(topic:str, key:str, value:str):

    producer = AIOProducer({
        'bootstrap.servers': 'kafka:9092',
    })

    try: 

        delivery_future = await producer.produce(
            topic=topic,
            key=key,
            value=value,
        
        )
        # wait the future for the message
        delivered_message = await delivery_future

        # flush any remaining messages
        await producer.flush()

    finally:
        await producer.close()
