from __future__ import annotations
from typing import Any
import firebase_admin as Firebase
from firebase_admin import firestore, App
# from google.cloud.firestore_v1.collection import CollectionReference
from google.cloud.firestore_v1.client import Client
import os
import json

def json_files() -> list[str]:
	temp = []
	for folder in os.environ["Path"].split(';'):
		try:
			temp.extend([os.path.join(folder, f) for f in os.listdir(folder) if f.endswith(".json") and f.count("firebase")])
		except Exception:
			pass
	return temp

def get_credentials_path(project_id: str) -> str:
	for file in json_files():
		with open(file, 'r') as f:
			if json.load(f).get('project_id', None) == project_id:
				return file 

class Database:
	def __init__(self, project_id: str, collection: str | None = None) -> None:
		self.__project_id__ = project_id
		self.__collection__ = collection
		if collection is not None:
			self.__create__()
		
	def __create__(self, collection: str | None = None):
		if collection is not None:
			self.__collection__ = collection
		self.__database_url__ = f'https://{self.__project_id__}.firebaseio.com'
		self.__credentials_path__ = get_credentials_path(self.__project_id__)
		self.__credentials__ = Firebase.credentials.Certificate(self.__credentials_path__)
		self.__app__: App = Firebase.initialize_app(self.__credentials__, {'databaseURL':self.__database_url__, 'project_id': self.__project_id__})
		self.__database__: Client = firestore.client()

	def collection(self, collection: str | None = None):
		return self.__database__.collection(self.__collection__) if collection is None else self.__database__.collection(collection)

	def set(self, document: str, data: dict, collection: str | None = None) -> None:
		self.collection(collection).document(document).set(data)

	def get(self,  document: str, collection: str | None = None) -> dict[str, Any] | None:
		return self.collection(collection).document(document).get().to_dict()

	def getAll(self, collection: str | None = None):
		for doc in self.collection(collection).stream():
			yield doc.to_dict()



if __name__ == "__main__":
	database = Database("dtu-server-test", "Test2")
	
	database.set("doc1", {"tal": 8, "bool": False, "Str": "sf", "float": 4.3})
	print(database.get("doc1"))

	for v in database.getAll("Test"):
		print(v)