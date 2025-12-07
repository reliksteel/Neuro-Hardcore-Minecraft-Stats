# NeuroMinecraft Statistics Dashboard

A Streamlit app to display and analyze NeuroMinecraft statistics.

## Local Development

### Setup

1. Create and activate virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the app:
```bash
streamlit run app.py
```

The app will open at `http://localhost:8501`

## Deployment to Streamlit Cloud

### Steps to Deploy:

1. **Push to GitHub:**

2. **Deploy on Streamlit Cloud:**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Sign in with GitHub
   - Click "New app"
   - Select your repository, branch (main), and main file (app.py)
   - Click "Deploy"

Your app will be live at: `https://YOUR_USERNAME-YOUR_REPO.streamlit.app`

### Important Files for Deployment:
- `app.py` - Main Streamlit application
- `requirements.txt` - Python dependencies
- `stats.ods` - Your data file (must be in the repository)
