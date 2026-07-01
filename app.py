import os
import urllib.parse
from datetime import datetime
import streamlit as st
import pandas as pd
import fitz
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Image as RLImage

st.set_page_config(page_title="Endless Xplorers", page_icon="🌍", layout="wide", initial_sidebar_state="expanded")

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
TEAL, DARK, GOLD, CREAM = "#063B3B", "#021F1F", "#D4AF37", "#F7F1DD"

PACKAGES = {
    "South India": {
        "Munnar": {"badge":"Best Weekend Escape","days":2,"places":["Tea Gardens","Mattupetty Dam","Echo Point","Top Station","Eravikulam National Park","Kundala Lake"],"desc":"Hill station package with tea gardens, waterfalls, viewpoints and nature experiences."},
        "Ooty": {"badge":"Family Favourite","days":2,"places":["Botanical Garden","Ooty Lake","Doddabetta Peak","Rose Garden","Pykara Lake","Toy Train"],"desc":"Cool climate, gardens, lake, scenic viewpoints and relaxing family experiences."},
        "Alleppey": {"badge":"Houseboat Special","days":2,"places":["Houseboat Cruise","Backwaters","Vembanad Lake","Village Visit","Beach Visit"],"desc":"Premium Kerala backwater experience with houseboat, food and peaceful views."},
        "Coorg": {"badge":"Nature + Coffee","days":3,"places":["Coffee Plantation","Golden Temple","Dubare Elephant Camp","Abbey Falls","Raja Seat"],"desc":"Coffee estates, waterfalls, monastery, viewpoints and nature stay."},
        "Mysore": {"badge":"Heritage Trip","days":2,"places":["Mysore Palace","Chamundi Hills","Brindavan Garden","Zoo"],"desc":"Palace, heritage, gardens and cultural experience."},
        "Kanyakumari": {"badge":"Sunrise Point","days":2,"places":["Vivekananda Rock","Thiruvalluvar Statue","Sunrise Point","Beach Visit"],"desc":"Southern tip of India with sunrise, sea views and spiritual places."}
    },
    "North India": {
        "Kashmir": {"badge":"Paradise Package","days":5,"places":["Srinagar","Dal Lake","Shikara Ride","Gulmarg","Pahalgam","Sonamarg"],"desc":"Snow, valleys, houseboats, shikara rides and premium hill experience."},
        "Himachal Pradesh": {"badge":"Adventure Hills","days":5,"places":["Shimla","Manali","Solang Valley","Kullu","Rohtang Pass"],"desc":"Mountains, adventure activities, valleys and beautiful weather."},
        "Agra - Jaipur": {"badge":"Golden Triangle","days":4,"places":["Taj Mahal","Agra Fort","Amer Fort","Hawa Mahal","City Palace"],"desc":"Heritage, monuments, architecture, photography and culture."},
        "Varanasi - Ayodhya": {"badge":"Spiritual Tour","days":4,"places":["Kashi Vishwanath","Ganga Aarti","Sarnath","Ram Mandir","Sarayu Aarti"],"desc":"Sacred temples, ghats, rituals and spiritual experience."}
    },
    "International": {
        "Dubai": {"badge":"Luxury Escape","days":5,"places":["Burj Khalifa","Dubai Mall","Desert Safari","Dubai Marina","Palm Jumeirah"],"desc":"Shopping, city tour, desert safari and luxury attractions."},
        "Bali": {"badge":"Couple Special","days":5,"places":["Ubud","Tanah Lot Temple","Kuta Beach","Nusa Penida","Bali Swing"],"desc":"Beaches, temples, private villas, romantic views and activities."},
        "Maldives": {"badge":"Premium Honeymoon","days":4,"places":["Male City","Water Villa","Private Beach","Sunset Cruise","Snorkeling"],"desc":"Water villas, beaches, romantic dinner and island experience."},
        "Singapore": {"badge":"Family + Fun","days":5,"places":["Merlion Park","Sentosa Island","Universal Studios","Gardens by the Bay"],"desc":"Modern city, family attractions, theme parks and shopping."}
    },
    "Educational": {
        "Industrial Visit": {"badge":"College IV","days":2,"places":["Industry Visit","Expert Session","Process Study","Certificate Session","Sightseeing"],"desc":"Educational trip with industry exposure, learning and safe student travel."},
        "Science & Technology Tour": {"badge":"Learning Trip","days":2,"places":["Science Centre","Innovation Lab","Robotics Demo","Knowledge Session"],"desc":"Hands-on learning experience for school and college students."}
    },
    "Corporate": {
        "Corporate Offsite": {"badge":"Team Retreat","days":2,"places":["Resort Stay","Team Activities","Leadership Games","Networking Dinner"],"desc":"Team outing, conference, activities and premium corporate travel support."},
        "Conference Travel": {"badge":"Business Support","days":1,"places":["Venue Setup","Seminar Session","Travel Management","Lunch"],"desc":"Professional event, meeting and conference travel arrangements."}
    },
    "Honeymoon": {
        "Kerala Honeymoon": {"badge":"Romantic Kerala","days":4,"places":["Munnar Hills","Alleppey Houseboat","Candlelight Dinner","Spa"],"desc":"Romantic hills, houseboat, candlelight dinner and private experience."},
        "Bali Honeymoon": {"badge":"International Couple","days":5,"places":["Private Villa","Bali Swing","Temple Visit","Beach Dinner"],"desc":"Beautiful villas, beach dinner, temple visits and romantic activities."}
    },
    "Pilgrimage": {
        "Tirupati - Rameswaram": {"badge":"South Pilgrimage","days":3,"places":["Tirupati Darshan","Padmavathi Temple","Rameswaram Temple","Dhanushkodi"],"desc":"Temple darshan, spiritual travel and comfortable transportation."},
        "Char Dham Yatra": {"badge":"Divine Journey","days":10,"places":["Yamunotri","Gangotri","Kedarnath","Badrinath"],"desc":"Sacred Himalayan yatra with route planning and travel support."}
    }
}

