from fastapi import APIRouter

from adan.services import PricesService

prices_router = APIRouter()
ps = PricesService()


@prices_router.get("/assets")
def get_assets():
    return ps.get_assets()


@prices_router.get("/historical")
def get_historical():
    return ps.get_historical()
