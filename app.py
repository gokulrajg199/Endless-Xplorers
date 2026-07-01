import streamlit as st
import os
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Image
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
# FILE PATHS
# =========================
APP_FOLDER = os.path.dirname(os.path.abspath(__file__))

LOGO_PATH = os.path.join(APP_FOLDER, "LOGO.jpg")
BROCHURE_PATH = os.path.join(APP_FOLDER, "Endless Xplorer Final 1.pdf")

CONTACT = "+91 9894591780"
EMAIL = "endlessxplorerofficial@gmail.com"
INSTAGRAM = "@endlessxplorers_official"
TAGLINE = "Explore Beyond Boundaries • Creating Memories Together"

# =========================
# DESTINATIONS
# =========================
DESTINATIONS = {
    "Domestic": {
        "Munnar": [
            "Mattupetty Dam", "Echo Point", "Tea Museum",
            "Top Station", "Eravikulam National Park", "Kundala Lake"
        ],
        "Ooty": [
            "Botanical Garden", "Ooty Lake", "Doddabetta Peak",
            "Rose Garden", "Pykara Lake", "Pine Forest"
        ],
        "Kodaikanal": [
            "Kodai Lake", "Coaker's Walk", "Pillar Rocks",
            "Bryant Park", "Guna Caves", "Silver Cascade Falls"
        ],
        "Coorg - Chikmagalur": [
            "Golden Temple", "Kaveri Nisargadhama", "Dubare Elephant Camp",
            "Mullayanagiri", "Baba Budangiri", "Coffee Plantation"
        ],
        "Kerala": [
            "Munnar", "Thekkady", "Alleppey Houseboat",
            "Kochi", "Athirappilly Falls", "Varkala Beach"
        ],
        "Goa": [
            "Baga Beach", "Calangute Beach", "Fort Aguada",
            "Dudhsagar Falls", "Cruise Ride", "Anjuna Beach"
        ],
        "Kashmir": [
            "Srinagar", "Dal Lake", "Gulmarg",
            "Pahalgam", "Sonamarg", "Mughal Garden"
        ],
        "Rajasthan": [
            "Jaipur", "Udaipur", "Jodhpur",
            "Jaisalmer", "Amer Fort", "City Palace"
        ],
        "Pilgrimage Tour": [
            "Tirupati", "Madurai", "Rameswaram",
            "Kashi", "Ayodhya", "Haridwar"
        ]
    },
    "International": {
        "Dubai": [
            "Burj Khalifa", "Dubai Mall", "Desert Safari",
            "Dubai Marina", "Palm Jumeirah", "Global Village"
        ],
        "Singapore": [
            "Merlion Park", "Sentosa Island", "Universal Studios",
            "Gardens by the Bay", "Marina Bay Sands", "Singapore Flyer"
        ],
        "Malaysia": [
            "Kuala Lumpur", "Petronas Twin Towers", "Batu Caves",
            "Genting Highlands", "Putrajaya", "Langkawi"
        ],
        "Thailand": [
            "Bangkok", "Pattaya", "Coral Island",
            "Safari World", "Floating Market", "Tiger Park"
        ],
        "Bali": [
            "Ubud", "Tanah Lot Temple", "Kuta Beach",
            "Nusa Penida", "Uluwatu Temple", "Bali Swing"
        ],
        "Maldives": [
            "Male City", "Water Villa Stay", "Private Beach",
            "Sunset Cruise", "Snorkeling", "Island Hopping"
        ],
        "Paris - Switzerland": [
            "Eiffel Tower", "Louvre Museum", "Seine River Cruise",
            "Mount Titlis", "Lucerne", "Interlaken"
        ]
    }
}

# =========================
# CSS
# =========================
st.markdown("""
<style>
.stApp {
    background:#f7fbfb;
}

[data-testid="stSidebar"] {
    background:#003c3c;
}

[data-testid="stSidebar"] * {
    color:white !important;
}

.hero {
    background:white;
    padding:28px;
    border-radius:18px;
    border-left:7px solid #00897b;
    box-shadow:0 5px 20px rgba(0,0,0,0.08);
}

.hero h1 {
    color:#003c3c;
    margin-bottom:5px;
    font-size:42px;
}

.hero h3 {
    color:#00897b;
    margin-top:0;
}

.card {
    background:white;
    padding:22px;
    border-radius:18px;
    box-shadow:0 5px 18px rgba(0,0,0,0.08);
    border:1px solid #e3eeee;
    margin-bottom:20px;
}

.title {
    color:#003c3c;
    font-weight:700;
}

.stButton button {
    background:#00897b;
    color:white;
    border:none;
    border-radius:10px;
    font-weight:700;
    padding:10px 18px;
}

.stDownloadButton button {
    background:#f4b400;
    color:#111;
    border:none;
    border-radius:10px;
    font-weight:700;
}

.footer {
    text-align:center;
    color:#003c3c;
    padding:20px;
}
</style>
""", unsafe_allow_html=True)

