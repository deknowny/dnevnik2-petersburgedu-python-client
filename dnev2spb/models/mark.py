import typing

import pydantic


class Mark(pydantic.BaseModel):
    date: str
    education_id: int
    estimate_comment: typing.Optional[str]
    estimate_type_code: int
    estimate_type_name: str
    estimate_value_code: str
    estimate_value_name: str
    id: int
    lesson_id: typing.Optional[int]
    subject_id: int
    subject_name: str
