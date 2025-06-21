import socketio

# Create a Socket.IO server for frontend
sio = socketio.Server(cors_allowed_origins='*')
app = socketio.WSGIApp(sio)

# Create a Socket.IO client to connect to WhisperLive backend
client_sio = socketio.Client()

@sio.event
def connect(sid, environ):
    print(f"[Frontend] Connected: {sid}")

@sio.event
def disconnect(sid):
    print(f"[Frontend] Disconnected: {sid}")

@sio.event
def audio(sid, data):
    # Relay incoming audio from frontend to WhisperLive backend
    if client_sio.connected:
        client_sio.emit("audio", data)

@client_sio.event
def transcription(data):
    print(f"[WhisperLive] Transcription: {data}")
    # Send result back to frontend
    sio.emit("transcription", data)

def start_whisperlive_client():
    try:
        print("🔌 Connecting to WhisperLive at http://localhost:5000...")
        client_sio.connect("http://localhost:5000")
        print("✅ Connected to WhisperLive!")
    except Exception as e:
        print(f"❌ Could not connect to WhisperLive: {e}")

if __name__ == '__main__':
    start_whisperlive_client()

    from werkzeug.serving import run_simple
    print("🚀 Starting proxy server on port 6000...")
    run_simple('0.0.0.0', 6000, app)
