import streamlit as st
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.pipeline import Pipeline
from spellchecker import SpellChecker
import pandas as pd
import os
from datetime import datetime

# Initialize spell checker
spell = SpellChecker()
MISSPELL_THRESHOLD = 0.2  # 20% misspelled words = suspicious

def spell_check_scam_heuristic(message):
    words = message.split()
    if not words:
        return False
    misspelled = spell.unknown(words)
    ratio = len(misspelled) / len(words)
    return ratio >= MISSPELL_THRESHOLD

# --- DO NOT MODIFY THESE ---
scam_samples = [
    "Congratulations! You've won a free iPhone. Click here to claim.",
    "Your bank account has been locked. Click to verify your identity.",
    "Give me $100 now or your account will be closed.",
    "You have been selected for a prize. Send your info to claim.",
    "Please send $50 in iTunes gift cards to unlock your computer.",
    "We detected suspicious activity. Pay $200 to restore access.",
    "Send Bitcoin to this address to avoid arrest.",
    "Get rich quick! Invest in this program today.",
    "URGENT: Your Social Security number has been compromised.",
    "This is Microsoft support. We need $100 in gift cards to fix your PC.",
    "Hi Mom, I lost my phone and I’m using a friend’s. Can you send me $400 through Zelle? I need it to get home.",
    "Your bank account has been temporarily suspended due to suspicious login activity. Please reply with your full name and last four digits of your SSN to unlock it.",
    "Congratulations! You’ve been selected to win a new iPhone 15 Pro. To claim your prize, please reply YES and confirm your shipping address.",
    "This is Amazon Security. A charge of $1,027.43 was attempted on your account for a MacBook. If this wasn’t you, reply CANCEL now.",
    "URGENT: Your PayPal account has been flagged. Please reply with your full name, date of birth, and billing zip code to verify your identity.",
    "This is Officer Jonathan Blake from the Social Security Administration. Your number has been linked to illegal activities. Call us immediately to avoid arrest.",
    "We were unable to deliver your FedEx package due to an incorrect address. Please reply with your full name and current address to reschedule delivery.",
    "You've been exposed to someone who tested positive for COVID-19. Click the link to schedule a mandatory test and avoid penalties.",
    "Your student loan may be eligible for full forgiveness under a new program. Reply FORGIVE to learn how to reduce or eliminate your balance.",
    "You missed jury duty and a warrant has been issued for your arrest. Pay the fine now to avoid legal consequences.",
    "Apple ID Alert: A device in Texas just logged into your account. If this was not you, reply STOP to prevent access.",
    "Your Netflix account will be suspended in 24 hours due to billing issues. Please reply with your name and the last 4 digits of your card to continue service.",
    "You’ve won a $100 Target gift card. To receive your reward, reply CLAIM and verify your address.",
    "This is Capital One Fraud Department. A $927.12 charge was declined. Please reply with YES or NO if this was you.",
    "Hi Grandma, I’m in trouble. I got into an accident and I need money for bail. Please don’t tell mom and dad. Can you send me $1,500?",
    "This is the IRS. You failed to pay back taxes and a warrant is pending. Call us now to avoid legal action.",
    "Your Chase account is currently restricted. Please reply with your username and zip code to verify.",
    "Great news! You’ve been approved for a $5,000 loan with 0% interest. No credit check required. Reply APPLY to begin.",
    "A family member has added you to a life insurance policy. Confirm your identity by sending your full name and date of birth.",
    "This is your last warning. You have outstanding toll violations. Failure to respond will result in license suspension.",
    "Your parcel is being held due to unpaid customs fees. Reply with your name and payment method to release it.",
    "A charge of $1,234.56 has been made at Best Buy on your Visa. If this is unauthorized, reply DISPUTE now.",
    "This is the DMV. Your driver’s license will be suspended due to unpaid citations. Call now to resolve.",
    "You have one voicemail from the U.S. Border Patrol regarding a customs investigation. Call now or reply YES to schedule a callback.",
    "Your computer has been infected with a virus. Do not turn off your machine. Call Microsoft Certified Support immediately at 1-800-*-**.",
    "Facebook has locked your account due to policy violations. To regain access, reply with your full name and email address.",
    "You’ve been entered in a raffle to win $5,000. Increase your odds by confirming your entry with your cell number and zip code.",
    "Your Wells Fargo online banking has been locked. Reply VERIFY to unlock access now.",
    "Google Pay has detected unusual activity. Please reply YES to confirm or NO to block the transaction.",
    "Your 2FA code is 493820. If you didn’t request this, your account may be compromised. Reply STOP.",
    "This is the electric company. Your account is past due and will be disconnected in 2 hours unless payment is received immediately. Call now.",
    "Hi, this is AT&T. Your number has been randomly selected to receive a $100 credit. To claim, reply CLAIM and confirm your account PIN.",
    "Security alert: Your account was accessed from an unfamiliar location. Please confirm your identity by replying with your birthday and zip code.",
    "You’ve been selected for an exclusive government grant. No repayment necessary. Reply YES for eligibility screening.",
    "This is your final notice regarding vehicle warranty expiration. Reply EXTEND to renew coverage.",
    "Please verify your address for a package being held under your name. Failure to do so will result in disposal.",
    "Congratulations! You qualify for Medicare benefits upgrades. Reply YES to speak with a licensed agent today.",
    "Your cash app payment failed. To avoid account suspension, reply with your username and full name.",
    "Hello, we noticed you haven’t claimed your tax refund. Please confirm your bank account for direct deposit.",
    "Hi, this is Brandon from HR. We need to verify your W-2 details for processing. Can you send a photo of your social security card?",
    "This is a scam",
    "Give me your credit card info"
]

