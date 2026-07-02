import os, urllib.parse
from datetime import datetime, date
import streamlit as st
import pandas as pd
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Image as RLImage

st.set_page_config(page_title='Endless Xplorers', page_icon='🌍', layout='wide', initial_sidebar_state='expanded')
BASE_DIR=os.path.dirname(os.path.abspath(__file__))
ASSET_DIR=os.path.join(BASE_DIR,'assets')
LOGO=os.path.join(ASSET_DIR,'logo_transparent.png')
LEADS_FILE=os.path.join(BASE_DIR,'customer_enquiries.csv')
ADMIN_PASSWORD='endlessxplorers'
COMPANY='Endless Xplorers'; CONTACT='9894591780'; PHONE='+91 9894591780'; EMAIL='endlessxplorerofficial@gmail.com'; INSTAGRAM='@endlessxplorers_official'
ADDRESS='21/1, Nanjappa Gounder Thottam Road, Telungupalayam, Coimbatore - 641039'
TAGLINE='Explore Beyond Boundaries • Creating Memories Together'
TEAL='#063B3B'; DARK='#021F1F'; GOLD='#D4AF37'; CREAM='#F7F1DD'
def img(name): return os.path.join(ASSET_DIR,name)
PACKAGES={
'South India':{'Munnar':{'image':'munnar.jpg','badge':'Popular','days':2,'base':4499,'desc':'Tea gardens, viewpoints, waterfalls and cool climate.','places':['Tea Gardens','Mattupetty Dam','Echo Point','Top Station','Eravikulam National Park']},'Ooty':{'image':'ooty.jpg','badge':'Family','days':2,'base':3999,'desc':'Gardens, lake, toy train and mountain views.','places':['Botanical Garden','Ooty Lake','Doddabetta Peak','Rose Garden','Pykara Lake']},'Alleppey':{'image':'alleppey.jpg','badge':'Houseboat','days':2,'base':5499,'desc':'Kerala backwaters and houseboat experience.','places':['Houseboat Cruise','Backwaters','Vembanad Lake','Village Visit','Beach Visit']},'Coorg':{'image':'coorg.jpg','badge':'Nature','days':3,'base':6499,'desc':'Coffee estates, waterfalls and peaceful stay.','places':['Coffee Plantation','Golden Temple','Dubare Elephant Camp','Abbey Falls','Raja Seat']}},
'North India':{'Kashmir':{'image':'kashmir.jpg','badge':'Paradise','days':5,'base':18999,'desc':'Snow, valleys, shikara ride and hill experience.','places':['Srinagar','Dal Lake','Shikara Ride','Gulmarg','Pahalgam','Sonamarg']},'Himachal':{'image':'himachal.jpg','badge':'Adventure','days':5,'base':15999,'desc':'Shimla, Manali, valleys and adventure activities.','places':['Shimla','Manali','Solang Valley','Kullu','Rohtang Pass']}},
'International':{'Dubai':{'image':'dubai.jpg','badge':'Luxury','days':5,'base':49999,'desc':'Burj Khalifa, desert safari, marina and shopping.','places':['Burj Khalifa','Dubai Mall','Desert Safari','Dubai Marina','Palm Jumeirah']},'Bali':{'image':'bali.jpg','badge':'Couple','days':5,'base':55999,'desc':'Beaches, temples, private villas and romantic views.','places':['Ubud','Tanah Lot Temple','Kuta Beach','Nusa Penida','Bali Swing']},'Maldives':{'image':'maldives.jpg','badge':'Honeymoon','days':4,'base':69999,'desc':'Water villas, private beach, cruise and snorkeling.','places':['Male City','Water Villa','Private Beach','Sunset Cruise','Snorkeling']},'Singapore':{'image':'singapore.jpg','badge':'Family Fun','days':5,'base':59999,'desc':'Sentosa, Universal Studios and city attractions.','places':['Merlion Park','Sentosa Island','Universal Studios','Gardens by the Bay']}},
'Educational':{'Industrial Visit':{'image':'educational.jpg','badge':'College IV','days':2,'base':1999,'desc':'Industry exposure, learning session and safe student travel.','places':['Industry Visit','Expert Session','Process Study','Certificate Session','Sightseeing']},'Science & Technology Tour':{'image':'educational.jpg','badge':'Learning','days':2,'base':2499,'desc':'Science centre, innovation lab and knowledge session.','places':['Science Centre','Innovation Lab','Robotics Demo','Knowledge Session']}},
'Corporate':{'Corporate Offsite':{'image':'corporate.jpg','badge':'Team Retreat','days':2,'base':4999,'desc':'Resort stay, team activities and networking dinner.','places':['Resort Stay','Team Activities','Leadership Games','Networking Dinner']}},
'Honeymoon':{'Kerala Honeymoon':{'image':'honeymoon.jpg','badge':'Romantic','days':4,'base':18999,'desc':'Munnar, houseboat, candlelight dinner and spa.','places':['Munnar Hills','Alleppey Houseboat','Candlelight Dinner','Spa']},'Bali Honeymoon':{'image':'bali.jpg','badge':'Premium','days':5,'base':59999,'desc':'Private villa, beach dinner and couple activities.','places':['Private Villa','Bali Swing','Temple Visit','Beach Dinner']}},
'Pilgrimage':{'Tirupati - Rameswaram':{'image':'pilgrimage.jpg','badge':'South Pilgrimage','days':3,'base':6999,'desc':'Temple darshan and comfortable pilgrimage travel.','places':['Tirupati Darshan','Padmavathi Temple','Rameswaram Temple','Dhanushkodi']},'Char Dham Yatra':{'image':'pilgrimage.jpg','badge':'Divine','days':10,'base':34999,'desc':'Yamunotri, Gangotri, Kedarnath and Badrinath.','places':['Yamunotri','Gangotri','Kedarnath','Badrinath']}}}
POPULAR=[('South India','Munnar'),('South India','Ooty'),('North India','Kashmir'),('International','Dubai'),('International','Bali'),('International','Maldives')]
GALLERY=['munnar.jpg','ooty.jpg','alleppey.jpg','coorg.jpg','kashmir.jpg','dubai.jpg','bali.jpg','maldives.jpg','singapore.jpg','pilgrimage.jpg','educational.jpg','corporate.jpg']
st.markdown(f"""
<style>
.stApp{{background:radial-gradient(circle at top left,rgba(212,175,55,.18),transparent 28%),radial-gradient(circle at top right,rgba(6,59,59,.18),transparent 28%),linear-gradient(135deg,#fffaf0,#eff9f6,#fff)}}
[data-testid='stSidebar']{{background:linear-gradient(180deg,{TEAL},{DARK})}} [data-testid='stSidebar'] *{{color:white!important}}
.block-container{{padding-top:1rem;max-width:1280px}} .hero{{min-height:500px;border-radius:34px;padding:52px;color:white;background:linear-gradient(135deg,rgba(2,31,31,.86),rgba(6,59,59,.46)),url('assets/hero.jpg');background-size:cover;background-position:center;box-shadow:0 30px 80px rgba(0,0,0,.25);border:1px solid {GOLD}}}
.hero h1{{font-size:66px;font-weight:900;margin:0;letter-spacing:-1px}} .hero h2{{color:{GOLD};font-size:30px}} .hero p{{font-size:18px;max-width:760px;line-height:1.7}}
.searchbar{{background:rgba(255,255,255,.94);border-radius:22px;padding:18px;border:1px solid rgba(212,175,55,.55);box-shadow:0 16px 40px rgba(0,0,0,.14);margin-top:28px}}
.title{{color:{TEAL};font-size:36px;font-weight:900;margin-top:26px;margin-bottom:14px}} .card,.metric,.review,.login-card{{background:rgba(255,255,255,.96);border-radius:24px;padding:22px;border:1px solid rgba(212,175,55,.52);box-shadow:0 16px 35px rgba(0,0,0,.10);margin-bottom:18px}}
.package{{background:white;border-radius:24px;overflow:hidden;border:1px solid rgba(212,175,55,.58);border-bottom:6px solid {GOLD};box-shadow:0 16px 35px rgba(0,0,0,.12);margin-bottom:20px}} .package img,.gallery img{{width:100%;height:220px;object-fit:cover;display:block}}
.package-body{{padding:20px;min-height:250px}} .package h3{{color:{TEAL};font-size:25px;font-weight:900;margin:6px 0}} .badge{{display:inline-block;padding:7px 12px;background:{TEAL};color:white;border-radius:99px;font-size:12px;font-weight:900;margin-bottom:8px}}
.gold{{color:{GOLD};font-weight:900}} .metric{{text-align:center}} .metric h1{{color:{TEAL};font-weight:900;margin:0}} .service{{background:linear-gradient(135deg,{TEAL},#087474);color:white;border-radius:22px;padding:22px;min-height:165px;text-align:center;border-bottom:6px solid {GOLD};box-shadow:0 16px 35px rgba(0,0,0,.16);margin-bottom:18px}}
.gallery{{background:white;border-radius:24px;overflow:hidden;border:1px solid rgba(212,175,55,.52);box-shadow:0 16px 35px rgba(0,0,0,.10);margin-bottom:18px}} .gallery h3{{padding:0 18px 18px 18px;color:{TEAL}}}
.whatsapp,.goldbtn{{display:inline-block;color:white!important;padding:12px 18px;border-radius:14px;font-weight:900;text-decoration:none!important;margin-top:8px}} .whatsapp{{background:#25D366}} .goldbtn{{background:linear-gradient(135deg,{GOLD},#f5d76e);color:#111!important}}
.social{{display:inline-block;margin:6px;padding:10px 14px;border-radius:14px;background:rgba(255,255,255,.12);color:white!important;text-decoration:none!important;font-weight:800}} .footer{{background:linear-gradient(135deg,{TEAL},{DARK});color:white;text-align:center;padding:24px;border-radius:28px;border:1px solid {GOLD};margin-top:30px}}
.floating-wa{{position:fixed;right:22px;bottom:22px;background:#25D366;color:white!important;border-radius:50px;padding:15px 18px;font-weight:900;text-decoration:none!important;box-shadow:0 12px 28px rgba(0,0,0,.25);z-index:9999}}
.stButton button{{background:linear-gradient(135deg,{TEAL},#0a7777);color:white;border:none;border-radius:14px;font-weight:900;padding:.7rem 1rem}} .stDownloadButton button{{background:linear-gradient(135deg,{GOLD},#f5d76e);color:#111;border:none;border-radius:14px;font-weight:900;padding:.7rem 1rem}}
@media(max-width:768px){{.hero{{padding:28px;min-height:420px;border-radius:22px}}.hero h1{{font-size:39px}}.hero h2{{font-size:22px}}.hero p{{font-size:15px}}.title{{font-size:28px}}.package img,.gallery img{{height:170px}}.package-body{{min-height:auto}}}}
</style>""",unsafe_allow_html=True)
def wa_link(msg): return f'https://wa.me/91{CONTACT}?text={urllib.parse.quote(msg)}'
def get_package(cat,dest): return PACKAGES[cat][dest]
def calc_budget(base,people,days,stay,transport):
    sf={'Budget':.9,'Standard':1.0,'Premium':1.35,'Luxury':1.8}[stay]; tf={'Cab':1.2,'Tempo Traveller':1.05,'Bus / Coach':.95,'Flight + Local Transport':1.75}[transport]
    total=int(base*people*max(days,1)/2*sf*tf); return total,int(total/max(people,1)),int(total*.5)
