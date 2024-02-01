from typing import Generic, TypeVar

from app.db.base_class import Base

ModelType = TypeVar("ModelType", bound=Base)


class DBBase(Generic[ModelType]):
    def __init__(self, model: type[ModelType]):
        self.model = model
