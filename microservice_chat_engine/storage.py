
from microservice_chat_engine.client_connection import Client
from typing import List



def singleton(class_):
    instances = {}
    def getinstance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]
    return getinstance

@singleton
class Storage():
    def __init__(self):
        self.connected_clents = {}


    def add_client(self, client: Client)->None:
        self.connected_clents[client.id] = client

    def get_client_by_sid(self, sid:str):
        for key in self.connected_clents.keys():
            if self.connected_clents[key].sid==sid:
                return self.connected_clents[key]
       

    def delete_client_by_sid(self, sid:str)->None:
        for key in self.connected_clents.keys():
            if self.connected_clents[key].sid==sid:

                del self.connected_clents[key]
                return
        