def itinerary(dest,places,days,start):
    out=[]
    for d in range(1,days+1):
        if d==1: items=[f'Departure from {start}',f'Arrival at {dest}','Hotel check-in and refreshment',places[0],places[1] if len(places)>1 else places[0],'Evening leisure / photography','Dinner and overnight stay']
        elif d==days: items=['Breakfast at hotel','Hotel check-out',places[-2] if len(places)>1 else places[0],places[-1],'Lunch',f'Return journey to {start}','Tour ends with memories']
        else:
            i=d%len(places); items=['Breakfast at hotel',places[i],places[(i+1)%len(places)],'Lunch',places[(i+2)%len(places)],'Leisure / group activity','Dinner and overnight stay']
        out.append((d,items))
    return out
def save_lead(data):
    df=pd.DataFrame([data])
    if os.path.exists(LEADS_FILE):
        old=pd.read_csv(LEADS_FILE)
        for c in df.columns:
            if c not in old.columns: old[c]=''
        for c in old.columns:
            if c not in df.columns: df[c]=''
        df=pd.concat([old,df[old.columns]],ignore_index=True)
    df.to_csv(LEADS_FILE,index=False)
def make_pdf(path,client,mobile,cat,dest,start,days,people,stay,transport,food,activities,budget_text,note):
    p=get_package(cat,dest); doc=SimpleDocTemplate(path,pagesize=A4,rightMargin=42,leftMargin=42,topMargin=32,bottomMargin=32); styles=getSampleStyleSheet(); title=ParagraphStyle('t',parent=styles['Title'],fontSize=20,textColor=colors.HexColor(TEAL),alignment=1); h=ParagraphStyle('h',parent=styles['Heading2'],fontSize=14,textColor=colors.HexColor(TEAL)); n=ParagraphStyle('n',parent=styles['Normal'],fontSize=10.5,leading=15); story=[]
    def header():
        logo=RLImage(LOGO,width=1.2*inch,height=1.2*inch) if os.path.exists(LOGO) else Paragraph(f'<b>{COMPANY}</b>',h); info=Paragraph(f'<b>{COMPANY}</b><br/>{PHONE}<br/>{EMAIL}<br/>{INSTAGRAM}',n); t=Table([[logo,info]],colWidths=[2*inch,4.8*inch]); t.setStyle(TableStyle([('ALIGN',(1,0),(1,0),'RIGHT'),('VALIGN',(0,0),(-1,-1),'MIDDLE')])); story.extend([t,Spacer(1,8)]); line=Table([['']],colWidths=[6.8*inch]); line.setStyle(TableStyle([('LINEBELOW',(0,0),(-1,-1),2,colors.HexColor(GOLD))])); story.extend([line,Spacer(1,14)])
    header(); story.extend([Paragraph('Premium Travel Proposal',title),Spacer(1,12),Paragraph(f'Dear <b>{client}</b>, here is your customized plan for <b>{dest}</b>.',n),Spacer(1,12)])
    rows=[['Client',client],['Mobile',mobile],['Category',cat],['Destination',dest],['Starting Location',start],['Days',str(days)],['Persons',str(people)],['Stay',stay],['Transport',transport],['Food',food],['Activities',activities],['Estimated Budget',budget_text]]; tbl=Table(rows,colWidths=[2.35*inch,4.45*inch]); tbl.setStyle(TableStyle([('GRID',(0,0),(-1,-1),.5,colors.lightgrey),('BACKGROUND',(0,0),(0,-1),colors.HexColor(CREAM)),('FONTNAME',(0,0),(0,-1),'Helvetica-Bold'),('BOTTOMPADDING',(0,0),(-1,-1),8),('TOPPADDING',(0,0),(-1,-1),8)])); story.extend([tbl,Spacer(1,14),Paragraph('Places Covered',h),Paragraph(', '.join(p['places']),n)])
    for day,items in itinerary(dest,p['places'],days,start):
        story.extend([Spacer(1,12),Paragraph(f'Day {day}',h)]); [story.append(Paragraph(f'• {item}',n)) for item in items]
    story.extend([PageBreak()]); header(); story.append(Paragraph('Package Inclusions',h)); [story.append(Paragraph(f'• {x}',n)) for x in ['Accommodation as per selected stay type.','Transport as per selected vehicle type.','Sightseeing places mentioned in itinerary.','Tour coordination and travel support.','Food as per selected package plan.']]
    story.append(Paragraph('Terms & Conditions',h)); [story.append(Paragraph(f'• {x}',n)) for x in ['50% advance payment is required to confirm booking.','Balance payment should be completed before departure.','Rates may vary based on availability, season and group size.','Cancellation charges may apply as per vendor policy.']]
    if note: story.extend([Paragraph('Special Notes',h),Paragraph(note,n)])
    story.extend([Spacer(1,24),Paragraph('*** Thank you for choosing Endless Xplorers ***',title),Paragraph(TAGLINE,title)]); doc.build(story)
