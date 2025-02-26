AI Voice Assistant Backend

PS C:\Users\PEEKI\OneDrive\Desktop\ai-voice-assignment 1> cd "C:\Users\PEEKI\OneDrive\Desktop\ai-voice-assignment 1\main folder"
>> 
PS C:\Users\PEEKI\OneDrive\Desktop\ai-voice-assignment 1\main folder> uvicorn app.main:app --reload

Kubernetes  minikube http://127.0.0.1:59732

Overview

This is a simple AI Voice Assistant Backend built using FastAPI. It is designed to process voice inputs, return AI-generated responses, and handle API requests efficiently.

Dockerized using a Dockerfile for easy deployment.

Hosted on Kubernetes via Minikube for scalability.

Exposed via a REST API for integration with frontend applications.

Logging enabled to track API requests and responses.

Features

FastAPI-based lightweight backend.

Dockerized for containerized deployment.

Kubernetes deployment for scalability.

Minikube service for local testing.

Logging for API request tracking.

Tech Stack

Backend: FastAPI (Python)

Containerization: Docker

Orchestration: Kubernetes (Minikube)

Cloud Registry: DockerHub

Logging: Python's logging module

Setup & Installation

1. Clone the Repository

git clone https://github.com/yourusername/ai-voice-assistant.git
cd ai-voice-assistant

2. Install Dependencies

Make sure you have Python installed, then run:

pip install -r requirements.txt

3. Run Locally

uvicorn main:app --host 0.0.0.0 --port 8000

4. Docker Setup

Build & Run Docker Container

docker build -t ai_voice_assistant .
docker run -p 8000:8000 ai_voice_assistant

Push to DockerHub

docker tag ai_voice_assistant your-dockerhub-username/ai_voice_assistant:latest
docker push your-dockerhub-username/ai_voice_assistant:latest

5. Kubernetes Deployment

Start Minikube

minikube start

Apply Deployment & Service

kubectl apply -f deployment.yaml
kubectl apply -f service.yaml

Get Service URL

minikube service ai-voice-assistant-service --u

Logging Implementation

 implemented logging to track API requests and responses. Logs 







 add gemini key and mongo uri in .env file
 
