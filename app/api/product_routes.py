from fastapi import APIRouter, Depends, Request

from app.middleware.auth_middleware import get_current_user

from app.schemas.product_schema import ProductResponse

from app.services.product_service import fetch_products
from app.services.permission_checker import PermissionChecker

router = APIRouter(tags=["Products"])


@router.get("/products", response_model=list[ProductResponse], dependencies=[Depends(PermissionChecker(["view_inventory"]))], summary="Get Products", description="""
            Retrieve available products.

            Requires:

            - view_inventory permission

            Returns product catalog information.""")

def get_products(request: Request, current_user=Depends(get_current_user)):

    authorization_header = request.headers.get("Authorization")

    token = authorization_header.replace("Bearer ", "")

    return fetch_products(token)