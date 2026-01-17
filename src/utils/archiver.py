import os
import shutil
import logging
from datetime import datetime, timedelta

# Constants
PROCESSED_DIR = "data/Processed"
ARCHIVE_DIR = "data/Archive"

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class Archiver:
    def __init__(self, retention_days=30):
        self.retention_days = retention_days
        
    def run(self):
        if not os.path.exists(PROCESSED_DIR):
            logger.info("No Processed directory to archive.")
            return

        now = datetime.now()
        files = [f for f in os.listdir(PROCESSED_DIR) if f.endswith('.json')]
        
        archived_count = 0
        
        for f in files:
            file_path = os.path.join(PROCESSED_DIR, f)
            try:
                # Get file creation/modification time
                mtime = os.path.getmtime(file_path)
                file_date = datetime.fromtimestamp(mtime)
                
                age_days = (now - file_date).days
                
                if age_days > self.retention_days:
                    self._archive_file(f, file_path, file_date)
                    archived_count += 1
            except Exception as e:
                logger.error(f"Error checking file {f}: {e}")
                
        if archived_count > 0:
            logger.info(f"📦 Archived {archived_count} files older than {self.retention_days} days.")
        else:
            logger.info("No files need archiving.")

    def _archive_file(self, filename, src_path, file_date):
        # Determine target folder (YYYY-MM)
        month_str = file_date.strftime("%Y-%m")
        target_dir = os.path.join(ARCHIVE_DIR, month_str)
        os.makedirs(target_dir, exist_ok=True)
        
        # Move file
        dst_path = os.path.join(target_dir, filename)
        shutil.move(src_path, dst_path)
        logger.info(f"Moved {filename} to {target_dir}")
        
        # Future: Trigger summary generation here before moving?
        # For now, per plan, just move. Summary generation can look at Archive dir later.

if __name__ == "__main__":
    archiver = Archiver()
    archiver.run()
