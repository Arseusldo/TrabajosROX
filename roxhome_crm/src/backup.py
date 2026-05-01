from shutil import copy2
from datetime import datetime
from .config import DB_PATH, BACKUP_DIR

def create_backup():
    target = BACKUP_DIR / f"roxhome_backup_{datetime.now().strftime('%Y%m%d_%H%M')}.db"
    copy2(DB_PATH, target)
    return target
