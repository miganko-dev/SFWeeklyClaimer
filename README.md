# SFGame Free Gift Claimer

Automated script to claim the **weekly free mushroom** from the SFGame shop for multiple characters.

This README is intentionally simplified. **Usage is only via GitHub fork + setting variables + enabling Actions.**
No local setup. No manual runs. No excuses.

---

## What It Does

* Automatically claims the weekly free gift for each character
* Runs on GitHub Actions (free tier)
* Supports multiple character IDs
* Optional creator code support
* Skips characters that are on cooldown

Result: **52 free mushrooms per character per year**, fully automated.

---

## Usage (3 Steps, That’s It)

### 1. Fork the Repository

Click **Fork** in the top-right corner and create your own copy of this repository.

---

### 2. Set GitHub Actions Variables (Secrets)

In your forked repository, go to:

**Settings → Secrets and variables → Actions → New repository secret**

Add the following secrets:

| Name            | Required | Description                                           |
| --------------- | -------- | ----------------------------------------------------- |
| `CHARACTER_IDS` | ✅ Yes    | Comma-separated list of character IDs ("id1,id2")    |
| `CREATOR_CODES` | ❌ No     | Comma-separated creator codes (defaults to `SFTOOLS`) |

#### Example

```text
CHARACTER_IDS=id1#123,id2#456,id3#789
CREATOR_CODES=Code1,Code2
```

---

### 3. Enable GitHub Actions

1. Go to **Settings → Actions → General**
2. Under **Actions permissions**, select:

   * ✅ *Allow all actions and reusable workflows*
3. Save the settings

That’s it. The workflow is now active.

---

## Execution

### Automatic

The workflow runs **every Monday at 05:00 UTC** automatically.

### Manual (Optional Test Run)

1. Go to the **Actions** tab
2. Select **Claim Free Gifts**
3. Click **Run workflow**

---

## Output

The workflow logs will show:

* Login process for each character
* Whether the free gift is available
* Successful claim or cooldown skip
* Final summary

---

## Common Issues

### ❌ `CHARACTER_IDS environment variable is not set`

* The secret is missing or named incorrectly
* Make sure it is exactly `CHARACTER_IDS`

### ⏳ Free Gift on Cooldown

* Expected behavior
* The gift is available once per week and will be skipped automatically

### 💥 Workflow Fails

* Check **Actions → Workflow run logs**
* Most failures are temporary GitHub runner issues

---

## License

MIT