# =========================
# ITINERARY FUNCTION
# =========================
def create_daywise_itinerary(destination, places, days, start_location):
    itinerary = []

    for day in range(1, days + 1):
        if day == 1:
            plan = [
                f"Departure from {start_location}",
                f"Arrival at {destination}",
                "Hotel check-in and refreshment",
                "Breakfast",
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
                "Shopping / photography",
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

# =========================
# PDF GENERATOR
# =========================
def generate_pdf(
    output_path,
    college_name,
    client_name,
    plan_name,
    tour_category,
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
):
    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        rightMargin=45,
        leftMargin=45,
        topMargin=35,
        bottomMargin=35
    )

    styles = getSampleStyleSheet()

    normal = ParagraphStyle(
        "normal",
        parent=styles["Normal"],
        fontSize=11,
        leading=16
    )

    small = ParagraphStyle(
        "small",
        parent=styles["Normal"],
        fontSize=10,
        leading=14
    )

    heading = ParagraphStyle(
        "heading",
        parent=styles["Heading2"],
        fontSize=15,
        leading=20,
        textColor=colors.HexColor("#003c3c")
    )

    title = ParagraphStyle(
        "title",
        parent=styles["Title"],
        fontSize=18,
        leading=24,
        alignment=1,
        textColor=colors.HexColor("#003c3c")
    )

    story = []

    def header():
        if os.path.exists(LOGO_PATH):
            logo = Image(LOGO_PATH, width=1.6 * inch, height=1.0 * inch)
        else:
            logo = Paragraph("<b>ENDLESS XPLORERS</b>", heading)

        contact = Paragraph(
            f"<b>Endless Xplorers</b><br/>"
            f"Contact: {CONTACT}<br/>"
            f"Email: {EMAIL}<br/>"
            f"Instagram: {INSTAGRAM}",
            small
        )

        header_table = Table(
            [[logo, contact]],
            colWidths=[2.2 * inch, 4.7 * inch]
        )

        header_table.setStyle(TableStyle([
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("ALIGN", (1, 0), (1, 0), "RIGHT"),
        ]))

        story.append(header_table)
        story.append(Spacer(1, 8))
        story.append(Table(
            [[""]],
            colWidths=[7 * inch],
            style=[("LINEBELOW", (0, 0), (-1, -1), 2, colors.black)]
        ))
        story.append(Spacer(1, 22))

    header()

    story.append(Paragraph(
        "We are pleased to welcome you as a valuable customer of "
        "<b>Endless Xplorers</b>.<br/>"
        "We hope your tour with us will be a memorable one.",
        normal
    ))

    story.append(Spacer(1, 22))

    details = [
        ["College / Company Name:", college_name],
        ["Client Name:", client_name],
        ["Tour Category:", tour_category],
        ["Plan:", plan_name],
        ["Destination:", destination],
        ["No. of Days:", str(days)]
    ]

    details_table = Table(details, colWidths=[2.2 * inch, 4.4 * inch])
    details_table.setStyle(TableStyle([
        ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
        ("FONTNAME", (1, 0), (1, -1), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 12),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
    ]))

    story.append(details_table)

    itinerary = create_daywise_itinerary(destination, places, days, start_location)

    for day, plan in itinerary:
        story.append(Spacer(1, 14))
        story.append(Paragraph(f"<b>Day {day} :</b>", heading))

        for item in plan:
            if item in ["Breakfast", "Lunch", "Dinner", "Night stay at hotel"]:
                story.append(Paragraph(f"<b>{item}</b>", normal))
            else:
                story.append(Paragraph(item, normal))

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
        ("TEXTCOLOR", (1, 0), (1, -1), colors.HexColor("#00897b")),
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
    story.append(Paragraph("<u>Note:</u>", heading))

    notes = [
        "Under unavoidable circumstances itineraries may be changed or reversed, however all inclusions in the itinerary will remain same.",
        "Tour manager will meet as per the above designated points. Kindly reconfirm details with our travel advisor one week prior to departure.",
        "Any delay due to natural calamities or vehicle mechanism complaints company will not be responsible for delay. Your safety will be ensured and resolved accordingly."
    ]

    for item in notes:
        story.append(Paragraph(f"• {item}", small))

    story.append(Spacer(1, 18))
    story.append(Paragraph("<u>Tour Payment by Guest:</u>", heading))

    payments = [
        "The guest will have to make 50% payment for confirming the services.",
        "The guest will have to make the full payment before tour departure.",
        "Any hike in visa fee / VFS fees or increase in government tax is not under the company's control. Such additional charges shall be paid by the guest."
    ]

    for item in payments:
        story.append(Paragraph(f"• {item}", small))

    story.append(Spacer(1, 18))
    story.append(Paragraph("<u>Cancellation Policy:</u>", heading))

    story.append(Paragraph(
        "If the guest decides to cancel the tour for any reason, she/he shall give a written "
        "application to the company within the specified time limit along with the original receipt. "
        "Cancellation charges will be calculated on gross tour cost and depend on date of departure "
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
        ("FONTSIZE", (0, 0), (-1, -1), 11),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 9),
        ("TOPPADDING", (0, 0), (-1, -1), 9),
    ]))

    story.append(cancel_table)

    story.append(Spacer(1, 70))
    story.append(Paragraph("*** Thank you for choosing Endless Xplorers. ***", title))
    story.append(Spacer(1, 15))
    story.append(Paragraph("Our services will continue with you forever. ***", title))
    story.append(Spacer(1, 40))
    story.append(Paragraph("Thank you", ParagraphStyle(
        "thanks",
        parent=styles["Title"],
        fontSize=36,
        textColor=colors.HexColor("#7fb3c8"),
        alignment=1
    )))

    doc.build(story)

