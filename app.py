import streamlit as st
import os
import base64
import urllib.parse
import pandas as pd
from datetime import datetime
from PIL import Image as PILImage
import fitz

from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Image as RLImage
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch

st.set_page_config(
    page_title="Endless Xplorers",
    page_icon="🌍",
    layout="wide"
)

APP_FOLDER = os.path.dirname(os.path.abspath(__file__))
LOGO_PATH = os.path.join(APP_FOLDER, "LOGO.jpg")
BROCHURE_PATH = os.path.join(APP_FOLDER, "Endless Xplorer Final 1.pdf")
LEADS_FILE = os.path.join(APP_FOLDER, "customer_enquiries.csv")

CONTACT = "9894591780"
PHONE_DISPLAY = "+91 9894591780"
EMAIL = "endlessxplorerofficial@gmail.com"
INSTAGRAM = "@endlessxplorers_official"
ADDRESS = "21/1, Nanjappa Gounder Thottam Road, Telungupalayam, Coimbatore - 641039"
TAGLINE = "Explore Beyond Boundaries • Creating Memories Together"

THEME = {
    "teal": "#063B3B",
    "gold": "#D4AF37",
    "cream": "#F7F1DD",
    "white": "#FFFFFF",
    "dark": "#0B1F1F"
}

