import streamlit as st
import pandas as pd
import os
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak
)
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch

st.set_page_config(
    page_title="Endless Xplorers AI Travel Planner",
    page_icon="🌍",
    layout="wide"
)

APP_FOLDER = os.path.dirname(os.path.abspath(__file__))

LOGO_PATH = os.path.join(APP_FOLDER, "LOGO.png")
BROCHURE_PATH = os.path.join(APP_FOLDER, "Endless Xplorer Final 1(1).pdf")

CONTACT = "+91 9894591780"
EMAIL = "endlessxplorerofficial@gmail.com"
INSTAGRAM = "@endlessxplorers_official"

DESTINATIONS = [
    {
        "name": "Munnar",
        "budget": 4500,
        "places": ["Mattupetty Dam", "Echo Point", "Tea Museum", "Top Station", "Eravikulam National Park"]
    },
    {
        "name": "Ooty",
        "budget": 4000,
        "places": ["Botanical Garden", "Ooty Lake", "Doddabetta Peak", "Rose Garden", "Pykara Lake"]
    },
    {
        "name": "Kodaikanal",
        "budget": 4200,
        "places": ["Kodai Lake", "Coaker's Walk", "Pillar Rocks", "Bryant Park", "Guna Caves"]
    },
    {
        "name": "Goa",
        "budget": 9000,
        "places": ["Baga Beach", "Calangute Beach", "Fort Aguada", "Dudhsagar Falls", "Cruise Ride"]
    },
    {
        "name": "Kerala",
        "budget": 8500,
        "places": ["Munnar", "Thekkady", "Alleppey", "Houseboat", "Kochi"]
    }
]

