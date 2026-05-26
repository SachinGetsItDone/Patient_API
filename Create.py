from typing import Annotated, Literal
from pydantic import BaseModel, Field, computed_field


class Patient(BaseModel):
    id: Annotated[str, Field(..., description='ID of the patient')]
    name: Annotated[str, Field(..., description='Name of the Patient', min_length=2, max_length=50)]
    age: Annotated[int, Field(..., description="Age of the patient", gt=0, lt=120)]
    height: Annotated[float, Field(..., description="Height of the patient in metres", gt=0)]
    weight: Annotated[float, Field(gt=0)]
    gender: Annotated[Literal['Male', 'Female', 'Others'], Field(..., description='Gender of the patient')]
    contact: Annotated[str, Field(min_length=10, max_length=10)]
    address: str

    @computed_field
    @property
    def bmi(self) -> float:
        return self.weight / (self.height ** 2)
