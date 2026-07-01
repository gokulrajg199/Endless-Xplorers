import streamlit as st
import os
import urllib.parse
import pandas as pd
from datetime import datetime
import fitz

from reportlab.lib.pagesizes import A4
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table,
    TableStyle, PageBreak, Image as RLImage
)
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="Endless Xplorers",
    page_icon="🌍",
    layout="wide"
)

# =========================
# PATHS
# =========================
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

TEAL = "#063B3B"
GOLD = "#D4AF37"
CREAM = "#F7F1DD"
WHITE = "#FFFFFF"

# =========================
# DESTINATION DATA
# =========================
DESTINATIONS = {
    "South India": {
        "Munnar": ["Tea Gardens", "Mattupetty Dam", "Echo Point", "Top Station", "Eravikulam National Park", "Kundala Lake"],
        "Alleppey": ["Houseboat Cruise", "Backwaters", "Vembanad Lake", "Village Experience", "Beach Visit"],
        "Coorg": ["Coffee Plantation", "Golden Temple", "Dubare Elephant Camp", "Abbey Falls", "Raja Seat"],
        "Madurai": ["Meenakshi Amman Temple", "Thirumalai Nayakkar Palace", "Gandhi Museum", "Alagar Kovil"],
        "Kanyakumari": ["Vivekananda Rock", "Thiruvalluvar Statue", "Sunrise Point", "Beach Visit"],
        "Mysore": ["Mysore Palace", "Chamundi Hills", "Brindavan Garden", "Zoo"],
        "Hampi": ["Virupaksha Temple", "Stone Chariot", "Vijaya Vittala Temple", "Lotus Mahal"],
        "Ooty": ["Botanical Garden", "Ooty Lake", "Doddabetta Peak", "Rose Garden", "Pykara Lake", "Toy Train"]
    },
    "North India": {
        "Kashmir": ["Srinagar", "Dal Lake", "Shikara Ride", "Gulmarg", "Pahalgam", "Sonamarg"],
        "Himachal Pradesh": ["Shimla", "Manali", "Solang Valley", "Kullu", "Rohtang Pass"],
        "Agra": ["Taj Mahal", "Agra Fort", "Mehtab Bagh", "Fatehpur Sikri"],
        "Jaipur": ["Amer Fort", "Hawa Mahal", "City Palace", "Jantar Mantar", "Jal Mahal"],
        "Rishikesh": ["Ganga Aarti", "Lakshman Jhula", "River Rafting", "Yoga Experience"],
        "Haridwar": ["Har Ki Pauri", "Ganga Aarti", "Mansa Devi Temple", "Chandi Devi Temple"],
        "Varanasi": ["Kashi Vishwanath Temple", "Ganga Aarti", "Boat Ride", "Sarnath"],
        "Leh-Ladakh": ["Pangong Lake", "Nubra Valley", "Magnetic Hill", "Leh Palace"]
    },
    "International": {
        "Dubai": ["Burj Khalifa", "Dubai Mall", "Desert Safari", "Dubai Marina", "Palm Jumeirah"],
        "Bali": ["Ubud", "Tanah Lot Temple", "Kuta Beach", "Nusa Penida", "Bali Swing"],
        "Maldives": ["Male City", "Water Villa", "Private Beach", "Sunset Cruise", "Snorkeling"],
        "Singapore": ["Merlion Park", "Sentosa Island", "Universal Studios", "Gardens by the Bay"],
        "Paris": ["Eiffel Tower", "Louvre Museum", "Seine River Cruise", "City Tour"],
        "Switzerland": ["Mount Titlis", "Lucerne", "Interlaken", "Swiss Alps"],
        "London": ["Big Ben", "London Eye", "Tower Bridge", "Buckingham Palace"],
        "New York": ["Statue of Liberty", "Times Square", "Central Park", "Brooklyn Bridge"]
    },
    "Educational": {
        "Science & Technology": ["Science Centre", "Innovation Lab", "Robotics Demo", "Knowledge Session"],
        "History & Heritage": ["Museum Visit", "Heritage Walk", "UNESCO Sites", "Cultural Learning"],
        "Wildlife & Nature": ["National Park", "Nature Trail", "Wildlife Safari", "Eco Learning"],
        "Industry Visit": ["Factory Visit", "Expert Interaction", "Industrial Process Study", "Career Guidance"]
    },
    "Corporate": {
        "Corporate Offsite": ["Resort Check-in", "Team Activities", "Leadership Games", "Networking Dinner"],
        "Team Building": ["Ice Breakers", "Outdoor Games", "Group Challenges", "Award Session"],
        "Conference Tour": ["Venue Setup", "Seminar Session", "Travel Management", "Lunch"],
        "Incentive Travel": ["Premium Stay", "Sightseeing", "Celebration Dinner", "Team Bonding"]
    },
    "Honeymoon": {
        "Maldives Honeymoon": ["Water Villa", "Private Beach Dinner", "Sunset Cruise", "Snorkeling"],
        "Bali Honeymoon": ["Romantic Villa", "Bali Swing", "Temple Visit", "Beach Dinner"],
        "Kerala Honeymoon": ["Munnar Hills", "Alleppey Houseboat", "Candlelight Dinner", "Spa"],
        "Switzerland Honeymoon": ["Swiss Alps", "Lucerne", "Mount Titlis", "Romantic Train Journey"]
    },
    "Pilgrimage": {
        "Char Dham Yatra": ["Yamunotri", "Gangotri", "Kedarnath", "Badrinath"],
        "Kashi - Ayodhya": ["Kashi Vishwanath", "Ganga Aarti", "Ayodhya Ram Mandir", "Sarayu Aarti"],
        "Tirupati - Rameswaram": ["Tirupati Darshan", "Padmavathi Temple", "Rameswaram Temple", "Dhanushkodi"],
        "Haridwar - Rishikesh": ["Har Ki Pauri", "Ganga Aarti", "Yoga Ashram", "Lakshman Jhula"]
    }
}

