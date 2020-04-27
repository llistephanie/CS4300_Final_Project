from app import app, socketio
import sys

cli = sys.modules['flask.cli']
cli.show_server_banner = lambda *x: None

if __name__ == "__main__":
  print("Flask app running at http://0.0.0.0:5000")
  socketio.run(app, host="0.0.0.0", port=5000)
