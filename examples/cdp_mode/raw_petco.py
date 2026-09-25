"""Test Petco search."""
from seleniumbase import SB

with SB(uc=True, test=True, guest=True) as sb:
    sb.activate_cdp_mode()
    sb.goto("https://www.petco.com/")
    sb.sleep(1.6)
    sb.solve_captcha()
    sb.sleep(1.8)
    query = "Salmon jerky dog treats"
    required_text = "Salmon"
    search_box = "input#header-search"
    sb.wait_for_element(search_box)
    sb.sleep(1.2)
    sb.press_keys(search_box, query)
    sb.sleep(1.2)
    sb.click('button[data-testid="standard-search-click"]')
    sb.sleep(3.6)
    print('*** Petco Search for "%s":' % query)
    print('    (Results must contain "%s".)' % required_text)
    unique_item_text = []
    soup = sb.get_beautiful_soup()
    items = soup.select('[data-track-widget="ProductListing"]')
    for item in items:
        item_text = item.get_text()
        if required_text.lower() in item_text.lower():
            description_element = item.select_one("h2")
            if description_element:
                description_text = description_element.get_text(strip=True)
                if description_text.lower() not in unique_item_text:
                    unique_item_text.append(description_text.lower())
                    print("* " + description_text)
                    price_element = item.select_one('p[class*="price_"]')
                    if price_element:
                        price_text = " ".join(price_element.get_text().split())
                        print("  (" + price_text + ")")
