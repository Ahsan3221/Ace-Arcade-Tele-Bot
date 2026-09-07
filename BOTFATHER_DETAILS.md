# Ace Arcade — Telegram / BotFather Details

Use this as a copy-paste checklist. Replace every placeholder before use.

## Identity

- **Bot name:** Ace Arcade
- **Bot username:** `@[your existing BotFather username]`
- **Support group ID:** `-100[replace with your private Topics-enabled group ID]`

## Short About text

Set this in BotFather using `/setabouttext`:

```text
Choose your game and chat with the Ace Arcade support team.
```

## Full description

Set this in BotFather using `/setdescription`:

```text
Welcome to Ace Arcade. Choose your game, select an available bonus option, and message our support team for help.
```

## Public privacy-policy URL

First upload the edited policy to a public GitHub repository. Then use this pattern:

```text
https://github.com/YOUR_GITHUB_USERNAME/ace-arcade-telegram-bot/blob/main/PRIVACY_POLICY.md
```

If Telegram requires a direct text-file URL, use GitHub Raw:

```text
https://raw.githubusercontent.com/YOUR_GITHUB_USERNAME/ace-arcade-telegram-bot/main/PRIVACY_POLICY.md
```

Use the same final URL as Railway’s `PRIVACY_POLICY_URL`. That makes the bot’s `/privacy` command show the live policy. Paste the link wherever Telegram/BotFather or any Telegram product/review flow asks for the privacy-policy URL.

## Public bot commands

The code registers its commands automatically after deployment. If you want to enter them manually in BotFather, paste:

```text
start - Start or restart your support chat
help - Show help and available commands
games - Choose or change your game
support - Reach the support team
privacy - View privacy information
delete_data - Delete your bot database record
```

## Staff commands (private support group only)

```text
id - Show the customer in this topic
close - Close this customer topic
stats - Show bot statistics
broadcast - Send a customer broadcast
addstaff - Authorize a staff member
removestaff - Remove a staff member
staff - List authorized staff
```

## Required bot/group settings

1. Keep the token secret; place it only in Railway as `BOT_TOKEN`.
2. Add this bot as an admin to the private support supergroup.
3. Enable **Topics** in that group.
4. Allow the bot to manage topics and send messages.
5. Disable BotFather **Group Privacy Mode** for this bot, or test after deployment that the bot receives a normal (not-command) staff reply in a topic. Normal staff replies must reach the bot for delivery to work.
6. Put at least one owner’s numeric Telegram ID in `AUTHORIZED_STAFF_IDS` before the first deployment. Unauthorised group members cannot reply to customers through this bot.

## Test checklist

1. From a normal customer account, send `/start` and confirm an immediate welcome message.
2. Choose a bonus/game and send a message.
3. Confirm a new customer topic appears in the support group.
4. From an authorized staff account, send a normal reply inside that topic.
5. Confirm the customer receives the reply.
6. Test `/id`, `/close`, and then a new customer message to confirm the topic reopens/recreates.
