# Ace Arcade CRM — Railway Update Guide (Roman Urdu)

## IMPORTANT: Production deployment
Production database ka snapshot/backup pehle lo. GitHub source backup PostgreSQL data ko include nahi karta. Original source ka backup GitHub branch `backup/pre-crm-20261011` par hai. GitHub `main` update hone se Railway auto-deploy ho sakta hai, agar service connected aur auto-deploy enabled ho.

## Required Railway environment
Purane values unchanged rakho:
- `BOT_TOKEN` — existing bot ka token
- `SUPPORT_GROUP_ID` — existing support supergroup ID
- `DATABASE_URL` — existing PostgreSQL connection
- `AUTHORIZED_STAFF_IDS` — optional initial staff IDs

NEW: `OWNER_IDS` = owner ka numeric Telegram user ID (example `123456789`). OWNER_IDS absent ho to bot start hoga, lekin admin/broadcast/deposit commands disabled rahengi. ASAP set karo.

Optional:
- `RETENTION_DAYS=0` — data retention cleanup off until policy finalized
- `MAX_DELIVERY_ATTEMPTS=8`
- `BROADCAST_GAP_SECONDS=0.15`
- `PRIVACY_POLICY_URL=https://your-real-privacy-policy-url`

## Telegram group permissions
Bot support supergroup ka admin hona chahiye. Manage Topics, Pin Messages, Send Messages, Delete Topics permissions verify karo.

## Verification after deploy
1. Railway logs mein Python startup / PostgreSQL migration errors check karo.
2. Existing user ka topic /start se test karo (same topic ID should persist).
3. Topic mein `/profile`, `/setaccount Juwa player123`, `/label VIP`, `/note customer details` test karo.
4. `/findaccount player123` se account lookup verify karo.
5. Staff reply customer ko deliver ho; customer message topic mein aaye.
6. `/close`, then customer message, topic reopen check karo.
7. `/health` from owner test karo.
8. `/deposit 20 REF123` is staff-entered record, **not payment verification**.

## Rollback
Original code GitHub branch: `backup/pre-crm-20261011`.
GitHub revert code alone does **not** revert database migrations. PostgreSQL snapshot separate rakho. Previous code should ignore added CRM tables/columns, but verify Railway and schema before rollback.

## Known limitations
Tests offline hain; production Telegram/Railway integrations untested. Telegram delivery may occasionally duplicate after a crash between send and database acknowledgement. Automatic payment verification is not implemented. Only one active bot polling worker run karo.


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
