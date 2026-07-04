"""
Simple file logger with size-based rotation. Max 1MB per file.
"""
import os
import datetime

LOG_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'logs')
LOG_FILE = os.path.join(LOG_DIR, 'app.log')
MAX_SIZE = 1 * 1024 * 1024  # 1MB


def _ensure_dir():
    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR)


def _timestamp():
    return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')


def _rotate():
    """Rename current log file with timestamp suffix, create fresh one."""
    if not os.path.exists(LOG_FILE):
        return
    stamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    base, ext = os.path.splitext(LOG_FILE)
    rotated = f'{base}.{stamp}{ext}'
    os.rename(LOG_FILE, rotated)


def _check_rotate():
    """Rotate if log file exceeds MAX_SIZE."""
    if os.path.exists(LOG_FILE) and os.path.getsize(LOG_FILE) >= MAX_SIZE:
        _rotate()


def log(level, message):
    """Write a log entry. level: 'INFO', 'WARN', 'ERROR'."""
    _ensure_dir()
    _check_rotate()
    line = f'[{_timestamp()}] [{level}] {message}\n'
    with open(LOG_FILE, 'a', encoding='utf-8') as f:
        f.write(line)


def info(message):
    log('INFO', message)


def warn(message):
    log('WARN', message)


def error(message):
    log('ERROR', message)
