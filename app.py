import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from datetime import datetime
import os

# --- Admin password ---
ADMIN_PASSWORD = "letmein123"  # Change this!

# === 100 Scam Messages ===
scam_samples = [
    "Your account has been locked. Click here to unlock.",
    "Win a free MacBook by entering your email today!",
    "Your PayPal account is suspended. Confirm now.",
    "Unusual login attempt. Secure your account now.",
    "Act now to claim your $500 gift card!",
    "You’ve won the lottery! Click to claim.",
    "Amazon order issue: log in to verify your identity.",
    "IRS alert: you owe taxes. Pay immediately.",
    "Apple security alert: someone logged into your ID.",
    "Get rich quick with our crypto platform.",
    "Reset your password now to avoid permanent lock.",
    "We noticed suspicious activity. Confirm your account.",
    "Free Netflix for a year – limited time only.",
    "Your social security number has been suspended.",
    "Confirm your Chase Bank info to avoid closure.",
    "Last chance to win a Samsung Galaxy S21!",
    "PayPal alert: unauthorized transaction detected.",
    "You're selected for a government grant. Apply now.",
    "Congratulations! You’re a lucky winner!",
    "Urgent: Account suspended for suspicious activity.",
    "Update billing info to continue service.",
    "Your package could not be delivered. Fix address.",
    "Final notice: car warranty expired.",
    "Earn $5,000/week working from home.",
    "Exclusive crypto investment opportunity. Don’t miss out!",
    "Security alert from your bank – verify now.",
    "Free iPhone for survey participants. Sign up here.",
    "You’re pre-approved for a $10,000 loan!",
    "Amazon rewards: you have a pending gift.",
    "Re: invoice – open attachment immediately.",
    "Facebook login attempt from unknown device.",
    "Walmart gift card waiting for you.",
    "Your PC is infected – download antivirus now.",
    "Reactivation required: email storage full.",
    "One-time offer: zero-interest credit card.",
    "Secure your email account before it's disabled.",
    "eBay refund pending – confirm identity.",
    "You’ve been selected for a mystery shopper program.",
    "Free AirPods offer ends soon!",
    "Microsoft Alert: Virus detected on your device.",
    "Click here to update your driver's license info.",
    "Bitcoin deal: double your money instantly.",
    "You have a voicemail from your bank.",
    "Wire transfer failed – verify immediately.",
    "Medical bill overdue – click to pay.",
    "Unlock $1,000 in Walmart cash now.",
    "Mobile carrier rebate expiring – claim now.",
    "Student loan forgiveness available – enroll today.",
    "Final warning: delete files unless you act.",
    "Please verify your identity to restore access.",
    "Congratulations! You qualify for free rent assistance.",
    "Security update required: click now.",
    "Get paid $250 for completing this survey.",
    "Urgent delivery failed: reschedule now.",
    "COVID-19 relief fund: apply immediately.",
    "Bank transaction alert: suspicious withdrawal.",
    "Government benefits unclaimed. Apply today.",
    "Re: unpaid invoice attached.",
    "Crypto giveaway – Elon Musk special event!",
    "Your Amazon Prime will expire today. Renew now.",
    "Click to accept payment of $980 USD.",
    "Netflix payment failed. Update info.",
    "Apple giveaway: first 1,000 get a MacBook.",
    "Help needed urgently – stranded abroad.",
    "One-time password: confirm to continue.",
    "Visa gift card reward available!",
    "You’ve been selected for cash back bonus.",
    "Urgent: Restore access to your cloud files.",
    "We detected unusual activity on your account.",
    "Click to avoid legal action.",
    "Social Security fraud alert – respond now.",
    "Act fast! iPad Pro giveaway ending today.",
    "Free phone service for a year – apply here.",
    "New login from New York – secure account.",
    "You're pre-approved for debt relief.",
    "Your loan application is incomplete – finish now.",
    "Exclusive rewards waiting for you – claim now!",
    "You’ve received a secure message – view here.",
    "$1000 Target gift card waiting.",
    "Recover deleted messages now – urgent.",
    "Password expired – update to continue.",
    "Warning: data breach reported. Protect info.",
    "Your subscription has been auto-renewed.",
    "Tap to collect your pending reward.",
    "Final alert: verify credit card for continuity.",
    "Activate emergency backup now.",
    "Click to authorize bank transaction.",
    "Exclusive travel deal for you!",
    "Account recovery in progress – verify code.",
    "Hot stock alert! Invest today.",
    "You've been overcharged – request refund.",
    "Banking error – resolve now.",
    "Delivery issue – missing signature. Fix now.",
    "Free Costco membership – sign up here.",
    "We found errors in your tax return.",
    "Crypto alert: wallet not secure.",
    "Child tax credit ready – update details.",
    "Service discontinued – resume access today.",
    "Cash out now before bonus expires.",
    "You’ve reached your data cap – upgrade required.",
    "One-click virus cleaner now available.",
    "We sent you money – accept transfer.",
    "Facebook security breach. Act now.",
    "Massive giveaway inside – you’re invited!"
]

