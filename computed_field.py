from typing import Annotated, Dict, List

from pydantic import BaseModel, EmailStr, Field, computed_field


class Patient(BaseModel):
    name: str
    email: EmailStr
    age: int
    weight: float
    height: Annotated[float, Field(gt=0)]
    married: bool
    allergies: List[str]
    contact_details: Dict[str, str]

    @computed_field
    @property
    def bmi(self) -> float:
        return self.weight / (self.height**2)


def update_patient_data(patient: Patient):
    print(patient.name)
    print(patient.age)
    print(patient.allergies)
    print(patient.married)
    print("Bmi", patient.bmi)
    print("updated")


if __name__ == "__main__":
    patient_info = {
        "name": "nitish",
        "email": "abc@gmail.com",
        "age": "30",
        "weight": 75.2,
        "height": 1.75,
        "married": True,
        "allergies": ["pollen", "dust"],
        "contact_details": {"phone": "2353462"},
    }

    patient1 = Patient(**patient_info)
    update_patient_data(patient1)
