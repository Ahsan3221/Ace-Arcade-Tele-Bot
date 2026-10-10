"""Pure business/formatting helpers, independently unit-testable."""
import html
import re
from settings import GAMES, LABELS, TRAFFIC_SOURCES, WORKFLOW


def parse_game(args):
    if not args:
        return None
    return next((g for g in GAMES if g.casefold() == args[0].strip().casefold()), None)


def parse_source(args):
    if not args:
        return None
    source = args[0].strip().lower().removeprefix("src_")
    return TRAFFIC_SOURCES.get(source)


def normalize_label(value):
    v = value.strip().casefold()
    if v not in LABELS:
        raise ValueError("Valid labels: " + ", ".join(LABELS))
    return v


def normalize_game(value):
    result = parse_game([value])
    if not result:
        raise ValueError("Valid games: " + ", ".join(GAMES))
    return result


def normalize_workflow(value):
    v = value.lower().strip().replace("-", "_")
    if v not in WORKFLOW:
        raise ValueError("Valid statuses: " + ", ".join(sorted(WORKFLOW)))
    return v


def short(value, limit=120):
    return re.sub(r"\s+", " ", str(value or "")).strip()[:limit]


def safe_username(value):
    result = str(value or "").lstrip("@")
    if not re.fullmatch(r"[\w.\-]{1,80}", result, re.ASCII):
        raise ValueError("Account username must be 1-80 letters, digits, dots, underscores or hyphens")
    return result


def topic_title(row):
    key = row.get("primary_label") or "new"
    label = LABELS.get(key, LABELS["new"])
    name = short(row.get("name") or row.get("username") or str(row["user_id"]), 48)
    game = short(row.get("game"), 23)
    text = f"{label} | {name}" + (f" | {game}" if game else "")
    return text[:120]


def profile_text(row, accounts=(), labels=(), notes=(), deposits=()):
    handle = f"@{row['username']}" if row.get("username") else "(no Telegram username)"
    tags = ", ".join(LABELS.get(x, x) for x in labels) or "🆕 New"
    acct = "\n".join(f"  • {x['game']}: {short(x['account_username'], 80)}" for x in accounts) or "  (none saved)"
    note_lines = "\n".join(f"  • {short(x['body'], 200)}" for x in notes[:3]) or "  (none)"
    amount = float(deposits["amount"]) if deposits else 0.0
    return (
        "📌 CUSTOMER PROFILE — ACE ARCADE\n"
        "━━━━━━━━━━━━━━━━━━\n"
        f"👤 {short(row.get('name'), 90)}\n"
        f"🔗 {handle}\n🆔 {row['user_id']}\n"
        f"🏷 {tags}\n"
        f"🎮 Selected: {row.get('game') or 'None'}\n"
        f"📋 Status: {row.get('workflow_status') or 'new'}\n"
        f"👨‍💼 Assigned staff ID: {row.get('assigned_staff') or 'Unassigned'}\n"
        "━━━━━━━━━━━━━━━━━━\n"
        f"🎮 SAVED GAME ACCOUNTS\n{acct}\n"
        "━━━━━━━━━━━━━━━━━━\n"
        f"📝 LATEST NOTES\n{note_lines}\n"
        "━━━━━━━━━━━━━━━━━━\n"
        f"💳 Recorded deposits: {deposits['count'] if deposits else 0} | ${amount:.2f}\n"
        f"🎁 Bonus: {row.get('bonus') or 'None'}\n"
        f"📊 Source: {row.get('source') or 'Direct'}\n"
        "ℹ️ Use /profile, /setaccount, /label, /note to edit.\n"
        "⚠️ Amounts are staff-entered records, not payment-provider verification."
    )[:3950]


def escape_text(value):
    return html.escape(str(value), quote=False)


def retry_delay(attempt):
    return min(3600, 2 ** min(int(attempt), 10))


def is_permanent_error(error):
    msg = str(error).casefold()
    return any(s in msg for s in (
        "bot was blocked", "user is deactivated", "chat not found", "user not found",
        "message to copy not found", "message can't be copied", "message can not be copied",
        "not enough rights", "bot is not a member", "forbidden", "message_id_invalid",
    ))


def is_topic_missing(error):
    msg = str(error).casefold()
    return any(s in msg for s in ("message thread not found", "thread_not_found", "forum topic not found", "topic_closed", "topic is closed"))
