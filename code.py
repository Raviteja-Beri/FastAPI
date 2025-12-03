from fastapi import FastAPI, Depends, HTTPException, Security
from fastapi.security import APIKeyHeader
from fastapi.middleware.cors import CORSMiddleware 

app = FastAPI(
    title="Company Type API",
    description="API to get company types by country.",
    version="1.0"
)

API_KEY = "key123456"

api_key_header = APIKeyHeader(name="Y-api_key", auto_error=False)

def verify_api_key(api_key: str = Security(api_key_header)):
    if api_key != API_KEY:
        raise HTTPException(status_code=403, detail="Could not validate API key")
    return api_key

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["*"],
)

COMPANY_TYPES = {
    "USA": ["LLC", "C-corp", "S-corp", "Partnership"],
    "India": ["PVT.LTD", "LTD", "Partnership", "Sole-Propreitorship", "LLC"],
    "United Kingdom": ["LTD", "PLL", "LLP", "LP", "Sole Trader"]
}

@app.get("/company-types")
def get_company_types(country: str, auth: str = Depends(verify_api_key)):
    country = country.strip()
    if country not in COMPANY_TYPES:
        raise HTTPException(status_code=404, detail="Country not found")

    return {
        "country": country,
        "company-types": COMPANY_TYPES[country]
    }



# Invoke-WebRequest `
#   -Uri "http://127.0.0.1:8000/company-types?country=India" `
#   -Headers @{ "Y-api_key" = "key123456" } `
#   -Method GET

# curl.exe -H "Y-api_key: key123456" "http://127.0.0.1:8000/company-types?country=India"

# Analyze "API-Security": sqp_38aa8e133bb58d9d15513fa38a460945547b59dd

# docker run --rm `
#   -e SONAR_HOST_URL="http://host.docker.internal:9000" `
#   -e SONAR_LOGIN="sqp_38aa8e133bb58d9d15513fa38a460945547b59dd" `
#   -v "$PWD:/usr/src" `
#   sonarsource/sonar-scanner-cli
