# Ace Arcade Telegram Support Bot

This is a branded Python support bot. It creates one **Telegram Forum Topic per customer** in your private support supergroup. Customer text/media is copied into their topic; a reply from an authorized staff member in that same topic is copied back to the customer.

## Included

- Branded `/start`, help, game and bonus flow
- Game deep links, e.g. `?start=juwa`
- Traffic-source deep links, e.g. `?start=website` or `?start=src_facebook`
- PostgreSQL storage for customers, topics, selections, sources and staff
- Separate `ace_arcade` database tables, so this bot cannot mix data with another bot—even when the same PostgreSQL server is used
- Topic reopen/recreate support and per-customer message queue protection
- Staff tools: `/id`, `/close`, `/stats`, `/broadcast`, `/addstaff`, `/removestaff`, `/staff`
- Privacy command `/privacy` and database deletion command `/delete_data`
- `PRIVACY_POLICY.md` and `BOTFATHER_DETAILS.md` ready to edit/publish

## Required Telegram setup

1. Create a **private supergroup** for support and enable **Topics**.
2. Add this exact bot to it as an **administrator**.
3. Give the bot permission to manage topics and send messages.
4. In BotFather, disable **Group Privacy Mode** for this bot (or confirm in testing that it receives normal staff messages in forum topics). It must receive staff replies to deliver them to customers.
5. Find the group’s numeric ID. It generally starts with `-100`.
6. Get the numeric Telegram ID of every staff member who may reply.

## Environment variables

Set these in Railway’s **Variables** page. Never place a live token in GitHub.

| Variable | Required | Meaning |
|---|---:|---|
| `BOT_TOKEN` | Yes | Token for this exact Ace Arcade bot only |
| `SUPPORT_GROUP_ID` | Yes | Private Topics-enabled support-group ID, such as `-1001234567890` |
| `DATABASE_URL` | Yes | PostgreSQL connection URL |
| `AUTHORIZED_STAFF_IDS` | Yes | Comma-separated numeric Telegram IDs permitted to reply/use admin commands |
| `PRIVACY_POLICY_URL` | Recommended | Public HTTPS link to this repository’s policy |

Use `.env.example` as a reference only. The production app receives values from Railway; it does not load a local `.env` file automatically.

## Deploy to Railway

1. Extract this ZIP and create a **separate GitHub repository** for this bot.
2. Edit all `[square-bracket placeholders]` in `PRIVACY_POLICY.md` with real business, privacy-contact and retention information. Commit the file publicly.
3. Create a Railway project → **Deploy from GitHub Repo**.
4. Add a Railway PostgreSQL service, then set `DATABASE_URL` to its connection URL (or use your external PostgreSQL URL).
5. Add every environment variable in the table above.
6. Railway uses the included `Procfile` automatically:
   ```text
   worker: python bot.py
   ```
7. Open Railway logs. A successful deployment prints `Bot is running...`.

## Publish privacy policy / Telegram details

Open `BOTFATHER_DETAILS.md`. It contains the branded About text, description, commands and the GitHub URL pattern. After you publish the policy, paste its public HTTPS link:

- into Railway as `PRIVACY_POLICY_URL`, so the bot’s `/privacy` command shows it; and
- wherever Telegram/BotFather or a Telegram product review asks for your bot’s privacy-policy link.

## Staff workflow

- A customer starts the bot, chooses options and/or sends a message.
- The bot creates one topic in the support group.
- **Only authorized staff IDs** can send a group message through the bot to a customer.
- Reply normally inside the customer’s topic. Do not use a command for the reply itself.
- Use `/id` in that topic to see stored customer information and `/close` when done.

## Important notes

- Keep the support group private: it contains customer messages and Telegram identifiers.
- The bot token, group ID and database are deliberately not hard-coded. Each ZIP needs its own `BOT_TOKEN`; support groups can be the same or different.
- This build intentionally has independent `ace_arcade` tables. If you use the same PostgreSQL database for both bots, data still stays separate.
- The Privacy Policy is a useful template, **not legal advice**. Before publishing, complete the placeholders and ensure your business, marketing and gaming activities comply with rules applicable to you and your customers.
- `/delete_data` deletes the account’s record from this bot’s PostgreSQL tables and tries to close the support topic. Telegram chat copies or records held by people may require separate handling under your retention policy.

## Local test (optional)

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export BOT_TOKEN='token-for-this-bot'
export SUPPORT_GROUP_ID='-1001234567890'
export DATABASE_URL='postgresql://user:password@host:5432/database'
export AUTHORIZED_STAFF_IDS='123456789'
export PRIVACY_POLICY_URL='https://github.com/OWNER/REPO/blob/main/PRIVACY_POLICY.md'
python bot.py
```
