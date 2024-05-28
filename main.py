import cv2
import time
import logging
import threading  # type: ignore

from colorama import Fore, init
from src.voice_assistant.config import Config
from src.voice_assistant.utils import delete_file
from src.voice_assistant.text_to_speech import text_to_speech
from src.voice_assistant.audio import record_audio, play_audio
from src.voice_assistant.transcription import transcribe_audio
from src.voice_assistant.response_generation import generate_response
from src.voice_assistant.api_key_manager import get_transcription_api_key, get_response_api_key, get_tts_api_key

# Configure logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Initialize colorama
init(autoreset=True)


def capture_frame_on_speech():
    """
    Capture a frame from the webcam when the user starts speaking.
    """
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        logging.error("Error: Could not open webcam.")
        return

    stop_event = threading.Event()

    def capture_frame():
        while not stop_event.is_set():
            ret, frame = cap.read()
            if not ret:
                logging.error("Error: Failed to capture frame.")
                break

            cv2.imshow('Webcam', frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                stop_event.set()
                break

    # Start the webcam thread
    webcam_thread = threading.Thread(target=capture_frame)
    webcam_thread.start()

    chat_history = [
        {"role": "system", "content": "You are a helpful Assistant. Keep your answers short and concise."}
    ]

    try:
        while not stop_event.is_set():
            try:
                # Record audio from the microphone and save it as 'test.wav'
                record_audio('test.wav')

                # Get the API key for transcription
                transcription_api_key = get_transcription_api_key()

                # Transcribe the audio file
                user_input = transcribe_audio(
                    Config.TRANSCRIPTION_MODEL, transcription_api_key, 'test.wav', Config.LOCAL_MODEL_PATH)
                logging.info(f"{Fore.GREEN}You said: {user_input}")

                # Capture a frame from the webcam
                ret, frame = cap.read()
                if ret:
                    cv2.imwrite('snapshot.jpg', frame)
                    logging.info(
                        f"{Fore.GREEN}Snapshot taken and saved as 'snapshot.jpg'")

                # Append the user's input to the chat history
                chat_history.append({"role": "user", "content": user_input})

                # Get the API key for response generation
                response_api_key = get_response_api_key()

                # Generate a response
                response_text = generate_response(
                    Config.RESPONSE_MODEL, response_api_key, chat_history, Config.LOCAL_MODEL_PATH)
                logging.info(f"{Fore.CYAN}Response: {response_text}")

                # Append the assistant's response to the chat history
                chat_history.append(
                    {"role": "assistant", "content": response_text})

                # Determine the output file format based on the TTS model
                output_file = 'output.mp3' if Config.TTS_MODEL == 'openai' else 'output.wav'

                # Get the API key for TTS
                tts_api_key = get_tts_api_key()

                # Convert the response text to speech and save it to the appropriate file
                text_to_speech(Config.TTS_MODEL, tts_api_key,
                               response_text, output_file, Config.LOCAL_MODEL_PATH)

                # Play the generated speech audio
                play_audio(output_file)

                # Clean up audio files
                delete_file('test.wav')
                delete_file(output_file)

            except Exception as e:
                logging.error(f"{Fore.RED}An error occurred: {e}")
                delete_file('test.wav')
                if 'output_file' in locals():
                    delete_file(output_file)
                time.sleep(1)
    finally:
        stop_event.set()
        webcam_thread.join()
        cap.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    capture_frame_on_speech()
