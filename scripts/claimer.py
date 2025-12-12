import os
import sys
import random
from datetime import datetime
from playwright.sync_api import sync_playwright, Page


def log_header(message: str):
    print("\n" + "=" * 60)
    print(f"  {message}")
    print("=" * 60)


def log_section(message: str):
    print(f"\n{'─' * 50}")
    print(f"  {message}")
    print("─" * 50)


def log_info(message: str):
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"[{timestamp}] [INFO]    {message}")


def log_success(message: str):
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"[{timestamp}] [SUCCESS] {message}")


def log_warning(message: str):
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"[{timestamp}] [SKIP]    {message}")


def log_error(message: str):
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"[{timestamp}] [FAIL]    {message}")


def log_step(step: int, total: int, message: str):
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"[{timestamp}] [STEP {step}/{total}] {message}")


def process_character(playwright, character_id: str, creator_code: str, index: int, total: int):
    log_section(f"Character {index + 1}/{total}")

    browser = playwright.chromium.launch(headless=True)
    page = browser.new_page()

    result = {"claimed": False, "on_cooldown": False, "error": False}

    try:
        log_step(1, 5, "Loading shop page...")
        page.goto("https://home.sfgame.net/en/shop/")
        page.wait_for_load_state("networkidle")
        page.wait_for_timeout(2000)

        cookie_button = page.locator("#didomi-notice-agree-button")
        if cookie_button.count() > 0:
            cookie_button.click()
            page.wait_for_timeout(1000)

        log_step(2, 5, "Opening login...")
        page.evaluate("if(typeof openLogin === 'function') openLogin();")
        page.wait_for_timeout(1000)
        page.wait_for_selector("#characterid", state="visible", timeout=10000)

        log_step(3, 5, "Logging in...")
        page.fill("#characterid", character_id.strip())
        page.locator("button.btn-primary:has(span[x-text=\"$t('enter')\"])").click()
        page.wait_for_timeout(3000)
        log_success("Logged in successfully")

        log_step(4, 5, "Checking free gift...")
        free_gift_button = page.locator("div[data-price='0'] button.btnCart:not([disabled])")

        if free_gift_button.count() > 0:
            log_info("Free gift available! Claiming...")
            free_gift_button.click()
            page.wait_for_timeout(2000)

            log_step(5, 5, "Completing checkout...")
            page.locator("button[x-on\\:click\\.prevent='open = ! open'].h-5.absolute.right-0.top-1.w-full").click()
            page.wait_for_selector("#creatorcode", state="visible", timeout=5000)

            log_info(f"Using creator code: {creator_code}")
            page.fill("#creatorcode", creator_code)
            page.locator("#btn-checkout").click()
            page.wait_for_timeout(3000)

            log_success("Free gift claimed!")
            result["claimed"] = True
        else:
            log_warning("Free gift is on cooldown, skipping...")
            result["on_cooldown"] = True

    except Exception as e:
        log_error(f"Failed: {e}")
        result["error"] = True

    finally:
        browser.close()

    return result


def get_random_creator_code():
    codes_str = os.environ.get("CREATOR_CODES", "SFTOOLS")
    codes = [code.strip().strip('"').strip("'") for code in codes_str.split(",") if code.strip()]
    if not codes:
        codes = ["SFTOOLS"]
    return random.choice(codes)


def claim_free_gifts():
    log_header("SFGame Free Gift Claimer")
    log_info(f"Started at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    character_ids_str = os.environ.get("CHARACTER_IDS", "")
    creator_codes_str = os.environ.get("CREATOR_CODES", "SFTOOLS")
    creator_codes = [code.strip().strip('"').strip("'") for code in creator_codes_str.split(",") if code.strip()]

    if not character_ids_str:
        log_error("CHARACTER_IDS environment variable is not set")
        sys.exit(1)

    character_ids = [cid.strip().strip('"').strip("'") for cid in character_ids_str.split(",") if cid.strip()]

    if not character_ids:
        log_error("No character IDs found in CHARACTER_IDS")
        sys.exit(1)

    log_info(f"Found {len(character_ids)} character(s) to process")
    log_info(f"Creator codes: {len(creator_codes)} configured")

    stats = {"claimed": 0, "on_cooldown": 0, "errors": 0}

    with sync_playwright() as p:
        for index, character_id in enumerate(character_ids):
            creator_code = get_random_creator_code()
            result = process_character(p, character_id, creator_code, index, len(character_ids))

            if result["claimed"]:
                stats["claimed"] += 1
            elif result["on_cooldown"]:
                stats["on_cooldown"] += 1
            if result["error"]:
                stats["errors"] += 1

    log_header("Summary")
    log_info(f"Total characters: {len(character_ids)}")
    log_success(f"Gifts claimed:    {stats['claimed']}")
    log_warning(f"On cooldown:      {stats['on_cooldown']}")
    if stats["errors"] > 0:
        log_error(f"Errors:           {stats['errors']}")

    log_info(f"Completed at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    if stats["errors"] > 0:
        sys.exit(1)


def main():
    claim_free_gifts()


if __name__ == "__main__":
    main()
