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
