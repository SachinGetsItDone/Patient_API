import json
from typing import Annotated, Literal, Optional

from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import JSONResponse

from pydantic import BaseModel, Field, computed_field


class Patient(BaseModel):
    id: Annotated[str, Field(..., description="ID of the patient")]
    name: Annotated[
        str, Field(..., description="Name of the Patient", min_length=2, max_length=50)
    ]
    age: Annotated[int, Field(..., description="Age of the patient", gt=0, lt=120)]
    height: Annotated[
        float, Field(..., description="Height of the patient in metres", gt=0)
    ]
    weight: Annotated[float, Field(gt=0)]
    gender: Annotated[
        Literal["Male", "Female", "Others"],
        Field(..., description="Gender of the patient"),
    ]
    contact: Annotated[str, Field(min_length=10, max_length=10)]
    address: str

    @computed_field
    @property
    def bmi(self) -> float:
        return round(self.weight / (self.height**2), 2)

    @computed_field
    @property
    def verdict(self) -> str:
        if self.bmi < 18.5:
            return "Underweight"
        elif self.bmi < 30:
            return "Normal"
        else:
            return "Overweight"


class PatientUpdate(BaseModel):
    name: Annotated[Optional[str], Field(default=None)]
    age: Annotated[Optional[int], Field(default=None)]
    height: Annotated[Optional[float], Field(default=None)]
    weight: Annotated[Optional[float], Field(default=None)]
    gender: Annotated[
        Optional[Literal["Male", "Female", "Others"]],
        Field(default=None),
    ]


app = FastAPI()


def load_data():
    with open("patients.json", "r") as file:
        data = json.load(file)
    return {p["id"].lower(): p for p in data["patients"]}


def save_data(data):
    with open("patients.json", "w") as f:
        json.dump({"patients": list(data.values())}, f, indent=2)


@app.get("/")
def hello():
    return {"message": "Sachin ka API chal raha hai!"}


@app.get("/about")
def about():
    return {"message": "This is a simple FastAPI application."}


@app.get("/view")
def view():
    data = load_data()
    return {"data": list(data.values())}


@app.get("/patients/{patient_id}")
def view_patient(patient_id: str):
    data = load_data()

    if patient_id in data:
        return data[patient_id]
    else:
        raise HTTPException(status_code=404, detail="Patient Not Found")


@app.get("/sort")
def sort_patient(
    sort_by: str = Query(..., description="Sort on the basis of height, age or bmi"),
    order: str = Query("asc", description="sort in asc or desc order"),
):
    valid_fields = ["height", "age", "bmi"]

    if sort_by not in valid_fields:
        raise HTTPException(
            status_code=400, detail=f"Invalid field select from {valid_fields}"
        )

    if order not in ["asc", "desc"]:
        raise HTTPException(status_code=400, detail="Invalid Request")

    data = load_data()

    sort_order = order == "desc"

    sorted_data = sorted(
        data.values(), key=lambda x: x.get(sort_by, 0), reverse=sort_order
    )

    return sorted_data


@app.post("/create")
def create_patient(patient: Patient):
    data = load_data()
    if patient.id in data:
        raise HTTPException(status_code=400, detail="Patient already exists")

    data[patient.id] = patient.model_dump(exclude={"id"})
    save_data(data)

    return JSONResponse(status_code=201, content={"message": "Patient Created"})


@app.put("/edit/{patient_id}")
def update_patient(patient_id: str, patient_update: PatientUpdate):
    data = load_data()

    if patient_id not in data:
        raise HTTPException(status_code=404, detail="Patient not found")

    existing_patient_info = data[patient_id]
    updated_patient_info = patient_update.model_dump(
        exclude_unset=True
    )  # creating disctionary

    for key, value in updated_patient_info.items():
        existing_patient_info[key] = value
    existing_patient_info["id"] = patient_id
    pydantic_obj = Patient(**existing_patient_info)
    existing_patient_info["bmi"] = pydantic_obj.bmi
    existing_patient_info["verdict"] = pydantic_obj.verdict
    data[patient_id] = existing_patient_info
    save_data(data)

    return JSONResponse(status_code=200, content={"message": "Patient Updated"})


@app.delete("/delete/{patient_id}")
def delete_patient(patient_id: str):
    data = load_data()

    if patient_id not in data:
        raise HTTPException(status_code=404, detail="Patient not found")

    del data[patient_id]

    save_data(data)

    return JSONResponse(status_code=200, content={"message": "Patient deleted"})
