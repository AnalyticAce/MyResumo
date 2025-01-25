from typing import Optional, Dict
import motor.motor_asyncio
from contextlib import asynccontextmanager
from app.credentials.config import MONGO_CONNECTION_STRING

class MongoConnectionManager:
    _instance: Optional['MongoConnectionManager'] = None
    _clients: Dict[str, motor.motor_asyncio.AsyncIOMotorClient] = {}
    
    MONGO_CONFIG = {
        "maxPoolSize": 1000,
        "minPoolSize": 50,
        "maxIdleTimeMS": 45000,
        "waitQueueTimeoutMS": 10000,
        "serverSelectionTimeoutMS": 10000,
        "retryWrites": True,
    }

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        self.url = MONGO_CONNECTION_STRING
        
    async def get_client(self) -> motor.motor_asyncio.AsyncIOMotorClient:
        if 'default' not in self._clients:
            self._clients['default'] = motor.motor_asyncio.AsyncIOMotorClient(
                self.url, 
                **self.MONGO_CONFIG
            )
        return self._clients['default']

    async def close_all(self):
        for client in self._clients.values():
            client.close()
        self._clients.clear()

    @asynccontextmanager
    async def get_collection(self, db_name: str, collection_name: str):
        client = await self.get_client()
        try:
            collection = client[db_name][collection_name]
            yield collection
        finally:
            pass