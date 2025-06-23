from pydantic import BaseModel

class ItemClass(BaseModel):
    Shop: list = []
    House: list = []
    Makelist: list = []
    Processing: list = []
    Alchemy: list = []
    Node: list = []
    Cooking: list = []
    Fishing: list = []
    Gathering: list = []

    def __getitem__(self, key):
        return getattr(self, key)