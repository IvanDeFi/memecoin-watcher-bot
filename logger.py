import logging

logger = logging.getLogger("memecoin-watcher")
logger.setLevel(logging.INFO)

formatter = logging.Formatter("[%(asctime)s] %(levelname)s — %(message)s")

console = logging.StreamHandler()
console.setFormatter(formatter)
logger.addHandler(console)