BROCHURE_PAGES = {"Cover":1,"Why Choose Us":3,"South India":4,"North India":5,"International":6,"Educational":7,"Corporate":8,"Honeymoon":9,"Pilgrimage":10,"Travel Services":12,"Contact":13}

st.markdown(f"""
<style>
.stApp {{background: radial-gradient(circle at top left, rgba(212,175,55,.22), transparent 28%), radial-gradient(circle at top right, rgba(6,59,59,.18), transparent 28%), linear-gradient(135deg,#fffaf0,#eff9f6,#fff);}}
[data-testid="stSidebar"] {{background:linear-gradient(180deg,{TEAL},{DARK});}}
[data-testid="stSidebar"] * {{color:white!important;}}
.block-container {{padding-top:1.2rem;}}
.hero {{min-height:430px;background:linear-gradient(135deg,rgba(2,31,31,.95),rgba(6,59,59,.88)),url('https://images.unsplash.com/photo-1507525428034-b723cf961d3e?auto=format&fit=crop&w=1600&q=80');background-size:cover;background-position:center;border-radius:32px;padding:52px;color:white;box-shadow:0 28px 70px rgba(0,0,0,.24);border:1px solid {GOLD};}}
.hero h1 {{font-size:62px;font-weight:900;margin-bottom:0;letter-spacing:-1px;}}
.hero h2 {{color:{GOLD};font-size:30px;margin-top:8px;}}
.hero p {{font-size:18px;max-width:760px;line-height:1.7;}}
.hero-badge,.badge {{display:inline-block;padding:7px 12px;background:{TEAL};color:white;border-radius:99px;font-size:12px;font-weight:800;margin-bottom:8px;}}
.hero-badge {{background:rgba(212,175,55,.18);color:{GOLD};border:1px solid {GOLD};font-size:14px;}}
.title {{color:{TEAL};font-size:36px;font-weight:900;margin-top:24px;margin-bottom:14px;}}
.sub {{color:#365c5c;font-size:17px;}}
.card,.package-card,.metric-card,.review {{background:rgba(255,255,255,.96);border-radius:24px;padding:22px;border:1px solid rgba(212,175,55,.52);box-shadow:0 16px 35px rgba(0,0,0,.10);margin-bottom:18px;}}
.package-card {{border-bottom:6px solid {GOLD};min-height:260px;background:linear-gradient(180deg,#fff,#fffaf0);}}
.package-card h3 {{color:{TEAL};font-weight:900;}}
.gold {{color:{GOLD};font-weight:900;}}
.service-card {{background:linear-gradient(135deg,{TEAL},#087474);color:white;border-radius:22px;padding:22px;min-height:170px;text-align:center;border-bottom:6px solid {GOLD};box-shadow:0 16px 35px rgba(0,0,0,.16);margin-bottom:18px;}}
.metric-card {{text-align:center;}}
.metric-card h1 {{color:{TEAL};font-weight:900;margin-bottom:0;}}
.review {{border-left:7px solid {GOLD};min-height:180px;}}
.whatsapp,.goldbtn {{display:inline-block;color:white!important;padding:12px 18px;border-radius:14px;font-weight:900;text-decoration:none!important;margin-top:8px;}}
.whatsapp {{background:#25D366;}}
.goldbtn {{background:linear-gradient(135deg,{GOLD},#f5d76e);color:#111!important;}}
.footer {{background:linear-gradient(135deg,{TEAL},{DARK});color:white;text-align:center;padding:30px;border-radius:28px;border:1px solid {GOLD};margin-top:32px;}}
.stButton button {{background:linear-gradient(135deg,{TEAL},#0a7777);color:white;border:none;border-radius:14px;font-weight:900;padding:.7rem 1rem;}}
.stDownloadButton button {{background:linear-gradient(135deg,{GOLD},#f5d76e);color:#111;border:none;border-radius:14px;font-weight:900;padding:.7rem 1rem;}}
@media(max-width:768px){{.hero{{padding:28px;min-height:360px;}}.hero h1{{font-size:40px;}}.hero h2{{font-size:23px;}}}}
</style>
""", unsafe_allow_html=True)

