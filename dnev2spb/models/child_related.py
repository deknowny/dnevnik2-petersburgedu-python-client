from __future__ import annotations

import typing

import pydantic


class ChildRelated(pydantic.BaseModel):
    firstname: str
    middlename: str
    surname: str
    educations: typing.List[ChildRelatedEducation]
    action_payload: ChildRelatedActionPayload
    identity: ChildRelatedIdentity


class ChildRelatedActionPayload(pydantic.BaseModel):
    can_apply_for_distance: bool
    can_print: typing.Optional[bool]


class ChildRelatedIdentity(pydantic.BaseModel):
    id: int


class ChildRelatedEducation(pydantic.BaseModel):
    distance_education: bool
    distance_education_updated_at: typing.Optional[str]
    education_id: int
    group_id: int
    group_name: str
    institution_id: int
    institution_name: str
    is_active: typing.Optional[bool]
    jurisdiction_id: int
    jurisdiction_name: str
    parent_email: typing.Optional[str]
    parent_firstname: typing.Optional[str]
    parent_middlename: typing.Optional[str]
    parent_surname: typing.Optional[str]
    push_subscribe: str


ChildRelated.update_forward_refs()