with st.sidebar:
    if os.path.exists(LOGO): st.image(LOGO,width=170)
    st.markdown(f'## {COMPANY}'); st.caption(TAGLINE); st.markdown(f'📞 **{PHONE}**'); st.markdown(f'📧 **{EMAIL}**'); st.markdown(f'📸 **{INSTAGRAM}**'); st.divider()
    menu=st.radio('Navigation',['Home','Packages','Budget Calculator','Package Builder','Itinerary PDF','Gallery','Services','Reviews','Enquiry','Admin']); st.divider(); st.markdown(f"<a class='whatsapp' href='{wa_link('Hi Endless Xplorers, I need travel package details.')}' target='_blank'>📲 WhatsApp Now</a>",unsafe_allow_html=True)
if menu=='Home':
    st.markdown(f"<div class='hero'><span class='badge'>Premium Travel Company</span><h1>{COMPANY}</h1><h2>{TAGLINE}</h2><p>Plan domestic tours, international holidays, educational trips, corporate travel, honeymoon packages and pilgrimage journeys with a premium, safe and customized travel experience.</p><a class='whatsapp' href='{wa_link('Hi Endless Xplorers, I want to plan a trip.')}' target='_blank'>📲 Plan Your Trip</a><a class='goldbtn' href='#popular'>⭐ Popular Packages</a></div>",unsafe_allow_html=True)
    st.markdown("<div class='searchbar'>",unsafe_allow_html=True); c1,c2,c3,c4=st.columns([1.2,1.2,1,1])
    with c1: qcat=st.selectbox('Select Category',list(PACKAGES.keys()))
    with c2: qdest=st.selectbox('Select Destination',list(PACKAGES[qcat].keys()))
    with c3: qpeople=st.number_input('People',1,500,2)
    with c4: qdate=st.date_input('Start Date')
    st.markdown('</div>',unsafe_allow_html=True); msg=f'Hi Endless Xplorers, I need package for {qdest}, {qpeople} persons, travel date {qdate}.'; st.markdown(f"<a class='whatsapp' href='{wa_link(msg)}' target='_blank'>📲 Search / Enquire Package</a>",unsafe_allow_html=True)
    st.markdown("<div class='title'>Travel Highlights</div>",unsafe_allow_html=True)
    for col,(a,b) in zip(st.columns(4),[('50+','Destinations'),('1000+','Happy Travellers'),('24/7','Support'),('100%','Custom Plans')]):
        with col: st.markdown(f"<div class='metric'><h1>{a}</h1><p>{b}</p></div>",unsafe_allow_html=True)
    st.markdown("<div id='popular' class='title'>Popular Packages</div>",unsafe_allow_html=True)
    for i in range(0,len(POPULAR),3):
        cols=st.columns(3)
        for col,(cat,dest) in zip(cols,POPULAR[i:i+3]):
            p=get_package(cat,dest)
            with col:
                st.markdown("<div class='package'>",unsafe_allow_html=True); st.image(img(p['image']),use_container_width=True); st.markdown(f"<div class='package-body'><span class='badge'>{p['badge']}</span><h3>{dest}</h3><p>{p['desc']}</p><p><b>From:</b> ₹{p['base']:,} / person</p></div></div>",unsafe_allow_html=True); st.markdown(f"<a class='whatsapp' href='{wa_link(f'Hi Endless Xplorers, I need details for {dest} package.')}' target='_blank'>📲 Enquire</a>",unsafe_allow_html=True)