def wa_link(message):
    return f"https://wa.me/91{CONTACT}?text={urllib.parse.quote(message)}"

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
            pno = i + 1
            img_path = os.path.join(out_dir, f"page_{pno}.png")
            if not os.path.exists(img_path):
                pix = pdf[i].get_pixmap(matrix=fitz.Matrix(1.3, 1.3), alpha=False)
                pix.save(img_path)
            pages[pno] = img_path
    except Exception:
        return {}
    return pages

PAGE_IMAGES = extract_brochure_pages()

def get_package(category, destination):
    return PACKAGES[category][destination]

def auto_itinerary(destination, places, days, start_location):
    plan = []
    for day in range(1, days + 1):
        if day == 1:
            items = [f"Departure from {start_location}", f"Arrival at {destination}", "Hotel check-in and refreshment", places[0], places[1] if len(places)>1 else places[0], "Evening leisure / shopping / photography", "Dinner and overnight stay"]
        elif day == days:
            items = ["Breakfast at hotel", "Hotel check-out", places[-2] if len(places)>=2 else places[0], places[-1], "Lunch", f"Return journey to {start_location}", "Tour ends with beautiful memories"]
        else:
            idx = day % len(places)
            items = ["Breakfast at hotel", places[idx], places[(idx+1)%len(places)], "Lunch", places[(idx+2)%len(places)], "Campfire / group activity / leisure time", "Dinner and overnight stay"]
        plan.append((day, items))
    return plan

def save_lead(data):
    df_new = pd.DataFrame([data])
    if os.path.exists(LEADS_FILE):
        old = pd.read_csv(LEADS_FILE)
        df_new = pd.concat([old, df_new], ignore_index=True)
    df_new.to_csv(LEADS_FILE, index=False)

