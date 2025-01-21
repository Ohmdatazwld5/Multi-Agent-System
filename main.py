from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from transformers import pipeline
from typing import Optional

# Create an instance of the FastAPI application
app = FastAPI()

# Load models using Hugging Face Transformers
gpt_model = pipeline("text-generation", model="google/flan-t5-small")
sentiment_model = pipeline("sentiment-analysis")

# Define a Pydantic model for user queries
class UserQuery(BaseModel):
    query: str
    category: Optional[str] = None  # Optional field

# Define valid categories
VALID_CATEGORIES = ["task_planner", "knowledge", "sentiment"]

# Context management for maintaining session state
conversation_context = {}

@app.post("/chat")
async def chat(user_query: UserQuery):
    try:
        # Validate that query is not empty
        if not user_query.query.strip():
            raise HTTPException(status_code=400, detail="Query cannot be empty")

        # Convert the user's query to lowercase to standardize input
        query = user_query.query.lower()

        # If category is provided, validate it
        if user_query.category and user_query.category not in VALID_CATEGORIES:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid category. Must be one of: {', '.join(VALID_CATEGORIES)}"
            )

        # Intent classification if category is not provided
        if not user_query.category:
            user_query.category = intent_classifier(query)

        # Process based on category
        if user_query.category == "task_planner":
            response = task_planner_agent(query)
        elif user_query.category == "knowledge":
            response = knowledge_agent(query)
        elif user_query.category == "sentiment":
            response = sentiment_analysis_agent(query)
        else:
            raise HTTPException(status_code=400, detail="Invalid intent classification")

        # Update conversation context
        if "history" not in conversation_context:
            conversation_context["history"] = []
        conversation_context["history"].append({"query": query, "response": response})

        return {"response": response}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

def intent_classifier(query: str) -> str:
    """Classify the intent of the user's query."""
    if any(keyword in query for keyword in ["task", "plan", "steps"]):
        return "task_planner"
    elif any(keyword in query for keyword in ["what", "who", "when", "where", "why", "how"]):
        return "knowledge"
    elif any(keyword in query for keyword in ["feel", "happy", "sad", "angry"]):
        return "sentiment"
    return "knowledge"  # Default fallback

def task_planner_agent(query: str) -> str:
    """Simulate breaking down a task into subtasks."""
    return f"Task breakdown for: {query}\n1. Analyze requirements\n2. Plan approach\n3. Execute steps"

def knowledge_agent(query: str) -> str:
    """Use the GPT model to answer general knowledge questions."""
    response = gpt_model(
        query,
        max_length=50,
        num_return_sequences=1,
        temperature=0.5,
        top_p=0.9,
        repetition_penalty=1.5,
        pad_token_id=50256
    )
    return response[0]['generated_text'].strip()

def sentiment_analysis_agent(query: str) -> str:
    """Analyze the sentiment of the user's input."""
    sentiment = sentiment_model(query)
    label = sentiment[0]['label']
    score = sentiment[0]['score']
    return f"Sentiment: {label}, Confidence: {score:.2f}"

@app.post("/summary")
async def summarize_conversation():
    """Summarize the conversation context."""
    if "history" not in conversation_context or not conversation_context["history"]:
        return {"summary": "No conversation history to summarize."}

    summary_input = "\n".join(
        [f"User: {entry['query']}\nAssistant: {entry['response']}" for entry in conversation_context["history"]]
    )
    summary = gpt_model(
        f"Summarize this conversation: {summary_input}",
        max_length=100,
        num_return_sequences=1,
        temperature=0.7
    )
    return {"summary": summary[0]['generated_text'].strip()}

@app.get("/status")
async def status():
    """Health check endpoint."""
    return {"status": "API is running smoothly!"}

@app.post("/reset")
async def reset():
    """Reset the conversation context."""
    conversation_context.clear()
    return {"message": "Conversation context has been reset."}
