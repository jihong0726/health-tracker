import json
from pathlib import Path
from utils.formatter import format_now_date, format_now_time

ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = ROOT / "data"
WEIGHTS_FILE = DATA_DIR / "weights.json"
MEALS_FILE = DATA_DIR / "meals.json"
SESSIONS_FILE = DATA_DIR / "sessions.json"

def _load_json(path: Path):
    if not path.exists():
        path.write_text("[]", encoding="utf-8")
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return []

def _save_json(path: Path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

def get_current_person(chat_id):
    data = _load_json(SESSIONS_FILE)
    for row in data:
        if str(row["chat_id"]) == str(chat_id):
            return row["person"]
    return "Ji Hong"

def set_current_person(chat_id, person):
    data = _load_json(SESSIONS_FILE)
    found = False
    for row in data:
        if str(row["chat_id"]) == str(chat_id):
            row["person"] = person
            found = True
            break
    if not found:
        data.append({"chat_id": str(chat_id), "person": person})
    _save_json(SESSIONS_FILE, data)

def add_weight(person, value):
    data = _load_json(WEIGHTS_FILE)
    data.append({
        "id": f"w_{len(data)+1:04d}",
        "person": person,
        "date": format_now_date(),
        "time": format_now_time(),
        "weight": f"{value:.1f} kg"
    })
    _save_json(WEIGHTS_FILE, data)

def add_meal(person, meal_type, content):
    data = _load_json(MEALS_FILE)
    data.append({
        "id": f"m_{len(data)+1:04d}",
        "person": person,
        "date": format_now_date(),
        "time": format_now_time(),
        "meal_type": meal_type,
        "content": content
    })
    _save_json(MEALS_FILE, data)

def get_today_data(person):
    date_str = format_now_date()
    weights = [x for x in _load_json(WEIGHTS_FILE) if x["person"] == person and x["date"] == date_str]
    meals = [x for x in _load_json(MEALS_FILE) if x["person"] == person and x["date"] == date_str]
    return weights, meals

def get_recent_data(person, limit=7):
    weights = [x for x in _load_json(WEIGHTS_FILE) if x["person"] == person]
    meals = [x for x in _load_json(MEALS_FILE) if x["person"] == person]
    return weights[-limit:], meals[-limit:]
