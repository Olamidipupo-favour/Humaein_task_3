# 🤖 AI Setup Guide

## Why You're Getting Fallback Responses

The AI Medical Coding feature is currently using **fallback responses** instead of real AI because the Google API key is not configured.

## 🔑 How to Enable Real AI

### Step 1: Get Google Gemini API Key

1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the generated API key

### Step 2: Set Environment Variable

#### Option A: Docker Compose (Recommended)
Add to your `docker-compose.yml`:

```yaml
api:
  environment:
    - GOOGLE_API_KEY=your_api_key_here
    # ... other environment variables
```

#### Option B: Local Development
Create a `.env` file in the `api/` directory:

```bash
GOOGLE_API_KEY=your_api_key_here
```

#### Option C: System Environment
```bash
export GOOGLE_API_KEY=your_api_key_here
```

### Step 3: Restart Services

```bash
docker-compose down
docker-compose up --build
```

## ✅ Verification

After setting up the API key:

1. Go to the **AI Medical Coding** page
2. Enter some clinical notes (e.g., "Patient has diabetes and hypertension")
3. You should see:
   - ✅ **AI Analysis** (green box) instead of ⚠️ **Fallback Mode** (yellow box)
   - Dynamic codes based on your input
   - Detailed AI rationale

## 🧪 Test Cases

Try these clinical notes to see AI in action:

- **Diabetes**: "Patient presents with uncontrolled type 2 diabetes, HbA1c 9.2%"
- **Hypertension**: "Patient has essential hypertension, BP 150/95"
- **Chest Pain**: "Patient complains of chest pain, EKG shows ST elevation"
- **Office Visit**: "Established patient follow-up for routine care"

## 🔍 What Changed

### Before (Fallback Mode):
- Simple keyword matching
- Same codes every time
- No real AI analysis

### After (AI Mode):
- Real AI analysis of clinical notes
- Dynamic code suggestions
- Detailed rationale
- Context-aware coding

## 🚨 Troubleshooting

If you still see fallback mode:

1. **Check API Key**: Ensure `GOOGLE_API_KEY` is set correctly
2. **Restart Services**: `docker-compose restart api`
3. **Check Logs**: `docker-compose logs api` for errors
4. **Verify Billing**: Ensure your Google Cloud account has billing enabled

## 💡 Pro Tips

- The AI will generate different codes based on the clinical context
- More detailed clinical notes = better AI suggestions
- The system gracefully falls back if AI is unavailable
- All responses include confidence scores