elif menu=='Packages':
    st.markdown("<div class='title'>Explore Packages</div>",unsafe_allow_html=True); cat=st.selectbox('Choose Category',list(PACKAGES.keys())); names=list(PACKAGES[cat].keys())
    for i in range(0,len(names),3):
        cols=st.columns(3)
        for col,dest in zip(cols,names[i:i+3]):
            p=get_package(cat,dest)
            with col:
                st.markdown("<div class='package'>",unsafe_allow_html=True); st.image(img(p['image']),use_container_width=True); st.markdown(f"<div class='package-body'><span class='badge'>{p['badge']}</span><h3>{dest}</h3><p>{p['desc']}</p><p><b>Suggested:</b> {p['days']} days</p><p><b>Places:</b> {', '.join(p['places'][:4])}</p><p><b>Starting from:</b> ₹{p['base']:,} / person</p></div></div>",unsafe_allow_html=True); st.markdown(f"<a class='whatsapp' href='{wa_link(f'Hi Endless Xplorers, I need details for {dest} package.')}' target='_blank'>📲 WhatsApp Enquiry</a>",unsafe_allow_html=True)
elif menu=='Budget Calculator':
    st.markdown("<div class='title'>Customer Budget Calculator</div>",unsafe_allow_html=True); c1,c2,c3=st.columns(3)
    with c1: cat=st.selectbox('Category',list(PACKAGES.keys()),key='bc1'); dest=st.selectbox('Destination',list(PACKAGES[cat].keys()),key='bc2'); days=st.slider('Days',1,15,get_package(cat,dest)['days'])
    with c2: people=st.number_input('Persons',1,500,2); stay=st.selectbox('Stay Type',['Budget','Standard','Premium','Luxury']); transport=st.selectbox('Transport',['Cab','Tempo Traveller','Bus / Coach','Flight + Local Transport'])
    with c3: food_extra=st.number_input('Extra Food / Person',0,5000,0); activity_extra=st.number_input('Extra Activities / Person',0,10000,0); discount=st.number_input('Discount',0,1000000,0)
    total,pp,adv=calc_budget(get_package(cat,dest)['base']+food_extra+activity_extra,people,days,stay,transport); total=max(total-discount,0); pp=int(total/max(people,1)); adv=int(total*.5)
    for col,(num,label) in zip(st.columns(3),[(f'₹{total:,}','Total Estimate'),(f'₹{pp:,}','Per Person'),(f'₹{adv:,}','50% Advance')]):
        with col: st.markdown(f"<div class='metric'><h1>{num}</h1><p>{label}</p></div>",unsafe_allow_html=True)
    msg=f'Hi Endless Xplorers, I need package details for {dest}. Days: {days}, Persons: {people}, Stay: {stay}, Transport: {transport}, Estimated: ₹{total:,}'; st.text_area('WhatsApp Budget Message',msg,height=160); st.markdown(f"<a class='whatsapp' href='{wa_link(msg)}' target='_blank'>📲 Send Budget</a>",unsafe_allow_html=True)
