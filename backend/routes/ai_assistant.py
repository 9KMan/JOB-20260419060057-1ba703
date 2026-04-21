from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional, Literal
from backend.database import get_db
from backend.models import User, AIGenerationLog
from backend.routes.auth import get_current_user
import os
import openai
import anthropic

router = APIRouter()

openai.api_key = os.getenv("OPENAI_API_KEY", "")
anthropic_api_key = os.getenv("ANTHROPIC_API_KEY", "")

class ChatMessage(BaseModel):
    role: Literal["user", "assistant"]
    content: str

class AIRequest(BaseModel):
    messages: list[ChatMessage]
    model: Literal["gpt-4", "gpt-3.5-turbo", "claude-3-opus", "claude-3-sonnet"] = "gpt-4"
    temperature: float = 0.7
    max_tokens: int = 1000

class AIResponse(BaseModel):
    message: ChatMessage
    usage: dict
    model: str

class GenerateDescriptionRequest(BaseModel):
    event_title: str
    event_type: str
    artist_name: str
    venue_name: str
    key_details: Optional[str] = None

@router.post("/chat", response_model=AIResponse)
async def chat(
    request: AIRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if request.model.startswith("gpt"):
        if not openai.api_key:
            raise HTTPException(status_code=500, detail="OpenAI API key not configured")
        try:
            response = openai.ChatCompletion.create(
                model=request.model,
                messages=[{"role": m.role, "content": m.content} for m in request.messages],
                temperature=request.temperature,
                max_tokens=request.max_tokens
            )
            log = AIGenerationLog(
                user_id=current_user.id,
                prompt=str(request.messages),
                response=response.choices[0].message.content,
                model=request.model,
                tokens_used=response.usage.total_tokens,
                generation_type="chat"
            )
            db.add(log)
            db.commit()
            return AIResponse(
                message=ChatMessage(
                    role="assistant",
                    content=response.choices[0].message.content
                ),
                usage={
                    "prompt_tokens": response.usage.prompt_tokens,
                    "completion_tokens": response.usage.completion_tokens,
                    "total_tokens": response.usage.total_tokens
                },
                model=request.model
            )
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"OpenAI error: {str(e)}")
    elif request.model.startswith("claude"):
        if not anthropic_api_key:
            raise HTTPException(status_code=500, detail="Anthropic API key not configured")
        try:
            client = anthropic.Anthropic(api_key=anthropic_api_key)
            response = client.messages.create(
                model=request.model,
                max_tokens=request.max_tokens,
                temperature=request.temperature,
                messages=[{"role": m.role, "content": m.content} for m in request.messages]
            )
            content = response.content[0].text
            log = AIGenerationLog(
                user_id=current_user.id,
                prompt=str(request.messages),
                response=content,
                model=request.model,
                tokens_used=response.usage.input_tokens + response.usage.output_tokens,
                generation_type="chat"
            )
            db.add(log)
            db.commit()
            return AIResponse(
                message=ChatMessage(role="assistant", content=content),
                usage={
                    "prompt_tokens": response.usage.input_tokens,
                    "completion_tokens": response.usage.output_tokens,
                    "total_tokens": response.usage.input_tokens + response.usage.output_tokens
                },
                model=request.model
            )
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Anthropic error: {str(e)}")
    raise HTTPException(status_code=400, detail="Invalid model")

@router.post("/generate-event-description")
async def generate_event_description(
    request: GenerateDescriptionRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    prompt = f"""Generate an engaging event description for a {request.event_type} called '{request.event_title}'.

Artist: {request.artist_name}
Venue: {request.venue_name}
{"Additional details: " + request.key_details if request.key_details else ""}

Write a compelling 2-3 paragraph description that would attract attendees. Make it sound professional and exciting."""

    if not openai.api_key:
        return {"description": f"{request.event_title} - A {request.event_type} featuring {request.artist_name} at {request.venue_name}. Don't miss this incredible night of music!"}

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.8,
            max_tokens=500
        )
        description = response.choices[0].message.content
        log = AIGenerationLog(
            user_id=current_user.id,
            prompt=prompt,
            response=description,
            model="gpt-4",
            tokens_used=response.usage.total_tokens,
            generation_type="event_description"
        )
        db.add(log)
        db.commit()
        return {"description": description}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Generation failed: {str(e)}")

@router.get("/usage")
def get_usage_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    logs = db.query(AIGenerationLog).filter(
        AIGenerationLog.user_id == current_user.id
    ).order_by(AIGenerationLog.created_at.desc()).limit(100).all()
    total_tokens = sum(log.tokens_used or 0 for log in logs)
    return {
        "total_requests": len(logs),
        "total_tokens": total_tokens,
        "recent_logs": [
            {
                "id": log.id,
                "generation_type": log.generation_type,
                "model": log.model,
                "tokens_used": log.tokens_used,
                "created_at": log.created_at
            }
            for log in logs[:10]
        ]
    }
