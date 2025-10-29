from typing import List, Literal, Optional
from pydantic import BaseModel


class Header(BaseModel):
    status: Literal["Draft", "Approved", "In Review", "Deprecated"]
    author: str
    version: str
    last_updated: str


class Problem(BaseModel):
    problem_statement: str
    user_personas_and_scenarios: List[str]


class SuccessMetric(BaseModel):
    goal: str
    key_performance_indicator: str
    target: str


class UserStory(BaseModel):
    story_id: str
    description: str
    acceptance_criteria: List[str]


class Epic(BaseModel):
    title: str
    stories: List[UserStory]


class NonFunctionalRequirements(BaseModel):
    performance: Optional[str]
    security: Optional[str]
    accessibility: Optional[str]
    scalability: Optional[str]


class Milestone(BaseModel):
    version: str
    target_date: str
    description: str


class Scope(BaseModel):
    out_of_scope_for_v1: List[str]
    future_work: List[str]


class AppendixItem(BaseModel):
    item_type: Literal["Open Question", "Dependency"]
    description: str


class ProductRequirementsDocument(BaseModel):
    product_name: str
    header: Header
    executive_summary_and_vision: str
    problem: Problem
    goals_and_success_metrics: List[SuccessMetric]
    functional_requirements: List[Epic]
    non_functional_requirements: NonFunctionalRequirements
    release_plan: List[Milestone]
    scope: Scope
    appendix: List[AppendixItem]