elif menu=='Package Builder':
    st.markdown("<div class='title'>Custom Package Builder</div>",unsafe_allow_html=True); c1,c2,c3=st.columns(3)
    with c1: customer=st.text_input('Customer Name'); mobile=st.text_input('Mobile'); start=st.text_input('Starting Location','Coimbatore')
    with c2: cat=st.selectbox('Category',list(PACKAGES.keys()),key='pb1'); dest=st.selectbox('Destination',list(PACKAGES[cat].keys()),key='pb2'); days=st.slider('Days',1,15,get_package(cat,dest)['days'],key='pb3')
    with c3: people=st.number_input('Persons',1,500,2,key='pb4'); budget=st.selectbox('Budget Type',['Budget','Standard','Premium','Luxury']); follow=st.date_input('Follow-up Date',date.today())
    p=get_package(cat,dest); st.image(img(p['image']),use_container_width=True)
    for d,items in itinerary(dest,p['places'],days,start):
        with st.expander(f'Day {d}',expanded=True):
            for item in items: st.write('•',item)
    msg=f"Endless Xplorers Package Request\nName: {customer}\nMobile: {mobile}\nFrom: {start}\nDestination: {dest}\nDays: {days}\nPersons: {people}\nBudget: {budget}\nFollow-up: {follow}\nPlaces: {', '.join(p['places'])}"; st.text_area('WhatsApp Message',msg,height=200); st.markdown(f"<a class='whatsapp' href='{wa_link(msg)}' target='_blank'>📲 Send Package Request</a>",unsafe_allow_html=True)
