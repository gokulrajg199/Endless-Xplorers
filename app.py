import streamlit as st
import pandas as pd
import os
import fitz
from datetime import datetime

st.set_page_config(
    page_title="Endless Xplorers AI Travel Planner",
    page_icon="🌍",
    layout="wide"
)

APP_FOLDER = r"C:\Users\ADMISSION CELL\Desktop\Gokulraj Project\Travel app"

def get_logo_path():
    for ext in ["png", "jpg", "jpeg", "webp"]:
        img_path = os.path.join(APP_FOLDER, f"LOGO.{ext}")
        if os.path.exists(img_path):
            return img_path

    pdf_path = os.path.join(APP_FOLDER, "LOGO.pdf")
    output_img = os.path.join(APP_FOLDER, "LOGO_converted.png")

    if os.path.exists(pdf_path):
        if not os.path.exists(output_img):
            doc = fitz.open(pdf_path)
            page = doc[0]
            pix = page.get_pixmap(matrix=fitz.Matrix(3, 3), alpha=True)
            pix.save(output_img)
            doc.close()
        return output_img

    return None

LOGO_PATH = get_logo_path()

DESTINATIONS = [
    {
        "name": "Munnar",
        "type": "Hill Station",
        "interests": ["Nature", "Adventure", "Photography"],
        "best_for": ["Family", "Couple", "Friends", "Students"],
        "budget": 4500,
        "season": "September to May",
        "places": ["Mattupetty Dam", "Echo Point", "Tea Museum", "Top Station", "Eravikulam National Park"],
        "hotels": ["Budget Homestay", "Deluxe Hill View Hotel", "Premium Resort"]
    },
    {
        "name": "Ooty",
        "type": "Hill Station",
        "interests": ["Nature", "Relaxation", "Photography"],
        "best_for": ["Family", "Couple", "Students"],
        "budget": 4000,
        "season": "October to June",
        "places": ["Botanical Garden", "Ooty Lake", "Doddabetta Peak", "Rose Garden", "Pykara Lake"],
        "hotels": ["Budget Lodge", "Family Hotel", "Luxury Cottage"]
    },
    {
        "name": "Kodaikanal",
        "type": "Nature",
        "interests": ["Nature", "Relaxation", "Photography"],
        "best_for": ["Couple", "Family", "Friends"],
        "budget": 4200,
        "season": "October to June",
        "places": ["Kodai Lake", "Coaker's Walk", "Pillar Rocks", "Bryant Park", "Guna Caves"],
        "hotels": ["Budget Stay", "Lake View Hotel", "Premium Villa"]
    },
    {
        "name": "Goa",
        "type": "Beach",
        "interests": ["Beach", "Adventure", "Nightlife"],
        "best_for": ["Friends", "Couple", "Corporate"],
        "budget": 9000,
        "season": "November to February",
        "places": ["Baga Beach", "Calangute Beach", "Fort Aguada", "Dudhsagar Falls", "Cruise Ride"],
        "hotels": ["Beach Stay", "Deluxe Resort", "Luxury Sea View Resort"]
    },
    {
        "name": "Kerala",
        "type": "Family",
        "interests": ["Nature", "Relaxation", "Houseboat"],
        "best_for": ["Family", "Couple", "Corporate"],
        "budget": 8500,
        "season": "September to March",
        "places": ["Munnar", "Thekkady", "Alleppey", "Houseboat", "Kochi"],
        "hotels": ["Family Hotel", "Houseboat Stay", "Premium Resort"]
    }
]

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background: linear-gradient(135deg, #f4fbfb 0%, #e8f7f6 45%, #fff8e5 100%);
}

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #002b2b, #005f5f);
}

[data-testid="stSidebar"] * {
    color: white !important;
}

.block-container {
    padding-top: 1.5rem;
    padding-bottom: 2rem;
}

