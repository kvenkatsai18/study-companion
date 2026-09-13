# Study Companion — AI Learning Partner

A voice-first AI study companion that talks to you, helps with research, and creates study materials. Speak or type — it responds aloud with a friendly animated avatar.

## Features

- 🎤 **Voice input** — speak naturally, the AI listens
- 🗣️ **Voice output** — responds audibly with realistic Edge TTS speech
- 🤖 **Animated avatar** — friendly robot face that animates while speaking
- 📚 **Study assistance** — exam prep, research, learning any topic
- 💬 **Conversational memory** — remembers your conversation within a session

## Tech Stack

- **Backend:** Python Flask
- **AI:** Groq (fast LPU inference, OpenAI-compatible API)
- **Voice:** Edge TTS (Microsoft)
- **Frontend:** HTML/CSS/JavaScript
- **Avatar:** CSS-animated robot character
- **Deploy:** Vercel

## Setup

### Local Development

1. Clone the repo:
   ```bash
   git clone https://github.com/kvenkatsai18/study-companion.git
   cd study-companion
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Add your Groq API key:
   ```bash
   cp .env.example .env
   # Edit .env and add: GROQ_API_KEY=your_key_here
   ```

   Get your key at [console.groq.com](https://console.groq.com/keys)

4. Run the app:
   ```bash
   python app.py
   ```

5. Open [http://localhost:5000](http://localhost:5000)

### Deploy to Vercel

1. Push to GitHub
2. Connect the repo to Vercel
3. Add `GROQ_API_KEY` environment variable in Vercel project settings
4. Deploy

**Live demo:** https://study-companion-sooty-six.vercel.app

## AI Model

Uses `groq/compound-mini` by default — fast, affordable, great for conversational AI. You can change the model in `app.py` (`GROQ_MODEL`) to any Groq-supported model like `llama-3.1-8b-instant`.

## Project Structure

```
study-companion/
├── app.py              # Flask backend + AI logic
├── requirements.txt    # Python dependencies
├── templates/
│   └── index.html      # Frontend UI
├── .env.example        # Environment variable template
└── README.md
```