elif menu=='Itinerary PDF':
    st.markdown("<div class='title'>Premium Itinerary PDF Generator</div>",unsafe_allow_html=True); c1,c2,c3=st.columns(3)
    with c1: client=st.text_input('Client Name','Customer Name'); mobile=st.text_input('Mobile',CONTACT); start=st.text_input('Starting Location','Coimbatore')
    with c2: cat=st.selectbox('Category',list(PACKAGES.keys()),key='pdf1'); dest=st.selectbox('Destination',list(PACKAGES[cat].keys()),key='pdf2'); days=st.slider('Days',1,15,get_package(cat,dest)['days'],key='pdf3')
    with c3: people=st.number_input('Persons',1,500,35,key='pdf4'); stay=st.selectbox('Stay',['Budget','Standard','Premium','Luxury']); transport=st.selectbox('Transport',['Cab','Tempo Traveller','Bus / Coach','Flight + Local Transport'])
    food=st.text_input('Food Plan','Breakfast, Lunch and Dinner as per package'); activities=st.text_input('Activities','Sightseeing, photography, leisure and campfire if applicable'); note=st.text_area('Special Notes','Package can be customized based on customer requirement.'); total,pp,adv=calc_budget(get_package(cat,dest)['base'],people,days,stay,transport); budget_text=f'₹{total:,} total | ₹{pp:,} per person | ₹{adv:,} advance'; st.success(budget_text)
    if st.button('📄 Generate Premium PDF',use_container_width=True):
        out=os.path.join(BASE_DIR,f"{dest.replace(' ','_')}_Premium_Itinerary.pdf"); make_pdf(out,client,mobile,cat,dest,start,days,people,stay,transport,food,activities,budget_text,note)
        with open(out,'rb') as f: st.download_button('✅ Download Premium Itinerary PDF',f,file_name=f'{dest}_Premium_Itinerary.pdf',mime='application/pdf',use_container_width=True)