def generate_client_pdf(output_path, client_name, mobile, category, destination, start_location, days, persons, budget, stay, transport, food, activities, note):
    package = get_package(category, destination)
    places = package["places"]
    itinerary = auto_itinerary(destination, places, days, start_location)
    doc = SimpleDocTemplate(output_path, pagesize=A4, rightMargin=42, leftMargin=42, topMargin=32, bottomMargin=32)
    styles = getSampleStyleSheet()
    title = ParagraphStyle("TitleX", parent=styles["Title"], fontSize=20, textColor=colors.HexColor(TEAL), alignment=1, spaceAfter=16)
    h = ParagraphStyle("HeadingX", parent=styles["Heading2"], fontSize=14, textColor=colors.HexColor(TEAL), spaceBefore=12, spaceAfter=8)
    n = ParagraphStyle("NormalX", parent=styles["Normal"], fontSize=10.5, leading=15)
    small = ParagraphStyle("SmallX", parent=styles["Normal"], fontSize=9.5, leading=13)
    story = []
    def header():
        if os.path.exists(LOGO_PATH):
            img = RLImage(LOGO_PATH, width=1.25*inch, height=.85*inch)
        else:
            img = Paragraph(f"<b>{COMPANY}</b>", h)
        info = Paragraph(f"<b>{COMPANY}</b><br/>{PHONE}<br/>{EMAIL}<br/>{INSTAGRAM}", small)
        t = Table([[img, info]], colWidths=[2*inch, 4.8*inch])
        t.setStyle(TableStyle([("ALIGN",(1,0),(1,0),"RIGHT"),("VALIGN",(0,0),(-1,-1),"MIDDLE")]))
        story.append(t); story.append(Spacer(1,8))
        line = Table([[""]], colWidths=[6.8*inch]); line.setStyle(TableStyle([("LINEBELOW",(0,0),(-1,-1),2,colors.HexColor(GOLD))]))
        story.append(line); story.append(Spacer(1,14))
    header()
    story.append(Paragraph("Premium Travel Proposal", title))
    story.append(Paragraph(f"Dear <b>{client_name}</b>, thank you for choosing <b>{COMPANY}</b>. Here is your customized travel plan for <b>{destination}</b>.", n))
    details = [["Client Name",client_name],["Mobile",mobile],["Tour Category",category],["Destination",destination],["Starting Location",start_location],["No. of Days",str(days)],["No. of Persons",str(persons)],["Budget Range",budget],["Stay Type",stay],["Transport",transport],["Food Plan",food],["Activities",activities]]
    table = Table(details, colWidths=[2.35*inch,4.45*inch])
    table.setStyle(TableStyle([("GRID",(0,0),(-1,-1),.5,colors.lightgrey),("BACKGROUND",(0,0),(0,-1),colors.HexColor(CREAM)),("FONTNAME",(0,0),(0,-1),"Helvetica-Bold"),("TEXTCOLOR",(1,0),(1,-1),colors.HexColor(TEAL)),("BOTTOMPADDING",(0,0),(-1,-1),8),("TOPPADDING",(0,0),(-1,-1),8)]))
    story.append(Spacer(1,12)); story.append(table); story.append(Spacer(1,14)); story.append(Paragraph("Places Covered", h)); story.append(Paragraph(", ".join(places), n))
    for day, items in itinerary:
        story.append(Spacer(1,12)); story.append(Paragraph(f"Day {day}", h))
        for item in items: story.append(Paragraph(f"• {item}", n))
    story.append(PageBreak()); header()
    story.append(Paragraph("Package Inclusions", h))
    for item in ["Accommodation as per selected stay type.","Transport as per selected vehicle type.","Sightseeing places mentioned in the itinerary.","Tour coordination and travel support.","Food as per selected package plan.","Customized planning based on client requirement."]:
        story.append(Paragraph(f"• {item}", n))
    story.append(Paragraph("Package Exclusions", h))
    for item in ["Personal expenses such as laundry, tips, telephone charges and shopping.","Extra sightseeing or vehicle usage not mentioned in itinerary.","Entry tickets, adventure activities or permits unless specifically included.","Medical, emergency or personal expenses.","Any item not mentioned under inclusions."]:
        story.append(Paragraph(f"• {item}", n))
    story.append(Paragraph("Terms & Conditions", h))
    for item in ["50% advance payment is required to confirm the booking.","Balance payment should be completed before tour departure.","Rates may vary based on hotel availability, season, transport and group size.","Final confirmation will be shared after payment and booking availability check."]:
        story.append(Paragraph(f"• {item}", n))
    if note:
        story.append(Paragraph("Customer Notes", h)); story.append(Paragraph(note, n))
    story.append(Spacer(1,28)); story.append(Paragraph("*** Thank you for choosing Endless Xplorers ***", title)); story.append(Paragraph(TAGLINE, title))
    doc.build(story)