BROCHURE_PAGES = {
    "Home": 1,
    "Why Choose Us": 3,
    "South India": 4,
    "North India": 5,
    "International": 6,
    "Educational": 7,
    "Corporate": 8,
    "Honeymoon": 9,
    "Pilgrimage": 10,
    "Travel Services": 12,
    "Contact": 13
}

# =========================
# BROCHURE IMAGE EXTRACTION
# =========================
@st.cache_resource
def extract_brochure_pages():
    output_dir = os.path.join(APP_FOLDER, "brochure_pages")
    os.makedirs(output_dir, exist_ok=True)
    pages = {}

    if not os.path.exists(BROCHURE_PATH):
        return pages

    pdf = fitz.open(BROCHURE_PATH)

    for page_no in range(len(pdf)):
        image_path = os.path.join(output_dir, f"page_{page_no + 1}.png")
        if not os.path.exists(image_path):
            page = pdf[page_no]
            pix = page.get_pixmap(matrix=fitz.Matrix(1.3, 1.3), alpha=False)
            pix.save(image_path)
        pages[page_no + 1] = image_path

    return pages

page_images = extract_brochure_pages()

# =========================
# HELPERS
# =========================
def whatsapp_link(message):
    return f"https://wa.me/91{CONTACT}?text={urllib.parse.quote(message)}"

