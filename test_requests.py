import requests

def test_chat():
    url = "http://127.0.0.1:8000/chat"  # Adjust if your server runs on a different address or port
    data = {
        "query": "What is the capital of France?",
        "category": "knowledge"
    }

    response = requests.post(url, json=data)

    if response.status_code == 200:
        print("Response from /chat:", response.json())
    else:
        print("Error:", response.status_code, response.text)

if __name__ == "__main__":
    test_chat()
