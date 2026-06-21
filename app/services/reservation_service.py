import requests

from fastapi import HTTPException

from app.core.config import settings


def fetch_reservation_status(transaction_id: int, token: str):

    try:

        response = requests.get(f"{settings.PROJECT4_BASE_URL}/reservations/transaction/{transaction_id}", headers={"Authorization": f"Bearer {token}"}, timeout=10)

        if response.status_code == 404:

            return None

        response.raise_for_status()

        return response.json()

    except requests.RequestException as error:

        raise HTTPException(status_code=503, detail=f"Reservation service unavailable: {str(error)}")