DESTINATIONS = {
    "South India": {
        "Munnar": ["Tea Gardens", "Mattupetty Dam", "Echo Point", "Top Station", "Eravikulam National Park", "Kundala Lake"],
        "Alleppey": ["Houseboat Cruise", "Backwaters", "Vembanad Lake", "Beach Visit", "Village Experience", "Sunset Cruise"],
        "Coorg": ["Coffee Plantation", "Golden Temple", "Dubare Elephant Camp", "Abbey Falls", "Raja Seat", "Nisargadhama"],
        "Madurai": ["Meenakshi Amman Temple", "Thirumalai Nayakkar Palace", "Gandhi Museum", "Alagar Kovil", "Local Shopping"],
        "Kanyakumari": ["Vivekananda Rock", "Thiruvalluvar Statue", "Sunrise Point", "Kanyakumari Beach", "Suchindram Temple"],
        "Mysore": ["Mysore Palace", "Chamundi Hills", "Brindavan Garden", "Zoo", "St. Philomena Church"],
        "Hampi": ["Virupaksha Temple", "Stone Chariot", "Vijaya Vittala Temple", "Lotus Mahal", "Tungabhadra River"],
        "Ooty": ["Botanical Garden", "Ooty Lake", "Doddabetta Peak", "Rose Garden", "Pykara Lake", "Toy Train"]
    },
    "North India": {
        "Kashmir": ["Srinagar", "Dal Lake Shikara Ride", "Gulmarg", "Pahalgam", "Sonamarg", "Mughal Garden"],
        "Himachal Pradesh": ["Shimla", "Manali", "Solang Valley", "Kullu", "Rohtang Pass", "Mall Road"],
        "Agra": ["Taj Mahal", "Agra Fort", "Mehtab Bagh", "Fatehpur Sikri", "Local Handicrafts"],
        "Jaipur": ["Amer Fort", "Hawa Mahal", "City Palace", "Jantar Mantar", "Jal Mahal", "Local Bazaar"],
        "Rishikesh": ["Ganga Aarti", "Lakshman Jhula", "River Rafting", "Beatles Ashram", "Yoga Experience"],
        "Haridwar": ["Har Ki Pauri", "Ganga Aarti", "Mansa Devi Temple", "Chandi Devi Temple", "Local Market"],
        "Varanasi": ["Kashi Vishwanath Temple", "Ganga Aarti", "Boat Ride", "Sarnath", "Banaras Streets"],
        "Leh-Ladakh": ["Pangong Lake", "Nubra Valley", "Magnetic Hill", "Leh Palace", "Shanti Stupa"]
    },
    "International": {
        "Dubai": ["Burj Khalifa", "Dubai Mall", "Desert Safari", "Dubai Marina", "Palm Jumeirah", "Global Village"],
        "Bali": ["Ubud", "Tanah Lot Temple", "Kuta Beach", "Nusa Penida", "Uluwatu Temple", "Bali Swing"],
        "Maldives": ["Male City", "Water Villa", "Private Beach", "Sunset Cruise", "Snorkeling", "Island Hopping"],
        "Singapore": ["Merlion Park", "Sentosa Island", "Universal Studios", "Gardens by the Bay", "Marina Bay Sands"],
        "Paris": ["Eiffel Tower", "Louvre Museum", "Seine River Cruise", "Notre Dame View", "City Tour"],
        "Switzerland": ["Mount Titlis", "Lucerne", "Interlaken", "Zurich", "Swiss Alps"],
        "London": ["Big Ben", "London Eye", "Tower Bridge", "Buckingham Palace", "Thames Cruise"],
        "New York": ["Statue of Liberty", "Times Square", "Central Park", "Brooklyn Bridge", "Empire State Building"]
    },
    "Educational": {
        "Science & Technology": ["Science Centre", "Innovation Lab", "Robotics Demo", "Hands-on Learning", "Knowledge Session"],
        "History & Heritage": ["Museum Visit", "Monuments", "UNESCO Sites", "Guided Heritage Walk", "Cultural Learning"],
        "Wildlife & Nature": ["National Park", "Nature Trail", "Wildlife Safari", "Eco Learning", "Conservation Session"],
        "Industry Visit": ["Factory Visit", "Expert Interaction", "Industrial Process Study", "Career Guidance", "Team Learning"]
    },
    "Corporate": {
        "Corporate Offsite": ["Resort Check-in", "Team Activities", "Leadership Games", "Networking Dinner", "Relaxation"],
        "Team Building": ["Ice Breakers", "Outdoor Games", "Problem Solving Tasks", "Group Challenges", "Award Session"],
        "Conference Tour": ["Venue Setup", "Seminar Session", "Travel Management", "Lunch", "Networking"],
        "Incentive Travel": ["Premium Stay", "Sightseeing", "Celebration Dinner", "Awards Night", "Team Bonding"]
    },
    "Honeymoon": {
        "Maldives Honeymoon": ["Water Villa", "Private Beach Dinner", "Sunset Cruise", "Snorkeling", "Couple Photoshoot"],
        "Bali Honeymoon": ["Romantic Villa", "Bali Swing", "Temple Visit", "Beach Dinner", "Spa Experience"],
        "Kerala Honeymoon": ["Munnar Hills", "Alleppey Houseboat", "Candlelight Dinner", "Ayurvedic Spa", "Backwater Cruise"],
        "Switzerland Honeymoon": ["Swiss Alps", "Lucerne", "Mount Titlis", "Romantic Train Journey", "Lake View"]
    },
    "Pilgrimage": {
        "Char Dham Yatra": ["Yamunotri", "Gangotri", "Kedarnath", "Badrinath", "Spiritual Darshan"],
        "Kashi - Ayodhya": ["Kashi Vishwanath", "Ganga Aarti", "Ayodhya Ram Mandir", "Sarayu Aarti", "Local Temple Visit"],
        "Tirupati - Rameswaram": ["Tirupati Darshan", "Padmavathi Temple", "Rameswaram Temple", "Dhanushkodi", "Agni Theertham"],
        "Haridwar - Rishikesh": ["Har Ki Pauri", "Ganga Aarti", "Yoga Ashram", "Lakshman Jhula", "Spiritual Walk"]
    }
}

BROCHURE_PAGE_MAP = {
    "Home": 1,
    "About": 2,
    "Why Choose Us": 3,
    "South India": 4,
    "North India": 5,
    "International": 6,
    "Educational": 7,
    "Corporate": 8,
    "Honeymoon": 9,
    "Pilgrimage": 10,
    "Experiences": 11,
    "Services": 12,
    "Contact": 13
}

