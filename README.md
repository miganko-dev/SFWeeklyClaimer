# SFGame Free Gift Claimer

Automated script to claim weekly free gifts from the SFGame shop for multiple characters.

## Why Use This?

The SFGame shop offers a **free mushroom every week** for each character. Manually claiming this for multiple characters is tedious and easy to forget.

### Benefits

| Benefit | Description |
|---------|-------------|
| **Set and Forget** | Runs automatically via GitHub Actions every Monday |
| **Multi-Character** | Claim for all your characters in one run |
| **Never Miss a Week** | Automated scheduling ensures you never forget |
| **Support Creators** | Automatically applies your favorite creator code |
| **Zero Cost** | Runs on GitHub Actions free tier |

### Yearly Savings
That's **52 free mushrooms per character per year** - completely automated!

## Features

- Claim free gifts for multiple character IDs in a single run
- Fresh browser session per character (reliable headless operation)
- Automatic cookie consent handling
- Creator code support
- Cooldown detection (skips characters with gifts on cooldown)
- Detailed logging with timestamps
- GitHub Actions ready (headless mode)

## Requirements

- Python 3.8+
- Playwright

## Installation

### 1. Clone the repository
### 2. Install dependencies

```bash
pip install playwright
playwright install chromium
```

## Configuration

### Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `CHARACTER_IDS` | Yes | Comma-separated list of character IDs (e.g., `"id1#123,id2#456,id3#789"`) |
| `CREATOR_CODES` | No | Comma-separated creator codes - picks random one per claim (default: `SFTOOLS`) |

## Usage

### Local Development

Set environment variables and run:

```bash
# Linux/macOS
export CHARACTER_IDS="id1#123,id2#456"
export CREATOR_CODES="Code1,Code2,Code3"
python scripts/claimer.py

# Windows (PowerShell)
$env:CHARACTER_IDS="id1#123,id2#456"
$env:CREATOR_CODES="Code1,Code2,Code3"
python scripts/claimer.py

# Windows (CMD)
set CHARACTER_IDS=id1#123,id2#456
set CREATOR_CODES=Code1,Code2,Code3
python scripts/claimer.py
```

## GitHub Actions Setup

### 1. Add Repository Secrets

Go to your repository **Settings** > **Secrets and variables** > **Actions** > **New repository secret**

Add the following secrets:

| Secret Name | Value |
|-------------|-------|
| `CHARACTER_IDS` | Your comma-separated character IDs (e.g., `"id1#123,id2#456"`) |
| `CREATOR_CODES` | Comma-separated creator codes (optional, e.g., `"Code1,Code2"`) |

### 2. Create Workflow File

Create `.github/workflows/claim.yml`:

```yaml
name: Claim Free Gifts

on:
  schedule:
    # Runs every Monday at 5:00 UTC
    - cron: '0 5 * * 1'
  workflow_dispatch: # Allows manual trigger

jobs:
  claim:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: |
          pip install playwright
          playwright install chromium
          playwright install-deps chromium

      - name: Run claimer
        env:
          CHARACTER_IDS: ${{ secrets.CHARACTER_IDS }}
          CREATOR_CODES: ${{ secrets.CREATOR_CODES }}
        run: python scripts/claimer.py
```

### 3. Enable GitHub Actions

1. Go to repository **Settings** > **Actions** > **General**
2. Under "Actions permissions", select "Allow all actions and reusable workflows"
3. Save

### 4. Manual Trigger

To run manually:
1. Go to **Actions** tab
2. Select "Claim Free Gifts" workflow
3. Click "Run workflow"

## Output Example

```
============================================================
  SFGame Free Gift Claimer
============================================================
[12:34:56] [INFO]    Started at 2025-12-12 12:34:56
[12:34:56] [INFO]    Found 2 character(s) to process
[12:34:56] [INFO]    Creator codes: 2 configured

──────────────────────────────────────────────────
  Character 1/2
──────────────────────────────────────────────────
[12:35:00] [STEP 1/5] Loading shop page...
[12:35:02] [STEP 2/5] Opening login...
[12:35:03] [STEP 3/5] Logging in...
[12:35:05] [SUCCESS] Logged in successfully
[12:35:05] [STEP 4/5] Checking free gift...
[12:35:06] [INFO]    Free gift available! Claiming...
[12:35:08] [STEP 5/5] Completing checkout...
[12:35:12] [SUCCESS] Free gift claimed!

──────────────────────────────────────────────────
  Character 2/2
──────────────────────────────────────────────────
[12:35:15] [STEP 1/5] Loading shop page...
[12:35:17] [STEP 2/5] Opening login...
[12:35:18] [STEP 3/5] Logging in...
[12:35:20] [SUCCESS] Logged in successfully
[12:35:20] [STEP 4/5] Checking free gift...
[12:35:21] [SKIP]    Free gift is on cooldown, skipping...

============================================================
  Summary
============================================================
[12:36:00] [INFO]    Total characters: 2
[12:36:00] [SUCCESS] Gifts claimed:    1
[12:36:00] [SKIP]    On cooldown:      1
[12:36:00] [INFO]    Completed at 2025-12-12 12:36:00
```

## Troubleshooting

### Common Issues

**"CHARACTER_IDS environment variable is not set"**
- Make sure you've set the `CHARACTER_IDS` environment variable or GitHub secret

**"Free gift is on cooldown"**
- The free gift resets weekly
- The script will automatically skip and continue with the next character

**GitHub Actions fails with browser error**
- Ensure `playwright install-deps chromium` is included in your workflow

## License

MIT