real_samples = [
    "Hi John, just checking if we’re still on for dinner tomorrow.",
    "The report is ready and attached to this email.",
    "Reminder: Your dentist appointment is on Friday at 3pm.",
    "Thanks for your purchase! Your order will arrive soon.",
    "Meeting rescheduled to Monday, please confirm availability.",
    "Can you review this document before our meeting?",
    "Happy birthday! Wishing you a great year ahead.",
    "Looking forward to seeing you at the conference next week.",
    "Please submit your timesheet by end of day.",
    "Don’t forget to RSVP for the company party.",
    "Good morning! Hope you slept well.",
    "Don't forget we have that group meeting at 4.",
    "I’m making pasta tonight if you want some.",
    "Hey, I saw this and thought of you: [link]",
    "Just talked to Mom, she said to say hi.",
    "I’m almost done with the project, just final touches left.",
    "You left your headphones on the kitchen counter.",
    "Let’s go for a walk later if the weather’s nice.",
    "Can you help me carry the groceries up?",
    "Want to do brunch this weekend?"
]

# Labels + model
texts = scam_samples + real_samples
labels = [1]*len(scam_samples) + [0]*len(real_samples)

pipeline = Pipeline([
    ('vect', CountVectorizer()),
    ('clf', RandomForestClassifier())
])
pipeline.fit(texts, labels)

# Streamlit UI
st.title("Scam Detector")
user_input = st.text_area("Enter a message or email content below:", height=150)

if st.button("Check for Scam"):
    if user_input.strip() == "":
        st.warning("Please enter a message first.")
    else:
        model_prediction = pipeline.predict([user_input])[0]
        spellcheck_flag = spell_check_scam_heuristic(user_input)
        keyword_flag = any(keyword in user_input.lower() for keyword in ["give me $", "credit card info"])
        final_prediction = model_prediction or spellcheck_flag or keyword_flag
        result_label = "SCAM" if final_prediction else "NOT SCAM"

        # Save to CSV log
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = pd.DataFrame([{
            "timestamp": timestamp,
            "input": user_input,
            "result": result_label
        }])
        if os.path.exists("scam_detection_logs.csv"):
            log_entry.to_csv("scam_detection_logs.csv", mode='a', header=False, index=False)
        else:
            log_entry.to_csv("scam_detection_logs.csv", index=False)

        if final_prediction:
            st.error("⚠️ This message appears to be a SCAM.")
        else:
            st.success("✅ This message appears to be safe.")

# Admin panel
if "admin_mode" not in st.session_state:
    st.session_state.admin_mode = False

if not st.session_state.admin_mode:
    if st.button("🔒 Admin Login"):
        password = st.text_input("Enter admin password:", type="password")
        if password == "Ihaveacrushoneathon1!":
            st.session_state.admin_mode = True
            st.experimental_rerun()
else:
    st.success("✅ Admin mode enabled.")
    if os.path.exists("scam_detection_logs.csv"):
        df_logs = pd.read_csv("scam_detection_logs.csv")
        st.dataframe(df_logs)
        st.download_button("📥 Download Log", df_logs.to_csv(index=False), "scam_detection_logs.csv", "text/csv")
    else:
        st.info("No logs found yet.")

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
