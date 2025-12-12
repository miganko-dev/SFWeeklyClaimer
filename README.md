# SFGame Free Gift Claimer

Automated script to claim daily free gifts from the SFGame shop for multiple characters.

## Features

- Claim free gifts for multiple character IDs in a single run
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

```bash
git clone https://github.com/yourusername/ShakesAndFidget.git
cd ShakesAndFidget
```

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
| `CREATOR_CODE` | No | Creator code to use during checkout (default: `Niisa`) |

### Finding Your Character ID

1. Go to [SFGame Shop](https://home.sfgame.net/en/shop/)
2. Click "Login"
3. Your Character ID is shown in your game profile (format: `xxxxxxxx#xxx`)

## Usage

### Local Development

Set environment variables and run:

```bash
# Linux/macOS
export CHARACTER_IDS="id1#123,id2#456"
export CREATOR_CODE="YourCode"
python scripts/claimer.py

# Windows (PowerShell)
$env:CHARACTER_IDS="id1#123,id2#456"
$env:CREATOR_CODE="YourCode"
python scripts/claimer.py

# Windows (CMD)
set CHARACTER_IDS=id1#123,id2#456
set CREATOR_CODE=YourCode
python scripts/claimer.py
```

## GitHub Actions Setup

### 1. Add Repository Secrets

Go to your repository **Settings** > **Secrets and variables** > **Actions** > **New repository secret**

Add the following secrets:

| Secret Name | Value |
|-------------|-------|
| `CHARACTER_IDS` | Your comma-separated character IDs (e.g., `"id1#123,id2#456"`) |
| `CREATOR_CODE` | Your creator code (optional) |

### 2. Create Workflow File

Create `.github/workflows/claim.yml`:

```yaml
name: Claim Free Gifts

on:
  schedule:
    # Runs every day at 8:00 UTC
    - cron: '0 8 * * *'
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
          CREATOR_CODE: ${{ secrets.CREATOR_CODE }}
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
[12:34:56] [INFO]    Found 3 character(s) to process
[12:34:56] [INFO]    Creator code: Niisa
[12:34:56] [INFO]    Launching browser (headless mode)...
[12:34:59] [SUCCESS] Shop page loaded

──────────────────────────────────────────────────
  Character 1/3: abc123#521
──────────────────────────────────────────────────
[12:35:00] [STEP 1/5] Opening login modal...
[12:35:01] [STEP 2/5] Entering character ID...
[12:35:02] [STEP 3/5] Submitting login...
[12:35:05] [SUCCESS] Logged in successfully
[12:35:05] [STEP 4/5] Checking free gift availability...
[12:35:06] [INFO]    Free gift available! Claiming...
[12:35:12] [SUCCESS] Free gift claimed for abc123#521!
[12:35:12] [STEP 5/5] Switching to next character...

============================================================
  Summary
============================================================
[12:36:00] [INFO]    Total characters: 3
[12:36:00] [INFO]    Processed:        3
[12:36:00] [SUCCESS] Gifts claimed:    2
[12:36:00] [WARNING] On cooldown:      1
```

## Troubleshooting

### Common Issues

**"CHARACTER_IDS environment variable is not set"**
- Make sure you've set the `CHARACTER_IDS` environment variable or GitHub secret

**"Free gift is on cooldown"**
- The free gift has a 3-day cooldown period per character
- The script will automatically skip and continue with the next character

**GitHub Actions fails with browser error**
- Ensure `playwright install-deps chromium` is included in your workflow

## License

MIT
