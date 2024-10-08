import logging

from openai import OpenAI
from deepgram import DeepgramClient, SpeakOptions


def text_to_speech(model, api_key, text, output_file_path, local_model_path=None):
    """
    Convert text to speech using the specified model.

    Args:
    model (str): The model to use for TTS ('openai', 'deepgram', 'local').
    api_key (str): The API key for the TTS service.
    text (str): The text to convert to speech.
    output_file_path (str): The path to save the generated speech audio file.
    local_model_path (str): The path to the local model (if applicable).
    """
    try:
        if model == 'openai':
            client = OpenAI(api_key=api_key)
            speech_response = client.audio.speech.create(
                model="tts-1",
                voice="fable",
                input=text,
                response_format="mp3"
            )
            logging.info(f"OpenAI filepath: {output_file_path}")
            speech_response.stream_to_file(output_file_path)
            with open(output_file_path, "wb") as audio_file:
                # Ensure this correctly accesses the binary content
                audio_file.write(speech_response['data'])

        elif model == 'deepgram':
            client = DeepgramClient(api_key=api_key)
            options = SpeakOptions(
                model="aura-angus-en",  # Change voice if needed
                encoding="linear16",
                container="wav"
            )
            SPEAK_OPTIONS = {"text": text}
            response = client.speak.v("1").save(
                output_file_path, SPEAK_OPTIONS, options)
            logging.info(f"Deepgram response: {response}")

        elif model == 'local':
            # Placeholder for local TTS model
            with open(output_file_path, "wb") as f:
                f.write(b"Local TTS audio data")
        else:
            raise ValueError("Unsupported TTS model")
    except Exception as e:
        logging.error(f"Failed to convert text to speech: {e}")
        return None