from microservice_chat_engine import sio
#from sqlalchemy.orm import Session
from sqlalchemy import select, and_, or_, desc, delete, update
from microservice_chat_engine.client_connection import Client
import json 
from confluent_kafka import Producer

from microservice_chat_engine.utils.kafka import kafka_topic_name_emit, conf_emit
from microservice_chat_engine.db_models.models import MissedEvent
from microservice_chat_engine.storage import Storage
from microservice_chat_engine import async_session
import logging

@sio.on('on_confirm_event')
async def on_confirm_event(sid, msg):
    print('on confirm event')
    async with async_session() as session:
        message_dict = json.loads(msg)
        query = delete(MissedEvent).where(MissedEvent.id==message_dict['event_id'])
        await session.execute(query)
        await session.commit()


async def _emitMessedEventsByClient(client):
    async with async_session() as session:
         

        try:
            query = select(MissedEvent).where(MissedEvent.user_id==client.id)
            missed_events = (await session.execute(query)).all()
            print(missed_events) 
            for event in missed_events:
                new_payload={}
                new_payload['event_id'] = event.MissedEvent.id
                new_payload['payload'] = event.MissedEvent.payload
                await sio.emit(event.MissedEvent.type_of_event, new_payload, room=client.sid)
        except:
            print('exception')
        

async def _emitWithConfirmation(user_id: int, type_of_event:str, payload:dict):
    async with async_session() as session:
        missed_event = MissedEvent(type_of_event = type_of_event, payload = payload, user_id=user_id)
        session.add(missed_event)
        try:
            await session.commit()
            await session.refresh(missed_event)
        except Exception as e:
            # logging.error(f'Ошибка при добавлении события: {e}')
            await session.rollback()  # Откат транзакции
            return
        new_payload={}
        new_payload['event_id']= missed_event.id
        new_payload['payload']= payload
        if user_id in Storage().connected_clents.keys():
            await sio.emit(type_of_event, new_payload, room=Storage().connected_clents[user_id].sid)
        print(new_payload)