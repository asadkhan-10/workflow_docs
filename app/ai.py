import logging
from functools import lru_cache

from groq import Groq
from pydantic import BaseModel, Field, ValidationError

from app.config import settings

logger = logging.getLogger(__name__)


class WorkflowDoc(BaseModel):
    overview: str = Field(min_length=1)
    trigger: str = Field(min_length=1)
    steps: list[str] = Field(min_length=1)
    output: str = Field(min_length=1)
    notes: str = ""


class DocumentationError(Exception):
    """Raised when documentation cannot be generated."""


@lru_cache
def _get_client() -> Groq:
    return Groq(api_key=settings.groq_api_key, timeout=30.0)


def _call_llm(prompt: str) -> str:
    response = _get_client().chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        response_format={"type": "json_object"},
    )
    return response.choices[0].message.content or ""


def _to_markdown(doc: WorkflowDoc) -> str:
    steps = "\n".join(f"{i}. {step}" for i, step in enumerate(doc.steps, 1))
    return (
        f"## Overview\n{doc.overview}\n\n"
        f"## Trigger\n{doc.trigger}\n\n"
        f"## Steps\n{steps}\n\n"
        f"## Output\n{doc.output}\n\n"
        f"## Notes\n{doc.notes or 'None'}"
    )


def generate_workflow_documentation(title: str, raw_input: str, input_type: str) -> str:
    if input_type == "json":
        input_section = f"Workflow JSON Definition:\n{raw_input}"
    else:
        input_section = f"Workflow Description (plain English):\n{raw_input}"

    prompt = f"""
    You are a technical documentation writer specializing in workflow automation.

    Write documentation for the following workflow.

    Workflow Title: {title}
    {input_section}

    Respond with only a JSON object with these keys:
    - overview: string, what this workflow does in 2-3 sentences
    - trigger: string, what starts this workflow
    - steps: list of strings, one clear explanation per step
    - output: string, what the workflow produces
    - notes: string, any important considerations
    """

    for attempt in range(2):
        try:
            content = _call_llm(prompt)
        except Exception as e:
            logger.error("Groq request failed: %s", e)
            raise DocumentationError("Documentation service unavailable") from e

        try:
            return _to_markdown(WorkflowDoc.model_validate_json(content))
        except ValidationError as e:
            logger.warning("Invalid LLM output (attempt %d): %s", attempt + 1, e)

    raise DocumentationError("Model returned invalid documentation")