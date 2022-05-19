from typing import List

from api.statistics.recommender.recommendation_queries import \
    get_number_of_recommendations_monthly
from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()


class RecommendationNumbers(BaseModel):
    service_id: int
    count: int
    month: int = None
    year: int = None


class ServiceList(BaseModel):
    service_ids: List[int]


@router.post("/statistics/recommendations/monthly", response_model=List[RecommendationNumbers], tags=['statistics'])
def get_monthly_number_of_recommendations(service_list: ServiceList):
    return [RecommendationNumbers(service_id=recommendation_id['service_id'],
                                  count=recommendation_count,
                                  month=recommendation_id['month'],
                                  year=recommendation_id['year'])
            for recommendation_id, recommendation_count
            in get_number_of_recommendations_monthly(service_list.service_ids)]