elif menu=='Gallery':
    st.markdown("<div class='title'>Destination Gallery</div>",unsafe_allow_html=True)
    for i in range(0,len(GALLERY),3):
        cols=st.columns(3)
        for col,g in zip(cols,GALLERY[i:i+3]):
            with col: st.markdown("<div class='gallery'>",unsafe_allow_html=True); st.image(img(g),use_container_width=True); st.markdown(f"<h3>{os.path.splitext(g)[0].replace('_',' ').title()}</h3></div>",unsafe_allow_html=True)
elif menu=='Services':
    st.markdown("<div class='title'>Travel Services</div>",unsafe_allow_html=True); services=[('✈️','Flight Booking','Domestic and international ticket support.'),('🏨','Hotel Reservation','Budget, premium, resort and villa stays.'),('🚌','Transportation','Cars, vans, tempo travellers and buses.'),('🛂','Visa Assistance','Document guidance for international travel.'),('🎫','Holiday Packages','Customized packages for all travel types.'),('🎓','Educational Trips','IV, industrial visits and student tours.'),('🏢','Corporate Tours','Team outings, meetings and offsite plans.'),('🛡️','Travel Insurance','Safe and worry-free travel support.')]
    for i in range(0,len(services),4):
        cols=st.columns(4)
        for col,s in zip(cols,services[i:i+4]):
            with col: st.markdown(f"<div class='service'><h2>{s[0]}</h2><h3>{s[1]}</h3><p>{s[2]}</p></div>",unsafe_allow_html=True)
elif menu=='Reviews':
    st.markdown("<div class='title'>Customer Reviews</div>",unsafe_allow_html=True); reviews=[('College IV Trip','Well organized transport, food and itinerary. Students enjoyed the trip safely.'),('Family Kerala Tour','Good hotel selection and smooth travel plan. Very comfortable experience.'),('Honeymoon Package','Beautiful stay and perfect planning. The package felt premium and memorable.'),('Corporate Outing','Team activities and resort arrangements were excellent. Highly recommended.')]
    for col,(rt,rx) in zip(st.columns(4),reviews):
        with col: st.markdown(f"<div class='review'><h3>⭐ {rt}</h3><p>{rx}</p><b class='gold'>- Happy Customer</b></div>",unsafe_allow_html=True)
elif menu=='Enquiry':
    st.markdown("<div class='title'>Customer Enquiry</div>",unsafe_allow_html=True); c1,c2,c3=st.columns(3)
    with c1: name=st.text_input('Name'); mobile=st.text_input('Mobile Number'); city=st.text_input('City / Starting Place','Coimbatore')
    with c2: cat=st.selectbox('Category',list(PACKAGES.keys()),key='lead1'); dest=st.selectbox('Destination',list(PACKAGES[cat].keys()),key='lead2'); travel_date=st.date_input('Expected Travel Date')
    with c3: people=st.number_input('Persons',1,500,2); budget=st.selectbox('Budget',['Budget','Standard','Premium','Luxury']); status=st.selectbox('Lead Status',['New','Follow-up','Confirmed','Cancelled'])
    follow=st.date_input('Follow-up Date',date.today()); note=st.text_area('Requirement / Notes','Need customized package details.'); total,pp,adv=calc_budget(get_package(cat,dest)['base'],people,get_package(cat,dest)['days'],budget,'Bus / Coach'); st.info(f'Estimated budget: ₹{total:,} total | ₹{pp:,} per person | Follow-up: {follow}')
    if st.button('✅ Save Customer Enquiry',use_container_width=True):
        if not name or not mobile: st.error('Please enter customer name and mobile number.')
        else:
            data={'DateTime':datetime.now().strftime('%Y-%m-%d %H:%M:%S'),'Name':name,'Mobile':mobile,'City':city,'Category':cat,'Destination':dest,'Travel Date':str(travel_date),'Follow-up Date':str(follow),'Persons':people,'Budget':budget,'Estimated Total':total,'Per Person':pp,'Advance':adv,'Status':status,'Note':note}; save_lead(data); st.success('Customer enquiry saved successfully.'); msg=f'New Travel Enquiry - Endless Xplorers\nName: {name}\nMobile: {mobile}\nCity: {city}\nDestination: {dest}\nTravel Date: {travel_date}\nFollow-up: {follow}\nPersons: {people}\nBudget: {budget}\nEstimated: ₹{total:,}\nStatus: {status}\nRequirement: {note}'; st.markdown(f"<a class='whatsapp' href='{wa_link(msg)}' target='_blank'>📲 Send to WhatsApp</a>",unsafe_allow_html=True)
