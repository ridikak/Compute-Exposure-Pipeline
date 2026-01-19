import json
from pathlib import Path
CFG = json.loads(Path("config.json").read_text())
