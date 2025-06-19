import requests
from requests_oauthlib import OAuth1
import os
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

prompt = (
    "I’m a tech creator simplifying cutting-edge AI — from Genomics AI and Retrieval-Augmented Generation (RAG) to video generation (Sora, Runway, Pika) and LLMs (GPT-4, Claude, LLaMA).I break down neural networks (MLP, CNN, RNN), transformers, embeddings, attention, and optimization (SGD, Adam). I explore NLP (tokenization, BERT, NER), multimodal AI (CLIP, GPT-4o), and GenAI (text-to-image, video, audio).I cover reinforcement learning (Q-learning, PPO), AutoGPT agents, protein folding (AlphaFold), and AI in genomics, healthcare, and law — with a side of memes and punchlines. If it’s powerful, complex, or hilarious in AI, I’m posting it. "
    "I want to add humor to make it engaging. Please give me two tweets: "
    "1. A funny AI one-liner (max 250 characters). "
    "2. A follow-up explanation tweet (also max 250 characters).Note Dont write follow up just provide text "
    "Add relevant emojis and hashtags. Only give the two tweet texts, no labels, no formatting."
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