with st.sidebar:
    if os.path.exists(LOGO_PATH): st.image(LOGO_PATH, width=165)
    st.markdown(f"## {COMPANY}"); st.caption(TAGLINE); st.markdown(f"📞 **{PHONE}**"); st.markdown(f"📧 **{EMAIL}**"); st.markdown(f"📸 **{INSTAGRAM}**")
    st.divider()
    if os.path.exists(BROCHURE_PATH):
        with open(BROCHURE_PATH,"rb") as f: st.download_button("📘 Download Brochure", f, file_name="Endless_Xplorers_Brochure.pdf", mime="application/pdf", use_container_width=True)
    st.markdown(f"<a class='whatsapp' href='{wa_link('Hi Endless Xplorers, I need travel package details.')}' target='_blank'>📲 WhatsApp Now</a>", unsafe_allow_html=True)

tabs = st.tabs(["🏠 Home","🌍 Explore Packages","🧳 Package Builder","📄 Itinerary PDF","📘 Brochure","🛎 Services","⭐ Reviews","📞 Enquiry","📊 Admin"])

with tabs[0]:
    st.markdown(f"""<div class="hero"><div class="hero-badge">Premium Travel Company</div><h1>{COMPANY}</h1><h2>{TAGLINE}</h2><p>Plan domestic tours, international holidays, educational trips, corporate travel, honeymoon packages and pilgrimage journeys with a premium, safe and customized travel experience.</p><a class="whatsapp" href="{wa_link('Hi Endless Xplorers, I want to plan a trip.')}" target="_blank">📲 Plan Your Trip</a><a class="goldbtn" href="#packages">🌍 Explore Packages</a></div>""", unsafe_allow_html=True)
    st.markdown("<div class='title'>Travel Highlights</div>", unsafe_allow_html=True)
    for col, (a,b) in zip(st.columns(4), [("50+","Destinations"),("6","Tour Categories"),("24/7","Support"),("100%","Custom Plans")]):
        with col: st.markdown(f"<div class='metric-card'><h1>{a}</h1><p>{b}</p></div>", unsafe_allow_html=True)
    st.markdown("<div class='title'>Quick Package Search</div>", unsafe_allow_html=True)
    q1,q2,q3 = st.columns(3)
    with q1: quick_category = st.selectbox("Category", list(PACKAGES.keys()), key="quick_cat")
    with q2: quick_dest = st.selectbox("Destination", list(PACKAGES[quick_category].keys()), key="quick_dest")
    with q3: quick_people = st.number_input("Persons", 1, 500, 2, key="quick_people")
    p = get_package(quick_category, quick_dest)
    st.markdown(f"<div class='card'><h2>{quick_dest}</h2><span class='badge'>{p['badge']}</span><p>{p['desc']}</p><p><b>Places:</b> {', '.join(p['places'])}</p><p><b>Suggested Days:</b> {p['days']} days</p></div>", unsafe_allow_html=True)
    st.markdown(f"<a class='whatsapp' href='{wa_link(f'Hi Endless Xplorers, I need details for {quick_dest} package for {quick_people} persons.')}' target='_blank'>📲 Enquire This Package</a>", unsafe_allow_html=True)

with tabs[1]:
    st.markdown("<div id='packages' class='title'>Explore Packages</div><p class='sub'>Attractive package cards with WhatsApp enquiry and auto itinerary support.</p>", unsafe_allow_html=True)
    category_filter = st.selectbox("Choose Package Category", list(PACKAGES.keys()), key="explore_cat")
    names = list(PACKAGES[category_filter].keys())
    for i in range(0, len(names), 3):
        for col, name in zip(st.columns(3), names[i:i+3]):
            data = PACKAGES[category_filter][name]
            with col:
                st.markdown(f"<div class='package-card'><span class='badge'>{data['badge']}</span><h3>{name}</h3><p>{data['desc']}</p><p><b>Suggested:</b> {data['days']} days</p><p><b>Places:</b> {', '.join(data['places'][:4])}</p></div>", unsafe_allow_html=True)
                st.markdown(f"<a class='whatsapp' href='{wa_link(f'Hi Endless Xplorers, I need details for {name} - {category_filter} package.')}' target='_blank'>📲 WhatsApp Enquiry</a>", unsafe_allow_html=True)