# =========================
# SIDEBAR
# =========================
if os.path.exists(LOGO_PATH):
    st.sidebar.image(LOGO_PATH, width=180)
else:
    st.sidebar.warning("LOGO.jpg not found")

st.sidebar.title("Endless Xplorers")
st.sidebar.write(CONTACT)
st.sidebar.write(EMAIL)
st.sidebar.write(INSTAGRAM)

if os.path.exists(BROCHURE_PATH):
    with open(BROCHURE_PATH, "rb") as f:
        st.sidebar.download_button(
            "📘 Download Brochure",
            f,
            file_name="Endless_Xplorers_Brochure.pdf",
            mime="application/pdf"
        )
else:
    st.sidebar.warning("Brochure PDF not found")

# =========================
# HEADER
# =========================
col1, col2 = st.columns([1, 5])

with col1:
    if os.path.exists(LOGO_PATH):
        st.image(LOGO_PATH, width=180)

with col2:
    st.markdown(f"""
    <div class="hero">
        <h1>Endless Xplorers</h1>
        <h3>Smart Travel Package Generator</h3>
        <p>Domestic • International • Educational • Corporate • Family Tours</p>
        <p><b>{TAGLINE}</b></p>
    </div>
    """, unsafe_allow_html=True)

st.write("")

# =========================
# FORM
# =========================
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.markdown("<h2 class='title'>🧳 Client Itinerary Package Generator</h2>", unsafe_allow_html=True)

c1, c2, c3 = st.columns(3)

with c1:
    college_name = st.text_input("College / Company Name", "SNMV")
    client_name = st.text_input("Client Name", "Praveen - IT")
    start_location = st.text_input("Starting Location", "Coimbatore")

with c2:
    tour_category = st.selectbox("Tour Category", ["Domestic", "International"])
    destination_name = st.selectbox("Destination Plan", list(DESTINATIONS[tour_category].keys()))
    days = st.slider("No. of Days", 1, 10, 2)

with c3:
    persons = st.number_input("No. of Students / Persons", 1, 500, 35)
    staff_count = st.number_input("No. of Staff", 0, 50, 2)
    accommodation = st.text_input("Accommodation Mode", "04 Sharing basis")

transport = st.text_input("Transport", "54 Seater")
food = st.text_input("Food", "Breakfast, Lunch and Dinner as per package")
activities = st.text_input("Additional Activities", "Entry Tickets, Jeep, DJ / Camp Fire")

places = DESTINATIONS[tour_category][destination_name]
plan_name = f"{destination_name} - {tour_category} Package"

st.markdown("### 🗓 Day-wise Preview")

preview = create_daywise_itinerary(destination_name, places, days, start_location)

for day, plan in preview:
    st.markdown(f"#### Day {day}")
    for item in plan:
        st.write("•", item)

if st.button("📥 Generate Client Itinerary PDF", use_container_width=True):
    output_pdf = os.path.join(APP_FOLDER, f"{destination_name}_Itinerary.pdf")

    generate_pdf(
        output_pdf,
        college_name,
        client_name,
        plan_name,
        tour_category,
        destination_name,
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
            file_name=f"{destination_name}_Package.pdf",
            mime="application/pdf",
            use_container_width=True
        )

st.markdown("</div>", unsafe_allow_html=True)

# =========================
# WHATSAPP MESSAGE
# =========================
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.markdown("<h2 class='title'>📲 WhatsApp Message</h2>", unsafe_allow_html=True)

promo = f"""
🌍 Endless Xplorers

✨ {destination_name} {tour_category} Tour Package ✨

📍 From: {start_location}
👥 Persons: {persons} + {staff_count} Staff
🏨 Stay: {accommodation}
🚌 Transport: {transport}
🍽 Food: {food}
🎯 Activities: {activities}

Places Covered:
{", ".join(places)}

📞 Contact: {CONTACT}
📧 Email: {EMAIL}
📸 Instagram: {INSTAGRAM}

✨ Explore Beyond Boundaries
✨ Creating Memories Together
"""

st.text_area("Copy WhatsApp Message", promo, height=260)

st.markdown("</div>", unsafe_allow_html=True)

# =========================
# FOOTER
# =========================
st.markdown(f"""
<div class="footer">
    <b>Endless Xplorers © 2026</b><br>
    {TAGLINE}<br>
    {CONTACT} | {INSTAGRAM}
</div>
""", unsafe_allow_html=True)
