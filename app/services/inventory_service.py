import requests

from fastapi import HTTPException

from app.core.config import settings


def create_inventory_reservation(payload: dict, token: str):

    try:

        response = requests.post(f"{settings.PROJECT4_BASE_URL}/events/transaction-created", json=payload, headers={"Authorization": f"Bearer {token}"}, timeout=10)

        response.raise_for_status()

        return response.json()

    except requests.RequestException as error:

        raise HTTPException(status_code=503, detail=f"Inventory service unavailable: {str(error)}")