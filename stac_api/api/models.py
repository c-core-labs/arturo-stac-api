"""api request/response models"""

import abc
from dataclasses import dataclass
from typing import Dict, Optional, Type, Union

from fastapi import Body, Path

from pydantic import BaseModel, create_model
from pydantic.fields import UndefinedType
from stac_api.config import ApiExtensions, ApiSettings


def _create_request_model(
    model: Type[BaseModel], settings: ApiSettings
) -> Type[BaseModel]:
    """Create a pydantic model for validating a request body"""

    fields = {}
    for (k, v) in model.__fields__.items():
        if k == "query":
            if not settings.api_extension_is_enabled(ApiExtensions.query):
                continue

        if k == "sortby":
            if not settings.api_extension_is_enabled(ApiExtensions.sort):
                continue

        if k == "field":
            if not settings.api_extension_is_enabled(ApiExtensions.fields):
                continue

        field_info = v.field_info
        body = Body(
            None
            if isinstance(field_info.default, UndefinedType)
            else field_info.default,
            default_factory=field_info.default_factory,
            alias=field_info.alias,
            alias_priority=field_info.alias_priority,
            title=field_info.title,
            description=field_info.description,
            const=field_info.const,
            gt=field_info.gt,
            ge=field_info.ge,
            lt=field_info.lt,
            le=field_info.le,
            multiple_of=field_info.multiple_of,
            min_items=field_info.min_items,
            max_items=field_info.max_items,
            min_length=field_info.min_length,
            max_length=field_info.max_length,
            regex=field_info.regex,
            extra=field_info.extra,
        )
        fields[k] = (v.outer_type_, body)
    return create_model(model.__name__, **fields, __base__=model)


@dataclass  # type:ignore
class APIRequest(abc.ABC):
    """Generic API Request base class"""

    @abc.abstractmethod
    def kwargs(self) -> Dict:
        """Transform api request params into format which matches the signature of the endpoint"""
        ...


@dataclass  # type:ignore
class CollectionUri(APIRequest):
    """Delete collection"""

    collectionId: str = Path(..., description="Collection ID")

    def kwargs(self) -> Dict:
        """kwargs"""
        return {"id": self.collectionId}


@dataclass
class ItemUri(CollectionUri):
    """Delete item"""

    itemId: str = Path(..., description="Item ID")

    def kwargs(self) -> Dict:
        """kwargs"""
        return {"id": self.itemId}


@dataclass
class EmptyRequest(APIRequest):
    """Empty request"""

    def kwargs(self) -> Dict:
        """kwargs"""
        return {}


@dataclass
class ItemCollectionUri(CollectionUri):
    """Get item collection"""

    limit: int = 10
    token: str = None

    def kwargs(self) -> Dict:
        """kwargs"""
        return {"id": self.collectionId, "limit": self.limit, "token": self.token}


@dataclass
class SearchGetRequest(APIRequest):
    """GET search request"""

    collections: Optional[str] = None
    ids: Optional[str] = None
    bbox: Optional[str] = None
    datetime: Optional[Union[str]] = None
    limit: Optional[int] = 10
    query: Optional[str] = None
    token: Optional[str] = None
    fields: Optional[str] = None
    sortby: Optional[str] = None

    def kwargs(self) -> Dict:
        """kwargs"""
        return {
            "collections": self.collections.split(",")
            if self.collections
            else self.collections,
            "ids": self.ids.split(",") if self.ids else self.ids,
            "bbox": self.bbox.split(",") if self.bbox else self.bbox,
            "datetime": self.datetime,
            "limit": self.limit,
            "query": self.query,
            "token": self.token,
            "fields": self.fields.split(",") if self.fields else self.fields,
            "sortby": self.sortby.split(",") if self.sortby else self.sortby,
        }


class Login(BaseModel):
    username: str
    password: str

    class Config:
        schema_extra = {"example": {"username": "TestAdmin", "password": "TestAdmin",}}

