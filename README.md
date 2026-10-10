# Ace Arcade Telegram Support Bot + CRM

Production bot for private Telegram customer support using customer-specific forum topics and PostgreSQL. This upgrade preserves the old `ace_arcade_users`, `ace_arcade_topics`, and `ace_arcade_staff` tables, and adds CRM features.

## Customer features
- `/start` — start support conversation
- `/games` — choose game
- `/support` — contact support
- `/help` — help
- `/privacy` — privacy information
- `/delete_data` — request data deletion, with confirmation
- `/optin` / `/optout` — optional broadcast subscription

## Staff commands (use inside the customer's topic)
- `/profile`, `/id` — customer profile
- `/setaccount Juwa player123` — save one account per game
- `/delaccount Juwa` — remove game account
- `/findaccount player123` — find account across customers
- `/label VIP`, `/unlabel VIP` — customer labels
- `/note text`, `/history` — staff notes and changes
- `/status pending`, `/assign TELEGRAM_ID` — customer workflow
- `/close` — close customer topic
- `/shortcuts`, `/use KEY` — saved replies
- `/stats` — basic analytics

## Owner commands (owner ID required)
- `/addstaff ID name`, `/removestaff ID`, `/staff`
- `/addshortcut KEY text`, `/delshortcut KEY`
- `/deposit 20 REFERENCE` — **manual record**, not payment verification
- `/broadcast [--label=VIP] message` — opted-in customer broadcast with confirmation
- `/health` — persistent delivery queue status

## Setup on Railway
`Procfile`: `worker: python bot.py`. Install `requirements.txt`, connect PostgreSQL, and configure:
```
BOT_TOKEN=your_existing_bot_token
SUPPORT_GROUP_ID=-1001234567890
DATABASE_URL=postgresql://...
AUTHORIZED_STAFF_IDS=123456789
OWNER_IDS=123456789
RETENTION_DAYS=0
```
Owner IDs are optional for *startup compatibility* only. Without `OWNER_IDS`, owner-restricted commands are disabled. Do not commit real secrets.

## Testing and deployment
```bash
python -m pytest -q
python -m compileall -q bot.py crm.py database.py settings.py
```
Offline tests pass; Telegram, live database migrations, and Railway were not integration-tested. Back up PostgreSQL before deploying. See `DEPLOY_GUIDE_ROMAN_URDU.md` for rollout and rollback instructions.

Original source snapshot GitHub branch: `backup/pre-crm-20261011`. Rolling GitHub code back is not the same as restoring PostgreSQL data.


## October 2026 — Case-insensitive CRM and automatic game accounts

Customer-facing game messages sent **by authorized staff inside a customer's Telegram support topic** are now inspected automatically. When a message contains exactly one `Username:` and one `Password:` line, the bot detects a known game suffix and saves the username/password to PostgreSQL while keeping the normal message-delivery behavior.

Recognized suffixes: `3s` Orionstars, `3fk` Firekirin, `3v` Vblink, `3u` Ultrapanda, `3r` Riversweeps, `3j` Juwa, `3gv` GameVault, `3mw` Milkyway, `3cm` CashMaster. Multiple consecutive 3s are supported, such as `Player333fk`. Any player-name prefix is accepted; `Dummy` is just a sample. For custom games, add a `Game: Custom Game` line.

```text
👤 Username: Michael333fk
🔑 Password: 009988
Log in and let me know if you need help ❤️✨
```

Use `/accounts` inside the customer topic to see saved game accounts and passwords, `/label Special Customer` to save a custom label (spaces allowed), `/unlabel special customer` to remove it, and `/setaccount Juwa player123 009988` to add an account manually. Labels, game selection/search, account lookup, and command names match case-insensitively; passwords keep their exact case. Passwords are stored as **plaintext** by request. Keep your Railway database and staff group access restricted.

**Deployment:** PostgreSQL schema migrations add an account-password column and an automatic-capture deduplication table. Always back up the database before rollout. The source-only rollback branch `backup/pre-crm-20261011` does not back up or restore PostgreSQL.
