from typing import Dict, List

from pydantic import BaseModel, EmailStr, model_validator


class Patient(BaseModel):
    name: str
    email: EmailStr
    age: int
    weight: float
    married: bool
    allergies: List[str]
    contact_details: Dict[str, str]

    @model_validator(mode="after")
    def validate_emergency_contact(self):
        if self.age > 60 and "emergency" not in self.contact_details:
            raise ValueError(
                "Patient older than 60 must have emergency number in their contact"
            )
        return self


def update_patient_data(patient: Patient):

    print(patient.name)
    print(patient.age)
    print(patient.allergies)
    print(patient.married)
    print("updated")


if __name__ == "__main__":
    patient_info = {
        "name": "nitish",
        "email": "abc@gmail.com",
        "age": "30",
        "weight": 75.2,
        "married": True,
        "allergies": ["pollen", "dust"],
        "contact_details": {"phone": "2353462"},
    }

    patient1 = Patient(**patient_info)
    update_patient_data(patient1)
