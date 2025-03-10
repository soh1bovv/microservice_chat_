from confluent_kafka import Producer
import json
from app.config import settings

kafka_topic_name = "delete_files" 
conf = {
        'bootstrap.servers' : f'{settings.KAFKA_HOST}:{settings.KAFKA_PORT}',
        } 


kafka_topic_name_emit = "emitWithConfirmation" 
conf_emit = {
        'bootstrap.servers' : f'{settings.KAFKA_HOST}:{settings.KAFKA_PORT}',
        } 


kafka_topic_name_push = "push" 
conf_push = {
        'bootstrap.servers' : f'{settings.KAFKA_HOST}:{settings.KAFKA_PORT}',
        } 