def save_lead(name, mobile, category, destination, persons, travel_date, note):
    row = {
        "DateTime": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Name": name,
        "Mobile": mobile,
        "Category": category,
        "Destination": destination,
        "Persons": persons,
        "Travel Date": str(travel_date),
        "Note": note
    }

    df = pd.DataFrame([row])
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
                places[-2] if len(places) > 2 else places[0],
                places[-1],
                "Lunch",
                "Shopping / photography / free time",
                "Dinner",
                f"Return back to {start_location}"
            ]
        else:
            plan = [
                "Breakfast",
                places[(day + 1) % len(places)],
                "Explore nearby attractions",
                "Lunch",
                places[(day + 2) % len(places)],
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
    heading = ParagraphStyle("heading", parent=styles["Heading2"], fontSize=15, textColor=colors.HexColor(TEAL))
    title = ParagraphStyle("title", parent=styles["Title"], fontSize=18, alignment=1, textColor=colors.HexColor(TEAL))

    story = []

    def header():
        if os.path.exists(LOGO_PATH):
            logo = RLImage(LOGO_PATH, width=1.45 * inch, height=1.0 * inch)
        else:
            logo = Paragraph("<b>ENDLESS XPLORERS</b>", heading)

        contact = Paragraph(
            f"<b>Endless Xplorers</b><br/>"
            f"{PHONE_DISPLAY}<br/>{EMAIL}<br/>{INSTAGRAM}",
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
                           style=[("LINEBELOW", (0, 0), (-1, -1), 2, colors.HexColor(GOLD))]))
        story.append(Spacer(1, 20))

    header()

    story.append(Paragraph(
        "We are pleased to welcome you as a valuable customer of <b>Endless Xplorers</b>.<br/>"
        "We hope your tour with us will be a memorable one.",
        normal
    ))
    story.append(Spacer(1, 18))

    details = [
        ["College / Company / Customer Name:", company_name],
        ["Client Contact Person:", client_name],
        ["Tour Category:", category],
        ["Plan:", plan_name],
        ["Destination:", destination],
        ["No. of Days:", str(days)]
    ]

    details_table = Table(details, colWidths=[2.7 * inch, 4.0 * inch])
    details_table.setStyle(TableStyle([
        ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
        ("FONTNAME", (1, 0), (1, -1), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 11),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 9),
    ]))
    story.append(details_table)

    itinerary = create_daywise_itinerary(destination, places, days, start_location)

    for day, plan in itinerary:
        story.append(Spacer(1, 14))
        story.append(Paragraph(f"<b>Day {day}</b>", heading))
        for item in plan:
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
        ("BACKGROUND", (0, 0), (0, -1), colors.HexColor(CREAM)),
        ("FONTNAME", (0, 0), (-1, -1), "Helvetica-Bold"),
        ("TEXTCOLOR", (1, 0), (1, -1), colors.HexColor(TEAL)),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("FONTSIZE", (0, 0), (-1, -1), 11),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
        ("TOPPADDING", (0, 0), (-1, -1), 10),
    ]))
    story.append(tariff_table)

    story.append(Spacer(1, 25))
    story.append(Paragraph("<u>Package Inclusions</u>", heading))
    inclusions = [
        "Accommodation in comfortable and convenient hotels.",
        "Sightseeing places as mentioned in the itinerary.",
        "Tour Manager services from meeting point till dropping point.",
        "Food as per the package food plan.",
        "Transport as per itinerary.",
        "Toll, parking, fuel, driver bata and applicable taxes if included.",
        "Under unavoidable circumstances alternative hotels and vehicles will be provided."
    ]

    for item in inclusions:
        story.append(Paragraph(f"• {item}", small))

    story.append(PageBreak())
    header()

    story.append(Paragraph("<u>Package Exclusions</u>", heading))
    exclusions = [
        "Personal expenses, laundry, telephone calls, tips, liquor, food or drink not part of the menu.",
        "Additional sightseeing or usage of vehicle not mentioned in the itinerary.",
        "Hotel room upgrade charges.",
        "Medical emergency, hospitalization or personal emergency expenses.",
        "Any service not mentioned in inclusions."
    ]

    for item in exclusions:
        story.append(Paragraph(f"• {item}", small))

    story.append(Spacer(1, 18))
    story.append(Paragraph("<u>Tour Payment by Guest</u>", heading))
    payments = [
        "50% payment is required for confirming the services.",
        "Full payment should be completed before tour departure.",
        "Any increase in government tax, visa fee, ticket fare, permit or entry charges shall be paid by the guest."
    ]

    for item in payments:
        story.append(Paragraph(f"• {item}", small))

    story.append(Spacer(1, 18))
    story.append(Paragraph("<u>Cancellation Policy</u>", heading))
    story.append(Paragraph(
        "Cancellation charges will depend on the date of departure and date of cancellation.",
        small
    ))

    story.append(PageBreak())
    header()

    cancel_table = Table([
        ["No. of days prior to departure", "Cancellation Charges"],
        ["10 Days Before", "25%"],
        ["5 Days Before", "50%"],
        ["2 Days Before", "75%"],
        ["24 hrs / No Show", "100%"],
    ], colWidths=[3.5 * inch, 3.2 * inch])

    cancel_table.setStyle(TableStyle([
        ("GRID", (0, 0), (-1, -1), 0.8, colors.grey),
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor(CREAM)),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
        ("TOPPADDING", (0, 0), (-1, -1), 10),
    ]))
    story.append(cancel_table)

    story.append(Spacer(1, 70))
    story.append(Paragraph("*** Thank you for choosing Endless Xplorers ***", title))
    story.append(Spacer(1, 15))
    story.append(Paragraph(TAGLINE, title))

    doc.build(story)

