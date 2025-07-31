# /// script
# requires-python = "==3.13"
# dependencies = [
#     "discord",
#     "python-dotenv",
#     "sqlalchemy",
#     "psycopg2-binary",
# ]
# ///

import dotenv
import os
import src

class Seanren(src.Bot):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

if __name__ == "__main__":
    dotenv.load_dotenv()
    seanren = Seanren(name="Seanren", version=[25, 0], prefix="!")
    try:
        seanren.run(os.getenv("seanren_key") or "")
    except Exception as e:
        seanren.log(seanren.name).error(f"Failed to connect to Seanren: {e}")
