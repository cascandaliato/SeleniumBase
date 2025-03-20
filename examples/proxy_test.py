from seleniumbase.config import settings
from seleniumbase import BaseCase
BaseCase.main(__name__, __file__)


class ProxyTests(BaseCase):
    def test_proxy(self):
        if self.headless or self.recorder_mode or self.browser == "safari":
            self.open_if_not_url("about:blank")
            print("\n  Unsupported mode for this test.")
            self.skip("Unsupported mode for this test.")
        settings.SKIP_JS_WAITS = True
        if not self.page_load_strategy == "none" and not self.undetectable:
            # This page takes too long to load otherwise
            self.get_new_driver(page_load_strategy="none")
        self.open("https://api.ipify.org/")
        ip_address = self.get_text("body")
        self.open("https://ipinfo.io/")
        self.type('input[name="search"]', ip_address, timeout=20)
        self.sleep(0.5)
        self.click('button span:contains("Search")')
        print("\n\nMy IP Address = %s\n" % ip_address)
        self.wait_for_text(ip_address, "h1", timeout=20)
        self.wait_for_element_present('[href="/signup"]')
        self.wait_for_text("Hosted domains", timeout=20)
        self.highlight("h1")
        self.highlight("#block-summary")
        self.highlight("#block-geolocation")
        self.sleep(2)
        self.click_if_visible("span.ipinfo-modal__close")
        print("Displaying Host Info:")
        text = self.get_text("#block-summary").split("Hosted domains")[0]
        rows = text.split("\n")
        data = []
        for row in rows:
            if row.strip() != "":
                data.append(row.strip())
        print("\n".join(data).replace('\n"', ' "'))
        print("\nDisplaying GeoLocation Info:")
        text = self.get_text("#block-geolocation")
        text = text.split("IP Geolocation data")[0]
        rows = text.split("\n")
        data = []
        for row in rows:
            if row.strip() != "":
                data.append(row.strip())
        print("\n".join(data).replace('\n"', ' "'))
        self.sleep(3)
