from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(
    title="Analytic BSD Verification Engine",
    description="API para cálculo de invariantes aritméticos de curvas elípticas.",
    version="0.1.0"
)

class CurveInput(BaseModel):
    a: float
    b: float

@app.get("/")
def home():
    return {
        "status": "online",
        "engine": "Analytic BSD Verification Engine",
        "version": "0.1.0"
    }

@app.post("/verify-curve")
def verify_curve(curve: CurveInput):
    delta = -16 * (4 * (curve.a ** 3) + 27 * (curve.b ** 2))
    
    is_valid = delta != 0
    
    if not is_valid:
        raise HTTPException(
            status_code=400, 
            detail="Curva inválida: O discriminante não pode ser zero (curva singular)."
        )
    
    return {
        "equation": f"y^2 = x^3 + ({curve.a})x + ({curve.b})",
        "parameters": {
            "a": curve.a,
            "b": curve.b
        },
        "invariants": {
            "discriminant": delta,
            "is_smooth": is_valid
        },
        "status": "Curva elíptica válida. Pronta para processamento dos invariantes BSD."
    }
