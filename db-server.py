import json
import os
from typing import Dict, Any, List
from mcp.server.mcpserver import MCPServer

mcp = MCPServer("database-manager")

JSON_DB_PATH = os.path.abspath("records.json")

if not os.path.exists(JSON_DB_PATH):
    with open(JSON_DB_PATH, "w") as f:
        json.dump([], f)

@mcp.tool()
def add_record_json(record: Dict[str, Any]) -> str:
    """Adds a new key-value dictionary record into local JSON database."""
    with open(JSON_DB_PATH, "r+") as f:
        data = json.load(f)
        data.append(record)
        f.seek(0)
        json.dump(data, f, indent=2)
        f.truncate()
    return f"Success: record added. Total count: {len(data)}"

@mcp.tool()
def list_records_json() -> str:
    """Retrieves all records stored in local JSON database."""
    with open(JSON_DB_PATH, "r") as f:
        data = json.load(f)
    return json.dumps(data, indent=2)

@mcp.tool()
def add_record_mongodb(database: str, collection: str, document: Dict[str, Any], mongo_uri: str = "mongodb://localhost:27017") -> str:
    """Inserts a document into specified MongoDB database and collection."""
    from pymongo import MongoClient
    client = MongoClient(mongo_uri)
    db = client[database]
    col = db[collection]
    res = col.insert_one(document)
    client.close()
    return f"Success: MongoDB inserted _id: {str(res.inserted_id)}"

if __name__ == "__main__":
    mcp.run();