with tabs[2]:
    st.markdown("<div class='title'>Custom Package Builder</div><p class='sub'>Build a quick customized package plan and send it directly through WhatsApp.</p>", unsafe_allow_html=True)
    b1,b2,b3 = st.columns(3)
    with b1:
        builder_name = st.text_input("Customer Name", key="builder_name"); builder_mobile = st.text_input("Mobile Number", key="builder_mobile"); builder_start = st.text_input("Starting Location", "Coimbatore", key="builder_start")
    with b2:
        builder_category = st.selectbox("Category", list(PACKAGES.keys()), key="builder_category"); builder_destination = st.selectbox("Destination", list(PACKAGES[builder_category].keys()), key="builder_dest"); builder_days = st.slider("Days", 1, 15, get_package(builder_category,builder_destination)["days"], key="builder_days")
    with b3:
        builder_persons = st.number_input("No. of Persons", 1, 500, 2, key="builder_persons"); builder_budget = st.selectbox("Budget Range", ["Budget","Standard","Premium","Luxury"], key="builder_budget"); builder_date = st.date_input("Travel Date", key="builder_date")
    pkg = get_package(builder_category, builder_destination)
    st.markdown("<div class='title'>Auto Day-wise Plan</div>", unsafe_allow_html=True)
    for day, items in auto_itinerary(builder_destination, pkg["places"], builder_days, builder_start):
        with st.expander(f"Day {day}", expanded=True):
            for item in items: st.write("•", item)
    builder_msg = f"""🌍 Endless Xplorers - Custom Package Enquiry\n\nName: {builder_name}\nMobile: {builder_mobile}\nFrom: {builder_start}\nCategory: {builder_category}\nDestination: {builder_destination}\nTravel Date: {builder_date}\nDays: {builder_days}\nPersons: {builder_persons}\nBudget: {builder_budget}\n\nPlaces Covered:\n{', '.join(pkg['places'])}\n\nPlease share package details."""
    st.text_area("WhatsApp Message Preview", builder_msg, height=220)
    st.markdown(f"<a class='whatsapp' href='{wa_link(builder_msg)}' target='_blank'>📲 Send Package Request</a>", unsafe_allow_html=True)

with tabs[3]:
    st.markdown("<div class='title'>Premium Itinerary PDF Generator</div>", unsafe_allow_html=True)
    p1,p2,p3 = st.columns(3)
    with p1:
        pdf_client = st.text_input("Client / Customer Name", "Customer Name", key="pdf_client"); pdf_mobile = st.text_input("Mobile", "9894591780", key="pdf_mobile"); pdf_start = st.text_input("Starting Location", "Coimbatore", key="pdf_start")
    with p2:
        pdf_category = st.selectbox("Tour Category", list(PACKAGES.keys()), key="pdf_category"); pdf_dest = st.selectbox("Destination", list(PACKAGES[pdf_category].keys()), key="pdf_dest"); pdf_days = st.slider("No. of Days", 1, 15, get_package(pdf_category,pdf_dest)["days"], key="pdf_days")
    with p3:
        pdf_persons = st.number_input("No. of Persons", 1, 500, 35, key="pdf_persons"); pdf_budget = st.selectbox("Budget Range", ["Budget","Standard","Premium","Luxury"], key="pdf_budget"); pdf_stay = st.selectbox("Stay Type", ["Standard Hotel","Premium Hotel","Resort","Villa","Houseboat","As per availability"], key="pdf_stay")
    pdf_transport = st.text_input("Transport", "AC Coach / Tempo Traveller / Cab as per group size", key="pdf_transport")
    pdf_food = st.text_input("Food Plan", "Breakfast, Lunch and Dinner as per package", key="pdf_food")
    pdf_activities = st.text_input("Activities", "Sightseeing, photography, leisure, campfire / DJ if applicable", key="pdf_activities")
    pdf_note = st.text_area("Special Notes", "Package can be customized based on hotel availability and customer requirement.", key="pdf_note")
    if st.button("📄 Generate Premium PDF", use_container_width=True):
        output_pdf = os.path.join(BASE_DIR, f"{pdf_dest.replace(' ','_')}_Premium_Itinerary.pdf")
        generate_client_pdf(output_pdf,pdf_client,pdf_mobile,pdf_category,pdf_dest,pdf_start,pdf_days,pdf_persons,pdf_budget,pdf_stay,pdf_transport,pdf_food,pdf_activities,pdf_note)
        with open(output_pdf,"rb") as f: st.download_button("✅ Download Premium Itinerary PDF", f, file_name=f"{pdf_dest}_Premium_Itinerary.pdf", mime="application/pdf", use_container_width=True)