# =========================
# CSS
# =========================
st.markdown(f"""
<style>
.stApp {{
    background: linear-gradient(135deg, #fffaf0, #eef9f7);
}}

[data-testid="stSidebar"] {{
    background: linear-gradient(180deg, {TEAL}, #021d1d);
}}

[data-testid="stSidebar"] * {{
    color: white !important;
}}

.hero {{
    background: linear-gradient(135deg, {TEAL}, #0b6666);
    color: white;
    padding: 34px;
    border-radius: 28px;
    box-shadow: 0 20px 45px rgba(0,0,0,0.18);
    border: 1px solid {GOLD};
}}

.hero h1 {{
    font-size: 54px;
    margin-bottom: 0;
}}

.gold {{
    color: {GOLD};
}}

.card {{
    background: rgba(255,255,255,0.95);
    border-radius: 24px;
    padding: 24px;
    box-shadow: 0 12px 30px rgba(0,0,0,0.10);
    border: 1px solid #e8d58a;
    margin-bottom: 22px;
}}

.package {{
    background: white;
    border-radius: 22px;
    padding: 20px;
    min-height: 165px;
    box-shadow: 0 10px 25px rgba(0,0,0,0.08);
    border-bottom: 5px solid {GOLD};
}}

.service {{
    background: linear-gradient(135deg, {TEAL}, #0b6666);
    color: white;
    border-radius: 20px;
    padding: 18px;
    min-height: 145px;
    text-align:center;
    border-bottom: 5px solid {GOLD};
}}

.section-title {{
    color: {TEAL};
    font-size: 34px;
    font-weight: 900;
    margin-top: 10px;
}}

.stButton button {{
    background: linear-gradient(135deg, {TEAL}, #0a7777);
    color: white;
    border: none;
    border-radius: 14px;
    font-weight: 800;
}}

.stDownloadButton button {{
    background: linear-gradient(135deg, {GOLD}, #f5d76e);
    color: #111;
    border: none;
    border-radius: 14px;
    font-weight: 800;
}}

.whatsapp {{
    display:inline-block;
    padding:14px 22px;
    background:#25D366;
    color:white !important;
    text-decoration:none;
    border-radius:14px;
    font-weight:900;
}}

.footer {{
    background:{TEAL};
    color:white;
    text-align:center;
    border-radius:26px;
    padding:28px;
    margin-top:25px;
}}
</style>
""", unsafe_allow_html=True)

# =========================
# SIDEBAR
# =========================
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

    st.success("Domestic • International • Educational • Corporate • Honeymoon • Pilgrimage")

# =========================
# MAIN TABS
# =========================
tabs = st.tabs([
    "🏠 Home",
    "🌍 Packages",
    "🧳 Itinerary Generator",
    "🛎 Services",
    "📘 Brochure Preview",
    "📞 Enquiry",
    "📊 Admin Leads"
])

