import streamlit as st
import pandas as pd
import os
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch

st.set_page_config(page_title="Endless Xplorers", page_icon="🌍", layout="wide")

APP_FOLDER = os.path.dirname(os.path.abspath(__file__))
LOGO_PATH = os.path.join(APP_FOLDER, "LOGO.png")
BROCHURE_PATH = os.path.join(APP_FOLDER, "Endless Xplorer Final 1(1).pdf")
TEMPLATE_PATH = os.path.join(APP_FOLDER, "Sample of Package templete.pdf")

CONTACT = "+91 9894591780"
EMAIL = "endlessxplorerofficial@gmail.com"
INSTAGRAM = "@endlessxplorers_official"
ADDRESS = "21/1, Nanjappa Gounder Thottam Road, Telungupalayam, Coimbatore - 641039"

DESTINATIONS = {
    "Domestic": {
        "Munnar": [
            "Mattupetty Dam", "Echo Point", "Tea Museum", "Top Station",
            "Eravikulam National Park", "Kundala Lake"
        ],
        "Ooty": [
            "Botanical Garden", "Ooty Lake", "Doddabetta Peak",
            "Rose Garden", "Pykara Lake", "Pine Forest"
        ],
        "Coorg - Chikmagalur": [
            "Harangi Dam", "Golden Temple", "Kaveri Nisargadhama",
            "Mullayanagiri", "Baba Budangiri", "Z View Point"
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
            "Tirupati", "Rameswaram", "Madurai",
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

st.markdown("""
<style>
.stApp {background:linear-gradient(135deg,#f5fbfb,#fff8e5);}
[data-testid="stSidebar"] {background:linear-gradient(180deg,#002b2b,#005f5f);}
[data-testid="stSidebar"] * {color:white!important;}
.hero{background:linear-gradient(135deg,#003c3c,#00796b);padding:34px;border-radius:28px;color:white;box-shadow:0 15px 40px rgba(0,0,0,.2);}
.card{background:white;padding:25px;border-radius:24px;box-shadow:0 10px 30px rgba(0,80,80,.15);border:1px solid #d9eeee;}
.title{color:#003c3c;font-weight:800;}
.stButton button{background:linear-gradient(135deg,#006d6d,#00a884);color:white;font-weight:800;border-radius:15px;border:none;padding:12px;}
</style>
""", unsafe_allow_html=True)

def create_daywise_itinerary(destination, places, days, start_location, tour_category):
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
            idx = min(day + 1, len(places) - 1)
            plan = [
                "Breakfast",
                "Proceed to sightseeing",
                places[idx],
                "Explore nearby attractions",
                "Lunch",
                places[idx - 1],
                "Evening leisure / camp fire / cultural experience",
                "Dinner",
                "Night stay at hotel"
            ]
        itinerary.append((day, plan))
    return itinerary

def generate_pdf(output_path, college_name, client_name, plan_name, tour_category, destination,
                 days, start_location, persons, staff_count, accommodation, transport, food,
                 activities, places):
    doc = SimpleDocTemplate(output_path, pagesize=A4, rightMargin=45, leftMargin=45, topMargin=35, bottomMargin=35)
    styles = getSampleStyleSheet()

    normal = ParagraphStyle("normal", parent=styles["Normal"], fontSize=11, leading=16)
    small = ParagraphStyle("small", parent=styles["Normal"], fontSize=10, leading=14)
    heading = ParagraphStyle("heading", parent=styles["Heading2"], fontSize=15, leading=20)
    title = ParagraphStyle("title", parent=styles["Title"], fontSize=18, leading=24, alignment=1)

    story = []

    def header():
        if os.path.exists(LOGO_PATH):
            logo_html = f'<img src="{LOGO_PATH}" width="115" height="75"/>'
        else:
            logo_html = "ENDLESS XPLORERS"

        contact_html = f"☎ {CONTACT}<br/>✉ {EMAIL}<br/>📷 {INSTAGRAM}"

        story.append(Table([[Paragraph(logo_html, normal), Paragraph(contact_html, heading)]],
                           colWidths=[2.5 * inch, 4.5 * inch]))
        story.append(Spacer(1, 10))
        story.append(Table([[""]], colWidths=[7 * inch],
                           style=[("LINEBELOW", (0, 0), (-1, -1), 2, colors.black)]))
        story.append(Spacer(1, 25))

    header()

    story.append(Paragraph(
        "We are pleased to welcome you as a valuable customer of <b>Endless Xplorers</b>.<br/>"
        "We hope your tour with us will be a memorable one.",
        normal
    ))
    story.append(Spacer(1, 22))

    details = [
        ["College / Company Name:", college_name],
        ["Client Name:", client_name],
        ["Tour Category:", tour_category],
        ["Plan:", plan_name],
    ]

    story.append(Table(details, colWidths=[2.1 * inch, 4.4 * inch], style=[
        ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
        ("FONTNAME", (1, 0), (1, -1), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 12),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 12),
    ]))

    itinerary = create_daywise_itinerary(destination, places, days, start_location, tour_category)

    for day, plan in itinerary:
        story.append(Spacer(1, 15))
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

    table = Table(tariff_data, colWidths=[3 * inch, 3.8 * inch])
    table.setStyle(TableStyle([
        ("GRID", (0, 0), (-1, -1), .8, colors.grey),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("FONTNAME", (1, 0), (1, -1), "Helvetica-Bold"),
        ("TEXTCOLOR", (1, 0), (1, -1), colors.HexColor("#00a884")),
        ("FONTSIZE", (0, 0), (-1, -1), 11),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
        ("TOPPADDING", (0, 0), (-1, -1), 10),
    ]))
    story.append(table)

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
        "If the guest decides to cancel the tour for any reason, she/he shall give a written application "
        "to the company within the specified time limit along with the original receipt. Cancellation charges "
        "will be calculated on gross tour cost and depend on date of departure and date of cancellation.",
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
        ("GRID", (0, 0), (-1, -1), .8, colors.grey),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 11),
    ]))
    story.append(cancel_table)

    story.append(Spacer(1, 70))
    story.append(Paragraph("*** Thank you for choosing us Endless Xplorers. ***", title))
    story.append(Spacer(1, 15))
    story.append(Paragraph("Our services will be continue with you forever. ***", title))
    story.append(Spacer(1, 40))
    story.append(Paragraph("Thank you", ParagraphStyle(
        "thanks", parent=styles["Title"], fontSize=36,
        textColor=colors.HexColor("#7fb3c8"), alignment=1
    )))

    doc.build(story)

