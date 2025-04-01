from typing import Optional, Dict
from typing import List
from app.database.connector import MongoConnectionManager


class BaseRepository:
    def __init__(self, db_name: str, collection_name: str):
        self.db_name = db_name
        self.collection_name = collection_name
        self.connection_manager = MongoConnectionManager()

    async def find_one(self, query: Dict) -> Optional[Dict]:
        try:
            async with self.connection_manager.get_collection(
                self.db_name, self.collection_name
            ) as collection:
                document = await collection.find_one(query)
                if document:
                    document["_id"] = str(document["_id"])
                return document
        except Exception as e:
            print(f"Error in find_one: {str(e)}")
            return None

    async def find(self, query: Dict) -> List[Dict]:
        try:
            async with self.connection_manager.get_collection(
                self.db_name, self.collection_name
            ) as collection:
                cursor = collection.find(query)
                documents = await cursor.to_list(length=None)
                for doc in documents:
                    doc["_id"] = str(doc["_id"])
                return documents
        except Exception as e:
            print(f"Error in find: {str(e)}")
            return []

    async def find_many(
        self, query: Dict, sort: Optional[List[tuple]] = None
    ) -> List[Dict]:
        try:
            async with self.connection_manager.get_collection(
                self.db_name, self.collection_name
            ) as collection:
                cursor = collection.find(query)
                if sort:
                    cursor.sort(sort)
                documents = await cursor.to_list(length=None)
                for doc in documents:
                    doc["_id"] = str(doc["_id"])
                return documents
        except Exception as e:
            print(f"Error in find_many: {str(e)}")
            return []

    async def insert_one(self, document: Dict) -> str:
        try:
            async with self.connection_manager.get_collection(
                self.db_name, self.collection_name
            ) as collection:
                result = await collection.insert_one(document)
                return str(result.inserted_id)
        except Exception as e:
            print(f"Error in insert_one: {str(e)}")
            return ""

    async def update_one(self, query: Dict, update: Dict) -> bool:
        try:
            async with self.connection_manager.get_collection(
                self.db_name, self.collection_name
            ) as collection:
                result = await collection.update_one(query, update)
                return result.modified_count > 0
        except Exception as e:
            print(f"Error in update_one: {str(e)}")
            return False

    async def delete_one(self, query: Dict) -> bool:
        try:
            async with self.connection_manager.get_collection(
                self.db_name, self.collection_name
            ) as collection:
                result = await collection.delete_one(query)
                return result.deleted_count > 0
        except Exception as e:
            print(f"Error in delete_one: {str(e)}")
            return False

    async def get_entity_by_email(self, email: str):
        try:
            async with self.connection_manager.get_collection(
                self.db_name, self.collection_name
            ) as collection:
                user = await collection.find_one({"email": email})
                if user:
                    return {**user}
                return None
        except Exception as e:
            print(f"Error in get_entity_by_email: {str(e)}")
            return None