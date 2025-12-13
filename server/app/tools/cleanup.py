def clean_ifixit_guide(raw_guide: dict) -> dict:
    steps = []

    for step in raw_guide.get("steps", []):
        steps.append({
            "title": step.get("title"),
            "text": step.get("body"),
            "images": [
                img.get("standard") for img in step.get("media", [])
            ]
        })

    return {
        "title": raw_guide.get("title"),
        "introduction": raw_guide.get("introduction"),
        "steps": steps
    }
