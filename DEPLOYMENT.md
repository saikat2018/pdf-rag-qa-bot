# Streamlit Cloud Deployment Guide

This guide will walk you through deploying your PDF RAG QA Bot to Streamlit Cloud.

## Prerequisites

- A GitHub account
- A Groq API key ([Get one here](https://console.groq.com/))
- Your code ready for deployment

## Step 1: Prepare Your Repository

### 1.1 Create a GitHub Repository

1. Go to [GitHub](https://github.com) and sign in
2. Click the "+" icon in the top right corner
3. Select "New repository"
4. Name your repository (e.g., `pdf-rag-qa-bot`)
5. Choose visibility (Public or Private)
6. **Do NOT** initialize with README, .gitignore, or license (we already have these)
7. Click "Create repository"

### 1.2 Initialize Git and Push Your Code

Open terminal/command prompt in your project directory and run:

```bash
# Initialize git repository (if not already done)
git init

# Add all files
git add .

# Make your first commit
git commit -m "Initial commit: PDF RAG QA Bot"

# Add your GitHub repository as remote (replace with your repository URL)
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git

# Push to GitHub
git branch -M main
git push -u origin main
```

**Important:** Make sure you've committed the `.gitignore` file to exclude sensitive files and local data.

## Step 2: Set Up Streamlit Cloud

### 2.1 Sign Up for Streamlit Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Click "Sign up" or "Continue with GitHub"
3. Authorize Streamlit Cloud to access your GitHub account

### 2.2 Deploy Your App

1. Click "New app" button
2. Fill in the deployment form:
   - **Repository**: Select your repository from the dropdown
   - **Branch**: Select `main` (or your default branch)
   - **Main file path**: Enter `app.py`
   - **App URL**: Choose a unique URL (e.g., `pdf-rag-qa-bot`)
3. Click "Advanced settings" to configure secrets

### 2.3 Configure Secrets (Environment Variables)

1. In the "Advanced settings" section, click "Secrets"
2. Add your Groq API key:
   ```
   GROQ_API_KEY=your_actual_groq_api_key_here
   ```
3. Click "Save"

**Important:** Never commit your `.env` file or API keys to GitHub. Use Streamlit Cloud's secrets feature instead.

## Step 3: Verify Deployment

1. After clicking "Deploy", Streamlit Cloud will:
   - Install dependencies from `requirements.txt`
   - Run your app
   - Provide you with a public URL

2. Wait for the deployment to complete (usually 2-3 minutes)

3. Once deployed, you can:
   - Access your app at the provided URL
   - Share the URL with others
   - Monitor logs and usage

## Step 4: Update Your Code

### Making Changes

1. Make changes to your code locally
2. Commit and push to GitHub:
   ```bash
   git add .
   git commit -m "Description of changes"
   git push
   ```
3. Streamlit Cloud will automatically redeploy your app

### Updating Secrets

1. Go to your app on Streamlit Cloud
2. Click "Settings" (⚙️ icon)
3. Click "Secrets"
4. Update your secrets and click "Save"
5. Your app will automatically restart with new secrets

## Troubleshooting

### Common Issues

1. **App fails to deploy**
   - Check that `app.py` is in the root directory
   - Verify `requirements.txt` has all dependencies
   - Check the deployment logs for error messages

2. **API key not working**
   - Verify the secret name matches what your code expects (`GROQ_API_KEY`)
   - Check that the API key is correct and active
   - Ensure there are no extra spaces in the secret value

3. **Dependencies failing to install**
   - Check `requirements.txt` for correct package names
   - Some packages may take longer to install (e.g., `sentence-transformers`)
   - Review the build logs for specific errors

4. **App running slowly**
   - First load may be slow due to model downloads
   - Consider using caching for embeddings
   - Check Groq API rate limits

### Viewing Logs

1. Go to your app on Streamlit Cloud
2. Click "Manage app" (⋮ menu)
3. Select "Logs" to view real-time logs

## Important Notes

- **Free Tier Limits**: Streamlit Cloud free tier has resource limits
- **API Rate Limits**: Be aware of Groq API rate limits
- **File Storage**: Uploaded files are stored in session state (temporary)
- **Vector Database**: ChromaDB data is stored per session (not persistent across deployments)

## Support

For issues with:
- **Streamlit Cloud**: Check [Streamlit Cloud docs](https://docs.streamlit.io/streamlit-community-cloud)
- **Groq API**: Check [Groq documentation](https://console.groq.com/docs)
- **This Application**: Open an issue on GitHub


