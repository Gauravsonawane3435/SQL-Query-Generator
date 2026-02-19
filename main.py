import os
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import google.generativeai as genai
from dotenv import load_dotenv
from a2wsgi import ASGIMiddleware

# Load environment variables
load_dotenv()

app = FastAPI(title="SQL Query Generator API")

# WSGI Adaptor for PythonAnywhere
wsgi_app = ASGIMiddleware(app)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure Gemini
load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")
if not API_KEY:
    # Fallback to the hardcoded key if .env is missing
    API_KEY = "AIzaSyDIsxp11FnfInfpFCSWWKYPt6gjK0Pkv50"

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

class QueryRequest(BaseModel):
    prompt: str
    dialect: str = "SQL"

class QueryResponse(BaseModel):
    sql: str
    explanation: str

@app.post("/generate", response_model=QueryResponse)
async def generate_sql(request: QueryRequest):
    if not request.prompt:
        raise HTTPException(status_code=400, detail="Prompt is required")
    
    # Try multiple model names based on your environment's availability
    model_names_to_try = [
        "models/gemini-1.5-flash",
        "models/gemini-2.0-flash",
        "models/gemini-2.5-flash",
        "models/gemini-pro",
        "gemini-1.5-flash",
        "gemini-pro"
    ]
    
    system_prompt = f"""
    You are an expert SQL specialized in generating perfect, optimized, and secure SQL queries.
    Convert the following natural language request into a valid {request.dialect} query.
    
    Return your response in EXACTLY this JSON format:
    {{
        "sql": "YOUR_SQL_QUERY_HERE",
        "explanation": "A_BRIEF_EXPLANATION_HERE"
    }}
    
    IMPORTANT: 
    - Use standard {request.dialect} syntax.
    - Provide ONLY the JSON object. 
    - Do not include any markdown formatting like ```json.
    - If the request is not related to SQL, return an error message in the SQL field.

    Request: {request.prompt}
    """
    
    last_error = None
    for model_name in model_names_to_try:
        try:
            print(f"DEBUG: Attempting to use model: {model_name}")
            current_model = genai.GenerativeModel(model_name)
            response = current_model.generate_content(system_prompt)
            
            # Check if response has valid parts (safety filters can block it)
            if not response.parts:
                print(f"DEBUG: Model {model_name} returned empty parts (Safety Filter?)")
                continue

            text = response.text.strip()
            print(f"DEBUG: AI Response from {model_name}: {text[:100]}...")
            
            # Robust JSON extraction
            if "```" in text:
                import re
                match = re.search(r'```(?:json)?\s*(.*?)\s*```', text, re.DOTALL)
                if match:
                    text = match.group(1).strip()

            try:
                import json
                data = json.loads(text)
                return QueryResponse(
                    sql=data.get("sql", text), 
                    explanation=data.get("explanation", "Generated SQL based on your instructions.")
                )
            except json.JSONDecodeError:
                return QueryResponse(
                    sql=text if text else "Error generating SQL",
                    explanation="Generated SQL, but formatting was slightly off."
                )
        except Exception as e:
            last_error = e
            print(f"DEBUG: Model {model_name} failed: {str(e)[:100]}...")
            continue
            
    # If all models failed
    import traceback
    error_detail = traceback.format_exc()
    print(f"CRITICAL ERROR: All models failed. Last error:\n{error_detail}")
    raise HTTPException(status_code=500, detail=f"AI Service Error: {str(last_error)}")

# Mount static files
app.mount("/", StaticFiles(directory="static", html=True), name="static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
