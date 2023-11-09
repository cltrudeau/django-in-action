# RiffMates/home/api.py
from ninja import Router

router = Router()


@router.get("/")
def home(request):
    return "RiffMates rocks!"


@router.get("/version/")
def version(request):
    data = {
        "version": "0.0.1",
    }
    return data
