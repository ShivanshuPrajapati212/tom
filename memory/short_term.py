working_memory = {
    "identity": {
        "agent_name": "TOM",
        "role": "Shivanshu's cognitive AI assistant",
        "core_rules": [
            "Be Real, Be Fun",
            "Prioritize active goals"
        ]
    },

    "attention": {
        "current_focus": None,
        "priority_level": 0.0
    },

    "goals": {
        "active": [],
        "queued": [],
        "completed": []
    },

    "current_plan": {
        "goal_id": None,
        "steps": [],
        "current_step": None,
        "status": "idle"
    },

    "recent_events": [],  # last 5–20 events (summarized)

    "context_cache": {
        "retrieved_memories": [],
        "external_data": []
    },

    "internal_state": {
        "mode": "normal",  # normal | analyzing | executing | reflecting
        "confidence": 1.0,
        "last_reflection": None
    }
}
