# Implementation Notes — Ace Arcade

This build is isolated for **Ace Arcade**.

- All customer-facing brand text uses the `BRAND` constant for this bot only.
- PostgreSQL table names use the `ace_arcade` prefix; a shared PostgreSQL server cannot mix customers, topics, staff or statistics with another bot.
- Tokens, group IDs, staff IDs and the policy URL are environment variables, not hard-coded secrets.
- A support-group message can be copied to a customer **only** when its sender is in `AUTHORIZED_STAFF_IDS` or has been added by `/addstaff`. This fixes an important security weakness in the original code, where any non-bot group member could reply to a customer.
- The message-queue cleanup was made safe at the idle boundary, preventing a newly received customer message from being left in an orphaned queue.
- `/privacy` displays the published policy link and `/delete_data` removes the customer’s PostgreSQL record for this bot.

Read `README.md`, update the policy placeholders, and test the complete customer-to-staff-to-customer flow before launch.