@st.cache_resource
def extract_brochure_pages():
    output_dir = os.path.join(APP_FOLDER, "brochure_pages")
    os.makedirs(output_dir, exist_ok=True)

    page_images = {}

    if not os.path.exists(BROCHURE_PATH):
        return page_images

    doc = fitz.open(BROCHURE_PATH)

    for page_no in range(len(doc)):
        output_path = os.path.join(output_dir, f"page_{page_no + 1}.png")

        if not os.path.exists(output_path):
            page = doc[page_no]
            pix = page.get_pixmap(matrix=fitz.Matrix(1.6, 1.6), alpha=False)
            pix.save(output_path)

        page_images[page_no + 1] = output_path

    return page_images

def image_to_base64(path):
    if not os.path.exists(path):
        return ""
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

def get_whatsapp_link(message):
    encoded = urllib.parse.quote(message)
    return f"https://wa.me/91{CONTACT}?text={encoded}"

def save_lead(name, mobile, category, destination, persons, date, note):
    data = {
        "DateTime": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Name": name,
        "Mobile": mobile,
        "Category": category,
        "Destination": destination,
        "Persons": persons,
        "Travel Date": str(date),
        "Note": note
    }

    df = pd.DataFrame([data])

    if os.path.exists(LEADS_FILE):
        old = pd.read_csv(LEADS_FILE)
        df = pd.concat([old, df], ignore_index=True)

    df.to_csv(LEADS_FILE, index=False)

def create_daywise_itinerary(destination, places, days, start_location):
    itinerary = []

    for day in range(1, days + 1):
        if day == 1:
            plan = [
                f"Departure from {start_location}",
                f"Arrival at {destination}",
                "Hotel check-in and refreshment",
                "Breakfast / Welcome drink",
                "Proceed to sightseeing",
                places[0],
                places[1] if len(places) > 1 else places[0],
                "Lunch",
                places[2] if len(places) > 2 else places[0],
                "Evening leisure / group activity",
                "Dinner",
                "Night stay at hotel"
            ]
        elif day == days:
            plan = [
                "Breakfast",
                "Hotel check-out",
                "Proceed to final sightseeing",
                places[-2] if len(places) > 2 else places[0],
                places[-1],
                "Lunch",
                "Shopping / photography / free time",
                "Dinner",
                f"Return back to {start_location}"
            ]
        else:
            first_place = places[(day + 1) % len(places)]
            second_place = places[(day + 2) % len(places)]

            plan = [
                "Breakfast",
                "Proceed to sightseeing",
                first_place,
                "Explore nearby attractions",
                "Lunch",
                second_place,
                "Evening leisure / camp fire / cultural experience",
                "Dinner",
                "Night stay at hotel"
            ]

        itinerary.append((day, plan))

    return itinerary

