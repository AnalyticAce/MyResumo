from typing import Optional, Dict
from app.db.connector import MongoConnectionManager
from typing import List

class BaseRepository:
    def __init__(self, db_name: str, collection_name: str):
        self.db_name = db_name
        self.collection_name = collection_name
        self.connection_manager = MongoConnectionManager()

    async def find_one(self, query: Dict) -> Optional[Dict]:
        async with self.connection_manager.get_collection(self.db_name, self.collection_name) as collection:
            document = await collection.find_one(query)
            if document:
                document["_id"] = str(document["_id"])
            return document

    async def find(self, query: Dict) -> List[Dict]:
        async with self.connection_manager.get_collection(self.db_name, self.collection_name) as collection:
            cursor = collection.find(query)
            documents = await cursor.to_list(length=None)
            for doc in documents:
                doc["_id"] = str(doc["_id"])
            return documents

    # async def find(
    #     self,
    #     query: dict,
    #     sort_by: Optional[List[tuple]] = None,
    #     limit: Optional[int] = None
    # ) -> List[Post]:
    #     cursor = self.collection.find(query)
    #     if sort_by:
    #         cursor = cursor.sort(sort_by)
    #     if limit:
    #         cursor = cursor.limit(limit)
    #     return [self.model(**doc) async for doc in cursor]
    
    async def insert_one(self, document: Dict) -> str:
        async with self.connection_manager.get_collection(self.db_name, self.collection_name) as collection:
            result = await collection.insert_one(document)
            return str(result.inserted_id)

    async def update_one(self, query: Dict, update: Dict) -> bool:
        async with self.connection_manager.get_collection(self.db_name, self.collection_name) as collection:
            result = await collection.update_one(query, update)
            return result.modified_count > 0

    async def delete_one(self, query: Dict) -> bool:
        async with self.connection_manager.get_collection(self.db_name, self.collection_name) as collection:
            result = await collection.delete_one(query)
            return result.deleted_count > 0