st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg,#f5fbfb,#fff8e5);
}
[data-testid="stSidebar"] {
    background: linear-gradient(180deg,#002b2b,#005f5f);
}
[data-testid="stSidebar"] * {
    color:white !important;
}
.hero {
    background: linear-gradient(135deg,#003c3c,#00796b);
    padding:32px;
    border-radius:28px;
    color:white;
    box-shadow:0 15px 40px rgba(0,0,0,0.20);
}
.card {
    background:white;
    padding:25px;
    border-radius:24px;
    box-shadow:0 10px 30px rgba(0,80,80,0.15);
    border:1px solid #d9eeee;
}
.title {
    color:#003c3c;
    font-weight:800;
}
.stButton button {
    background:linear-gradient(135deg,#006d6d,#00a884);
    color:white;
    font-weight:800;
    border-radius:15px;
    border:none;
    padding:12px;
}
</style>
""", unsafe_allow_html=True)

def generate_itinerary(destination, days, start_location):
    places = destination["places"]
    itinerary = []

    for day in range(1, days + 1):
        if day == 1:
            plan = [
                f"Departure from {start_location}",
                f"Arrival at {destination['name']}",
                "Check In Hotel",
                "Breakfast",
                "Proceed to Sightseeings",
                places[0],
                places[1] if len(places) > 1 else places[0],
                "Lunch",
                places[2] if len(places) > 2 else places[0],
                places[3] if len(places) > 3 else places[0],
                "Dinner",
                "Night stay at hotel"
            ]
        elif day == days:
            plan = [
                f"Departure from {destination['name']}",
                "Breakfast",
                "Proceed to Sightseeings",
                places[-2] if len(places) > 2 else places[0],
                places[-1],
                "Lunch",
                "Shopping / Photography",
                "Dinner",
                f"Return back to {start_location}"
            ]
        else:
            plan = [
                "Breakfast",
                "Proceed to Sightseeings",
                places[min(day, len(places)-1)],
                "Explore nearby attractions",
                "Lunch",
                "Evening leisure / Camp fire",
                "Dinner",
                "Night stay at hotel"
            ]

        itinerary.append((day, plan))

    return itinerary

def build_package_pdf(
    file_path,
    college_name,
    client_name,
    plan_name,
    destination,
    days,
    start_location,
    persons,
    staff_count,
    accommodation,
    transport,
    food,
    package_cost,
    activities
):
    doc = SimpleDocTemplate(
        file_path,
        pagesize=A4,
        rightMargin=45,
        leftMargin=45,
        topMargin=35,
        bottomMargin=35
    )

    styles = getSampleStyleSheet()
    normal = ParagraphStyle("normal", parent=styles["Normal"], fontSize=11, leading=16)
    title = ParagraphStyle("title", parent=styles["Title"], fontSize=18, leading=24, alignment=1)
    heading = ParagraphStyle("heading", parent=styles["Heading2"], fontSize=15, leading=20)
    small = ParagraphStyle("small", parent=styles["Normal"], fontSize=10, leading=14)

    story = []

    def header():
        if os.path.exists(LOGO_PATH):
            story.append(Table([
                [f'<img src="{LOGO_PATH}" width="110" height="70"/>',
                 Paragraph(f"☎ {CONTACT}<br/>✉ {EMAIL}<br/>📷 {INSTAGRAM}", heading)]
            ], colWidths=[2.5*inch, 4.5*inch]))
        else:
            story.append(Paragraph("ENDLESS XPLORERS", title))
            story.append(Paragraph(f"{CONTACT}<br/>{EMAIL}<br/>{INSTAGRAM}", normal))

        story.append(Spacer(1, 12))
        story.append(Table([[""]], colWidths=[7*inch],
                           style=[("LINEBELOW", (0,0), (-1,-1), 2, colors.black)]))
        story.append(Spacer(1, 25))

    header()

    story.append(Paragraph(
        "We are pleased to welcome you as a valuable customer of <b>Endless Xplorers</b>.<br/>"
        "We hope your tour with us will be a memorable one.",
        normal
    ))
    story.append(Spacer(1, 22))

    details = [
        ["College Name:", college_name],
        ["Client Name:", client_name],
        ["Plan:", plan_name],
    ]

    story.append(Table(details, colWidths=[1.6*inch, 4.5*inch], style=[
        ("FONTNAME", (0,0), (0,-1), "Helvetica-Bold"),
        ("FONTNAME", (1,0), (1,-1), "Helvetica-Bold"),
        ("FONTSIZE", (0,0), (-1,-1), 12),
        ("BOTTOMPADDING", (0,0), (-1,-1), 12),
    ]))

    itinerary = generate_itinerary(destination, days, start_location)

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
        ["No. of Person", f"{persons} Students + {staff_count} Staff"],
        ["Accommodation Mode", accommodation],
        ["Transport", transport],
        ["Food", food],
        ["Package cost", f"Rs.{package_cost}/- Per Head"],
        ["Additional Activities", activities],
    ]

    tariff_table = Table(tariff_data, colWidths=[3*inch, 3.8*inch])
    tariff_table.setStyle(TableStyle([
        ("GRID", (0,0), (-1,-1), 0.8, colors.grey),
        ("BACKGROUND", (0,0), (-1,-1), colors.white),
        ("FONTNAME", (0,0), (0,-1), "Helvetica"),
        ("FONTNAME", (1,0), (1,-1), "Helvetica-Bold"),
        ("TEXTCOLOR", (1,0), (1,-1), colors.HexColor("#00a884")),
        ("ALIGN", (0,0), (-1,-1), "CENTER"),
        ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
        ("FONTSIZE", (0,0), (-1,-1), 11),
        ("BOTTOMPADDING", (0,0), (-1,-1), 10),
        ("TOPPADDING", (0,0), (-1,-1), 10),
    ]))
    story.append(tariff_table)

    story.append(Spacer(1, 25))
    story.append(Paragraph("<u>Package Inclusions:</u>", heading))
    inclusions = [
        "Accommodation in comfortable and convenient hotels.",
        "Entrance fees of sightseeing places as mentioned in the tariff chart.",
        "Tour Manager services from Day 1 meeting point till dropping point on last day.",
        "Breakfast, Lunch and Dinner as per the package food plan.",
        "Additional activities as mentioned in the tariff chart.",
        "Bus / Train / Flight tickets if included in the package.",
        "Toll, parking, fuel, driver bata and applicable taxes.",
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
    cancel_text = (
        "If the guest decides to cancel the tour for any reason, she/he shall give a written "
        "application to the company within the specified time limit along with the original receipt. "
        "Cancellation charges will be calculated on gross tour cost and depend on the date of departure "
        "and date of cancellation."
    )
    story.append(Paragraph(cancel_text, small))

    story.append(PageBreak())
    header()

    cancel_table = Table([
        ["No of days Prior to Departure", "% of Cancellation Charges"],
        ["10 Days Before", "25%"],
        ["5 Days Before", "50%"],
        ["2 Days Before", "75%"],
        ["24 hrs. / No Show", "100%"],
    ], colWidths=[3.5*inch, 3.2*inch])

    cancel_table.setStyle(TableStyle([
        ("GRID", (0,0), (-1,-1), 0.8, colors.grey),
        ("ALIGN", (0,0), (-1,-1), "CENTER"),
        ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),
        ("FONTSIZE", (0,0), (-1,-1), 11),
        ("BOTTOMPADDING", (0,0), (-1,-1), 8),
        ("TOPPADDING", (0,0), (-1,-1), 8),
    ]))

    story.append(cancel_table)
    story.append(Spacer(1, 70))
    story.append(Paragraph("*** Thank you for choosing us Endless Xplorers. ***", title))
    story.append(Spacer(1, 15))
    story.append(Paragraph("Our services will be continue with you forever. ***", title))
    story.append(Spacer(1, 40))
    story.append(Paragraph("Thank you", ParagraphStyle(
        "thanks",
        parent=styles["Title"],
        fontSize=36,
        textColor=colors.HexColor("#7fb3c8"),
        alignment=1
    )))

    doc.build(story)

def recommend_destination(destination_name):
    for d in DESTINATIONS:
        if d["name"] == destination_name:
            return d
    return DESTINATIONS[0]

# Sidebar
if os.path.exists(LOGO_PATH):
    st.sidebar.image(LOGO_PATH, use_container_width=True)

st.sidebar.title("Endless Xplorers")
st.sidebar.write(CONTACT)
st.sidebar.write(EMAIL)
st.sidebar.write(INSTAGRAM)

if os.path.exists(BROCHURE_PATH):
    with open(BROCHURE_PATH, "rb") as f:
        st.sidebar.download_button(
            "📘 Download Company Brochure",
            f,
            file_name="Endless_Xplorers_Brochure.pdf",
            mime="application/pdf"
        )

# Header
col1, col2 = st.columns([1, 4])

with col1:
    if os.path.exists(LOGO_PATH):
        st.image(LOGO_PATH, use_container_width=True)
    else:
        st.warning("Upload LOGO.png")

with col2:
    st.markdown("""
    <div class="hero">
        <h1>Endless Xplorers</h1>
        <h3>AI-Powered Smart Travel Planner</h3>
        <p>Explore Beyond Boundaries • Creating Memories Together</p>
    </div>
    """, unsafe_allow_html=True)

st.write("")

st.markdown("<div class='card'>", unsafe_allow_html=True)
st.markdown("<h2 class='title'>🧳 Client Package Generator</h2>", unsafe_allow_html=True)

c1, c2, c3 = st.columns(3)

with c1:
    college_name = st.text_input("College / Company Name", "SNMV")
    client_name = st.text_input("Client Name", "Praveen - IT")
    start_location = st.text_input("Starting Location", "Coimbatore")

with c2:
    destination_name = st.selectbox("Destination Plan", [d["name"] for d in DESTINATIONS])
    days = st.slider("No. of Days", 1, 7, 2)
    persons = st.number_input("No. of Students / Persons", 1, 500, 35)

with c3:
    staff_count = st.number_input("No. of Staff", 0, 50, 2)
    accommodation = st.text_input("Accommodation Mode", "04 Sharing basis (Non A/c)")
    transport = st.text_input("Transport", "54 Seater")

food = st.text_input("Food", "6 Times (4 Times Non-Veg)")
package_cost = st.text_input("Package Cost Per Head", "5950")
activities = st.text_input("Additional Activities", "Entry Tickets, Jeep, DJ")

selected = recommend_destination(destination_name)
plan_name = f"{destination_name} Package"

st.write("")
st.markdown("### Preview Itinerary")

itinerary = generate_itinerary(selected, days, start_location)

for day, plan in itinerary:
    st.markdown(f"#### Day {day}")
    for item in plan:
        st.write("•", item)

st.write("")

if st.button("📥 Generate & Download Client Package PDF", use_container_width=True):
    output_pdf = os.path.join(APP_FOLDER, f"{destination_name}_Client_Package.pdf")

    build_package_pdf(
        output_pdf,
        college_name,
        client_name,
        plan_name,
        selected,
        days,
        start_location,
        persons,
        staff_count,
        accommodation,
        transport,
        food,
        package_cost,
        activities
    )

    with open(output_pdf, "rb") as f:
        st.download_button(
            "✅ Download Package PDF",
            f,
            file_name=f"{destination_name}_Package.pdf",
            mime="application/pdf",
            use_container_width=True
        )

st.markdown("</div>", unsafe_allow_html=True)

st.write("")

st.markdown("<div class='card'>", unsafe_allow_html=True)
st.markdown("<h2 class='title'>📢 WhatsApp Promotion Message</h2>", unsafe_allow_html=True)

promo = f"""
🌍 Endless Xplorers

✨ {destination_name} Travel Package ✨

📍 From: {start_location}
👥 Persons: {persons} + {staff_count} Staff
🏨 Stay: {accommodation}
🚌 Transport: {transport}
🍽 Food: {food}
💰 Package Cost: Rs.{package_cost}/- Per Head

📞 Contact: {CONTACT}
📸 Instagram: {INSTAGRAM}

✨ Explore Beyond Boundaries
✨ Creating Memories Together
"""

st.text_area("Copy Message", promo, height=230)

st.markdown("</div>", unsafe_allow_html=True)

st.markdown("""
<br>
<center>
<b>Endless Xplorers © 2026</b><br>
Explore Beyond Boundaries | Creating Memories Together
</center>
""", unsafe_allow_html=True)