def generate_pdf(output_path, company_name, client_name, plan_name, category, destination,
                 days, start_location, persons, staff_count, accommodation, transport,
                 food, activities, places):
    doc = SimpleDocTemplate(output_path, pagesize=A4, rightMargin=45, leftMargin=45, topMargin=35, bottomMargin=35)
    styles = getSampleStyleSheet()

    normal = ParagraphStyle("normal", parent=styles["Normal"], fontSize=11, leading=16)
    small = ParagraphStyle("small", parent=styles["Normal"], fontSize=10, leading=14)
    heading = ParagraphStyle("heading", parent=styles["Heading2"], fontSize=15, leading=20, textColor=colors.HexColor(THEME["teal"]))
    title = ParagraphStyle("title", parent=styles["Title"], fontSize=18, leading=24, alignment=1, textColor=colors.HexColor(THEME["teal"]))

    story = []

    def header():
        if os.path.exists(LOGO_PATH):
            logo = RLImage(LOGO_PATH, width=1.5 * inch, height=1.0 * inch)
        else:
            logo = Paragraph("<b>ENDLESS XPLORERS</b>", heading)

        contact = Paragraph(
            f"<b>Endless Xplorers</b><br/>"
            f"Contact: {PHONE_DISPLAY}<br/>"
            f"Email: {EMAIL}<br/>"
            f"Instagram: {INSTAGRAM}",
            small
        )

        table = Table([[logo, contact]], colWidths=[2.1 * inch, 4.8 * inch])
        table.setStyle(TableStyle([
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("ALIGN", (1, 0), (1, 0), "RIGHT"),
        ]))

        story.append(table)
        story.append(Spacer(1, 8))
        story.append(Table([[""]], colWidths=[7 * inch],
                           style=[("LINEBELOW", (0, 0), (-1, -1), 2, colors.HexColor(THEME["gold"]))]))
        story.append(Spacer(1, 20))

    header()

    story.append(Paragraph(
        "We are pleased to welcome you as a valuable customer of <b>Endless Xplorers</b>.<br/>"
        "We hope your tour with us will be a memorable one.",
        normal
    ))
    story.append(Spacer(1, 18))

    details = [
        ["College / Company Name:", company_name],
        ["Client Name:", client_name],
        ["Tour Category:", category],
        ["Plan:", plan_name],
        ["Destination:", destination],
        ["No. of Days:", str(days)]
    ]

    details_table = Table(details, colWidths=[2.2 * inch, 4.4 * inch])
    details_table.setStyle(TableStyle([
        ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
        ("FONTNAME", (1, 0), (1, -1), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 12),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 9),
    ]))
    story.append(details_table)

    itinerary = create_daywise_itinerary(destination, places, days, start_location)

    for day, plan in itinerary:
        story.append(Spacer(1, 14))
        story.append(Paragraph(f"<b>Day {day} :</b>", heading))

        for item in plan:
            if item in ["Breakfast", "Lunch", "Dinner", "Night stay at hotel", "Breakfast / Welcome drink"]:
                story.append(Paragraph(f"<b>{item}</b>", normal))
            else:
                story.append(Paragraph(f"• {item}", normal))

        if day != days:
            story.append(PageBreak())
            header()

    story.append(PageBreak())
    header()

    story.append(Paragraph("<b>TARIFF CHART</b>", title))
    story.append(Spacer(1, 12))

    tariff_data = [
        ["No. of Person", f"{persons} Persons + {staff_count} Staff"],
        ["Accommodation Mode", accommodation],
        ["Transport", transport],
        ["Food", food],
        ["Additional Activities", activities],
    ]

    tariff_table = Table(tariff_data, colWidths=[3 * inch, 3.8 * inch])
    tariff_table.setStyle(TableStyle([
        ("GRID", (0, 0), (-1, -1), 0.8, colors.grey),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("FONTNAME", (1, 0), (1, -1), "Helvetica-Bold"),
        ("TEXTCOLOR", (1, 0), (1, -1), colors.HexColor(THEME["teal"])),
        ("FONTSIZE", (0, 0), (-1, -1), 11),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
        ("TOPPADDING", (0, 0), (-1, -1), 10),
    ]))
    story.append(tariff_table)

    story.append(Spacer(1, 25))
    story.append(Paragraph("<u>Package Inclusions:</u>", heading))

    inclusions = [
        "Accommodation in comfortable and convenient hotels.",
        "Sightseeing places as mentioned in the itinerary.",
        "Tour Manager services from Day 1 meeting point till dropping point on last day.",
        "Breakfast, Lunch and Dinner as per the package food plan.",
        "Additional activities as mentioned in the tariff chart.",
        "Bus / Train / Flight tickets if included in the package.",
        "Toll, parking, fuel, driver bata and applicable taxes if included.",
        "Travel by comfortable A/c or Non A/c coach / vehicle as per itinerary.",
        "Under unavoidable circumstances alternative hotels and vehicles will be provided."
    ]

    for item in inclusions:
        story.append(Paragraph(f"• {item}", small))

    story.append(PageBreak())
    header()

    story.append(Paragraph("<u>Package Exclusions:</u>", heading))

    exclusions = [
        "Any extra expense such as route change, personal expenses, laundry, telephone calls, tips, liquor, food or drink which is not part of a set group menu.",
        "Additional sightseeing or usage of vehicle not mentioned in the itinerary.",
        "Any upgradation in hotel room category.",
        "Any extra cost incurred due to illness, accident, hospitalization or personal emergency.",
        "Any services or activity charges other than those included in the tour itinerary."
    ]

    for item in exclusions:
        story.append(Paragraph(f"• {item}", small))

    story.append(Spacer(1, 18))
    story.append(Paragraph("<u>Tour Payment by Guest:</u>", heading))
    payments = [
        "The guest will have to make 50% payment for confirming the services.",
        "The guest will have to make the full payment before tour departure.",
        "Any increase in government tax, visa fee, ticket fare, permit or entry charges shall be paid by the guest."
    ]

    for item in payments:
        story.append(Paragraph(f"• {item}", small))

    story.append(Spacer(1, 18))
    story.append(Paragraph("<u>Cancellation Policy:</u>", heading))
    story.append(Paragraph(
        "If the guest decides to cancel the tour for any reason, she/he shall give a written application "
        "to the company within the specified time limit. Cancellation charges will depend on the date of departure "
        "and date of cancellation.",
        small
    ))

    story.append(PageBreak())
    header()

    cancel_table = Table([
        ["No of days Prior to Departure", "% of Cancellation Charges"],
        ["10 Days Before", "25%"],
        ["5 Days Before", "50%"],
        ["2 Days Before", "75%"],
        ["24 hrs. / No Show", "100%"],
    ], colWidths=[3.5 * inch, 3.2 * inch])

    cancel_table.setStyle(TableStyle([
        ("GRID", (0, 0), (-1, -1), 0.8, colors.grey),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor(THEME["cream"])),
        ("FONTSIZE", (0, 0), (-1, -1), 11),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 9),
        ("TOPPADDING", (0, 0), (-1, -1), 9),
    ]))

    story.append(cancel_table)
    story.append(Spacer(1, 70))
    story.append(Paragraph("*** Thank you for choosing Endless Xplorers. ***", title))
    story.append(Spacer(1, 15))
    story.append(Paragraph(TAGLINE, title))

    doc.build(story)

