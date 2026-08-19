from werkzeug.exceptions import HTTPException
import logging
from flask import jsonify, current_app    # ← import current_app instead
                                          # ← remove "from app import app"

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# ─── Custom Exception Classes ─────────────────────────────

class ValidationError(Exception):
    def __init__(self, message, status_code=400):
        self.message = message
        self.status_code = status_code


class AuthenticationError(Exception):
    def __init__(self, message='Authentication required'):
        self.message = message
        self.status_code = 401


# ─── Error Handlers ───────────────────────────────────────
# Register these as plain functions — attach to app in app.py

def not_found(error):
    return jsonify({
        'error': 'Resource not found',
        'message': str(error)
    }), 404


def unauthorized(error):
    return jsonify({
        'error': 'Unauthorized',
        'message': str(error)
    }), 401


def handle_validation_error(error):
    return jsonify({
        'error': 'Validation failed',
        'message': error.message
    }), error.status_code


def handle_http_exception(error):
    return jsonify({
        'error': error.name,
        'message': error.description
    }), error.code


def handle_unexpected_error(error):
    logger.error(f'Unexpected error: {error}', exc_info=True)

    if current_app.config['DEBUG']:          # ← current_app works inside a request
        return jsonify({
            'error': 'Internal server error',
            'message': str(error)
        }), 500

    return jsonify({
        'error': 'Internal server error',
        'message': 'An unexpected error occurred'
    }), 500