from playwright.sync_api import Page, expect

def login(page: Page):
    page.goto("https://kolkata.bugbash.live/")
    page.get_by_role("link", name="Sign In").click()
    page.get_by_text("Select Username").click()
    page.get_by_text("demouser", exact=True).click()
    page.get_by_text("Select Password").click()
    page.get_by_text("testingisfun99", exact=True).click()
    page.get_by_role("button", name="Log In").click()
    expect(page.get_by_text("Featured")).to_be_visible()

def test_favorites_flow(page: Page):
    login(page)

    # --- 1. Add products to favorites ---
    added_ids = []
    for i in range(1, 4):  # Let's test 3 products for simplicity
        product = page.locator(f'[id="{i}"]')
        heart = product.get_by_role("button", name="delete")
        heart.click()
        added_ids.append(i)

    # --- 2. Go to Favourites page ---
    page.get_by_role("link", name="Favourites").click()
    expect(page).to_have_url(re.compile(".*favourites"))

    # --- 3. Validate all 3 favorited products appear ---
    for i in added_ids:
        assert page.locator(f'[id="{i}"]').is_visible(), f"Product ID {i} not found in favourites"

    # --- 4. Edge Case: Un-favorite all items and check empty state ---
    for i in added_ids:
        fav = page.locator(f'[id="{i}"]').get_by_role("button", name="delete")
        fav.click()

    # Expect some kind of "no favourites" message or empty state
    expect(page.locator("text=No favourites yet")).to_be_visible()

def test_favoriting_then_filtering_breaks_wishlist_state(page: Page):
    login(page)

    # Favorite a product
    product = page.locator('[id="1"]')
    product.get_by_role("button", name="add to favourites").click()

    # Apply a filter that does *not* include that product (e.g., OnePlus if this is Apple)
    page.get_by_role("button", name="Filters").click()
    page.get_by_label("OnePlus").check()

    # Go to Favourites and check if the product still appears
    page.get_by_role("link", name="Favourites").click()
    # ❗ You might want to validate whether the previously favorited item still exists or was cleared
    assert page.locator('[id="1"]').is_visible(), "Favorited product lost after filtering!"
