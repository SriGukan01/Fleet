import os
import json
import uuid
import asyncio
import logging
from typing import Any, Dict, List, Optional
from datetime import datetime
from backend.app.config import settings

logger = logging.getLogger("veritrust.database")

class LocalCursor:
    def __init__(self, data: List[Dict[str, Any]]):
        self._data = data
        self._index = 0

    def sort(self, key_or_list, direction=1):
        if isinstance(key_or_list, str):
            reverse = direction == -1
            self._data.sort(key=lambda x: x.get(key_or_list, ""), reverse=reverse)
        elif isinstance(key_or_list, list) and len(key_or_list) > 0:
            k, d = key_or_list[0]
            self._data.sort(key=lambda x: x.get(k, ""), reverse=(d == -1))
        return self

    def limit(self, n: int):
        self._data = self._data[:n]
        return self

    def skip(self, n: int):
        self._data = self._data[n:]
        return self

    async def to_list(self, length: Optional[int] = None) -> List[Dict[str, Any]]:
        if length is not None:
            return self._data[:length]
        return list(self._data)

    def __aiter__(self):
        self._index = 0
        return self

    async def __anext__(self):
        if self._index < len(self._data):
            val = self._data[self._index]
            self._index += 1
            return val
        raise StopAsyncIteration


class LocalCollection:
    def __init__(self, name: str, store: "LocalDocumentStore"):
        self.name = name
        self.store = store

    def _matches(self, doc: Dict[str, Any], query: Dict[str, Any]) -> bool:
        if not query:
            return True
        for key, val in query.items():
            if key == "$or" and isinstance(val, list):
                if not any(self._matches(doc, q) for q in val):
                    return False
                continue
            if key == "$and" and isinstance(val, list):
                if not all(self._matches(doc, q) for q in val):
                    return False
                continue
            if isinstance(val, dict):
                # e.g. {"$in": [...]}, {"$ne": ...}, {"$gte": ...}
                doc_val = doc.get(key)
                if "$in" in val and doc_val not in val["$in"]:
                    return False
                if "$nin" in val and doc_val in val["$nin"]:
                    return False
                if "$ne" in val and doc_val == val["$ne"]:
                    return False
                if "$gt" in val and not (doc_val is not None and doc_val > val["$gt"]):
                    return False
                if "$gte" in val and not (doc_val is not None and doc_val >= val["$gte"]):
                    return False
                if "$lt" in val and not (doc_val is not None and doc_val < val["$lt"]):
                    return False
                if "$lte" in val and not (doc_val is not None and doc_val <= val["$lte"]):
                    return False
            else:
                if doc.get(key) != val:
                    return False
        return True

    async def find_one(self, query: Optional[Dict[str, Any]] = None) -> Optional[Dict[str, Any]]:
        query = query or {}
        items = self.store.data.get(self.name, [])
        for doc in items:
            if self._matches(doc, query):
                return dict(doc)
        return None

    def find(self, query: Optional[Dict[str, Any]] = None) -> LocalCursor:
        query = query or {}
        items = self.store.data.get(self.name, [])
        matches = [dict(doc) for doc in items if self._matches(doc, query)]
        return LocalCursor(matches)

    async def insert_one(self, document: Dict[str, Any]):
        doc = dict(document)
        if "_id" not in doc:
            doc["_id"] = str(uuid.uuid4())
        if "created_at" not in doc:
            doc["created_at"] = datetime.utcnow().isoformat()
        if "updated_at" not in doc:
            doc["updated_at"] = doc["created_at"]
        self.store.data.setdefault(self.name, []).append(doc)
        self.store.save()
        class InsertResult:
            def __init__(self, inserted_id):
                self.inserted_id = inserted_id
        return InsertResult(doc["_id"])

    async def insert_many(self, documents: List[Dict[str, Any]]):
        ids = []
        for d in documents:
            res = await self.insert_one(d)
            ids.append(res.inserted_id)
        class ManyResult:
            def __init__(self, ids):
                self.inserted_ids = ids
        return ManyResult(ids)

    async def update_one(self, query: Dict[str, Any], update: Dict[str, Any]):
        items = self.store.data.get(self.name, [])
        matched = 0
        modified = 0
        for doc in items:
            if self._matches(doc, query):
                matched = 1
                if "$set" in update:
                    for k, v in update["$set"].items():
                        doc[k] = v
                    doc["updated_at"] = datetime.utcnow().isoformat()
                    modified = 1
                if "$unset" in update:
                    for k in update["$unset"]:
                        doc.pop(k, None)
                    modified = 1
                break
        if modified:
            self.store.save()
        class UpdateResult:
            def __init__(self, m, mod):
                self.matched_count = m
                self.modified_count = mod
        return UpdateResult(matched, modified)

    async def delete_one(self, query: Dict[str, Any]):
        items = self.store.data.get(self.name, [])
        deleted = 0
        for i, doc in enumerate(items):
            if self._matches(doc, query):
                del items[i]
                deleted = 1
                break
        if deleted:
            self.store.save()
        class DeleteResult:
            def __init__(self, c):
                self.deleted_count = c
        return DeleteResult(deleted)

    async def count_documents(self, query: Optional[Dict[str, Any]] = None) -> int:
        query = query or {}
        items = self.store.data.get(self.name, [])
        return sum(1 for doc in items if self._matches(doc, query))


class LocalDocumentStore:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.data: Dict[str, List[Dict[str, Any]]] = {}
        self.load()

    def load(self):
        if os.path.exists(self.file_path):
            try:
                with open(self.file_path, "r", encoding="utf-8") as f:
                    self.data = json.load(f)
            except Exception as e:
                logger.error(f"Failed to load local DB: {e}")
                self.data = {}
        else:
            self.data = {}

    def save(self):
        try:
            with open(self.file_path, "w", encoding="utf-8") as f:
                json.dump(self.data, f, indent=2, default=str)
        except Exception as e:
            logger.error(f"Failed to save local DB: {e}")

    def __getitem__(self, name: str) -> LocalCollection:
        return LocalCollection(name, self)


class DatabaseManager:
    def __init__(self):
        self.is_atlas: bool = False
        self.client = None
        self.db = None
        self.local_store = None

    async def connect(self):
        if settings.MONGODB_URL:
            try:
                from motor.motor_asyncio import AsyncIOMotorClient
                self.client = AsyncIOMotorClient(
                    settings.MONGODB_URL,
                    serverSelectionTimeoutMS=3000
                )
                # Test connection
                await self.client.admin.command('ping')
                self.db = self.client[settings.MONGODB_DB_NAME]
                self.is_atlas = True
                logger.info("Connected successfully to MongoDB Atlas")
                return
            except Exception as e:
                logger.warning(f"MongoDB Atlas connection failed: {e}. Falling back to Local Document Store.")
        
        # Local Document Store Fallback
        db_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "db.json")
        self.local_store = LocalDocumentStore(db_file)
        self.db = self.local_store
        self.is_atlas = False
        logger.info(f"Using Local Document Store at {db_file}")

    def get_collection(self, collection_name: str):
        if self.db is None:
            db_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "db.json")
            self.local_store = LocalDocumentStore(db_file)
            self.db = self.local_store
        return self.db[collection_name]

db_manager = DatabaseManager()

def get_db():
    return db_manager
