import requests

from fastapi import HTTPException

from app.core.config import settings


def fetch_products(token: str):

    try:

        response = requests.get(f"{settings.PROJECT4_BASE_URL}/products", headers={"Authorization": f"Bearer {token}"}, timeout=5)

        response.raise_for_status()

        return response.json()

    except requests.exceptions.RequestException as error:

        raise HTTPException(status_code=503, detail=f"Product service unavailable: {str(error)}")
    
    
def fetch_product_by_id(product_id: int, token: str):

    products = fetch_products(token)

    for product in products:

        if product["id"] == product_id:

            return product

    return None
