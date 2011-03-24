import os.path
import gettext

TRANSLATION_DOMAIN = "pylabra"
LOCALE_DIR = os.path.join(os.path.dirname(__file__), "locale")

gettext.install(TRANSLATION_DOMAIN, LOCALE_DIR)