# =========================
# HOME
# =========================
with tabs[0]:
    c1, c2 = st.columns([1.15, 1])

    with c1:
        st.markdown(f"""
        <div class="hero">
            <h1>Endless Xplorers</h1>
            <h2 class="gold">Explore Beyond Boundaries</h2>
            <p style="font-size:18px;">Premium travel packages for domestic, international, educational, corporate, honeymoon and pilgrimage tours.</p>
            <h3>{TAGLINE}</h3>
        </div>
        """, unsafe_allow_html=True)

        st.write("")
        m1, m2, m3 = st.columns(3)
        with m1:
            st.markdown("<div class='service'><h2>50+</h2><p>Destinations</p></div>", unsafe_allow_html=True)
        with m2:
            st.markdown("<div class='service'><h2>24/7</h2><p>Support</p></div>", unsafe_allow_html=True)
        with m3:
            st.markdown("<div class='service'><h2>100%</h2><p>Custom Plans</p></div>", unsafe_allow_html=True)

    with c2:
        if 1 in page_images:
            st.image(page_images[1], use_container_width=True)
        elif os.path.exists(LOGO_PATH):
            st.image(LOGO_PATH, use_container_width=True)

    st.markdown("<h2 class='section-title'>Why Choose Endless Xplorers?</h2>", unsafe_allow_html=True)

    cols = st.columns(4)
    why = [
        ("🎯", "Customized Packages", "Itineraries for your budget, group and travel style."),
        ("💎", "Premium Experience", "Quality stay, transport and trusted travel partners."),
        ("🛡️", "Safe & Secure", "Carefully planned travel with reliable support."),
        ("📞", "24/7 Support", "Assistance before, during and after your trip.")
    ]

    for col, item in zip(cols, why):
        with col:
            st.markdown(f"""
            <div class="package">
                <h2>{item[0]}</h2>
                <h3>{item[1]}</h3>
                <p>{item[2]}</p>
            </div>
            """, unsafe_allow_html=True)

# =========================
# PACKAGES
# =========================
with tabs[1]:
    st.markdown("<h2 class='section-title'>Package Collections</h2>", unsafe_allow_html=True)

    package_tabs = st.tabs(list(DESTINATIONS.keys()))

    for tab, category in zip(package_tabs, DESTINATIONS.keys()):
        with tab:
            page_no = BROCHURE_PAGES.get(category)
            if page_no in page_images:
                with st.expander(f"View {category} brochure preview", expanded=False):
                    st.image(page_images[page_no], use_container_width=True)

            names = list(DESTINATIONS[category].keys())

            for i in range(0, len(names), 4):
                cols = st.columns(4)
                for col, name in zip(cols, names[i:i+4]):
                    with col:
                        places = DESTINATIONS[category][name]
                        msg = f"Hi Endless Xplorers, I need details for {name} package."
                        st.markdown(f"""
                        <div class="package">
                            <h3>{name}</h3>
                            <p>{", ".join(places[:4])}</p>
                            <b class="gold">Custom package available</b>
                        </div>
                        """, unsafe_allow_html=True)
                        st.markdown(
                            f"<a class='whatsapp' href='{whatsapp_link(msg)}' target='_blank'>Enquire</a>",
                            unsafe_allow_html=True
                        )

# =========================
# ITINERARY GENERATOR
# =========================
with tabs[2]:
    st.markdown("<h2 class='section-title'>Premium Client Itinerary Generator</h2>", unsafe_allow_html=True)

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

    if st.button("📥 Generate Client Itinerary PDF", use_container_width=True):
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

    st.text_area("WhatsApp Message", whatsapp_msg, height=240)
    st.markdown(
        f"<a class='whatsapp' href='{whatsapp_link(whatsapp_msg)}' target='_blank'>📲 Send on WhatsApp</a>",
        unsafe_allow_html=True
    )

# =========================
# SERVICES
# =========================
with tabs[3]:
    st.markdown("<h2 class='section-title'>Our Travel Services</h2>", unsafe_allow_html=True)

    services = [
        ("✈️", "Flight Bookings", "Domestic and international flight booking support."),
        ("🏨", "Hotel Reservations", "Comfortable stays for every budget and preference."),
        ("🚌", "Transportation", "Buses, cars and private vehicle arrangements."),
        ("🛂", "Visa Assistance", "Guidance and documentation support."),
        ("🛡️", "Travel Insurance", "Protection for worry-free travel."),
        ("🎫", "Holiday Packages", "Carefully curated packages for all travellers."),
        ("📋", "Tour Planning", "Customized itinerary planning."),
        ("📞", "24/7 Support", "Assistance throughout your journey.")
    ]

    for i in range(0, len(services), 4):
        cols = st.columns(4)
        for col, s in zip(cols, services[i:i+4]):
            with col:
                st.markdown(f"""
                <div class="service">
                    <h1>{s[0]}</h1>
                    <h3>{s[1]}</h3>
                    <p>{s[2]}</p>
                </div>
                """, unsafe_allow_html=True)

