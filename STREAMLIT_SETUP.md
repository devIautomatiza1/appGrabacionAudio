# Streamlit Cloud Setup Guide

This guide explains how to configure your audio recording application on Streamlit Cloud.

## 1. Deploying to Streamlit Cloud

### Prerequisites
- A GitHub account with your project repository
- A Streamlit Cloud account (free at https://streamlit.io/cloud)

### Deployment Steps

1. **Push your code to GitHub**
   ```bash
   git add .
   git commit -m "Ready for Streamlit Cloud deployment"
   git push origin main
   ```

2. **Log in to Streamlit Cloud**
   - Visit https://share.streamlit.io
   - Sign in with your GitHub account or create a new account

3. **Deploy New App**
   - Click "New app" button
   - Select your GitHub repository
   - Select the branch (usually `main`)
   - Enter the main file path: `streamlit_app.py`
   - Click "Deploy"

## 2. Configuring Secrets

Sensitive information like API keys should never be committed to GitHub. Streamlit Cloud uses Secrets management for this.

### Adding Secrets in Streamlit Cloud

1. **Go to App Settings**
   - On your deployed app page, click the three dots (⋮) in the top right
   - Select "Settings"

2. **Navigate to Secrets**
   - In the settings, find the "Secrets" section
   - Click on the "Secrets" tab

3. **Add Your Configuration**
   - Paste the following template and fill in your values:

   ```ini
   GEMINI_API_KEY = "your-gemini-api-key-here"
   SUPABASE_URL = "your-supabase-url-here"
   SUPABASE_KEY = "your-supabase-key-here"
   LOG_LEVEL = "INFO"
   ```

### Example with Real Values
```ini
GEMINI_API_KEY = "AIzaSyD..."
SUPABASE_URL = "https://your-project.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
LOG_LEVEL = "INFO"
```

4. **Save** - Click the Save button

## 3. Getting Your API Credentials

### Google Gemini API Key
1. Visit Google Cloud Console: https://console.cloud.google.com
2. Create a new project or select existing one
3. Enable the Generative AI API
4. Create an API key in Credentials section
5. Copy the API key to `GEMINI_API_KEY`

### Supabase Credentials
1. Visit Supabase: https://supabase.com
2. Log in or create account
3. Open your project
4. Go to Settings → API
5. Find your project URL (under "Project URL") → copy to `SUPABASE_URL`
6. Find your API key (under "Project API keys" - "anon" public key) → copy to `SUPABASE_KEY`

## 4. Using Secrets in Local Development

### Create `.env` file for local testing
```bash
# Copy the template
cp .env.example .env

# Edit .env and add your actual values
# DO NOT commit this file!
```

### Your `.env` file should look like:
```ini
GEMINI_API_KEY=your-actual-key
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-actual-key
LOG_LEVEL=INFO
```

## 5. Local vs Cloud Configuration

### How Streamlit reads secrets:

**Local Development:**
- Reads from `.env` file (via `python-dotenv`)
- Falls back to `st.secrets` if `.env` not found

**Streamlit Cloud:**
- Reads from "Secrets" section in app settings
- Uses `st.secrets` directly
- `.env` files are not used (security)

### Example Code (already in use)
```python
# This automatically checks both local .env and Streamlit Cloud secrets
supabase_url = st.secrets.get("SUPABASE_URL")
supabase_key = st.secrets.get("SUPABASE_KEY")
gemini_key = st.secrets.get("GEMINI_API_KEY")
```

## 6. Database Setup

After deploying to Streamlit Cloud, you need to ensure your Supabase database is initialized:

1. Run your app once - it will automatically create the database tables if they don't exist
2. Or manually run the SQL from `basedatos.sql` in Supabase SQL Editor
3. Verify tables are created: `recordings`, `transcriptions`, `opportunities`

## 7. Troubleshooting

### "name 'st' is not defined" or import errors
- Make sure all required packages are in `requirements.txt`
- Check Streamlit Logs in app settings for detailed errors

### "Secret 'SUPABASE_URL' not found"
- Make sure you added the secret in Streamlit Cloud Settings → Secrets section
- Redeploy or refresh after adding secrets
- Check the exact key name (case-sensitive)

### "Connection timeout to Supabase"
- Verify `SUPABASE_URL` is correct format: `https://your-project.supabase.co`
- Check `SUPABASE_KEY` is valid in Supabase dashboard
- Ensure Supabase project is not paused

### "ModuleNotFoundError: No module named 'X'"
- Add missing package to `requirements.txt`
- Run `pip install -r requirements.txt` locally
- Commit changes and redeploy

### Logs not appearing
- Check `LOG_LEVEL` setting (default is "INFO")
- Logs appear in app's "Logs" section in Streamlit Cloud Settings
- Can also check terminal output if running locally

## 8. Security Best Practices

✅ **DO:**
- Keep `.env` file in `.gitignore` (already configured)
- Use Streamlit Cloud Secrets for production
- Rotate API keys periodically
- Use Supabase Row Level Security (RLS) for database

❌ **DON'T:**
- Commit API keys to GitHub
- Share `.env` files with anyone
- Use the same keys for development and production
- Post keys in GitHub issues or discussions

## 9. Useful Commands

```bash
# Test local setup
streamlit run streamlit_app.py

# Check requirements are installed
pip install -r requirements.txt

# View logs locally
tail -f logs/app.log

# Deploy specific branch
# (Done through Streamlit Cloud UI)
```

## 10. Support Resources

- **Streamlit Documentation**: https://docs.streamlit.io
- **Streamlit Cloud Docs**: https://docs.streamlit.io/streamlit-community-cloud
- **Google Gemini API**: https://ai.google.dev
- **Supabase Documentation**: https://supabase.com/docs
