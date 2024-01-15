# RiffMates/promoters/api.py
from django.shortcuts import get_object_or_404
from ninja import ModelSchema, Router
from promoters.models import Promoter

router = Router()


class PromoterSchema(ModelSchema):
    class Meta:
        model = Promoter
        fields = ["id", "full_name", "birth", "death"]


@router.get("/promoters/", response=list[PromoterSchema])
def promoters(request):
    return Promoter.objects.all()


@router.get("/promoter/{promoter_id}/", response=PromoterSchema)
def promoter(request, promoter_id):
    promoter = get_object_or_404(Promoter, id=promoter_id)
    return promoter
