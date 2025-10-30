"""FastAPI endpoint that orchestrates a CrewAI roundtable."""

from __future__ import annotations

import json
import os
import random
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List

from crewai import Agent
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Request, status
from langchain_openai import ChatOpenAI

load_dotenv()


ARTIFACT_DIR = Path("artifacts/agent_meetings")
PRD_PATH = Path("artifacts/day1_prd.md")
DEFAULT_MEETING_QUESTION = (
    "Given the PRD for OnboardPro, which customer segments should we prioritize for launch, "
    "and how should product, pricing, and positioning evolve over the next year to win those segments?"
)


PERSONAS: List[Dict[str, str]] = [
    {
        "name": "Dana Mitchell",
        "title": "Chief Executive Officer",
        "goal": "Balance strategic vision with near-term go-to-market success for OnboardPro.",
        "backstory": "Seasoned SaaS CEO focused on sustainable growth, stakeholder alignment, and investor confidence.",
    },
    {
        "name": "Priya Desai",
        "title": "VP of Product Management",
        "goal": "Shape the roadmap to deliver differentiated onboarding experiences aligned with the PRD.",
        "backstory": "Leads multi-disciplinary product teams and obsesses over product-market fit and adoption metrics.",
    },
    {
        "name": "Marcus Lee",
        "title": "Head of Human Resources",
        "goal": "Ensure OnboardPro addresses HR compliance, new-hire satisfaction, and program scalability.",
        "backstory": "Built onboarding programs for hyper-growth companies and champions employee-centric design.",
    },
    {
        "name": "Elena Petrova",
        "title": "Chief Compliance & Legal Counsel",
        "goal": "Mitigate regulatory risk while enabling fast market entry across industries and geographies.",
        "backstory": "Expert in global employment law, data privacy, and vendor contracts for HR tech platforms.",
    },
    {
        "name": "Noah Alvarez",
        "title": "Chief Financial Officer",
        "goal": "Model revenue scenarios, pricing strategy, and unit economics for sustainable scaling.",
        "backstory": "Finance leader with experience steering SaaS companies through Series B to IPO milestones.",
    },
    {
        "name": "Sofia Bennett",
        "title": "VP of Sales",
        "goal": "Define high-propensity customer segments and craft a compelling sales motion for OnboardPro.",
        "backstory": "Leads enterprise and mid-market sales teams, zeroing in on buyer personas and objections.",
    },
    {
        "name": "Ethan Clark",
        "title": "Director of Customer Success",
        "goal": "Ensure onboarding journeys deliver measurable outcomes and long-term account expansion.",
        "backstory": "Drives customer health programs and post-sale adoption strategies for HR technology suites.",
    },
    {
        "name": "Aisha Rahman",
        "title": "Principal Engineering Lead",
        "goal": "Align technical feasibility, platform scalability, and integration roadmap with product vision.",
        "backstory": "Architect behind previous onboarding platform rollouts with strong focus on security and APIs.",
    },
]


def load_prd() -> str:
    if not PRD_PATH.exists():
        raise FileNotFoundError(f"Required PRD artifact not found at {PRD_PATH}")
    return PRD_PATH.read_text(encoding="utf-8")


def create_agents(llm: ChatOpenAI) -> List[Dict[str, Any]]:
    agent_entries: List[Dict[str, Any]] = []
    for persona in PERSONAS:
        agent = Agent(
            role=persona["title"],
            goal=persona["goal"],
            backstory=persona["backstory"],
            allow_delegation=False,
            verbose=False,
            llm=llm,
            memory=True,
        )
        agent_entries.append({"persona": persona, "agent": agent})
    return agent_entries


def build_system_prompt(persona: Dict[str, str], meeting_question: str, prd_context: str) -> str:
    return (
        f"You are {persona['name']}, {persona['title']} at OnboardPro. "
        f"Your objective: {persona['goal']}\n"
        "You are participating in a live, high-stakes two-hour strategy roundtable about the OnboardPro product. "
        "Ground every contribution in the product requirements document (PRD) excerpt provided. "
        "Respond with thoughtful, context-rich commentary; reference others' points where appropriate, "
        "and avoid repeating earlier ideas verbatim. Offer new analysis, trade-offs, or follow-up actions.\n"
        f"Guiding strategic prompt: {meeting_question}\n"
        "PRD context follows between triple backticks.\n"
        f"```\n{prd_context}\n```"
    )


