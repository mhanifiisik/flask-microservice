import signal
import sys
import threading
import os
from time import sleep, time
from flask import Flask, request, jsonify
from werkzeug.middleware.proxy_fix import ProxyFix
from werkzeug.serving import make_server
from werkzeug.exceptions import RequestTimeout
from prometheus_flask_exporter import PrometheusMetrics
import socket
from loguru import logger

from config import Config

is_shutting_down = False
server = None

def configure_logging():
    """Configure Loguru logger instance"""
    logger.remove()
    
    logger.add(
        sys.stdout,
        format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
        level=Config.LOG_LEVEL,
        colorize=True
    )
    
    logger.add(
        "logs/app.log",
        rotation="500 MB",
        retention="10 days",
        compression="zip",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
        level=Config.LOG_LEVEL
    )

def create_server(app):
    """Create and configure server instance"""
    server = make_server(Config.HOST, Config.PORT, app, threaded=True)
    server.socket.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
    server.socket.settimeout(Config.KEEP_ALIVE_TIMEOUT)
    return server

def run_server(server):
    """Run server in a separate thread"""
    def server_thread():
        logger.info(f"Starting server on {Config.HOST}:{Config.PORT}")
        server.serve_forever()

    thread = threading.Thread(target=server_thread)
    thread.start()
    return thread

def create_app():
    """Create and configure Flask application"""
    app = Flask(__name__)
    app.wsgi_app = ProxyFix(app.wsgi_app)
    app.config.from_object(Config)
    
    metrics = PrometheusMetrics(app)
    metrics.info('flask_info', 'Flask application info', 
                version='1.0.0', app_name='flask-app')
    
    return app

def setup_routes(app):
    """Configure application routes"""
    @app.route('/')
    def index():
        logger.debug("Processing request to index endpoint")
        return jsonify({"message": "Hello, World!"})

    @app.route('/health-check')
    def health_check():
        logger.debug("Health check requested")
        return jsonify({"message": "OK!"})

    @app.route('/shutdown', methods=['POST'])
    def shutdown():
        logger.warning("Shutdown requested via endpoint")
        initiate_shutdown()
        return jsonify({"message": "Server shutting down..."})

def setup_request_handlers(app):
    """Configure request handlers and middleware"""
    @app.before_request
    def start_request():
        request.start_time = time()
        logger.info(f"Incoming {request.method} request to {request.url}")

    @app.after_request
    def end_request(response):
        duration = time() - request.start_time
        if duration > Config.REQUEST_TIMEOUT:
            logger.error(f"Request timeout: {request.method} {request.url} ({duration:.2f}s)")
            return jsonify({
                'error': 'Request timed out',
                'message': 'The request took too long to process'
            }), 408
        logger.info(f"Request completed: {response.status} ({duration:.2f}s)")
        return response

def initiate_shutdown(timeout=None):
    """Initiate graceful server shutdown"""
    global is_shutting_down
    if is_shutting_down:
        logger.warning("Shutdown already in progress")
        return

    is_shutting_down = True
    timeout = timeout or Config.GRACEFUL_SHUTDOWN_TIMEOUT

    def shutdown_server():
        logger.warning(f"Graceful shutdown initiated with {timeout}s timeout")
        if server:
            server.shutdown()
        logger.info("Server has been shut down")
        os._exit(0)

    threading.Thread(target=shutdown_server).start()

def setup_signal_handlers():
    """Configure system signal handlers"""
    def signal_handler(sig, frame):
        if not is_shutting_down:
            logger.warning(f"Received signal {sig}, initiating graceful shutdown")
            initiate_shutdown()
        else:
            logger.info("Ignoring signal, shutdown already in progress")

    signal.signal(signal.SIGTERM, signal_handler)
    signal.signal(signal.SIGINT, signal_handler)

def main():
    """Application entry point"""
    global server
    
    configure_logging()
    logger.info("Starting Flask application")
    
    try:
        app = create_app()
        setup_routes(app)
        setup_request_handlers(app)
        setup_signal_handlers()
        
        server = create_server(app)
        server_thread = run_server(server)
        
        while not is_shutting_down:
            sleep(1)
            
    except Exception as e:
        logger.exception(f"Unexpected error occurred: {e}")
        initiate_shutdown()
    except (KeyboardInterrupt, SystemExit):
        if not is_shutting_down:
            logger.warning("Main thread received exit signal")
            initiate_shutdown()

if __name__ == '__main__':
    main()