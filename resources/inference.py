from prodiapy import AsyncProdia, Prodia
import os

prodia = AsyncProdia(os.getenv("PRODIA"))
syncprodia = Prodia(os.getenv("PRODIA"))