with tabs[4]:
    st.markdown("<div class='title'>Brochure Preview</div>", unsafe_allow_html=True); st.info("Home page brochure front page is removed. Brochure is shown only here as selected preview.")
    c1,c2 = st.columns([1,1])
    with c1:
        section = st.selectbox("Select Brochure Section", list(BROCHURE_PAGES.keys())); pno = BROCHURE_PAGES[section]
        if pno in PAGE_IMAGES: st.image(PAGE_IMAGES[pno], use_container_width=True)
        else: st.warning("Brochure preview not available. Check PDF filename.")
    with c2:
        st.markdown(f"<div class='card'><h2>{COMPANY} Brochure</h2><p>This preview section keeps the website clean. The full brochure can be downloaded and shared with customers.</p><p><b>Available sections:</b> Domestic, International, Educational, Corporate, Honeymoon, Pilgrimage and Travel Services.</p></div>", unsafe_allow_html=True)
        if os.path.exists(BROCHURE_PATH):
            with open(BROCHURE_PATH,"rb") as f: st.download_button("📘 Download Full Brochure", f, file_name="Endless_Xplorers_Brochure.pdf", mime="application/pdf", use_container_width=True)

with tabs[5]:
    st.markdown("<div class='title'>Travel Services</div>", unsafe_allow_html=True)
    services = [("✈️","Flight Booking","Domestic and international ticket assistance."),("🏨","Hotel Reservation","Budget, premium, resort and villa stays."),("🚌","Transportation","Cars, vans, tempo travellers and buses."),("🛂","Visa Assistance","Document guidance for international travel."),("🎫","Holiday Packages","Customized packages for all travel types."),("🎓","Educational Trips","IV, industrial visits and student tours."),("🏢","Corporate Tours","Team outings, meetings and offsite plans."),("🛡️","Travel Insurance","Safe and worry-free travel support.")]
    for i in range(0,len(services),4):
        for col,s in zip(st.columns(4), services[i:i+4]):
            with col: st.markdown(f"<div class='service-card'><h2>{s[0]}</h2><h3>{s[1]}</h3><p>{s[2]}</p></div>", unsafe_allow_html=True)
    st.markdown("<div class='title'>Trust & Support</div>", unsafe_allow_html=True)
    for col,t in zip(st.columns(4), [("🛡️","Safe Travel","Planned routes and trusted vendors."),("💰","Best Price","Budget-friendly and premium options."),("📞","24/7 Support","Support throughout the journey."),("🎯","Custom Plans","Flexible plans for every customer.")]):
        with col: st.markdown(f"<div class='package-card'><h2>{t[0]}</h2><h3>{t[1]}</h3><p>{t[2]}</p></div>", unsafe_allow_html=True)

with tabs[6]:
    st.markdown("<div class='title'>Customer Reviews</div>", unsafe_allow_html=True)
    reviews = [("College IV Trip","Well organized transport, food and itinerary. Students enjoyed the trip safely."),("Family Kerala Tour","Good hotel selection and smooth travel plan. Very comfortable experience."),("Honeymoon Package","Beautiful stay and perfect planning. The package felt premium and memorable."),("Corporate Outing","Team activities and resort arrangements were excellent. Highly recommended.")]
    for col,(rt,rx) in zip(st.columns(4), reviews):
        with col: st.markdown(f"<div class='review'><h3>⭐ {rt}</h3><p>{rx}</p><b class='gold'>- Happy Customer</b></div>", unsafe_allow_html=True)

