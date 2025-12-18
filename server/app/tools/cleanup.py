def clean_ifixit_guide(raw_guide: dict) -> dict:
    """Extract only text + image URLs to save tokens."""
    steps = []
    for step in raw_guide.get("steps", []):
        steps.append({
            "title": step.get("title"),
            "text": step.get("body"),
            "images": [img.get("standard") for img in step.get("media", []) if img.get("standard")]
        })
    return {
        "title": raw_guide.get("title"),
        "introduction": raw_guide.get("introduction"),
        "steps": steps
    }


def format_final_answer(state: dict) -> str:
    """Format the final response for output"""
    if "repair_steps" in state:
        steps = state["repair_steps"].get("steps", [])
        text_steps = [f"{i+1}. {s.get('title', '')}\n{s.get('text', '')}" for i, s in enumerate(steps)]
        return "\n\n".join(text_steps)
    elif "final_response" in state:
        return str(state["final_response"])
    return "No results found."
