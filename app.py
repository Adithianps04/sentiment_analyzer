import openai
import requests

def read_keys_from_file(file_path='keys.txt'):
    with open(file_path, 'r') as file:
        keys = {}
        for line in file:
            key, value = line.strip().split('=')
            keys[key] = value
        return keys

def download_social_media_post(url):
    response = requests.get(url)
    
    if response.status_code == 200:
        return response.text
    else:
        print(f"Failed to download content. Status code: {response.status_code}")
        return None

def analyze_sentiment_with_openai(text, api_key):
    openai.api_key = api_key
    prompt = f"Sentiment analysis of the following text: '{text}'"

    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=100
    )

    sentiment = response['choices'][0]['text'].strip()
    return sentiment

# Read API key and social media post URL from keys.txt
keys = read_keys_from_file()
api_key = keys.get('OPENAI_API_KEY', '')
social_media_post_url = keys.get('SOCIAL_MEDIA_POST_URL', '')

if not api_key or not social_media_post_url:
    print("API key or social media post URL not found in keys.txt")
else:
    post_content = download_social_media_post(social_media_post_url)

    if post_content:
        sentiment = analyze_sentiment_with_openai(post_content, api_key)
        print(f'Sentiment: {sentiment}')
