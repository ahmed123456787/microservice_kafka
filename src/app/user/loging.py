import logging
from fluent import sender
from fluent import event
import json
from datetime import datetime

# Configure Fluentd sender
fluent_sender = sender.FluentSender('user-service', host='fluentd', port=24224)

class FluentHandler(logging.Handler):
    def __init__(self, tag_prefix='user-service'):
        super().__init__()
        self.tag_prefix = tag_prefix
        
    def emit(self, record):
        try:
            # Create structured log data
            log_data = {
                'timestamp': datetime.fromtimestamp(record.created).isoformat(),
                'level': record.levelname,
                'message': record.getMessage(),
                'module': record.module,
                'function': record.funcName,
                'line': record.lineno,
                'service': 'user-service'
            }
            
            # Add exception info if present
            if record.exc_info:
                log_data['exception'] = self.format(record)
            
            # Send to Fluentd
            tag = f"{self.tag_prefix}.{record.levelname.lower()}"
            fluent_sender.emit(tag, log_data)
            
        except Exception:
            # Fallback to console if Fluentd is unavailable
            pass

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

# Get logger and add Fluentd handler
logger = logging.getLogger('user-service')
fluent_handler = FluentHandler()
logger.addHandler(fluent_handler)


# Convenience functions for structured logging
def log_user_action(action: str, user_id: int = None, details: dict = None):
    """Log user-related actions with structured data"""
    log_data = {
        'action': action,
        'user_id': user_id,
        'details': details or {},
        'service': 'user-service',
        'timestamp': datetime.now().isoformat()
    }
    fluent_sender.emit('user-service.action', log_data)


def log_api_request(method: str, endpoint: str, status_code: int, duration: float = None, user_id: int = None):
    """Log API requests with structured data"""
    log_data = {
        'method': method,
        'endpoint': endpoint,
        'status_code': status_code,
        'duration_ms': duration,
        'user_id': user_id,
        'service': 'user-service',
        'timestamp': datetime.now().isoformat()
    }
    fluent_sender.emit('user-service.api', log_data)


def log_error(error_type: str, message: str, details: dict = None):
    """Log errors with structured data"""
    log_data = {
        'error_type': error_type,
        'message': message,
        'details': details or {},
        'service': 'user-service',
        'timestamp': datetime.now().isoformat()
    }
    fluent_sender.emit('user-service.error', log_data)