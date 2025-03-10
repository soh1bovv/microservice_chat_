import asyncio
from aiokafka import AIOKafkaConsumer
from microservice_chat_engine import emit
from microservice_chat_engine.config import settings
from microservice_chat_engine.custom_emitter import _emitWithConfirmation
import json
import logging

async def consume_emit():
    while True:  # Бесконечный цикл
        consumer_emit = AIOKafkaConsumer(
            'emitWithConfirmation',
            group_id='KfConsumer3',
            bootstrap_servers=f'{settings.KAFKA_HOST}:{settings.KAFKA_PORT}',
            loop=loop
        )
        print('BEGIN')
        await consumer_emit.start()
        # logging.info(f'Kafka consumer started chat engine')
        
        try:
            async for message in consumer_emit:
                new_message = json.loads(message.value.decode('utf-8'))
                # logging.info(f'Emit success from microservice to phone: {new_message}')
                print(new_message)
                type_of_event = new_message.get('type_of_event') 
                payload = new_message.get('payload') 
                user_id = new_message.get('user_id')
                await _emitWithConfirmation(user_id, type_of_event, payload)

        except Exception as e:
            pass
            # logging.error(f'Error occurred: {e}')
            # Здесь можно обработать ошибку, например, записать её в лог.
        
        finally:
            await consumer_emit.stop()  # Остановить потребитель в конце

        print("END")
        await asyncio.sleep(1)  # Небольшая пауза перед перезапуском

@emit.on_event("startup")
async def startup_event():
    global loop
    loop = asyncio.get_event_loop()
    loop.create_task(consume_emit())