from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from backend.model.rate_model import InterestRateModel

app = FastAPI()
model = InterestRateModel()
model.train("backend/data/mfi_dataset.csv")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class LoanRequest(BaseModel):
    loan_amount: int
    business_type: str
    location: str
    season: str
    repayment_history: float
    existing_debt_ratio: float

@app.post("/predict")
async def predict_rate(request: LoanRequest):
    try:
        default_prob = model.predict(request.model_dump())
        base_rate = 0.15
        risk_adjustment = default_prob * 0.5
        final_rate = (base_rate + risk_adjustment) * 100
        
        return {
            "default_probability": round(default_prob, 3),
            "interest_rate": round(final_rate, 1),
            "components": {
                "base_rate": base_rate * 100,
                "risk_premium": round(risk_adjustment * 100, 1)
            }
        }
    except Exception as e:
        return {"error": str(e)}