elif menu=='Admin':
    st.markdown("<div class='title'>Admin Dashboard</div>",unsafe_allow_html=True); st.markdown("<div class='login-card'><h3>🔐 Secure Admin Access</h3><p>Enter password to manage enquiries, follow-ups and lead status.</p></div>",unsafe_allow_html=True); password=st.text_input('Admin Password',type='password')
    if password==ADMIN_PASSWORD:
        if os.path.exists(LEADS_FILE):
            df=pd.read_csv(LEADS_FILE)
            for col in ['DateTime','Name','Mobile','City','Category','Destination','Travel Date','Follow-up Date','Persons','Budget','Estimated Total','Per Person','Advance','Status','Note']:
                if col not in df.columns: df[col]=''
            today=datetime.now().strftime('%Y-%m-%d'); metrics=[(len(df),'Total Leads'),(len(df[df['DateTime'].astype(str).str.startswith(today)]),'Today'),(len(df[df['Status'].astype(str).str.lower()=='follow-up']),'Follow-up'),(len(df[df['Status'].astype(str).str.lower()=='confirmed']),'Confirmed')]
            for col,(n,l) in zip(st.columns(4),metrics):
                with col: st.markdown(f"<div class='metric'><h1>{n}</h1><p>{l}</p></div>",unsafe_allow_html=True)
            search=st.text_input('Search lead'); view=df.copy()
            if search: view=view[view.astype(str).apply(lambda r:r.str.lower().str.contains(search.lower()).any(),axis=1)]
            st.dataframe(view,use_container_width=True)
            if len(df)>0:
                st.markdown('### Update Lead Status'); options=[f"{i} - {r.get('Name','')} - {r.get('Destination','')} - {r.get('Mobile','')}" for i,r in df.iterrows()]; selected=st.selectbox('Select Lead',options); idx=int(selected.split(' - ')[0]); new_status=st.selectbox('New Status',['New','Follow-up','Confirmed','Cancelled']); new_follow=st.date_input('New Follow-up Date',date.today(),key='adminf'); admin_note=st.text_area('Admin Note','')
                if st.button('💾 Update Lead',use_container_width=True):
                    df.loc[idx,'Status']=new_status; df.loc[idx,'Follow-up Date']=str(new_follow)
                    if admin_note: df.loc[idx,'Note']=str(df.loc[idx,'Note'])+' | Admin: '+admin_note
                    df.to_csv(LEADS_FILE,index=False); st.success('Lead updated. Refresh page to view changes.')
                row=df.loc[idx]; msg=f"Hi {row.get('Name','')}, your enquiry for {row.get('Destination','')} package is noted. Please confirm your travel plan. Endless Xplorers {PHONE}"; st.markdown(f"<a class='whatsapp' href='{wa_link(msg)}' target='_blank'>📲 WhatsApp Selected Lead</a>",unsafe_allow_html=True)
            csv=df.to_csv(index=False).encode('utf-8'); st.download_button('⬇️ Download Leads CSV',csv,file_name='Endless_Xplorers_Leads.csv',mime='text/csv',use_container_width=True)
        else: st.info('No leads saved yet.')
    elif password: st.error('Wrong password.')
st.markdown(f"<a class='floating-wa' href='{wa_link('Hi Endless Xplorers, I need travel package details.')}' target='_blank'>💬 WhatsApp</a><div class='footer'><h2>{COMPANY}</h2><p>{TAGLINE}</p><p>{PHONE} | {EMAIL} | {INSTAGRAM}</p><a class='social' href='https://wa.me/91{CONTACT}' target='_blank'>WhatsApp</a><a class='social' href='https://www.instagram.com/endlessxplorers_official' target='_blank'>Instagram</a><a class='social' href='mailto:{EMAIL}'>Email</a><p>{ADDRESS}</p></div>",unsafe_allow_html=True)
