from pydantic import BaseModel
from openai import OpenAI
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import uvicorn


class Relationship(BaseModel):
    closeness: float
    attraction: float
    respect: float
    harmony: float
    commitment: float
    show_summary: float
    summary_text: str


app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)


@app.post("/v1/summary")
async def get_request_data(request: Request):
    request_data = await request.json()

    """Get request data and send to OpenAI client with predefined type."""
    client = OpenAI(base_url="http://34.85.251.9:8000/v1", api_key="gazai0507")

    # Create completion request
    completion = client.beta.chat.completions.parse(
        model="shisa-ai/shisa-v2-llama3.3-70b",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": request_data["prompt"]},
        ],
        response_format=Relationship,
    )

    message = completion.choices[0].message
    print(message)
    assert message.parsed
    print("Closeness:", message.parsed.closeness)
    print("Attraction:", message.parsed.attraction)
    print("Respect:", message.parsed.respect)
    print("Harmony:", message.parsed.harmony)
    print("Commitment:", message.parsed.commitment)
    print("Show Summary:", message.parsed.show_summary)
    print("Summary Text:", message.parsed.summary_text)

    return {
        "closeness": message.parsed.closeness,
        "attraction": message.parsed.attraction,
        "respect": message.parsed.respect,
        "harmony": message.parsed.harmony,
        "commitment": message.parsed.commitment,
        "show_summary": message.parsed.show_summary,
        "summary_text": message.parsed.summary_text,
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8081)