with tabs[7]:
    st.markdown("<div class='title'>Customer Enquiry</div>", unsafe_allow_html=True)
    e1,e2,e3 = st.columns(3)
    with e1:
        name = st.text_input("Name", key="lead_name"); mobile = st.text_input("Mobile Number", key="lead_mobile"); city = st.text_input("City / Starting Place", "Coimbatore", key="lead_city")
    with e2:
        lead_category = st.selectbox("Category", list(PACKAGES.keys()), key="lead_category"); lead_dest = st.selectbox("Destination", list(PACKAGES[lead_category].keys()), key="lead_dest"); lead_date = st.date_input("Expected Travel Date", key="lead_date")
    with e3:
        lead_persons = st.number_input("No. of Persons", 1, 500, 2, key="lead_persons"); lead_budget = st.selectbox("Budget", ["Budget","Standard","Premium","Luxury"], key="lead_budget"); lead_status = st.selectbox("Lead Status", ["New","Follow-up","Confirmed","Cancelled"], key="lead_status")
    note = st.text_area("Requirement / Notes", "Need customized package details.", key="lead_note")
    if st.button("✅ Save Customer Enquiry", use_container_width=True):
        if not name or not mobile: st.error("Please enter customer name and mobile number.")
        else:
            data = {"DateTime":datetime.now().strftime("%Y-%m-%d %H:%M:%S"),"Name":name,"Mobile":mobile,"City":city,"Category":lead_category,"Destination":lead_dest,"Travel Date":str(lead_date),"Persons":lead_persons,"Budget":lead_budget,"Status":lead_status,"Note":note}
            save_lead(data); st.success("Customer enquiry saved successfully.")
            msg = f"""New Travel Enquiry - Endless Xplorers\n\nName: {name}\nMobile: {mobile}\nCity: {city}\nCategory: {lead_category}\nDestination: {lead_dest}\nTravel Date: {lead_date}\nPersons: {lead_persons}\nBudget: {lead_budget}\nStatus: {lead_status}\nRequirement: {note}"""
            st.markdown(f"<a class='whatsapp' href='{wa_link(msg)}' target='_blank'>📲 Send to WhatsApp</a>", unsafe_allow_html=True)

with tabs[8]:
    st.markdown("<div class='title'>Admin Dashboard</div>", unsafe_allow_html=True)
    password = st.text_input("Admin Password", type="password")
    if password == ADMIN_PASSWORD:
        if os.path.exists(LEADS_FILE):
            df = pd.read_csv(LEADS_FILE)
            total = len(df); today_str = datetime.now().strftime("%Y-%m-%d")
            today_count = len(df[df["DateTime"].astype(str).str.startswith(today_str)]) if "DateTime" in df.columns else 0
            confirmed = len(df[df["Status"].astype(str).str.lower()=="confirmed"]) if "Status" in df.columns else 0
            for col,(a,b) in zip(st.columns(3), [(total,"Total Leads"),(today_count,"Today Leads"),(confirmed,"Confirmed")]):
                with col: st.markdown(f"<div class='metric-card'><h1>{a}</h1><p>{b}</p></div>", unsafe_allow_html=True)
            search = st.text_input("Search lead by name, mobile, category or destination")
            view = df.copy()
            if search:
                s = search.lower(); view = view[view.astype(str).apply(lambda row: row.str.lower().str.contains(s).any(), axis=1)]
            st.dataframe(view, use_container_width=True)
            csv = df.to_csv(index=False).encode("utf-8")
            st.download_button("⬇️ Download Leads CSV", csv, file_name="Endless_Xplorers_Leads.csv", mime="text/csv", use_container_width=True)
            with st.expander("Danger Zone"):
                st.warning("This will clear all saved enquiries.")
                if st.button("Clear All Leads"):
                    pd.DataFrame(columns=df.columns).to_csv(LEADS_FILE, index=False); st.success("All leads cleared. Refresh the page.")
        else: st.info("No leads saved yet.")
    elif password: st.error("Wrong password.")

st.markdown(f"<div class='footer'><h2>{COMPANY}</h2><p>{TAGLINE}</p><p>{PHONE} | {EMAIL} | {INSTAGRAM}</p><p>{ADDRESS}</p></div>", unsafe_allow_html=True)