# Sidebar
if os.path.exists(LOGO_PATH):
    st.sidebar.image(LOGO_PATH, use_container_width=True)

st.sidebar.title("Endless Xplorers")
st.sidebar.write(CONTACT)
st.sidebar.write(EMAIL)
st.sidebar.write(INSTAGRAM)

if os.path.exists(BROCHURE_PATH):
    with open(BROCHURE_PATH, "rb") as f:
        st.sidebar.download_button("📘 Download Company Brochure", f, "Endless_Xplorers_Brochure.pdf", "application/pdf")

if os.path.exists(TEMPLATE_PATH):
    with open(TEMPLATE_PATH, "rb") as f:
        st.sidebar.download_button("📄 Download Sample Itinerary Template", f, "Sample_Package_Template.pdf", "application/pdf")

# Header
col1, col2 = st.columns([1, 4])
with col1:
    if os.path.exists(LOGO_PATH):
        st.image(LOGO_PATH, use_container_width=True)
    else:
        st.warning("Add LOGO.png")
with col2:
    st.markdown("""
    <div class="hero">
        <h1>Endless Xplorers</h1>
        <h3>AI-Powered Smart Travel Planner</h3>
        <p>Domestic • International • Honeymoon • Educational • Corporate • Pilgrimage Tours</p>
        <p>Explore Beyond Boundaries • Creating Memories Together</p>
    </div>
    """, unsafe_allow_html=True)

st.write("")

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
    accommodation = st.text_input("Accommodation Mode", "04 Sharing basis (Non A/c)")

transport = st.text_input("Transport", "54 Seater")
food = st.text_input("Food", "Breakfast, Lunch and Dinner as per package")
activities = st.text_input("Additional Activities", "Entry Tickets, Jeep, DJ / Camp Fire")

places = DESTINATIONS[tour_category][destination_name]
plan_name = f"{destination_name} - {tour_category} Package"

st.markdown("### 🗓 Day-wise Preview")
preview = create_daywise_itinerary(destination_name, places, days, start_location, tour_category)

for day, plan in preview:
    st.markdown(f"#### Day {day}")
    for item in plan:
        st.write("•", item)

if st.button("📥 Generate Client Itinerary PDF", use_container_width=True):
    output_pdf = os.path.join(APP_FOLDER, f"{destination_name}_Itinerary.pdf")

    generate_pdf(
        output_pdf, college_name, client_name, plan_name, tour_category,
        destination_name, days, start_location, persons, staff_count,
        accommodation, transport, food, activities, places
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

st.write("")

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
📸 Instagram: {INSTAGRAM}

✨ Explore Beyond Boundaries
✨ Creating Memories Together
"""

st.text_area("Copy WhatsApp Message", promo, height=260)
st.markdown("</div>", unsafe_allow_html=True)

st.markdown("""
<br>
<center>
<b>Endless Xplorers © 2026</b><br>
Explore Beyond Boundaries | Creating Memories Together
</center>
""", unsafe_allow_html=True)
