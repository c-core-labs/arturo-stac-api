"""FastAPI application."""
import os

from stac_api.api import create_app
from stac_api.config import ApiSettings

os.environ["AWS_REQUEST_PAYER"] = "requester"


settings = ApiSettings(
    stac_api_extensions=["context", "fields", "query", "sort", "transaction"],
    add_ons=["tiles"],
    default_includes={
        "id",
        "type",
        "geometry",
        "bbox",
        "links",
        "assets",
        "properties.datetime",
        "properties.updated",
        "properties.created",
        "properties.gsd",
        "properties.eo:bands",
        "properties.proj:epsg",
        "properties.naip:quadrant",
        "properties.naip:cell_id",
        "properties.naip:statename",
        "properties.naip:utm_zone",
        "properties.naip:quad_location",
    },
)
app = create_app(settings=settings)
