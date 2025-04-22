"""MongoDB connection management module.

This module provides the MongoConnectionManager class which handles database connections
and implements the singleton pattern to ensure efficient connection reuse throughout
the application. It manages connection pooling and provides context managers for
safe database operations.
"""

import os
from contextlib import asynccontextmanager
from typing import Dict, Optional

import motor.motor_asyncio
from dotenv import load_dotenv

load_dotenv()

MONGO_CONNECTION_STRING = os.getenv(
    "MONGO_CONNECTION_STRING", "mongodb://localhost:27017"
)


class MongoConnectionManager:
    """Singleton class for managing MongoDB connections.

    This class implements the singleton pattern to ensure only one instance of the
    connection manager exists. It manages connection pooling to MongoDB and provides
    methods for retrieving and closing connections.

    Attributes:
        _instance: Class-level singleton instance reference
        _clients: Dictionary of motor AsyncIOMotorClient instances
        url: MongoDB connection string
    """

    _instance: Optional["MongoConnectionManager"] = None
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
        """Singleton implementation ensuring only one instance is created.

        Returns:
            The singleton MongoConnectionManager instance
        """
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        """Initialize the MongoConnectionManager with the connection string.

        The initialization only happens once due to the singleton pattern.
        """
        self.url = MONGO_CONNECTION_STRING

    async def get_client(self) -> motor.motor_asyncio.AsyncIOMotorClient:
        """Get the MongoDB client instance, creating it if it doesn't exist.

        Returns:
            AsyncIOMotorClient: MongoDB motor client for asynchronous operations
        """
        if "default" not in self._clients:
            self._clients["default"] = motor.motor_asyncio.AsyncIOMotorClient(
                self.url, **self.MONGO_CONFIG
            )
        return self._clients["default"]

    async def close_all(self):
        """Close all active MongoDB connections.

        This method should be called during application shutdown to properly
        release all database connections.
        """
        for client in self._clients.values():
            client.close()
        self._clients.clear()

    @asynccontextmanager
    async def get_collection(self, db_name: str, collection_name: str):
        """Get a MongoDB collection as an async context manager.

        Args:
            db_name: Name of the database
            collection_name: Name of the collection

        Yields:
            motor.motor_asyncio.AsyncIOMotorCollection: The requested collection

        Examples:
            ```python
            async with connection_manager.get_collection("mydb", "users") as collection:
                await collection.find_one({"email": "user@example.com"})
            ```
        """
        client = await self.get_client()
        try:
            collection = client[db_name][collection_name]
            yield collection
        finally:
            pass
