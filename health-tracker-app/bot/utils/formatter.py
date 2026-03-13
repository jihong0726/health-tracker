from datetime import datetime
from zoneinfo import ZoneInfo

TZ = ZoneInfo("Asia/Kuala_Lumpur")

def now_local():
    return datetime.now(TZ)

def format_now_date():
    return now_local().strftime("%d.%m.%Y")

def format_now_time():
    return now_local().strftime("%I:%M %p").lstrip("0").lower()

def build_today_summary(person, weights, meals):
    date_str = format_now_date()
    lines = [f"今日记录 - {person}", f"日期: {date_str}", "", "体重"]
    if weights:
        for row in weights:
            lines.append(f"- {row['time']} - {row['weight']}")
    else:
        lines.append("- 暂无记录")
    lines.extend(["", "饮食"])
    if meals:
        for row in meals:
            lines.append(f"- {row['time']} - {row['meal_type']} - {row['content']}")
    else:
        lines.append("- 暂无记录")
    lines.extend(["", "提醒"])
    if not meals and not weights:
        lines.append("- 记得先记录今天的体重和饮食")
    elif not meals:
        lines.append("- 记得补充今天吃了什么")
    else:
        lines.append("- 今天记录已更新")
    return "\n".join(lines)

def build_history_summary(person, weights, meals):
    lines = [f"最近记录 - {person}", "", "最近体重"]
    if weights:
        for row in weights[-7:]:
            lines.append(f"- {row['date']} {row['time']} - {row['weight']}")
    else:
        lines.append("- 暂无记录")
    lines.extend(["", "最近饮食"])
    if meals:
        for row in meals[-7:]:
            lines.append(f"- {row['date']} {row['time']} - {row['meal_type']} - {row['content']}")
    else:
        lines.append("- 暂无记录")
    return "\n".join(lines)