# =========================
# BROCHURE PREVIEW
# =========================
with tabs[4]:
    st.markdown("<h2 class='section-title'>Brochure Preview</h2>", unsafe_allow_html=True)
    st.info("Only selected preview is shown here. Full brochure can be downloaded from the sidebar.")

    b1, b2 = st.columns([1, 1])

    with b1:
        selected = st.selectbox("Select preview section", list(BROCHURE_PAGES.keys()))
        selected_page = BROCHURE_PAGES[selected]

        if selected_page in page_images:
            st.image(page_images[selected_page], use_container_width=True)
        else:
            st.warning("Brochure preview not available.")

    with b2:
        st.markdown("""
        <div class="card">
            <h2>Endless Xplorers Brochure</h2>
            <p>Our brochure includes Domestic Tours, International Tours, Honeymoon Packages, Pilgrimage Tours, Educational Tours, Corporate Tours and Travel Services.</p>
            <p><b>Use this section only as preview. Download the full PDF for sharing.</b></p>
        </div>
        """, unsafe_allow_html=True)

        if os.path.exists(BROCHURE_PATH):
            with open(BROCHURE_PATH, "rb") as f:
                st.download_button(
                    "📘 Download Full Brochure",
                    f,
                    file_name="Endless_Xplorers_Brochure.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )

# =========================
# ENQUIRY
# =========================
with tabs[5]:
    st.markdown("<h2 class='section-title'>Customer Enquiry Form</h2>", unsafe_allow_html=True)

    e1, e2 = st.columns(2)

    with e1:
        name = st.text_input("Customer Name")
        mobile = st.text_input("Mobile Number")
        enq_category = st.selectbox("Interested Category", list(DESTINATIONS.keys()), key="enqcat")

    with e2:
        enq_destination = st.selectbox("Interested Destination", list(DESTINATIONS[enq_category].keys()), key="enqdest")
        enq_persons = st.number_input("Number of Persons", 1, 500, 2, key="enqpersons")
        travel_date = st.date_input("Expected Travel Date")

    note = st.text_area("Requirement / Notes", "Need customized travel package details.")

    if st.button("✅ Save Enquiry", use_container_width=True):
        if name and mobile:
            save_lead(name, mobile, enq_category, enq_destination, enq_persons, travel_date, note)
            st.success("Enquiry saved successfully.")

            msg = f"""
New Travel Enquiry - Endless Xplorers

Name: {name}
Mobile: {mobile}
Category: {enq_category}
Destination: {enq_destination}
Persons: {enq_persons}
Travel Date: {travel_date}
Requirement: {note}
"""
            st.markdown(
                f"<a class='whatsapp' href='{whatsapp_link(msg)}' target='_blank'>📲 Send to WhatsApp</a>",
                unsafe_allow_html=True
            )
        else:
            st.error("Please enter customer name and mobile number.")

    st.info(f"""
📞 {PHONE_DISPLAY}  
📧 {EMAIL}  
📸 {INSTAGRAM}  
📍 {ADDRESS}
""")

# =========================
# ADMIN LEADS
# =========================
with tabs[6]:
    st.markdown("<h2 class='section-title'>Admin Leads</h2>", unsafe_allow_html=True)

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

# =========================
# FOOTER
# =========================
st.markdown(f"""
<div class="footer">
    <h2>Endless Xplorers</h2>
    <p>{TAGLINE}</p>
    <p>{PHONE_DISPLAY} | {EMAIL} | {INSTAGRAM}</p>
    <p>{ADDRESS}</p>
</div>
""", unsafe_allow_html=True)
