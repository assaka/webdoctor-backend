from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from scraper import scrape_website_data
from lighthouse import run_lighthouse
from gemini_analysis import analyze_keywords_with_gemini

app = FastAPI()

class URLRequest(BaseModel):
    url: str

app = FastAPI(
    title="AI GTM Audit",
    description="Audit websites and Google Tag Manager setup",
    version="1.0.0"
)

# # ✅ This must come immediately after app is created
# app.include_router(gtm.router, prefix="/gtm", tags=["GTM Audit"])

@app.get("/")
async def root():
    return {"message": "Welcome to the AI GTM Audit API!"}

@app.post("/analyze")
async def analyze(request: URLRequest):
    try:
        # 1. Scrape SEO + Cookies + GTM data
        scraped = scrape_website_data(request.url)

        # 2. Run Lighthouse audit (Headless Chrome required)
        lighthouse_result = run_lighthouse(request.url)

        # 3. Use Gemini to analyze keywords in meta and content
        keyword_analysis = analyze_keywords_with_gemini(scraped.get("keywords", []))

        return {
            "seo_meta": scraped["seo_meta"],
            "cookies": scraped["cookies"],
            "datalayers": scraped["datalayers"],
            "lighthouse": lighthouse_result,
            "keyword_insights": keyword_analysis,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
