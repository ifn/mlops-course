from typing import List

from fastapi import APIRouter, HTTPException, status, Depends

from app.database.database import get_session
from app.models.billing.transaction import FinancialTransaction
from app.services.crud.billing import transaction as TransactionService


transaction_router = APIRouter()


@transaction_router.get("/", response_model=List[FinancialTransaction])
async def retrieve_all_transactions(
    session=Depends(get_session),
) -> List[FinancialTransaction]:
    return TransactionService.get_all_transactions(session)


@transaction_router.get("/{id}", response_model=FinancialTransaction)
async def retrieve_transaction(
    id: int,
    session=Depends(get_session),
) -> FinancialTransaction:
    transaction = TransactionService.get_transaction_by_id(session, id)
    if not transaction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="FinancialTransaction with supplied ID does not exist",
        )
    return transaction


@transaction_router.post("/new")
async def create_transaction(
    transaction_req: FinancialTransaction,
    session=Depends(get_session),
) -> FinancialTransaction:
    transaction: FinancialTransaction = TransactionService.create_transaction(
        session,
        transaction_req,
    )
    return transaction
