import os
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from dotenv import load_dotenv, find_dotenv

# Load environment variables
def load_environment_variables():
    load_dotenv(find_dotenv())
    return os.getenv("COOKIE")

# Create headers for the request
def create_headers(cookie):
    return {
        "Accept": "application/json, text/plain, */*",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "en-US,en;q=0.9",
        "Content-Type": "application/json",
        "Cookie": f"{cookie}",
        "Origin": "https://www.zerogpt.com",
        "Referer": "https://www.zerogpt.com/",
        "Sec-Ch-Ua": "\"Google Chrome\";v=\"125\", \"Chromium\";v=\"125\", \"Not.A/Brand\";v=\"24\"",
        "Sec-Ch-Ua-Mobile": "?0",
        "Sec-Ch-Ua-Platform": "\"Windows\"",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-site",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
    }

# Create a retry-enabled session
def create_retry_session(total_retries=3, backoff_factor=1, status_forcelist=None, allowed_methods=None):
    if status_forcelist is None:
        status_forcelist = [429, 500, 502, 503, 504]
    if allowed_methods is None:
        allowed_methods = ["HEAD", "GET", "OPTIONS", "POST"]
    
    retry_strategy = Retry(
        total=total_retries,
        status_forcelist=status_forcelist,
        allowed_methods=allowed_methods,
        backoff_factor=backoff_factor
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session = requests.Session()
    session.mount("https://", adapter)
    session.mount("http://", adapter)
    return session

# Perform a POST request with retry
def post_request(url, headers, body, timeout=10):
    session = create_retry_session()
    try:
        response = session.post(url, headers=headers, json=body, timeout=timeout)
        response.raise_for_status()
        return response
    except requests.exceptions.RequestException as e:
        print(f"An error occurred during the POST request: {e}")
        return None

# Main function to execute the POST request
def main():
    try:
        cookie = load_environment_variables()
        if not cookie:
            raise ValueError("COOKIE environment variable not set.")
        
        headers = create_headers(cookie)
        data = ""  # Replace with your actual data
        body = {"input_text": data}

        response = post_request(URL, headers, body)
        if response:
            print(f"Status Code: {response.status_code}")
            print(f"Response: {response.json()}")
        else:
            print("Failed to get a valid response.")
    except Exception as e:
        print(f"An error occurred in main: {e}")

if __name__ == "__main__":
    URL = "https://api.zerogpt.com/api/detect/detectText"
    main()