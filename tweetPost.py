import requests
from requests_oauthlib import OAuth1
import os
import random
# === Your Keys ===
API_KEY = os.environ.get("API_KEY")
API_SECRET = os.environ.get("API_SECRET")
ACCESS_TOKEN = os.environ.get("ACCESS_TOKEN")
ACCESS_SECRET = os.environ.get("ACCESS_SECRET")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

auth = OAuth1(API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_SECRET)

# === Step 1: Ask Gemini to generate 2-part content ===
gemini_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}"
headers = {"Content-Type": "application/json"}
topics = [
    "Genomics AI", "Retrieval-Augmented Generation (RAG)", "video generation (Sora, Runway, Pika)",
    "large language models (GPT-4, Claude, LLaMA)", "transformers", "embeddings", "attention mechanisms",
    "optimization (SGD, Adam)", "tokenization", "BERT", "NER",
    "multimodal AI (CLIP, GPT-4o)", "text-to-image", "text-to-video", "text-to-audio",
    "reinforcement learning (Q-learning, PPO)", "AutoGPT agents", "protein folding (AlphaFold)",
    "AI in genomics", "AI in healthcare", "AI in law", "AI in finance", "AI in blockchain", 
    "AI in customer support", "AI in education", "AI in logistics", "AI in gaming",
    "LLM hallucinations", "prompt engineering", "debugging with ChatGPT", "LLM jailbreaking"
]
selected_topic = random.choice(topics)
prompt = (
    f"You're an AI humorist and tech creator. Today's topic is: {selected_topic}.\n"
    "Write:\n"
    "1. A funny one-liner tweet about this topic (max 250 characters).\n"
    "2. A follow-up explanation tweet (max 250 characters).\n"
    "Respond with only the two tweets as plain text, separated by a line break. No labels, no intro, no extra formatting."
)
data = {
    "contents": [
        {
            "parts": [{"text": prompt}]
        }
    ]
}

gemini_response = requests.post(gemini_url, headers=headers, json=data)

if gemini_response.status_code == 200:
    raw_output = gemini_response.json()['candidates'][0]['content']['parts'][0]['text'].strip()
    lines = raw_output.split("\n")
    tweets = [line.strip() for line in lines if line.strip()]

    if len(tweets) >= 2:
        tweet1_text = tweets[0]
        tweet2_text = tweets[1]

        # === Step 2: Post Tweet 1 ===
        tweet1 = {"text": tweet1_text}
        response1 = requests.post("https://api.twitter.com/2/tweets", auth=auth, json=tweet1)

        if response1.status_code == 201:
            tweet1_id = response1.json()["data"]["id"]
            print("Tweet 1 posted:", tweet1_text)

            # === Step 3: Post Tweet 2 as a reply ===
            tweet2 = {
                "text": tweet2_text,
                "reply": {"in_reply_to_tweet_id": tweet1_id}
            }

            response2 = requests.post("https://api.twitter.com/2/tweets", auth=auth, json=tweet2)

            if response2.status_code == 201:
                print("Tweet 2 posted as thread:", tweet2_text)
            else:
                print("Tweet 2 failed:", response2.text)

        else:
            print("Tweet 1 failed:", response1.text)

    else:
        print("Gemini did not return two tweet lines:", tweets)

else:
    print("Gemini API failed:", gemini_response.text)
