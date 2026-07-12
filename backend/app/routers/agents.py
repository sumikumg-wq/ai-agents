from fastapi import APIRouter, HTTPException
from app.models.schemas import (
    ScriptRequest, ScriptResponse,
    TrendRequest, TrendResponse,
)
from app.agents.script_writer import script_writer_agent
from app.agents.trend_hunter import trend_hunter_agent

router = APIRouter(prefix="/api/agents", tags=["agents"])


@router.post("/script", response_model=ScriptResponse)
def generate_script(req: ScriptRequest) -> ScriptResponse:
    try:
        return script_writer_agent.generate(req)
    except RuntimeError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Script generation failed: {e}")


@router.post("/trends", response_model=TrendResponse)
def get_trends(req: TrendRequest) -> TrendResponse:
    try:
        return trend_hunter_agent.find_trends(req)
    except RuntimeError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Trend fetch failed: {e}")