.hero {
    background: linear-gradient(135deg, #003c3c, #006d6d, #00a884);
    padding: 35px;
    border-radius: 28px;
    box-shadow: 0 18px 45px rgba(0, 60, 60, 0.28);
    color: white;
    margin-bottom: 25px;
}

.hero-title {
    font-size: 46px;
    font-weight: 800;
    margin-bottom: 5px;
}

.hero-sub {
    color: #ffe16b;
    font-size: 20px;
    font-weight: 700;
}

.hero-text {
    font-size: 15px;
    opacity: 0.95;
}

.logo-card {
    background: white;
    padding: 18px;
    border-radius: 22px;
    text-align: center;
    box-shadow: 0 12px 30px rgba(0,0,0,0.18);
}

.stat-card {
    background: white;
    padding: 22px;
    border-radius: 22px;
    box-shadow: 0 10px 30px rgba(0, 65, 65, 0.12);
    border: 1px solid #d7eeee;
    text-align: center;
}

.stat-card h2 {
    color: #005f5f;
    margin: 0;
    font-weight: 800;
}

.stat-card p {
    color: #4c6666;
    margin: 5px 0 0 0;
    font-weight: 600;
}

.form-card {
    background: white;
    padding: 25px;
    border-radius: 24px;
    box-shadow: 0 12px 35px rgba(0, 65, 65, 0.13);
    border: 1px solid #d8eeee;
}

.result-card {
    background: white;
    padding: 30px;
    border-radius: 26px;
    box-shadow: 0 15px 45px rgba(0, 65, 65, 0.16);
    border-left: 8px solid #00a884;
}

.section-title {
    color: #003c3c;
    font-weight: 800;
}

.badge {
    display: inline-block;
    background: #e7f8f5;
    color: #006d6d;
    padding: 8px 14px;
    border-radius: 30px;
    font-weight: 700;
    margin: 5px 6px 5px 0;
}

.footer {
    text-align: center;
    color: #006d6d;
    font-weight: 600;
    margin-top: 30px;
}

.stButton > button {
    background: linear-gradient(135deg, #006d6d, #00a884);
    color: white;
    border: none;
    border-radius: 16px;
    padding: 14px;
    font-weight: 800;
    font-size: 17px;
}

.stButton > button:hover {
    background: linear-gradient(135deg, #004f4f, #008f76);
    color: white;
}

.stDownloadButton > button {
    background: #ffb703;
    color: #102020;
    border-radius: 14px;
    border: none;
    font-weight: 800;
}
</style>
""", unsafe_allow_html=True)

def recommend_destination(days, budget, travelers, interest, travel_type):
    scored = []

    for d in DESTINATIONS:
        score = 0

        if interest in d["interests"]:
            score += 40

        if travel_type in d["best_for"]:
            score += 30

        total = d["budget"] * days * travelers

        if total <= budget:
            score += 30
        else:
            score -= 10

        scored.append((score, d, total))

    scored.sort(reverse=True, key=lambda x: x[0])
    return scored[0]

def generate_itinerary(destination, days, start):
    places = destination["places"]
    itinerary = []

    for day in range(1, days + 1):
        if day == 1:
            plan = [
                f"Start journey from {start}",
                "Hotel check-in and refreshment",
                f"Visit {places[0]}",
                f"Evening sightseeing at {places[1]}",
                "Dinner and overnight stay"
            ]
        elif day == days:
            plan = [
                f"Morning visit to {places[-1]}",
                "Shopping and photography",
                "Hotel check-out",
                f"Return journey to {start}"
            ]
        else:
            index = min(day, len(places) - 1)
            plan = [
                f"Visit {places[index]}",
                "Explore nearby attractions",
                "Lunch break",
                "Evening leisure time",
                "Overnight stay"
            ]

        itinerary.append((day, plan))

    return itinerary

def budget_table(total):
    return pd.DataFrame({
        "Category": ["Hotel", "Transport", "Food", "Activities", "Miscellaneous"],
        "Amount ₹": [
            int(total * 0.35),
            int(total * 0.30),
            int(total * 0.18),
            int(total * 0.12),
            int(total * 0.05)
        ]
    })

if LOGO_PATH:
    st.sidebar.image(LOGO_PATH, use_container_width=True)

st.sidebar.markdown("## Endless Xplorers")
st.sidebar.write("📞 9894591780")
st.sidebar.write("📸 @endlessxplorers_official")
st.sidebar.markdown("---")
st.sidebar.write("✅ AI Trip Recommendation")
st.sidebar.write("✅ Budget Prediction")
st.sidebar.write("✅ Day-wise Itinerary")
st.sidebar.write("✅ Hotel Suggestions")
st.sidebar.write("✅ WhatsApp Promotion")
st.sidebar.write("✅ Download Plan")

hero_col1, hero_col2 = st.columns([1, 4])

with hero_col1:
    st.markdown("<div class='logo-card'>", unsafe_allow_html=True)
    if LOGO_PATH:
        st.image(LOGO_PATH, use_container_width=True)
    else:
        st.markdown("## 🌍")
        st.warning("LOGO.pdf not found")
    st.markdown("</div>", unsafe_allow_html=True)

with hero_col2:
    st.markdown("""
    <div class="hero">
        <div class="hero-title">Endless Xplorers</div>
        <div class="hero-sub">AI-Powered Smart Travel Planner</div>
        <p class="hero-text">
            Premium travel planning system for customized packages, smart budget estimation,
            day-wise itinerary generation and instant WhatsApp promotions.
        </p>
        <span class="badge">Explore Beyond Boundaries</span>
        <span class="badge">Creating Memories Together</span>
    </div>
    """, unsafe_allow_html=True)

s1, s2, s3, s4 = st.columns(4)

s1.markdown("<div class='stat-card'><h2>25+</h2><p>Tour Packages</p></div>", unsafe_allow_html=True)
s2.markdown("<div class='stat-card'><h2>AI</h2><p>Smart Planner</p></div>", unsafe_allow_html=True)
s3.markdown("<div class='stat-card'><h2>₹</h2><p>Budget Estimator</p></div>", unsafe_allow_html=True)
s4.markdown("<div class='stat-card'><h2>24/7</h2><p>Customer Support</p></div>", unsafe_allow_html=True)

st.write("")

left, right = st.columns(2)

with left:
    st.markdown("<div class='form-card'>", unsafe_allow_html=True)
    st.markdown("<h3 class='section-title'>🧳 Customer Travel Details</h3>", unsafe_allow_html=True)

    start_location = st.text_input("Starting Location", "Coimbatore")
    days = st.slider("Number of Days", 1, 10, 3)
    travelers = st.number_input("Number of Travelers", min_value=1, max_value=100, value=2)
    budget = st.number_input("Total Budget ₹", min_value=1000, max_value=500000, value=20000)

    st.markdown("</div>", unsafe_allow_html=True)

with right:
    st.markdown("<div class='form-card'>", unsafe_allow_html=True)
    st.markdown("<h3 class='section-title'>🎯 Travel Preferences</h3>", unsafe_allow_html=True)

    interest = st.selectbox(
        "Interest",
        ["Nature", "Adventure", "Beach", "Relaxation", "Photography", "Houseboat", "Nightlife"]
    )

    travel_type = st.selectbox(
        "Travel Type",
        ["Family", "Couple", "Friends", "Students", "Corporate"]
    )

    hotel_type = st.selectbox(
        "Hotel Preference",
        ["Budget", "Deluxe", "Premium", "Luxury"]
    )

    food_preference = st.selectbox(
        "Food Preference",
        ["Veg", "Non-Veg", "Both"]
    )

    st.markdown("</div>", unsafe_allow_html=True)

st.write("")

if st.button("🚀 Generate Premium AI Travel Plan", use_container_width=True):
    score, selected, total = recommend_destination(days, budget, travelers, interest, travel_type)
    itinerary = generate_itinerary(selected, days, start_location)
    df = budget_table(total)

    st.markdown("<div class='result-card'>", unsafe_allow_html=True)

    st.markdown(f"<h2 class='section-title'>✅ AI Recommended Destination: {selected['name']}</h2>", unsafe_allow_html=True)

    r1, r2, r3, r4 = st.columns(4)
    r1.metric("Destination", selected["name"])
    r2.metric("Duration", f"{days} Days")
    r3.metric("Estimated Cost", f"₹{int(total)}")
    r4.metric("AI Match", f"{max(score, 0)}%")

    st.markdown("### 📌 Package Summary")
    st.write(f"**From:** {start_location}")
    st.write(f"**Destination:** {selected['name']}")
    st.write(f"**Travel Type:** {travel_type}")
    st.write(f"**Travelers:** {travelers}")
    st.write(f"**Hotel Type:** {hotel_type}")
    st.write(f"**Food Preference:** {food_preference}")
    st.write(f"**Best Season:** {selected['season']}")

    full_text = f"""
ENDLESS XPLORERS - AI TRAVEL PLAN

Generated On: {datetime.now().strftime("%d-%m-%Y %I:%M %p")}

From: {start_location}
Destination: {selected['name']}
Duration: {days} Days
Travelers: {travelers}
Travel Type: {travel_type}
Hotel Type: {hotel_type}
Food Preference: {food_preference}
Estimated Budget: ₹{int(total)}

DAY-WISE ITINERARY
"""

    st.markdown("### 🗓 Day-Wise Itinerary")
    for day, plan in itinerary:
        st.markdown(f"#### Day {day}")
        full_text += f"\nDay {day}\n"
        for item in plan:
            st.write(f"✅ {item}")
            full_text += f"- {item}\n"

    st.markdown("### 💰 Budget Split-Up")
    st.dataframe(df, use_container_width=True, hide_index=True)

    full_text += "\nBUDGET SPLIT-UP\n"
    for _, row in df.iterrows():
        full_text += f"{row['Category']}: ₹{row['Amount ₹']}\n"

    st.markdown("### 🏨 Suggested Hotels")
    for hotel in selected["hotels"]:
        st.write(f"🏨 {hotel}")

    promo = f"""
🌍 Endless Xplorers

✨ {selected['name']} {days} Days Travel Package ✨

📍 From: {start_location}
👥 Travelers: {travelers}
🏨 Stay: {hotel_type}
🍽 Food Preference: {food_preference}
💰 Estimated Budget: ₹{int(total)}

Places Covered:
{", ".join(selected['places'])}

📞 Contact: 9894591780
📸 Instagram: @endlessxplorers_official

✨ Explore Beyond Boundaries
✨ Creating Memories Together
"""

    st.markdown("### 📲 AI WhatsApp Promotion")
    st.text_area("Copy Message", promo, height=240)

    st.download_button(
        "📥 Download Travel Plan",
        data=full_text,
        file_name=f"{selected['name']}_Travel_Plan.txt",
        mime="text/plain"
    )

    st.markdown("</div>", unsafe_allow_html=True)

st.write("")
st.markdown("<div class='form-card'>", unsafe_allow_html=True)
st.markdown("<h3 class='section-title'>📞 Customer Enquiry Form</h3>", unsafe_allow_html=True)

with st.form("enquiry_form"):
    c1, c2 = st.columns(2)
    with c1:
        customer_name = st.text_input("Customer Name")
    with c2:
        mobile = st.text_input("Mobile Number")

    requirement = st.text_area("Customer Requirement")
    submit = st.form_submit_button("Save Enquiry")

    if submit:
        st.success("Customer enquiry saved successfully.")

st.markdown("</div>", unsafe_allow_html=True)

st.markdown("""
<div class="footer">
    Endless Xplorers © 2026 | Explore Beyond Boundaries | Creating Memories Together
</div>
""", unsafe_allow_html=True)