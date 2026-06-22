from __future__ import annotations
import pandas as pd
from utils.db import get_client


def get_active_programs() -> list[dict]:
    client = get_client()
    result = (
        client.table("programs")
        .select("*")
        .eq("active", True)
        .order("display_order")
        .execute()
    )
    return result.data


def get_all_programs() -> list[dict]:
    client = get_client()
    result = client.table("programs").select("*").order("display_order").execute()
    return result.data


def get_sessions(program_id: str) -> pd.DataFrame:
    client = get_client()
    result = (
        client.table("sessions")
        .select("*")
        .eq("program_id", program_id)
        .order("session_date", desc=True)
        .execute()
    )
    return pd.DataFrame(result.data)


def get_responses(session_id: str) -> pd.DataFrame:
    client = get_client()
    result = (
        client.table("responses")
        .select("*")
        .eq("session_id", session_id)
        .execute()
    )
    return pd.DataFrame(result.data)


def session_exists(program_id: str, session_date: str, topic: str) -> dict | None:
    client = get_client()
    result = (
        client.table("sessions")
        .select("id")
        .eq("program_id", program_id)
        .eq("session_date", session_date)
        .eq("topic", topic)
        .execute()
    )
    return result.data[0] if result.data else None


def upsert_session(data: dict) -> str:
    client = get_client()
    existing = session_exists(data["program_id"], data["session_date"], data["topic"])
    if existing:
        client.table("responses").delete().eq("session_id", existing["id"]).execute()
        client.table("sessions").update(
            {k: v for k, v in data.items() if k != "program_id"}
        ).eq("id", existing["id"]).execute()
        return existing["id"]
    result = client.table("sessions").insert(data).execute()
    return result.data[0]["id"]


def insert_responses(session_id: str, responses: list[dict]) -> None:
    if not responses:
        return
    client = get_client()
    rows = [{**r, "session_id": session_id} for r in responses]
    client.table("responses").insert(rows).execute()


def add_program(data: dict) -> None:
    get_client().table("programs").insert(data).execute()


def update_program(program_id: str, data: dict) -> None:
    get_client().table("programs").update(data).eq("id", program_id).execute()
