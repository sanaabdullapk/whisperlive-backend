# run_server.py

import socketio
import eventlet
from faster_whisper import WhisperModel

# Create a Socket.IO server
sio = socketio.Server(cors_allowed_origins='*')
app = socketio.WSGIApp(sio)

# Load Whisper model (you can use "tiny", "base", "small", "medium")
print("🔄 Loading Whisper model...")
model = WhisperModel("base")
print("✅ Whisper model loaded!")

# Handle client connection
@sio.event
def connect(sid, environ):
    print(f"🔌 Client connected: {sid}")

# Handle incoming audio chunks
@sio.event
def audio(sid, data):
    print(f"🎧 Received audio from {sid} - {len(data)} bytes")

    try:
        # Convert bytes to float32 numpy array
        import numpy as np
        audio_array = np.frombuffer(data, np.int16).astype(np.float32) / 32768.0

        # Transcribe using faster-whisper
        segments, _ = model.transcribe(audio_array)

        # Combine the text from all segments
        full_text = " ".join(segment.text for segment in segments).strip()

        if full_text:
            print(f"📝 Transcribed: {full_text}")
            # Emit the transcription back to client
            sio.emit('transcription', full_text, to=sid)
        else:
            print("🔇 No speech detected.")

    except Exception as e:
        print(f"⚠️ Error during transcription: {e}")
        sio.emit('transcription', '', to=sid)

# Handle client disconnection
@sio.event
def disconnect(sid):
    print(f"❌ Client disconnected: {sid}")

# Run the WSGI server
if __name__ == '__main__':
    print("🚀 Starting WhisperLive backend on port 5000...")
    eventlet.wsgi.server(eventlet.listen(('0.0.0.0', 5000)), app)



