import time
import pygame
import logging
import speech_recognition as sr


def record_audio(file_path, timeout=100, phrase_time_limit=50, retries=3):
    """
    Record audio from the microphone and save it as a WAV file.

    Args:
    file_path (str): The path to save the recorded audio file.
    timeout (int): Maximum time to wait for a phrase to start (in seconds).
    phrase_time_limit (int): Maximum time for the phrase to be recorded (in seconds).
    retries (int): Number of retries if recording fails.
    """
    recognizer = sr.Recognizer()
    for attempt in range(retries):
        try:
            with sr.Microphone() as source:
                logging.info("Recording started")
                # Listen for the first phrase and extract it into audio data
                audio_data = recognizer.listen(
                    source, timeout=timeout, phrase_time_limit=phrase_time_limit)
                logging.info("Recording complete")
                # Save the recorded audio data to a WAV file
                with open(file_path, "wb") as audio_file:
                    audio_file.write(audio_data.get_wav_data())
                return
        except sr.WaitTimeoutError:
            logging.warning(
                f"Listening timed out, retrying... ({attempt + 1}/{retries})")
        except Exception as e:
            logging.error(f"Failed to record audio: {e}")
            break
    else:
        logging.error("Recording failed after all retries")


def play_audio(file_path, sleep_duration=1, check_interval=0.1):
    """
    Play an audio file using pygame.

    Args:
    file_path (str): The path to the audio file to play.
    sleep_duration (float): Duration to sleep between checks if the audio is still playing.
    check_interval (float): Interval to check if the audio is still playing.
    """
    try:
        pygame.mixer.init()
        pygame.mixer.music.load(file_path)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            time.sleep(check_interval)
        pygame.mixer.quit()
    except pygame.error as e:
        logging.error(f"Failed to play audio: {e}")
    except Exception as e:
        logging.error(f"An unexpected error occurred while playing audio: {e}")