# === 100 Real Messages ===
real_samples = [
    "Hey, are we still on for coffee tomorrow?",
    "Your order from Target has shipped.",
    "Meeting is rescheduled to 3 PM Thursday.",
    "Thanks for your help with the report!",
    "Can you send over the project files?",
    "Dinner at 7 sound good?",
    "Happy anniversary! Love you!",
    "Looking forward to seeing you this weekend.",
    "Just landed, I’ll call soon.",
    "Check your inbox for the Zoom link.",
    "Doctor’s appointment confirmed for Monday.",
    "I left the keys under the mat.",
    "Don’t forget to call Grandma today.",
    "Running late, be there in 15.",
    "Great work on the presentation!",
    "Let’s finalize the slides tonight.",
    "Package delivered at your front door.",
    "Your Uber is arriving now.",
    "Flight delayed, new departure at 6 PM.",
    "Can we move our meeting to Tuesday?",
    "Happy birthday! 🎉",
    "What time is the game on?",
    "I uploaded the document to the shared folder.",
    "Congrats on the new job!",
    "It’s raining here. Drive safe.",
    "Lunch tomorrow at our usual spot?",
    "Payment received – thank you!",
    "Don’t forget your umbrella!",
    "Your weekly schedule is updated.",
    "Please approve the latest draft.",
    "We should catch up soon!",
    "Let me know your ETA.",
    "No worries – take your time.",
    "All set for the interview.",
    "I'll bring dessert tonight.",
    "Here’s the recipe I mentioned.",
    "Need anything from the store?",
    "Loved your latest blog post!",
    "School pickup is at 2:30.",
    "Call me when you’re free.",
    "The file is too large – use Drive.",
    "See you at the gym tomorrow?",
    "Thanks for the referral!",
    "Let’s plan a trip soon.",
    "Your subscription was renewed.",
    "Team lunch next Friday – RSVP.",
    "Great seeing you yesterday!",
    "Invoice attached – due Friday.",
    "Let’s chat after your meeting.",
    "I sent the flowers this morning.",
    "Did you get my message?",
    "Need help with your resume?",
    "Join the Zoom call at 4.",
    "Movie night this weekend?",
    "Hope you feel better soon.",
    "The baby photos are adorable!",
    "Meeting notes are in your inbox.",
    "Practice starts at 6 PM sharp.",
    "Dinner was amazing – thank you!",
    "I’ll resend the file right now.",
    "Take care and talk soon!",
    "Confirmed: appointment at 11 AM.",
    "Let’s grab drinks after work.",
    "Final edit is ready for review.",
    "Just wanted to say hi!",
    "Your check has been deposited.",
    "Catch you later!",
    "See you in class tomorrow.",
    "Thanks again for your feedback.",
    "Bringing snacks to the party!",
    "Check out this article!",
    "Reservation is under your name.",
    "Let me know if it prints.",
    "I’ll email you the quote.",
    "Leaving now – see you soon.",
    "Can you proofread this real quick?",
    "Just checking in on you.",
    "Your points expire next month.",
    "Don't forget to water the plants.",
    "Printer is out of paper again!",
    "Sending love from all of us!",
    "Don’t stay up too late!",
    "Made it home safe – thanks!",
    "Are you free for a call?",
    "Link to the event below.",
    "Let’s touch base next week.",
    "Miss you – call when you can.",
    "Calendar invite sent.",
    "I’ll take care of it.",
    "Make sure to lock up.",
    "Flight info: Gate B12.",
    "Finished the book you gave me.",
    "Meeting recap attached.",
    "The kids loved it!",
    "New photos in the album.",
    "How’s your weekend going?",
    "FYI: traffic on 5th is bad.",
    "Uploading now – standby.",
    "All systems look good!",
    "Don’t forget your badge.",
    "App update available.",
    "Let’s celebrate soon!",
    "Thanks for being awesome."
]

# Create dataset
data = pd.DataFrame({
    "message": scam_samples + real_samples,
    "label": [1]*len(scam_samples) + [0]*len(real_samples)
})

# Train/test split & train model once on startup
X_train, X_test, y_train, y_test = train_test_split(data["message"], data["label"], test_size=0.2, random_state=42)
pipeline = Pipeline([
    ("tfidf", TfidfVectorizer()),
    ("clf", LogisticRegression(max_iter=1000))
])
pipeline.fit(X_train, y_train)

st.title("🔍 Scam Detector with Admin Login")

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    password = st.text_input("Enter admin password", type="password")
    if st.button("Login"):
        if password == ADMIN_PASSWORD:
            st.session_state.logged_in = True
            st.success("Logged in successfully!")
        else:
            st.error("Incorrect password")
else:
    st.write("### Enter message to check if it’s a Scam or Real:")
    user_msg = st.text_area("Message", height=150)

    if st.button("Detect Scam"):
        if not user_msg.strip():
            st.warning("Please enter a message.")
        else:
            pred = pipeline.predict([user_msg])[0]
            label = "Scam" if pred == 1 else "Real"
            st.markdown(f"**Prediction:** {label}")

            # Log prediction
            log_entry = {
                "timestamp": datetime.now().isoformat(),
                "message": user_msg,
                "prediction": label
            }
            log_df = pd.DataFrame([log_entry])
            log_file = "admin_log.csv"
            if os.path.exists(log_file):
                log_df.to_csv(log_file, mode='a', header=False, index=False)
            else:
                log_df.to_csv(log_file, index=False)

    if st.button("Logout"):
        st.session_state.logged_in = False
        st.experimental_rerun()

# Footer credits
st.markdown("""
<style>
.footer {
    position: fixed;
    bottom: 10px;
    left: 20px;
    font-size: 13px;
    color: #666666;
}
</style>
<div class="footer">
    Credits: Michael Sun, Ethan Soesilo, Shaurya Singh, Raul Shrestha, Adrhit Bhadauria, Rem Fellenz
</div>
""", unsafe_allow_html=True)
