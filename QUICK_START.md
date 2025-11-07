# Quick Start: Deploy to Streamlit Cloud

## 🚀 Fast Track (5 Minutes)

### Step 1: Push to GitHub (2 minutes)

```bash
# In your project directory
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
git push -u origin main
```

**Important:** Replace `YOUR_USERNAME` and `YOUR_REPO_NAME` with your actual GitHub username and repository name.

### Step 2: Deploy on Streamlit Cloud (3 minutes)

1. **Go to Streamlit Cloud**
   - Visit: https://share.streamlit.io
   - Sign in with GitHub

2. **Create New App**
   - Click "New app"
   - Select your repository
   - Branch: `main`
   - Main file: `app.py`

3. **Add Secrets**
   - Click "Advanced settings"
   - Click "Secrets"
   - Add:
     ```
     GROQ_API_KEY=your_groq_api_key_here
     ```
   - Click "Save"

4. **Deploy**
   - Click "Deploy"
   - Wait 2-3 minutes
   - Your app will be live!

### Step 3: Test Your App

- Upload a PDF
- Ask a question
- Verify answers and sources are displayed

## 📋 What Gets Deployed

- ✅ `app.py` - Main application
- ✅ `rag_utility.py` - Utility functions
- ✅ `requirements.txt` - Dependencies
- ✅ `.gitignore` - Excludes sensitive files
- ❌ `.env` - NOT deployed (use secrets instead)
- ❌ `doc_vectorstore/` - NOT deployed (created per session)

## 🔑 Getting Your Groq API Key

1. Go to https://console.groq.com/
2. Sign up or log in
3. Navigate to API Keys
4. Create a new API key
5. Copy the key and add it to Streamlit Cloud secrets

## ⚠️ Important Notes

- **File Storage**: Uploaded files are temporary (session-based)
- **Vector Database**: Created fresh for each user session
- **API Limits**: Be aware of Groq API rate limits
- **First Load**: May be slow due to model downloads (one-time)

## 🐛 Troubleshooting

**App won't deploy?**
- Check that `app.py` is in root directory
- Verify `requirements.txt` is correct
- Check deployment logs

**API key errors?**
- Verify secret name is `GROQ_API_KEY` (exact match)
- Check API key is valid and active
- No extra spaces in secret value

**Need help?**
- Check `DEPLOYMENT.md` for detailed guide
- Review Streamlit Cloud docs: https://docs.streamlit.io/streamlit-community-cloud

## ✅ You're Done!

Your app is now live and shareable! 🎉


