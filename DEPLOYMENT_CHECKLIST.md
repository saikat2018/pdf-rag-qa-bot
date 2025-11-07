# Streamlit Cloud Deployment Checklist

Use this checklist to ensure your app is ready for deployment.

## Pre-Deployment Checklist

### ✅ Code Files
- [x] `app.py` - Main application file (root directory)
- [x] `rag_utility.py` - Utility functions
- [x] `requirements.txt` - All dependencies listed
- [x] `.gitignore` - Excludes sensitive files and local data
- [x] `README.md` - Project documentation

### ✅ Files to Verify
- [ ] `.gitignore` includes `.env`, `doc_vectorstore/`, `__pycache__/`
- [ ] `requirements.txt` has all required packages
- [ ] No hardcoded API keys in code
- [ ] No local file paths that won't work on cloud

### ✅ GitHub Repository
- [ ] Repository created on GitHub
- [ ] Code pushed to GitHub
- [ ] `.env` file is NOT committed (check `.gitignore`)
- [ ] `doc_vectorstore/` is NOT committed (check `.gitignore`)
- [ ] All necessary files are committed

### ✅ Streamlit Cloud Setup
- [ ] Account created at share.streamlit.io
- [ ] GitHub account connected
- [ ] Repository selected
- [ ] Main file path set to `app.py`
- [ ] Secrets configured:
  - [ ] `GROQ_API_KEY` added to secrets

## Post-Deployment Checklist

### ✅ Testing
- [ ] App loads successfully
- [ ] Can upload PDF file
- [ ] Document processes correctly
- [ ] Can ask questions
- [ ] Answers are generated
- [ ] Source chunks are displayed
- [ ] Error handling works for irrelevant questions

### ✅ Security
- [ ] API keys are in secrets (not in code)
- [ ] No sensitive data in logs
- [ ] `.env` file is not in repository

## Quick Deploy Steps

1. **Prepare Code**
   ```bash
   git add .
   git commit -m "Ready for deployment"
   git push
   ```

2. **Deploy on Streamlit Cloud**
   - Go to share.streamlit.io
   - Click "New app"
   - Select repository and branch
   - Set main file to `app.py`
   - Add secrets (GROQ_API_KEY)
   - Click "Deploy"

3. **Verify**
   - Wait for deployment (2-3 minutes)
   - Test all features
   - Check logs if issues occur

## Common Issues

- **Import errors**: Check `requirements.txt`
- **API key errors**: Verify secrets are set correctly
- **File not found**: Check file paths are relative
- **Slow loading**: Normal on first load (model downloads)


