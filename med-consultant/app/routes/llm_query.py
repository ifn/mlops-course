from typing import List

from fastapi import APIRouter, Body, HTTPException, status, Depends

from app.database.database import get_session
from app.models.llm_query import LLMQuery
from app.models.dialogue import Dialogue
from app.services.crud import llm_query as LLMQueryService
from app.services.crud import dialogue as DialogueService
from app.rabbitmq.client import publish_message


llm_query_router = APIRouter()


@llm_query_router.get("/", response_model=List[LLMQuery])
async def retrieve_all_llm_queries(
    session=Depends(get_session),
) -> List[LLMQuery]:
    return LLMQueryService.get_all_llm_queries(session)


@llm_query_router.get("/{id}", response_model=LLMQuery)
async def retrieve_llm_query(
    id: int,
    session=Depends(get_session),
) -> LLMQuery:
    llm_query = LLMQueryService.get_llm_query_by_id(session, id)
    if not llm_query:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="LLMQuery with supplied ID does not exist",
        )
    return llm_query


@llm_query_router.post("/new")
async def create_llm_query(
    llm_query_req: LLMQuery,
    session=Depends(get_session),
) -> LLMQuery:
    # TODO: refactor
    # Create dialogue if it is not passed in request
    if llm_query_req.dialogue_id is None:
        dialogue = Dialogue(user_id=llm_query_req.user_id)
        DialogueService.create_dialogue(session, dialogue)
        llm_query_req.dialogue_id = dialogue.id

    llm_query: LLMQuery = LLMQueryService.create_llm_query(session, llm_query_req)

    queue_name = "ml_task_queue"
    llm_query_js = llm_query.model_dump_json()
    publish_message(queue_name, llm_query_js)

    # create withdrawal

    return llm_query


@llm_query_router.delete("/{id}")
async def delete_llm_query(
    id: int,
    session=Depends(get_session),
) -> dict:
    res = LLMQueryService.delete_llm_query(session, id)
    if not res:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="LLMQuery with supplied ID does not exist",
        )
    return {"message": "LLMQuery deleted successfully"}
