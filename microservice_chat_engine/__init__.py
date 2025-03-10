from microservice_chat_engine.config import settings
from fastapi import FastAPI
from starlette.config import Config 
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase
from fastapi_socketio import SocketManager
import multiprocessing as mp
import socketio
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from typing import AsyncGenerator
import sys, os
import logging
import asyncio
from aiokafka import AIOKafkaConsumer

sio = socketio.AsyncServer(async_mode="asgi")
socket_app = socketio.ASGIApp(sio)
emit = FastAPI()



logging.basicConfig(
    filename='/root/ChatServer/microservice_chat_engine/emit.log',  # Имя файла для записи логов
    level=logging.INFO,  # Уровень логирования
    filemode='a',
    force=True,
    format='%(asctime)s - %(levelname)s - %(message)s',  # Формат сообщений с временной меткой
    datefmt='%Y-%m-%d %H:%M:%S'  # Формат времени
)

# logging.info('start logging service')

emit.mount('/', socket_app)

engine = create_async_engine(settings.DATABASE_URL, pool_pre_ping=True)


async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit = False)
lifetime = 3600*5

class Base(DeclarativeBase):
    pass


from microservice_chat_engine.db_models import models
from microservice_chat_engine import client_socket
import microservice_chat_engine.kafka_tasks