import os
import sys
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


def click_element_by_selector(page: Page, selector: str, wait_time: int = 1000, timeout: int = 10000):
    element = page.locator(selector)
    element.wait_for(state="visible", timeout=timeout)
    page.wait_for_timeout(wait_time)
    element.click()


def fill_input(page: Page, selector: str, value: str, timeout: int = 10000):
    page.wait_for_selector(selector, state="visible", timeout=timeout)
    page.fill(selector, value.strip())


def close_all_modals(page: Page):
    page.evaluate("if(typeof closeLogin === 'function') closeLogin();")
    page.evaluate("if(window.Alpine && Alpine.store('userOpen')) Alpine.store('userOpen').on = false;")
    page.wait_for_timeout(1000)


def open_login_modal(page: Page):
    close_all_modals(page)
    page.wait_for_timeout(500)
    login_btn = page.locator("button.btn-login:has(.icon-user):not(.btn-playnow)")
    login_btn.wait_for(state="visible", timeout=10000)
    page.evaluate("if(typeof openLogin === 'function') openLogin();")
    page.wait_for_timeout(1000)
    page.wait_for_selector("#characterid", state="visible", timeout=10000)


def claim_free_gifts():
    log_header("SFGame Free Gift Claimer")
    log_info(f"Started at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    character_ids_str = os.environ.get("CHARACTER_IDS", "")
    creator_code = os.environ.get("CREATOR_CODE", "Niisa")

    if not character_ids_str:
        log_error("CHARACTER_IDS environment variable is not set")
        sys.exit(1)

    character_ids = [cid.strip().strip('"').strip("'") for cid in character_ids_str.split(",") if cid.strip()]

    if not character_ids:
        log_error("No character IDs found in CHARACTER_IDS")
        sys.exit(1)

    log_info(f"Found {len(character_ids)} character(s) to process")
    log_info(f"Creator code: {creator_code}")

    stats = {"processed": 0, "claimed": 0, "on_cooldown": 0, "errors": 0}

    with sync_playwright() as p:
        log_info("Launching browser (headless mode)...")
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        try:
            log_info("Navigating to SFGame shop...")
            page.goto("https://home.sfgame.net/en/shop/")
            page.wait_for_load_state("networkidle")
            page.wait_for_timeout(2000)
            log_success("Shop page loaded")

            log_info("Checking for cookie banner...")
            cookie_button = page.locator("#didomi-notice-agree-button")
            if cookie_button.count() > 0:
                log_info("Accepting cookies...")
                cookie_button.click()
                page.wait_for_timeout(1000)
                log_success("Cookies accepted")
            else:
                log_info("No cookie banner found")

            for index, character_id in enumerate(character_ids):
                log_section(f"Character {index + 1}/{len(character_ids)}")

                try:
                    log_step(1, 5, "Opening login modal...")
                    open_login_modal(page)

                    log_step(2, 5, "Entering character ID...")
                    fill_input(page, "#characterid", character_id)

                    log_step(3, 5, "Submitting login...")
                    click_element_by_selector(page, "button.btn-primary:has(span[x-text=\"$t('enter')\"])")
                    page.wait_for_timeout(3000)
                    log_success("Logged in successfully")

                    log_step(4, 5, "Checking free gift availability...")
                    free_gift_button = page.locator("div[data-price='0'] button.btnCart:not([disabled])")

                    if free_gift_button.count() > 0:
                        log_info("Free gift available! Claiming...")
                        click_element_by_selector(page, "div[data-price='0'] button.btnCart:not([disabled])")
                        page.wait_for_timeout(2000)

                        log_info("Opening creator code input...")
                        click_element_by_selector(page, "button[x-on\\:click\\.prevent='open = ! open'].h-5.absolute.right-0.top-1.w-full")
                        page.wait_for_selector("#creatorcode", state="visible", timeout=5000)

                        log_info(f"Entering creator code: {creator_code}")
                        fill_input(page, "#creatorcode", creator_code)

                        log_info("Completing checkout...")
                        click_element_by_selector(page, "#btn-checkout")
                        page.wait_for_timeout(3000)

                        log_success("Free gift claimed!")
                        stats["claimed"] += 1
                    else:
                        log_warning("Free gift is on cooldown, skipping...")
                        stats["on_cooldown"] += 1

                    stats["processed"] += 1

                    if index < len(character_ids) - 1:
                        log_step(5, 5, "Switching to next character...")
                        close_all_modals(page)

                        click_element_by_selector(page, "button.btn-login:has(.icon-user):not(.btn-playnow)")
                        page.wait_for_timeout(1000)

                        click_element_by_selector(page, "button.btnChangeCharacterId")
                        page.wait_for_timeout(1000)
                        log_info("Ready for next character")

                except Exception as e:
                    log_error(f"Failed to process character: {e}")
                    stats["errors"] += 1

                    if index < len(character_ids) - 1:
                        log_info("Attempting to recover for next character...")
                        try:
                            page.goto("https://home.sfgame.net/en/shop/")
                            page.wait_for_load_state("networkidle")
                            page.wait_for_timeout(2000)
                        except:
                            pass

        except Exception as e:
            log_error(f"Critical error: {e}")
            stats["errors"] += 1

        finally:
            browser.close()
            log_info("Browser closed")

    log_header("Summary")
    log_info(f"Total characters: {len(character_ids)}")
    log_info(f"Processed:        {stats['processed']}")
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
