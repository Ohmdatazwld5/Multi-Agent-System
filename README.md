# Multi-Agent Conversational System

# Overview

This repository contains a multi-agent conversational system built using FastAPI. The system is designed to assist users with various tasks by leveraging specialized agents, including:

# 1.TaskPlannerAgent: Helps users break down tasks into subtasks and prioritize them.

# 2.KnowledgeAgent: Answers factual questions using OpenAI's GPT model.

# 3.SentimentAnalysisAgent: Analyzes the sentiment of user input and provides feedback.

# 4.SummaryAgent: Summarizes the conversation at the end of a session.

The system maintains conversation context, allowing seamless follow-up queries, and uses an intent classifier to route user queries to the appropriate agent.

# Features

# Agents

TaskPlannerAgent: Provides a structured breakdown of user tasks.

KnowledgeAgent: Handles factual queries and general knowledge questions.

SentimentAnalysisAgent: Performs sentiment analysis using a pre-trained model.

SummaryAgent: Generates a summary of the conversation context.

# Endpoints

POST /chat:

Accepts user queries and routes them to the appropriate agent based on the category or intent classification.

Updates the conversation context for follow-up queries.

POST /summary:

Summarizes the conversation context.

GET /status:

Health check endpoint to verify the system is running.

POST /reset:

Resets the conversation context for a user session.

# Intent Classification

The system uses a simple keyword-based approach to classify user intent when no category is provided:

Queries related to tasks or planning are routed to the TaskPlannerAgent.

Questions starting with interrogative words are routed to the KnowledgeAgent.

Inputs with emotional keywords are routed to the SentimentAnalysisAgent.

# Context Management

The conversation context is maintained in memory to track user queries and responses, enabling follow-up interactions and summarization.

Getting Started

Prerequisites

Python 3.8+

pip for managing dependencies

Installation

Clone the repository:

git clone https://github.com/your-username/multi-agent-conversational-system.git
cd multi-agent-conversational-system

Create a virtual environment and activate it:

python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`

Install dependencies:

pip install -r requirements.txt

Running the Application

Start the FastAPI server:

uvicorn main:app --reload

The API will be available at http://127.0.0.1:8000.

Test the /chat endpoint using the test_request.py script:

# Example Usage

Chat Request

Send a POST request to /chat:

{
  "query": "What is the capital of France?",
  "category": "knowledge"
}

Response:

{
  "response": "The capital of France is Paris."
}

Summary Request

Send a POST request to /summary:

{}

Response:

{
  "summary": "User: What is the capital of France?\nAssistant: The capital of France is Paris."
}

Reset Request

Send a POST request to /reset:

{}

Response:

{
  "message": "Conversation context has been reset."
}

# File Structure

main.py: Contains the FastAPI application and agent implementations.

test_request.py: Script to test the /chat endpoint.

requirements.txt: List of dependencies for the application.

# Dependencies

1.fastapi

2.uvicorn

3.transformers

4.pydantic

5.requests

# Future Improvements

Please change the LLM like GPT-4 and so on.

Implement a more sophisticated intent classification model.

Add persistent storage for conversation context.

Extend agents to handle more complex queries.

Integrate user authentication for session management.

# License

Its an open-source and you can use it for free.

# Contributions

Contributions are welcome! Please open an issue or submit a pull request for any feature requests or bug fixes




