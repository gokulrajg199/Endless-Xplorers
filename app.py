
import os
import urllib.parse
from datetime import datetime, date

import streamlit as st
import pandas as pd
import fitz

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Image as RLImage

# ============================================================
# ENDLESS XPLORERS - PREMIUM WEBSITE + CRM APPLICATION
# ============================================================

st.set_page_config(
    page_title="Endless Xplorers",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOGO_PATH = os.path.join(BASE_DIR, "LOGO.jpg")
BROCHURE_PATH = os.path.join(BASE_DIR, "Endless Xplorer Final 1.pdf")
LEADS_FILE = os.path.join(BASE_DIR, "customer_enquiries.csv")

ADMIN_PASSWORD = "endlessxplorers"

COMPANY = "Endless Xplorers"
CONTACT = "9894591780"
PHONE = "+91 9894591780"
EMAIL = "endlessxplorerofficial@gmail.com"
INSTAGRAM = "@endlessxplorers_official"
ADDRESS = "21/1, Nanjappa Gounder Thottam Road, Telungupalayam, Coimbatore - 641039"
TAGLINE = "Explore Beyond Boundaries • Creating Memories Together"

TEAL = "#063B3B"
DARK = "#021F1F"
GOLD = "#D4AF37"
CREAM = "#F7F1DD"

# ============================================================
# DATA
# ============================================================

PACKAGES = {
    "South India": {
        "Munnar": {"badge": "Popular", "days": 2, "base": 4499, "desc": "Tea gardens, viewpoints, waterfalls and cool climate.", "places": ["Tea Gardens", "Mattupetty Dam", "Echo Point", "Top Station", "Eravikulam National Park"]},
        "Ooty": {"badge": "Family", "days": 2, "base": 3999, "desc": "Gardens, lake, toy train and mountain views.", "places": ["Botanical Garden", "Ooty Lake", "Doddabetta Peak", "Rose Garden", "Pykara Lake"]},
        "Alleppey": {"badge": "Houseboat", "days": 2, "base": 5499, "desc": "Kerala backwaters and houseboat experience.", "places": ["Houseboat Cruise", "Backwaters", "Vembanad Lake", "Village Visit", "Beach Visit"]},
        "Coorg": {"badge": "Nature", "days": 3, "base": 6499, "desc": "Coffee estates, waterfalls and peaceful stay.", "places": ["Coffee Plantation", "Golden Temple", "Dubare Elephant Camp", "Abbey Falls", "Raja Seat"]},
        "Mysore": {"badge": "Heritage", "days": 2, "base": 3499, "desc": "Palace, gardens, heritage and culture.", "places": ["Mysore Palace", "Chamundi Hills", "Brindavan Garden", "Zoo"]},
        "Kanyakumari": {"badge": "Sunrise", "days": 2, "base": 3999, "desc": "Southern tip of India with sunrise and sea views.", "places": ["Vivekananda Rock", "Thiruvalluvar Statue", "Sunrise Point", "Beach Visit"]},
    },
    "North India": {
        "Kashmir": {"badge": "Paradise", "days": 5, "base": 18999, "desc": "Snow, valleys, shikara ride and hill experience.", "places": ["Srinagar", "Dal Lake", "Shikara Ride", "Gulmarg", "Pahalgam", "Sonamarg"]},
        "Himachal Pradesh": {"badge": "Adventure", "days": 5, "base": 15999, "desc": "Shimla, Manali, valleys and adventure activities.", "places": ["Shimla", "Manali", "Solang Valley", "Kullu", "Rohtang Pass"]},
        "Agra - Jaipur": {"badge": "Golden Triangle", "days": 4, "base": 11999, "desc": "Taj Mahal, forts, palaces and culture.", "places": ["Taj Mahal", "Agra Fort", "Amer Fort", "Hawa Mahal", "City Palace"]},
        "Varanasi - Ayodhya": {"badge": "Spiritual", "days": 4, "base": 9999, "desc": "Kashi, Ganga Aarti, Ram Mandir and divine journey.", "places": ["Kashi Vishwanath", "Ganga Aarti", "Sarnath", "Ram Mandir", "Sarayu Aarti"]},
    },
    "International": {
        "Dubai": {"badge": "Luxury", "days": 5, "base": 49999, "desc": "Burj Khalifa, desert safari, marina and shopping.", "places": ["Burj Khalifa", "Dubai Mall", "Desert Safari", "Dubai Marina", "Palm Jumeirah"]},
        "Bali": {"badge": "Couple", "days": 5, "base": 55999, "desc": "Beaches, temples, private villas and romantic views.", "places": ["Ubud", "Tanah Lot Temple", "Kuta Beach", "Nusa Penida", "Bali Swing"]},
        "Maldives": {"badge": "Honeymoon", "days": 4, "base": 69999, "desc": "Water villas, private beach, cruise and snorkeling.", "places": ["Male City", "Water Villa", "Private Beach", "Sunset Cruise", "Snorkeling"]},
        "Singapore": {"badge": "Family Fun", "days": 5, "base": 59999, "desc": "Sentosa, Universal Studios and city attractions.", "places": ["Merlion Park", "Sentosa Island", "Universal Studios", "Gardens by the Bay"]},
    },
    "Educational": {
        "Industrial Visit": {"badge": "College IV", "days": 2, "base": 1999, "desc": "Industry exposure, learning session and safe student travel.", "places": ["Industry Visit", "Expert Session", "Process Study", "Certificate Session", "Sightseeing"]},
        "Science & Technology Tour": {"badge": "Learning", "days": 2, "base": 2499, "desc": "Science centre, innovation lab and knowledge session.", "places": ["Science Centre", "Innovation Lab", "Robotics Demo", "Knowledge Session"]},
    },
    "Corporate": {
        "Corporate Offsite": {"badge": "Team Retreat", "days": 2, "base": 4999, "desc": "Resort stay, team activities and networking dinner.", "places": ["Resort Stay", "Team Activities", "Leadership Games", "Networking Dinner"]},
        "Conference Travel": {"badge": "Business", "days": 1, "base": 2999, "desc": "Venue, travel, food and meeting coordination.", "places": ["Venue Setup", "Seminar Session", "Travel Management", "Lunch"]},
    },
    "Honeymoon": {
        "Kerala Honeymoon": {"badge": "Romantic", "days": 4, "base": 18999, "desc": "Munnar, houseboat, candlelight dinner and spa.", "places": ["Munnar Hills", "Alleppey Houseboat", "Candlelight Dinner", "Spa"]},
        "Bali Honeymoon": {"badge": "Premium", "days": 5, "base": 59999, "desc": "Private villa, beach dinner and couple activities.", "places": ["Private Villa", "Bali Swing", "Temple Visit", "Beach Dinner"]},
    },
    "Pilgrimage": {
        "Tirupati - Rameswaram": {"badge": "South Pilgrimage", "days": 3, "base": 6999, "desc": "Temple darshan and comfortable pilgrimage travel.", "places": ["Tirupati Darshan", "Padmavathi Temple", "Rameswaram Temple", "Dhanushkodi"]},
        "Char Dham Yatra": {"badge": "Divine", "days": 10, "base": 34999, "desc": "Yamunotri, Gangotri, Kedarnath and Badrinath.", "places": ["Yamunotri", "Gangotri", "Kedarnath", "Badrinath"]},
    },
}

POPULAR = [
    ("South India", "Munnar"),
    ("South India", "Ooty"),
    ("North India", "Kashmir"),
    ("International", "Dubai"),
    ("International", "Bali"),
    ("Honeymoon", "Kerala Honeymoon"),
]

GALLERY = [
    ("Munnar", "https://images.unsplash.com/photo-1593693397690-362cb9666fc2?auto=format&fit=crop&w=900&q=80"),
    ("Kashmir", "https://images.unsplash.com/photo-1595815771614-ade9d652a65d?auto=format&fit=crop&w=900&q=80"),
    ("Dubai", "https://images.unsplash.com/photo-1512453979798-5ea266f8880c?auto=format&fit=crop&w=900&q=80"),
    ("Bali", "https://images.unsplash.com/photo-1537996194471-e657df975ab4?auto=format&fit=crop&w=900&q=80"),
    ("Maldives", "https://images.unsplash.com/photo-1514282401047-d79a71a590e8?auto=format&fit=crop&w=900&q=80"),
    ("Singapore", "https://images.unsplash.com/photo-1525625293386-3f8f99389edd?auto=format&fit=crop&w=900&q=80"),
]

BROCHURE_PAGES = {
    "Cover": 1,
    "Why Choose Us": 3,
    "South India": 4,
    "North India": 5,
    "International": 6,
    "Educational": 7,
    "Corporate": 8,
    "Honeymoon": 9,
    "Pilgrimage": 10,
    "Travel Services": 12,
    "Contact": 13,
}

# ============================================================
# STYLE
# ============================================================

st.markdown(f"""
<style>
.stApp {{
    background:
    radial-gradient(circle at top left, rgba(212,175,55,.22), transparent 28%),
    radial-gradient(circle at top right, rgba(6,59,59,.18), transparent 28%),
    linear-gradient(135deg,#fffaf0,#eff9f6,#fff);
}}
[data-testid="stSidebar"] {{
    background:linear-gradient(180deg,{TEAL},{DARK});
}}
[data-testid="stSidebar"] * {{
    color:white!important;
}}
.block-container {{
    padding-top:1.2rem;
}}
.hero {{
    background:
    linear-gradient(135deg,rgba(2,31,31,.95),rgba(6,59,59,.86)),
    url('https://images.unsplash.com/photo-1507525428034-b723cf961d3e?auto=format&fit=crop&w=1600&q=80');
    min-height:430px;
    background-size:cover;
    background-position:center;
    border-radius:34px;
    padding:54px;
    color:white;
    box-shadow:0 28px 70px rgba(0,0,0,.22);
    border:1px solid {GOLD};
}}
.hero h1 {{
    font-size:64px;
    font-weight:900;
    margin-bottom:0;
}}
.hero h2 {{
    color:{GOLD};
    font-size:30px;
}}
.hero p {{
    font-size:18px;
    max-width:760px;
    line-height:1.7;
}}
.title {{
    color:{TEAL};
    font-size:36px;
    font-weight:900;
    margin-top:24px;
    margin-bottom:14px;
}}
.sub {{
    color:#365c5c;
    font-size:17px;
}}
.card,.package-card,.metric-card,.review,.gallery-card {{
    background:rgba(255,255,255,.96);
    border-radius:24px;
    padding:22px;
    border:1px solid rgba(212,175,55,.52);
    box-shadow:0 16px 35px rgba(0,0,0,.10);
    margin-bottom:18px;
}}
.package-card {{
    border-bottom:6px solid {GOLD};
    min-height:275px;
    background:linear-gradient(180deg,#fff,#fffaf0);
}}
.package-card h3 {{
    color:{TEAL};
    font-weight:900;
}}
.badge {{
    display:inline-block;
    padding:7px 12px;
    background:{TEAL};
    color:white;
    border-radius:99px;
    font-size:12px;
    font-weight:800;
    margin-bottom:8px;
}}
.gold {{
    color:{GOLD};
    font-weight:900;
}}
.service-card {{
    background:linear-gradient(135deg,{TEAL},#087474);
    color:white;
    border-radius:22px;
    padding:22px;
    min-height:170px;
    text-align:center;
    border-bottom:6px solid {GOLD};
    box-shadow:0 16px 35px rgba(0,0,0,.16);
    margin-bottom:18px;
}}
.metric-card {{
    text-align:center;
}}
.metric-card h1 {{
    color:{TEAL};
    font-weight:900;
    margin-bottom:0;
}}
.review {{
    border-left:7px solid {GOLD};
    min-height:180px;
}}
.gallery-card {{
    padding:0;
    overflow:hidden;
}}
.gallery-card img {{
    width:100%;
    height:210px;
    object-fit:cover;
}}
.gallery-card h3 {{
    padding:0 18px 18px 18px;
    color:{TEAL};
}}
.whatsapp,.goldbtn {{
    display:inline-block;
    color:white!important;
    padding:12px 18px;
    border-radius:14px;
    font-weight:900;
    text-decoration:none!important;
    margin-top:8px;
}}
.whatsapp {{
    background:#25D366;
}}
.goldbtn {{
    background:linear-gradient(135deg,{GOLD},#f5d76e);
    color:#111!important;
}}
.social {{
    display:inline-block;
    margin:6px;
    padding:10px 14px;
    border-radius:14px;
    background:rgba(255,255,255,.12);
    color:white!important;
    text-decoration:none!important;
    font-weight:800;
}}
.footer {{
    background:linear-gradient(135deg,{TEAL},{DARK});
    color:white;
    text-align:center;
    padding:30px;
    border-radius:28px;
    border:1px solid {GOLD};
    margin-top:32px;
}}
.stButton button {{
    background:linear-gradient(135deg,{TEAL},#0a7777);
    color:white;
    border:none;
    border-radius:14px;
    font-weight:900;
    padding:.7rem 1rem;
}}
.stDownloadButton button {{
    background:linear-gradient(135deg,{GOLD},#f5d76e);
    color:#111;
    border:none;
    border-radius:14px;
    font-weight:900;
    padding:.7rem 1rem;
}}
@media(max-width:768px) {{
    .block-container {{padding-left:1rem;padding-right:1rem;}}
    .hero {{padding:28px;min-height:360px;border-radius:24px;}}
    .hero h1 {{font-size:40px;}}
    .hero h2 {{font-size:22px;}}
    .hero p {{font-size:15px;}}
    .title {{font-size:28px;}}
    .package-card,.card,.service-card {{min-height:auto;padding:18px;}}
    .gallery-card img {{height:170px;}}
}}
</style>
""", unsafe_allow_html=True)

# ============================================================
# FUNCTIONS
# ============================================================

def wa_link(message):
    return f"https://wa.me/91{CONTACT}?text={urllib.parse.quote(message)}"

def package(category, destination):
    return PACKAGES[category][destination]

def auto_itinerary(destination, places, days, start_location):
    result = []
    for day in range(1, days + 1):
        if day == 1:
            items = [
                f"Departure from {start_location}",
                f"Arrival at {destination}",
                "Hotel check-in and refreshment",
                places[0],
                places[1] if len(places) > 1 else places[0],
                "Evening leisure / shopping / photography",
                "Dinner and overnight stay",
            ]
        elif day == days:
            items = [
                "Breakfast at hotel",
                "Hotel check-out",
                places[-2] if len(places) >= 2 else places[0],
                places[-1],
                "Lunch",
                f"Return journey to {start_location}",
                "Tour ends with beautiful memories",
            ]
        else:
            idx = day % len(places)
            items = [
                "Breakfast at hotel",
                places[idx],
                places[(idx + 1) % len(places)],
                "Lunch",
                places[(idx + 2) % len(places)],
                "Group activity / leisure / campfire if applicable",
                "Dinner and overnight stay",
            ]
        result.append((day, items))
    return result

def calculate_budget(base, persons, days, stay_type, transport_type):
    stay_factor = {
        "Budget": 0.90,
        "Standard": 1.00,
        "Premium": 1.35,
        "Luxury": 1.80,
    }[stay_type]
    transport_factor = {
        "Cab": 1.20,
        "Tempo Traveller": 1.05,
        "Bus / Coach": 0.95,
        "Flight + Local Transport": 1.75,
    }[transport_type]
    total = int(base * persons * max(days, 1) / 2 * stay_factor * transport_factor)
    per_person = int(total / max(persons, 1))
    advance = int(total * 0.50)
    return total, per_person, advance

def save_lead(data):
    df_new = pd.DataFrame([data])
    if os.path.exists(LEADS_FILE):
        old = pd.read_csv(LEADS_FILE)
        for col in df_new.columns:
            if col not in old.columns:
                old[col] = ""
        for col in old.columns:
            if col not in df_new.columns:
                df_new[col] = ""
        df_new = pd.concat([old, df_new[old.columns]], ignore_index=True)
    df_new.to_csv(LEADS_FILE, index=False)

@st.cache_resource
def extract_brochure_pages():
    pages = {}
    if not os.path.exists(BROCHURE_PATH):
        return pages
    out_dir = os.path.join(BASE_DIR, "brochure_pages")
    os.makedirs(out_dir, exist_ok=True)
    try:
        pdf = fitz.open(BROCHURE_PATH)
        for i in range(len(pdf)):
            page_no = i + 1
            img_path = os.path.join(out_dir, f"page_{page_no}.png")
            if not os.path.exists(img_path):
                pix = pdf[i].get_pixmap(matrix=fitz.Matrix(1.3, 1.3), alpha=False)
                pix.save(img_path)
            pages[page_no] = img_path
    except Exception:
        return {}
    return pages

def generate_pdf(output_path, client_name, mobile, category, destination, start_location, days, persons, stay_type, transport_type, food, activities, budget_text, note):
    data = package(category, destination)
    places = data["places"]
    itinerary = auto_itinerary(destination, places, days, start_location)

    doc = SimpleDocTemplate(output_path, pagesize=A4, rightMargin=42, leftMargin=42, topMargin=32, bottomMargin=32)
    styles = getSampleStyleSheet()
    title = ParagraphStyle("TitleX", parent=styles["Title"], fontSize=20, textColor=colors.HexColor(TEAL), alignment=1)
    h = ParagraphStyle("HeadingX", parent=styles["Heading2"], fontSize=14, textColor=colors.HexColor(TEAL))
    n = ParagraphStyle("NormalX", parent=styles["Normal"], fontSize=10.5, leading=15)
    small = ParagraphStyle("SmallX", parent=styles["Normal"], fontSize=9.5, leading=13)

    story = []

    def header():
        if os.path.exists(LOGO_PATH):
            logo = RLImage(LOGO_PATH, width=1.25 * inch, height=0.85 * inch)
        else:
            logo = Paragraph(f"<b>{COMPANY}</b>", h)
        info = Paragraph(f"<b>{COMPANY}</b><br/>{PHONE}<br/>{EMAIL}<br/>{INSTAGRAM}", small)
        t = Table([[logo, info]], colWidths=[2.0 * inch, 4.8 * inch])
        t.setStyle(TableStyle([("ALIGN", (1, 0), (1, 0), "RIGHT"), ("VALIGN", (0, 0), (-1, -1), "MIDDLE")]))
        story.append(t)
        story.append(Spacer(1, 8))
        line = Table([[""]], colWidths=[6.8 * inch])
        line.setStyle(TableStyle([("LINEBELOW", (0, 0), (-1, -1), 2, colors.HexColor(GOLD))]))
        story.append(line)
        story.append(Spacer(1, 14))

    header()
    story.append(Paragraph("Premium Travel Proposal", title))
    story.append(Spacer(1, 12))
    story.append(Paragraph(f"Dear <b>{client_name}</b>, thank you for choosing <b>{COMPANY}</b>. Here is your customized travel plan for <b>{destination}</b>.", n))
    story.append(Spacer(1, 12))

    details = [
        ["Client Name", client_name],
        ["Mobile", mobile],
        ["Category", category],
        ["Destination", destination],
        ["Starting Location", start_location],
        ["Days", str(days)],
        ["Persons", str(persons)],
        ["Stay Type", stay_type],
        ["Transport", transport_type],
        ["Food", food],
        ["Activities", activities],
        ["Estimated Budget", budget_text],
    ]
    tbl = Table(details, colWidths=[2.35 * inch, 4.45 * inch])
    tbl.setStyle(TableStyle([
        ("GRID", (0, 0), (-1, -1), 0.5, colors.lightgrey),
        ("BACKGROUND", (0, 0), (0, -1), colors.HexColor(CREAM)),
        ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
        ("TEXTCOLOR", (1, 0), (1, -1), colors.HexColor(TEAL)),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
    ]))
    story.append(tbl)

    story.append(Spacer(1, 14))
    story.append(Paragraph("Places Covered", h))
    story.append(Paragraph(", ".join(places), n))

    for day, items in itinerary:
        story.append(Spacer(1, 12))
        story.append(Paragraph(f"Day {day}", h))
        for item in items:
            story.append(Paragraph(f"• {item}", n))

    story.append(PageBreak())
    header()
    story.append(Paragraph("Package Inclusions", h))
    for item in [
        "Accommodation as per selected stay type.",
        "Transport as per selected vehicle type.",
        "Sightseeing places mentioned in the itinerary.",
        "Tour coordination and travel support.",
        "Food as per selected package plan.",
        "Customized planning based on customer requirement.",
    ]:
        story.append(Paragraph(f"• {item}", n))

    story.append(Paragraph("Package Exclusions", h))
    for item in [
        "Personal expenses such as laundry, tips, telephone charges and shopping.",
        "Extra sightseeing or vehicle usage not mentioned in itinerary.",
        "Entry tickets, adventure activities or permits unless specifically included.",
        "Medical, emergency or personal expenses.",
        "Any item not mentioned under inclusions.",
    ]:
        story.append(Paragraph(f"• {item}", n))

    story.append(Paragraph("Terms & Conditions", h))
    for item in [
        "50% advance payment is required to confirm the booking.",
        "Balance payment should be completed before tour departure.",
        "Rates may vary based on hotel availability, season, transport and group size.",
        "Final confirmation will be shared after payment and booking availability check.",
        "Cancellation charges may apply based on hotel, transport and vendor policy.",
    ]:
        story.append(Paragraph(f"• {item}", n))

    if note:
        story.append(Paragraph("Customer Notes", h))
        story.append(Paragraph(note, n))

    story.append(Spacer(1, 24))
    story.append(Paragraph("*** Thank you for choosing Endless Xplorers ***", title))
    story.append(Paragraph(TAGLINE, title))
    doc.build(story)

PAGE_IMAGES = extract_brochure_pages()

# ============================================================
# SIDEBAR NAVIGATION
# ============================================================

with st.sidebar:
    if os.path.exists(LOGO_PATH):
        st.image(LOGO_PATH, width=165)

    st.markdown(f"## {COMPANY}")
    st.caption(TAGLINE)
    st.markdown(f"📞 **{PHONE}**")
    st.markdown(f"📧 **{EMAIL}**")
    st.markdown(f"📸 **{INSTAGRAM}**")
    st.divider()

    menu = st.radio(
        "Navigation",
        [
            "Home",
            "Explore Packages",
            "Budget Calculator",
            "Package Builder",
            "Itinerary PDF",
            "Brochure",
            "Gallery",
            "Services",
            "Reviews",
            "Enquiry",
            "Admin",
        ],
    )

    st.divider()
    if os.path.exists(BROCHURE_PATH):
        with open(BROCHURE_PATH, "rb") as f:
            st.download_button("📘 Download Brochure", f, file_name="Endless_Xplorers_Brochure.pdf", mime="application/pdf", use_container_width=True)

    st.markdown(f"<a class='whatsapp' href='{wa_link('Hi Endless Xplorers, I need travel package details.')}' target='_blank'>📲 WhatsApp Now</a>", unsafe_allow_html=True)

# ============================================================
# HOME
# ============================================================

if menu == "Home":
    st.markdown(f"""
    <div class="hero">
        <span class="badge">Premium Travel Company</span>
        <h1>{COMPANY}</h1>
        <h2>{TAGLINE}</h2>
        <p>Plan domestic tours, international holidays, educational trips, corporate travel, honeymoon packages and pilgrimage journeys with a premium, safe and customized travel experience.</p>
        <a class="whatsapp" href="{wa_link('Hi Endless Xplorers, I want to plan a trip.')}" target="_blank">📲 Plan Your Trip</a>
        <a class="goldbtn" href="#popular">⭐ Popular Packages</a>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div class='title'>Travel Highlights</div>", unsafe_allow_html=True)
    for col, (a, b) in zip(st.columns(4), [("50+", "Destinations"), ("6", "Tour Categories"), ("24/7", "Support"), ("100%", "Custom Plans")]):
        with col:
            st.markdown(f"<div class='metric-card'><h1>{a}</h1><p>{b}</p></div>", unsafe_allow_html=True)

    st.markdown("<div id='popular' class='title'>Popular Packages</div>", unsafe_allow_html=True)
    for i in range(0, len(POPULAR), 3):
        cols = st.columns(3)
        for col, (cat, dest) in zip(cols, POPULAR[i:i+3]):
            p = package(cat, dest)
            with col:
                st.markdown(f"""
                <div class='package-card'>
                    <span class='badge'>{p['badge']}</span>
                    <h3>{dest}</h3>
                    <p>{p['desc']}</p>
                    <p><b>Category:</b> {cat}</p>
                    <p><b>Suggested:</b> {p['days']} days</p>
                    <p><b>Starting from:</b> ₹{p['base']:,} / person</p>
                </div>
                """, unsafe_allow_html=True)
                msg = f"Hi Endless Xplorers, I need details for {dest} package."
                st.markdown(f"<a class='whatsapp' href='{wa_link(msg)}' target='_blank'>📲 Enquire</a>", unsafe_allow_html=True)

    st.markdown("<div class='title'>Destination Gallery</div>", unsafe_allow_html=True)
    for i in range(0, 3, 3):
        cols = st.columns(3)
        for col, (name, url) in zip(cols, GALLERY[:3]):
            with col:
                st.markdown(f"<div class='gallery-card'><img src='{url}'><h3>{name}</h3></div>", unsafe_allow_html=True)

# ============================================================
# EXPLORE PACKAGES
# ============================================================

elif menu == "Explore Packages":
    st.markdown("<div class='title'>Explore Packages</div>", unsafe_allow_html=True)
    cat = st.selectbox("Choose Package Category", list(PACKAGES.keys()))
    names = list(PACKAGES[cat].keys())

    for i in range(0, len(names), 3):
        cols = st.columns(3)
        for col, dest in zip(cols, names[i:i+3]):
            p = package(cat, dest)
            with col:
                st.markdown(f"""
                <div class='package-card'>
                    <span class='badge'>{p['badge']}</span>
                    <h3>{dest}</h3>
                    <p>{p['desc']}</p>
                    <p><b>Suggested:</b> {p['days']} days</p>
                    <p><b>Places:</b> {", ".join(p['places'][:4])}</p>
                    <p><b>Starting from:</b> ₹{p['base']:,} / person</p>
                </div>
                """, unsafe_allow_html=True)
                st.markdown(f"<a class='whatsapp' href='{wa_link(f'Hi Endless Xplorers, I need details for {dest} package.')}' target='_blank'>📲 WhatsApp Enquiry</a>", unsafe_allow_html=True)

# ============================================================
# BUDGET CALCULATOR
# ============================================================

elif menu == "Budget Calculator":
    st.markdown("<div class='title'>Customer Budget Calculator</div>", unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    with c1:
        calc_cat = st.selectbox("Category", list(PACKAGES.keys()), key="calc_cat")
        calc_dest = st.selectbox("Destination", list(PACKAGES[calc_cat].keys()), key="calc_dest")
        calc_days = st.slider("No. of Days", 1, 15, package(calc_cat, calc_dest)["days"], key="calc_days")
    with c2:
        calc_persons = st.number_input("No. of Persons", 1, 500, 2, key="calc_persons")
        stay_type = st.selectbox("Stay Type", ["Budget", "Standard", "Premium", "Luxury"], key="calc_stay")
        transport_type = st.selectbox("Transport Type", ["Cab", "Tempo Traveller", "Bus / Coach", "Flight + Local Transport"], key="calc_transport")
    with c3:
        food_cost = st.number_input("Extra Food / Person", 0, 5000, 0, key="food_cost")
        activity_cost = st.number_input("Extra Activities / Person", 0, 10000, 0, key="activity_cost")
        discount = st.number_input("Discount Amount", 0, 1000000, 0, key="discount")

    base = package(calc_cat, calc_dest)["base"] + food_cost + activity_cost
    total, per_person, advance = calculate_budget(base, calc_persons, calc_days, stay_type, transport_type)
    total = max(total - discount, 0)
    per_person = int(total / max(calc_persons, 1))
    advance = int(total * 0.5)

    m1, m2, m3 = st.columns(3)
    with m1:
        st.markdown(f"<div class='metric-card'><h1>₹{total:,}</h1><p>Total Estimate</p></div>", unsafe_allow_html=True)
    with m2:
        st.markdown(f"<div class='metric-card'><h1>₹{per_person:,}</h1><p>Per Person</p></div>", unsafe_allow_html=True)
    with m3:
        st.markdown(f"<div class='metric-card'><h1>₹{advance:,}</h1><p>50% Advance</p></div>", unsafe_allow_html=True)

    msg = f"""Hi Endless Xplorers, I need package details.

Destination: {calc_dest}
Category: {calc_cat}
Days: {calc_days}
Persons: {calc_persons}
Stay: {stay_type}
Transport: {transport_type}
Estimated Budget: ₹{total:,}
Per Person: ₹{per_person:,}
"""
    st.text_area("WhatsApp Budget Message", msg, height=190)
    st.markdown(f"<a class='whatsapp' href='{wa_link(msg)}' target='_blank'>📲 Send Budget on WhatsApp</a>", unsafe_allow_html=True)

# ============================================================
# PACKAGE BUILDER
# ============================================================

elif menu == "Package Builder":
    st.markdown("<div class='title'>Custom Package Builder</div>", unsafe_allow_html=True)

    b1, b2, b3 = st.columns(3)
    with b1:
        customer = st.text_input("Customer Name")
        mobile = st.text_input("Mobile Number")
        start = st.text_input("Starting Location", "Coimbatore")
    with b2:
        cat = st.selectbox("Category", list(PACKAGES.keys()), key="build_cat")
        dest = st.selectbox("Destination", list(PACKAGES[cat].keys()), key="build_dest")
        days = st.slider("Days", 1, 15, package(cat, dest)["days"], key="build_days")
    with b3:
        persons = st.number_input("Persons", 1, 500, 2, key="build_persons")
        budget = st.selectbox("Budget Type", ["Budget", "Standard", "Premium", "Luxury"], key="build_budget")
        follow_up = st.date_input("Follow-up Date", date.today(), key="build_follow")

    p = package(cat, dest)
    for day, items in auto_itinerary(dest, p["places"], days, start):
        with st.expander(f"Day {day}", expanded=True):
            for item in items:
                st.write("•", item)

    msg = f"""🌍 Endless Xplorers - Package Request

Name: {customer}
Mobile: {mobile}
From: {start}
Category: {cat}
Destination: {dest}
Days: {days}
Persons: {persons}
Budget Type: {budget}
Follow-up Date: {follow_up}

Places: {", ".join(p["places"])}
"""
    st.text_area("WhatsApp Message Preview", msg, height=210)
    st.markdown(f"<a class='whatsapp' href='{wa_link(msg)}' target='_blank'>📲 Send Package Request</a>", unsafe_allow_html=True)

# ============================================================
# PDF
# ============================================================

elif menu == "Itinerary PDF":
    st.markdown("<div class='title'>Premium Itinerary PDF Generator</div>", unsafe_allow_html=True)

    p1, p2, p3 = st.columns(3)
    with p1:
        client = st.text_input("Client Name", "Customer Name")
        mobile = st.text_input("Mobile", CONTACT)
        start = st.text_input("Starting Location", "Coimbatore")
    with p2:
        cat = st.selectbox("Tour Category", list(PACKAGES.keys()), key="pdf_cat")
        dest = st.selectbox("Destination", list(PACKAGES[cat].keys()), key="pdf_dest")
        days = st.slider("No. of Days", 1, 15, package(cat, dest)["days"], key="pdf_days")
    with p3:
        persons = st.number_input("No. of Persons", 1, 500, 35)
        stay_type = st.selectbox("Stay Type", ["Budget", "Standard", "Premium", "Luxury"])
        transport_type = st.selectbox("Transport", ["Cab", "Tempo Traveller", "Bus / Coach", "Flight + Local Transport"])

    food = st.text_input("Food Plan", "Breakfast, Lunch and Dinner as per package")
    activities = st.text_input("Activities", "Sightseeing, photography, leisure and campfire if applicable")
    note = st.text_area("Special Notes", "Package can be customized based on customer requirement.")

    total, per_person, advance = calculate_budget(package(cat, dest)["base"], persons, days, stay_type, transport_type)
    budget_text = f"₹{total:,} approx total | ₹{per_person:,} per person | ₹{advance:,} advance"

    st.success(budget_text)

    if st.button("📄 Generate Premium PDF", use_container_width=True):
        out = os.path.join(BASE_DIR, f"{dest.replace(' ', '_')}_Premium_Itinerary.pdf")
        generate_pdf(out, client, mobile, cat, dest, start, days, persons, stay_type, transport_type, food, activities, budget_text, note)
        with open(out, "rb") as f:
            st.download_button("✅ Download Premium Itinerary PDF", f, file_name=f"{dest}_Premium_Itinerary.pdf", mime="application/pdf", use_container_width=True)

# ============================================================
# BROCHURE
# ============================================================

elif menu == "Brochure":
    st.markdown("<div class='title'>Brochure Preview</div>", unsafe_allow_html=True)
    st.info("Brochure is shown only here. Home page is clean and not split by brochure pages.")

    c1, c2 = st.columns([1, 1])
    with c1:
        section = st.selectbox("Select Brochure Section", list(BROCHURE_PAGES.keys()))
        pno = BROCHURE_PAGES[section]
        if pno in PAGE_IMAGES:
            st.image(PAGE_IMAGES[pno], use_container_width=True)
        else:
            st.warning("Brochure preview not available. Check PDF filename.")
    with c2:
        st.markdown(f"<div class='card'><h2>{COMPANY} Brochure</h2><p>Download the complete brochure and share it with customers.</p></div>", unsafe_allow_html=True)
        if os.path.exists(BROCHURE_PATH):
            with open(BROCHURE_PATH, "rb") as f:
                st.download_button("📘 Download Full Brochure", f, file_name="Endless_Xplorers_Brochure.pdf", mime="application/pdf", use_container_width=True)

# ============================================================
# GALLERY
# ============================================================

elif menu == "Gallery":
    st.markdown("<div class='title'>Destination Gallery</div>", unsafe_allow_html=True)

    for i in range(0, len(GALLERY), 3):
        cols = st.columns(3)
        for col, (name, url) in zip(cols, GALLERY[i:i+3]):
            with col:
                st.markdown(f"<div class='gallery-card'><img src='{url}'><h3>{name}</h3></div>", unsafe_allow_html=True)

# ============================================================
# SERVICES
# ============================================================

elif menu == "Services":
    st.markdown("<div class='title'>Travel Services</div>", unsafe_allow_html=True)

    services = [
        ("✈️", "Flight Booking", "Domestic and international ticket support."),
        ("🏨", "Hotel Reservation", "Budget, premium, resort and villa stays."),
        ("🚌", "Transportation", "Cars, vans, tempo travellers and buses."),
        ("🛂", "Visa Assistance", "Document guidance for international travel."),
        ("🎫", "Holiday Packages", "Customized packages for all travel types."),
        ("🎓", "Educational Trips", "IV, industrial visits and student tours."),
        ("🏢", "Corporate Tours", "Team outings, meetings and offsite plans."),
        ("🛡️", "Travel Insurance", "Safe and worry-free travel support."),
    ]

    for i in range(0, len(services), 4):
        cols = st.columns(4)
        for col, s in zip(cols, services[i:i+4]):
            with col:
                st.markdown(f"<div class='service-card'><h2>{s[0]}</h2><h3>{s[1]}</h3><p>{s[2]}</p></div>", unsafe_allow_html=True)

# ============================================================
# REVIEWS
# ============================================================

elif menu == "Reviews":
    st.markdown("<div class='title'>Customer Reviews</div>", unsafe_allow_html=True)

    reviews = [
        ("College IV Trip", "Well organized transport, food and itinerary. Students enjoyed the trip safely."),
        ("Family Kerala Tour", "Good hotel selection and smooth travel plan. Very comfortable experience."),
        ("Honeymoon Package", "Beautiful stay and perfect planning. The package felt premium and memorable."),
        ("Corporate Outing", "Team activities and resort arrangements were excellent. Highly recommended."),
    ]

    cols = st.columns(4)
    for col, (rt, rx) in zip(cols, reviews):
        with col:
            st.markdown(f"<div class='review'><h3>⭐ {rt}</h3><p>{rx}</p><b class='gold'>- Happy Customer</b></div>", unsafe_allow_html=True)

# ============================================================
# ENQUIRY
# ============================================================

elif menu == "Enquiry":
    st.markdown("<div class='title'>Customer Enquiry</div>", unsafe_allow_html=True)

    e1, e2, e3 = st.columns(3)
    with e1:
        name = st.text_input("Name")
        mobile = st.text_input("Mobile Number")
        city = st.text_input("City / Starting Place", "Coimbatore")
    with e2:
        lead_category = st.selectbox("Category", list(PACKAGES.keys()), key="lead_cat")
        lead_dest = st.selectbox("Destination", list(PACKAGES[lead_category].keys()), key="lead_dest")
        travel_date = st.date_input("Expected Travel Date")
    with e3:
        persons = st.number_input("No. of Persons", 1, 500, 2)
        budget_type = st.selectbox("Budget", ["Budget", "Standard", "Premium", "Luxury"])
        status = st.selectbox("Lead Status", ["New", "Follow-up", "Confirmed", "Cancelled"])

    follow_up = st.date_input("Follow-up Date", date.today())
    note = st.text_area("Requirement / Notes", "Need customized package details.")

    p = package(lead_category, lead_dest)
    total, per_person, advance = calculate_budget(p["base"], persons, p["days"], budget_type, "Bus / Coach")
    st.info(f"Estimated budget: ₹{total:,} total | ₹{per_person:,} per person | Follow-up: {follow_up}")

    if st.button("✅ Save Customer Enquiry", use_container_width=True):
        if not name or not mobile:
            st.error("Please enter customer name and mobile number.")
        else:
            data = {
                "DateTime": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Name": name,
                "Mobile": mobile,
                "City": city,
                "Category": lead_category,
                "Destination": lead_dest,
                "Travel Date": str(travel_date),
                "Follow-up Date": str(follow_up),
                "Persons": persons,
                "Budget": budget_type,
                "Estimated Total": total,
                "Per Person": per_person,
                "Advance": advance,
                "Status": status,
                "Note": note,
            }
            save_lead(data)
            st.success("Customer enquiry saved successfully.")

            msg = f"""New Travel Enquiry - Endless Xplorers

Name: {name}
Mobile: {mobile}
City: {city}
Category: {lead_category}
Destination: {lead_dest}
Travel Date: {travel_date}
Follow-up Date: {follow_up}
Persons: {persons}
Budget: {budget_type}
Estimated Total: ₹{total:,}
Status: {status}
Requirement: {note}
"""
            st.markdown(f"<a class='whatsapp' href='{wa_link(msg)}' target='_blank'>📲 Send to WhatsApp</a>", unsafe_allow_html=True)

# ============================================================
# ADMIN
# ============================================================

elif menu == "Admin":
    st.markdown("<div class='title'>Admin Dashboard</div>", unsafe_allow_html=True)

    password = st.text_input("Admin Password", type="password")

    if password == ADMIN_PASSWORD:
        if os.path.exists(LEADS_FILE):
            df = pd.read_csv(LEADS_FILE)

            for col in ["DateTime", "Name", "Mobile", "City", "Category", "Destination", "Travel Date", "Follow-up Date", "Persons", "Budget", "Estimated Total", "Per Person", "Advance", "Status", "Note"]:
                if col not in df.columns:
                    df[col] = ""

            today_str = datetime.now().strftime("%Y-%m-%d")
            total_count = len(df)
            today_count = len(df[df["DateTime"].astype(str).str.startswith(today_str)])
            follow_count = len(df[df["Status"].astype(str).str.lower() == "follow-up"])
            confirmed_count = len(df[df["Status"].astype(str).str.lower() == "confirmed"])

            for col, (num, label) in zip(st.columns(4), [(total_count, "Total Leads"), (today_count, "Today"), (follow_count, "Follow-up"), (confirmed_count, "Confirmed")]):
                with col:
                    st.markdown(f"<div class='metric-card'><h1>{num}</h1><p>{label}</p></div>", unsafe_allow_html=True)

            search = st.text_input("Search lead")
            view = df.copy()
            if search:
                s = search.lower()
                view = view[view.astype(str).apply(lambda row: row.str.lower().str.contains(s).any(), axis=1)]

            st.markdown("### Leads Table")
            st.dataframe(view, use_container_width=True)

            st.markdown("### Update Lead Status")
            if len(df) > 0:
                lead_options = [f"{i} - {row.get('Name','')} - {row.get('Destination','')} - {row.get('Mobile','')}" for i, row in df.iterrows()]
                selected = st.selectbox("Select Lead", lead_options)
                selected_index = int(selected.split(" - ")[0])
                new_status = st.selectbox("New Status", ["New", "Follow-up", "Confirmed", "Cancelled"], index=0)
                new_follow = st.date_input("New Follow-up Date", date.today(), key="admin_follow")
                admin_note = st.text_area("Admin Note", "")

                c1, c2 = st.columns(2)
                with c1:
                    if st.button("💾 Update Lead", use_container_width=True):
                        df.loc[selected_index, "Status"] = new_status
                        df.loc[selected_index, "Follow-up Date"] = str(new_follow)
                        if admin_note:
                            old_note = str(df.loc[selected_index, "Note"])
                            df.loc[selected_index, "Note"] = old_note + " | Admin: " + admin_note
                        df.to_csv(LEADS_FILE, index=False)
                        st.success("Lead updated successfully. Refresh Admin page to view changes.")

                with c2:
                    row = df.loc[selected_index]
                    msg = f"""Follow-up from Endless Xplorers

Hi {row.get('Name','')},
Your enquiry for {row.get('Destination','')} package is noted.

Category: {row.get('Category','')}
Travel Date: {row.get('Travel Date','')}
Persons: {row.get('Persons','')}
Budget: {row.get('Budget','')}
Estimated Total: ₹{row.get('Estimated Total','')}

Please confirm your travel plan.

Endless Xplorers
{PHONE}
{INSTAGRAM}
"""
                    st.markdown(f"<a class='whatsapp' href='{wa_link(msg)}' target='_blank'>📲 WhatsApp Selected Lead</a>", unsafe_allow_html=True)

            csv = df.to_csv(index=False).encode("utf-8")
            st.download_button("⬇️ Download Leads CSV", csv, file_name="Endless_Xplorers_Leads.csv", mime="text/csv", use_container_width=True)

            with st.expander("Danger Zone"):
                st.warning("This will clear all saved enquiries.")
                if st.button("Clear All Leads"):
                    pd.DataFrame(columns=df.columns).to_csv(LEADS_FILE, index=False)
                    st.success("All leads cleared. Refresh the page.")
        else:
            st.info("No leads saved yet.")
    elif password:
        st.error("Wrong password.")

# ============================================================
# FOOTER
# ============================================================

st.markdown(f"""
<div class='footer'>
    <h2>{COMPANY}</h2>
    <p>{TAGLINE}</p>
    <p>{PHONE} | {EMAIL} | {INSTAGRAM}</p>
    <a class='social' href='https://wa.me/91{CONTACT}' target='_blank'>WhatsApp</a>
    <a class='social' href='https://www.instagram.com/endlessxplorers_official' target='_blank'>Instagram</a>
    <a class='social' href='mailto:{EMAIL}'>Email</a>
    <p>{ADDRESS}</p>
</div>
""", unsafe_allow_html=True)
