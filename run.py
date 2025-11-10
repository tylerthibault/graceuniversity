from src import create_app

"""Application entry point.

This module serves as the entry point for running the Flask application.
It imports and runs the app instance created in the __init__ file.
"""


app = create_app()

if __name__ == '__main__':
    """Run the Flask development server.
    
    Debug mode is enabled for development. In production, this should be
    run with a proper WSGI server (gunicorn, uwsgi, etc.) with debug=False.
    """
    app.run(debug=True, host='0.0.0.0', port=5000)