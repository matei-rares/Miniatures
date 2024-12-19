from flask import Flask, request, redirect, session
import requests

app = Flask(__name__)
app.secret_key = 'your_secret_key'

CLIENT_KEY = "your_client_key"
CLIENT_SECRET = "your_client_secret"
REDIRECT_URI = "https://your-redirect-uri.com"

@app.route('/')
def home():
    return redirect(f"https://www.tiktok.com/auth/authorize/?client_key={CLIENT_KEY}&scope=user.info.basic&response_type=code&redirect_uri={REDIRECT_URI}")

@app.route('/callback')
def callback():
    code = request.args.get('code')
    # Exchange code for access token
    token_url = "https://open-api.tiktok.com/oauth/access_token/"
    response = requests.post(token_url, data={
        'client_key': CLIENT_KEY,
        'client_secret': CLIENT_SECRET,
        'code': code,
        'grant_type': 'authorization_code'
    })
    session['access_token'] = response.json().get('data', {}).get('access_token')
    return "Authorization successful!"

if __name__ == "__main__":
    app.run(debug=True)