page_images = extract_brochure_pages()

st.markdown(f"""
<style>
.stApp {{
    background: linear-gradient(135deg, #f8f3df 0%, #ffffff 50%, #edf7f6 100%);
}}

[data-testid="stSidebar"] {{
    background: linear-gradient(180deg, {THEME["teal"]}, #021f1f);
}}

[data-testid="stSidebar"] * {{
    color: white !important;
}}

.main-title {{
    font-size: 54px;
    font-weight: 900;
    color: {THEME["teal"]};
    margin-bottom: 0px;
}}

.gold {{
    color: {THEME["gold"]};
}}

.hero-box {{
    background: linear-gradient(135deg, rgba(6,59,59,0.95), rgba(6,59,59,0.75));
    border-radius: 28px;
    padding: 35px;
    color: white;
    box-shadow: 0px 20px 55px rgba(0,0,0,0.20);
    border: 1px solid rgba(212,175,55,0.5);
}}

.premium-card {{
    background: rgba(255,255,255,0.95);
    padding: 24px;
    border-radius: 24px;
    box-shadow: 0px 12px 35px rgba(0,0,0,0.10);
    border: 1px solid #eadca1;
    margin-bottom: 20px;
}}

.metric-card {{
    background: linear-gradient(135deg, {THEME["teal"]}, #0b5f5f);
    color: white;
    padding: 22px;
    border-radius: 22px;
    text-align: center;
    border-bottom: 5px solid {THEME["gold"]};
}}

.package-card {{
    background: white;
    padding: 18px;
    border-radius: 20px;
    border: 1px solid #eadca1;
    box-shadow: 0 8px 25px rgba(0,0,0,0.08);
    min-height: 170px;
}}

.section-title {{
    color: {THEME["teal"]};
    font-size: 32px;
    font-weight: 900;
    margin-top: 15px;
}}

.stButton button {{
    background: linear-gradient(135deg, {THEME["teal"]}, #0b7777);
    color: white;
    border-radius: 14px;
    border: none;
    font-weight: 800;
    padding: 12px 20px;
}}

.stDownloadButton button {{
    background: linear-gradient(135deg, {THEME["gold"]}, #f5d76e);
    color: #111;
    border-radius: 14px;
    border: none;
    font-weight: 800;
}}

a.whatsapp {{
    display:inline-block;
    padding:14px 22px;
    background:#25D366;
    color:white !important;
    text-decoration:none;
    border-radius:14px;
    font-weight:900;
    margin-top:10px;
}}

.footer {{
    text-align:center;
    background:{THEME["teal"]};
    color:white;
    padding:30px;
    border-radius:25px;
    margin-top:25px;
}}
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    if os.path.exists(LOGO_PATH):
        st.image(LOGO_PATH, width=170)

    st.title("Endless Xplorers")
    st.write(PHONE_DISPLAY)
    st.write(EMAIL)
    st.write(INSTAGRAM)

    st.divider()

    if os.path.exists(BROCHURE_PATH):
        with open(BROCHURE_PATH, "rb") as f:
            st.download_button(
                "📘 Download Brochure",
                f,
                file_name="Endless_Xplorers_Brochure.pdf",
                mime="application/pdf",
                use_container_width=True
            )

    st.info("Domestic • International • Educational • Corporate • Honeymoon • Pilgrimage")

tabs = st.tabs([
    "🏠 Home",
    "🌍 Packages",
    "🧳 Itinerary Generator",
    "📸 Brochure Gallery",
    "📞 Enquiry",
    "📊 Leads"
])

with tabs[0]:
    col1, col2 = st.columns([1.1, 1])

    with col1:
        st.markdown("""
        <div class="hero-box">
            <h1 style="font-size:54px;margin-bottom:5px;">Endless Xplorers</h1>
            <h2 style="color:#D4AF37;">Explore Beyond Boundaries</h2>
            <p style="font-size:18px;">Premium Domestic, International, Educational, Corporate, Honeymoon and Pilgrimage travel packages.</p>
            <p><b>Creating Memories Together...</b></p>
        </div>
        """, unsafe_allow_html=True)

        st.write("")
        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown("<div class='metric-card'><h2>50+</h2><p>Destinations</p></div>", unsafe_allow_html=True)
        with c2:
            st.markdown("<div class='metric-card'><h2>24/7</h2><p>Support</p></div>", unsafe_allow_html=True)
        with c3:
            st.markdown("<div class='metric-card'><h2>100%</h2><p>Custom Plans</p></div>", unsafe_allow_html=True)

    with col2:
        if 1 in page_images:
            st.image(page_images[1], use_container_width=True)
        elif os.path.exists(LOGO_PATH):
            st.image(LOGO_PATH, use_container_width=True)

    st.markdown("<h2 class='section-title'>Why Choose Endless Xplorers?</h2>", unsafe_allow_html=True)

    w1, w2, w3, w4 = st.columns(4)
    items = [
        ("🎯", "Customized Packages", "Tailored itineraries for your budget and needs."),
        ("🛡️", "Safe & Secure", "Trusted travel support from start to finish."),
        ("💎", "Premium Experience", "Quality hotels, transport and service partners."),
        ("📞", "24/7 Support", "Always available before, during and after your journey.")
    ]

    for col, item in zip([w1, w2, w3, w4], items):
        with col:
            st.markdown(f"""
            <div class="package-card">
                <h2>{item[0]}</h2>
                <h3>{item[1]}</h3>
                <p>{item[2]}</p>
            </div>
            """, unsafe_allow_html=True)

with tabs[1]:
    st.markdown("<h2 class='section-title'>Explore Our Package Collections</h2>", unsafe_allow_html=True)

    cat_tabs = st.tabs(list(DESTINATIONS.keys()))

    for cat_tab, category in zip(cat_tabs, DESTINATIONS.keys()):
        with cat_tab:
            page_no = BROCHURE_PAGE_MAP.get(category)
            if page_no and page_no in page_images:
                st.image(page_images[page_no], use_container_width=True)

            st.write("")
            names = list(DESTINATIONS[category].keys())

            for i in range(0, len(names), 4):
                cols = st.columns(4)
                for col, name in zip(cols, names[i:i+4]):
                    with col:
                        places = DESTINATIONS[category][name]
                        st.markdown(f"""
                        <div class="package-card">
                            <h3>{name}</h3>
                            <p>{", ".join(places[:4])}</p>
                            <b class="gold">Custom itinerary available</b>
                        </div>
                        """, unsafe_allow_html=True)

with tabs[2]:
    st.markdown("<h2 class='section-title'>Client Itinerary Package Generator</h2>", unsafe_allow_html=True)

    with st.container():
        c1, c2, c3 = st.columns(3)

        with c1:
            company_name = st.text_input("College / Company / Customer Name", "SNMV")
            client_name = st.text_input("Client Contact Person", "Praveen - IT")
            start_location = st.text_input("Starting Location", "Coimbatore")

        with c2:
            category = st.selectbox("Tour Category", list(DESTINATIONS.keys()))
            destination = st.selectbox("Destination / Package", list(DESTINATIONS[category].keys()))
            days = st.slider("No. of Days", 1, 12, 3)

        with c3:
            persons = st.number_input("No. of Persons / Students", 1, 500, 35)
            staff_count = st.number_input("No. of Staff / Coordinators", 0, 50, 2)
            accommodation = st.text_input("Accommodation Mode", "04 Sharing basis")

        transport = st.text_input("Transport", "54 Seater Coach / As per group size")
        food = st.text_input("Food", "Breakfast, Lunch and Dinner as per package")
        activities = st.text_input("Additional Activities", "Entry Tickets, Jeep, DJ / Camp Fire / Cruise if applicable")

        places = DESTINATIONS[category][destination]
        plan_name = f"{destination} - {category} Package"

        st.markdown("### Day-wise Preview")

        preview = create_daywise_itinerary(destination, places, days, start_location)

        for day, plan in preview:
            with st.expander(f"Day {day}", expanded=True):
                for item in plan:
                    st.write("•", item)

        if st.button("📥 Generate Premium Client Itinerary PDF", use_container_width=True):
            output_pdf = os.path.join(APP_FOLDER, f"{destination}_Itinerary.pdf")

            generate_pdf(
                output_pdf,
                company_name,
                client_name,
                plan_name,
                category,
                destination,
                days,
                start_location,
                persons,
                staff_count,
                accommodation,
                transport,
                food,
                activities,
                places
            )

            with open(output_pdf, "rb") as f:
                st.download_button(
                    "✅ Download Client Package PDF",
                    f,
                    file_name=f"{destination}_Package.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )

        whatsapp_msg = f"""
🌍 Endless Xplorers

✨ {destination} {category} Tour Package ✨

📍 From: {start_location}
👥 Persons: {persons} + {staff_count} Staff
🏨 Stay: {accommodation}
🚌 Transport: {transport}
🍽 Food: {food}
🎯 Activities: {activities}

Places Covered:
{", ".join(places)}

📞 Contact: {PHONE_DISPLAY}
📧 Email: {EMAIL}
📸 Instagram: {INSTAGRAM}

✨ Explore Beyond Boundaries
✨ Creating Memories Together
"""
        st.text_area("Copy WhatsApp Message", whatsapp_msg, height=250)
        st.markdown(f"<a class='whatsapp' href='{get_whatsapp_link(whatsapp_msg)}' target='_blank'>📲 Send Enquiry on WhatsApp</a>", unsafe_allow_html=True)

with tabs[3]:
    st.markdown("<h2 class='section-title'>Brochure Gallery</h2>", unsafe_allow_html=True)

    if page_images:
        labels = list(BROCHURE_PAGE_MAP.keys())
        selected_label = st.selectbox("Select Brochure Page", labels)
        selected_page = BROCHURE_PAGE_MAP[selected_label]

        if selected_page in page_images:
            st.image(page_images[selected_page], use_container_width=True)

        st.write("")
        st.markdown("### Quick Gallery")
        for i in range(1, 14, 3):
            cols = st.columns(3)
            for col, page_no in zip(cols, range(i, min(i+3, 14))):
                with col:
                    if page_no in page_images:
                        st.image(page_images[page_no], caption=f"Page {page_no}", use_container_width=True)
    else:
        st.warning("Brochure PDF not found. Please upload 'Endless Xplorer Final 1.pdf'.")

with tabs[4]:
    st.markdown("<h2 class='section-title'>Customer Enquiry Form</h2>", unsafe_allow_html=True)

    e1, e2 = st.columns(2)

    with e1:
        enq_name = st.text_input("Customer Name")
        enq_mobile = st.text_input("Mobile Number")
        enq_category = st.selectbox("Interested Category", list(DESTINATIONS.keys()), key="enqcat")

    with e2:
        enq_destination = st.selectbox("Interested Destination", list(DESTINATIONS[enq_category].keys()), key="enqdest")
        enq_persons = st.number_input("Number of Persons", 1, 500, 2, key="enqpersons")
        enq_date = st.date_input("Expected Travel Date")

    enq_note = st.text_area("Requirement / Notes", "Need customized travel package details.")

    if st.button("✅ Save Enquiry & Prepare WhatsApp Message", use_container_width=True):
        if enq_name and enq_mobile:
            save_lead(enq_name, enq_mobile, enq_category, enq_destination, enq_persons, enq_date, enq_note)
            st.success("Customer enquiry saved successfully.")

            msg = f"""
New Travel Enquiry - Endless Xplorers

Name: {enq_name}
Mobile: {enq_mobile}
Category: {enq_category}
Destination: {enq_destination}
Persons: {enq_persons}
Travel Date: {enq_date}
Requirement: {enq_note}
"""
            st.markdown(f"<a class='whatsapp' href='{get_whatsapp_link(msg)}' target='_blank'>📲 Send to WhatsApp</a>", unsafe_allow_html=True)
        else:
            st.error("Please enter customer name and mobile number.")

    st.write("")
    st.markdown("### Contact Details")
    st.info(f"""
📞 {PHONE_DISPLAY}  
📧 {EMAIL}  
📸 {INSTAGRAM}  
📍 {ADDRESS}
""")

with tabs[5]:
    st.markdown("<h2 class='section-title'>Customer Leads</h2>", unsafe_allow_html=True)

    password = st.text_input("Enter Admin Password", type="password")

    if password == "endless9894":
        if os.path.exists(LEADS_FILE):
            df = pd.read_csv(LEADS_FILE)
            st.dataframe(df, use_container_width=True)

            csv = df.to_csv(index=False).encode("utf-8")
            st.download_button(
                "Download Leads CSV",
                csv,
                file_name="Endless_Xplorers_Leads.csv",
                mime="text/csv",
                use_container_width=True
            )
        else:
            st.info("No enquiries saved yet.")
    elif password:
        st.error("Wrong password.")

st.markdown(f"""
<div class="footer">
    <h2>Endless Xplorers</h2>
    <p>{TAGLINE}</p>
    <p>{PHONE_DISPLAY} | {EMAIL} | {INSTAGRAM}</p>
    <p>{ADDRESS}</p>
</div>
""", unsafe_allow_html=True)
