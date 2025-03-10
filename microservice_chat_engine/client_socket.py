
import logging
from microservice_chat_engine import sio
from microservice_chat_engine.custom_emitter import _emitMessedEventsByClient
from microservice_chat_engine.storage import Storage
from microservice_chat_engine.custom_emitter import *


@sio.on("connect")
async def on_connect(sid, env):
    headers = env['HTTP_AUTHORIZATION']
    client_id = int(headers.split(' ')[-1])
    #logging.info(f'connected client with id: {client_id}')
    client=Client(sid=sid, id=client_id)
    Storage().add_client(client)
    await _emitMessedEventsByClient(client)
    


@sio.event
def disconnect(sid):
    
    Storage().delete_client_by_sid(sid)
    
