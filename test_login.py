import pytest
from playwright.sync_api import Page, expect

def test_login_success(page: Page):
    page.goto("https://kolkata.bugbash.live/")
    page.get_by_role("link", name="Sign In").click()
    page.get_by_text("Select Username").click()
    page.get_by_text("demouser", exact=True).click()
    page.get_by_text("Select Password").click()
    page.get_by_text("testingisfun99", exact=True).click()
    page.get_by_role("button", name="Log In").click()

    # Assert successful login
    expect(page.get_by_role("heading", name="Featured")).to_be_visible()