def generate_turn(
    llm: ChatOpenAI,
    persona: Dict[str, str],
    conversation_so_far: List[Dict[str, Any]],
    meeting_question: str,
    prd_context: str,
    current_time: datetime,
    start_time: datetime,
    total_duration_minutes: int,
) -> str:
    elapsed = int((current_time - start_time).total_seconds() // 60)
    transcript_lines = [
        f"[{msg['timestamp']}] {msg['speaker']} ({msg['title']}): {msg['content']}"
        for msg in conversation_so_far
    ]
    transcript_text = "\n".join(transcript_lines) or "(No prior dialogue.)"
    prompt = (
        "You are in the middle of a leadership roundtable. "
        f"Current meeting time marker: minute {elapsed} of {total_duration_minutes}.\n"
        "Conversation so far is provided below. Build on it naturally, address opportunities or concerns, "
        "and keep momentum. You may pose questions, challenge assumptions, or assign follow-up actions.\n"
        "Avoid filler phrases; be concise yet substantive (4-7 sentences or a short bullet list).\n"
        f"Conversation so far:\n{transcript_text}\n"
        "Return only your contribution."
    )

    messages = [
        {"role": "system", "content": build_system_prompt(persona, meeting_question, prd_context)},
        {"role": "user", "content": prompt},
    ]

    response = llm.invoke(messages)
    return response.content.strip() if hasattr(response, "content") else str(response)


def orchestrate_roundtable(meeting_question: str) -> Dict[str, Any]:
    prd_context = load_prd()
    llm = ChatOpenAI(model="gpt-4o", temperature=0.6)
    agent_entries = create_agents(llm)

    start_time = datetime.utcnow().replace(second=0, microsecond=0)
    conversation: List[Dict[str, Any]] = []

    rng = random.Random()
    total_minutes = 120
    elapsed = 0
    last_speaker_name: str | None = None

    while elapsed < total_minutes:
        step = rng.randint(7, 18)
        elapsed = min(total_minutes, elapsed + step)
        current_time = start_time + timedelta(minutes=elapsed)

        possible_entries = [entry for entry in agent_entries if entry["persona"]["name"] != last_speaker_name]
        if not possible_entries:
            possible_entries = agent_entries
        speaker_entry = rng.choice(possible_entries)
        persona = speaker_entry["persona"]

        content = generate_turn(
            llm,
            persona,
            conversation,
            meeting_question,
            prd_context,
            current_time,
            start_time,
            total_minutes,
        )

        conversation.append(
            {
                "timestamp": current_time.isoformat(),
                "elapsed_minutes": elapsed,
                "speaker": persona["name"],
                "title": persona["title"],
                "content": content,
            }
        )
        last_speaker_name = persona["name"]

    summary_prompt = (
        "You are an executive communications lead summarizing a strategic roundtable. "
        "Produce a markdown briefing with the following sections: Meeting Overview, Key Discussion Themes, "
        "Aligned Decisions, Open Questions, and Next Actions. "
        "Capture nuance and disagreements without omitting important details. Keep it under 450 words."
    )
    transcript_text = "\n".join(
        f"- {entry['timestamp']} ({entry['title']} - {entry['speaker']}): {entry['content']}"
        for entry in conversation
    )
    summary_messages = [
        {"role": "system", "content": summary_prompt},
        {
            "role": "user",
            "content": (
                f"Meeting strategic prompt: {meeting_question}\n"
                f"PRD excerpt:\n{prd_context}\n\nFull conversation transcript:\n{transcript_text}"
            ),
        },
    ]
    summary_response = llm.invoke(summary_messages)
    summary_text = summary_response.content.strip() if hasattr(summary_response, "content") else str(summary_response)

    timestamp_label = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
    ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)
    transcript_path = ARTIFACT_DIR / f"meeting_{timestamp_label}.json"
    summary_path = ARTIFACT_DIR / f"meeting_{timestamp_label}.md"

    transcript_payload = {
        "meeting_question": meeting_question,
        "generated_at": datetime.utcnow().isoformat(),
        "duration_minutes": total_minutes,
        "participants": PERSONAS,
        "messages": conversation,
    }

    transcript_path.write_text(json.dumps(transcript_payload, indent=2), encoding="utf-8")
    summary_path.write_text(summary_text, encoding="utf-8")

    return {
        "summary": summary_text,
        "summary_path": str(summary_path),
        "transcript_path": str(transcript_path),
    }


app = FastAPI(title="OnboardPro Agent Roundtable API")


@app.post("/agent-chat")
async def agent_chat(request: Request):
    payload = await request.json()
    meeting_question = payload.get("question") or DEFAULT_MEETING_QUESTION

    try:
        result = orchestrate_roundtable(meeting_question)
    except FileNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(exc)) from exc
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(exc)) from exc

    return result
