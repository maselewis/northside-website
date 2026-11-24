#!/usr/bin/env python3
"""Builds the Northside Engine Company static site into ../site/"""
import html, json, os, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "docs"
OUT.mkdir(exist_ok=True)

FB = "https://www.facebook.com/northsideenginecompany/"
IG = "https://www.instagram.com/northsideengineco4/"
EMAIL = "info@nsec4.org"
VENMO = "https://account.venmo.com/u/northsidefire"
ZEFFY = "https://www.zeffy.com/en-US/embed/donation-form/0aa583fd-22ea-407d-ae3f-dafd78c17bf9"

ABOUT_GROUP = [("about-us.html", "About Us"), ("history.html", "History"),
               ("officers--admin.html", "Officers & Admin"), ("fire-scene-images.html", "Fire Scene Images"),
               ("around-station-4.html", "Around Station 4"), ("northside-fire-apparatus.html", "Our Apparatus"),
               ("building-491.html", "Building 491"), ("491-wetdown.html", "491 Wetdown")]
JOIN_GROUP = [("join-northside.html", "Join Northside"), ("find-a-fd-to-join.html", "Find A Fire Department")]
RES_GROUP = [("dashboard.html", "Member Dashboard"), ("interesting-stuff.html", "Interesting Stuff")]

def img(path, alt="", cls=""):
    return f'<img src="images/{path}" alt="{html.escape(alt)}" loading="lazy"{f" class={cls!r}" if cls else ""}>'

def fig(path, cap=""):
    c = f"<figcaption>{cap}</figcaption>" if cap else ""
    return f'<figure class="figure">{img(path, cap or "Northside photo")}{c}</figure>'

def gallery(items):
    out = []
    for it in items:
        p, cap = (it if isinstance(it, tuple) else (it, ""))
        c = f"<figcaption>{html.escape(cap)}</figcaption>" if cap else ""
        out.append(f'<figure><a href="images/{p}" target="_blank" rel="noopener">{img(p, cap or "Northside photo")}</a>{c}</figure>')
    return '<div class="gallery">' + "".join(out) + "</div>"

def video(yt):
    return f'<div class="video"><iframe src="https://www.youtube.com/embed/{yt}" title="YouTube video" allowfullscreen loading="lazy"></iframe></div>'

def nav(cur):
    def sub(group):
        return '<ul class="sub">' + "".join(
            f'<li><a href="{h}"{" aria-current=page" if h == cur else ""}>{t}</a></li>' for h, t in group) + "</ul>"
    return f'''<header class="site-header"><div class="wrap">
<a class="brand" href="./"><span class="badge">4</span><span><b>Northside Engine Co. No. 4</b><small>Tinton Falls, NJ</small></span></a>
<button class="menu-toggle" aria-expanded="false" aria-controls="nav">Menu</button>
<ul class="nav" id="nav">
<li><a href="about-us.html">About</a>{sub(ABOUT_GROUP)}</li>
<li><a href="join-northside.html">Join</a>{sub(JOIN_GROUP)}</li>
<li><a href="dashboard.html">Resources</a>{sub(RES_GROUP)}</li>
<li><a href="contact-us.html"{" aria-current=page" if cur == "contact-us.html" else ""}>Contact</a></li>
<li><a class="btn btn-primary" href="donate.html">Donate</a></li>
</ul></div></header>'''

FOOTER = f'''<footer class="site-footer"><div class="wrap">
<div class="cols">
<div><h4>Northside Engine Company No. 4</h4><p>Volunteer firefighters serving the Borough of Tinton Falls since 1955.</p><p>35 Springdale Ave<br>Tinton Falls, NJ 07724</p></div>
<div><h4>Contact</h4><ul><li><a href="mailto:{EMAIL}">{EMAIL}</a></li><li><a href="tel:+17327413205">732.741.3205</a></li><li><a href="{FB}">Facebook</a></li><li><a href="{IG}">Instagram</a></li></ul></div>
<div><h4>Get Involved</h4><ul><li><a href="join-northside.html">Join Northside</a></li><li><a href="find-a-fd-to-join.html">Find a FD to Join</a></li><li><a href="donate.html">Donate</a></li></ul></div>
</div>
<div class="alert">For emergencies, always call 9-1-1</div>
<p class="legal">© <span id="yr">2026</span> Northside Engine Company No. 4 · A volunteer fire company</p>
</div></footer>
<script>
document.getElementById('yr').textContent=new Date().getFullYear();
const t=document.querySelector('.menu-toggle'),n=document.getElementById('nav');
t.addEventListener('click',()=>{{const o=n.classList.toggle('open');t.setAttribute('aria-expanded',o)}});
</script>'''

HEAD = '''<!doctype html>
<html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="icon" href="images/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=DM+Sans:opsz,wght@9..40,400;9..40,500;9..40,700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="styles.css?v=12">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="https://www.northsideenginecompany.org/images/background-images/1218312023.jpg">
<meta property="og:type" content="website">
<meta name="theme-color" content="#A63A2E">
</head><body><a class="skip" href="#main">Skip to content</a>'''

DESC = "Northside Engine Company No. 4 — volunteer firefighters serving Tinton Falls, NJ since 1955."

def page(fn, title, body, crumbs=None, group=None):
    side = ""
    if group:
        side = '<aside class="sidebar"><div class="box"><h3>In this section</h3><ul>' + "".join(
            f'<li><a href="{h}"{" aria-current=page" if h == fn else ""}>{t}</a></li>' for h, t in group) + "</ul></div></aside>"
    crumb = f'<div class="crumbs"><a href="./">Home</a> / {crumbs}</div>' if crumbs else ""
    doc = HEAD.format(title=f"{title} | Northside Engine Company No. 4", desc=DESC) + nav(fn)
    doc += f'<main id="main"><section class="page-head"><div class="wrap">{crumb}<h1>{title}</h1></div></section>'
    doc += f'<div class="wrap page-body"><article class="article">{body}</article>{side}</div></main>' + FOOTER + "</body></html>"
    (OUT / fn).write_text(doc)

# ---------------- HOME ----------------
cards = [("northside-fire-apparatus.html", "Our Apparatus", "Ladder 36-491, Engine 36-477, Brush 36-494 and Rescue 36-486.", "editor/491_2.jpeg"),
         ("history.html", "History", "Chartered February 28, 1955 by 21 founding members.", "published/6970060-orig.jpeg"),
         ("fire-scene-images.html", "Fire Scene Images", "Selected photos from Northside fire scenes.", "editor/ye2.jpeg"),
         ("around-station-4.html", "Around Station 4", "Drills, parades, Memorial Day and community events.", "editor/night.jpeg"),
         ("officers--admin.html", "Officers & Admin", "Our line and administrative officers.", "published/off.jpeg"),
         ("building-491.html", "Building 491", "How our 100-ft Seagrave ladder came together in 2009.", "5396125-orig.jpg")]
card_html = "".join(f'<a class="card" href="{h}">{img(i, t)}<div><h3>{t}</h3><p>{d}</p><span class="more">Learn more →</span></div></a>' for h, t, d, i in cards)
home = HEAD.format(title="Northside Engine Company No. 4 | Tinton Falls, NJ", desc=DESC) + nav("index.html") + f'''
<main id="main">
<section class="hero"><div class="wrap hero-grid">
<div>
<span class="chip">Volunteer fire company · Since 1955</span>
<h1>Your neighbors, ready when you call.</h1>
<p>Northside Engine Company No. 4 has protected Tinton Falls since 1955. We answer 300+ calls a year, any day, any hour.</p>
<div class="actions"><a class="btn btn-primary" href="join-northside.html">Join our team</a><a class="btn btn-outline" href="donate.html">Make a donation</a></div>
</div>
<div class="hero-photo">{img("background-images/1218312023.jpg", "Northside fire apparatus lined up outside Station 4")}</div>
</div></section>
<section class="stats"><div class="wrap">
<div><b>1955</b><span>Year chartered</span></div><div><b>300+</b><span>Calls each year</span></div>
<div><b>15 yrs</b><span>Average experience</span></div><div><b>100%</b><span>Volunteer</span></div>
</div></section>
<section class="section"><div class="wrap split">
<div><span class="eyebrow">Who we are</span><h2>Neighbors protecting neighbors.</h2>
<p class="lede">Northside Engine Company (NSEC) is one of the four Tinton Falls fire departments — and the youngest. Our members average 15 years of experience and train monthly to keep the borough safe. We are proud to serve our neighbors when they call.</p>
<a class="btn btn-outline" href="about-us.html">About Us</a></div>
<div class="rounded">{img("northside-766-shrews_orig.jpg", "Northside apparatus")}</div>
</div></section>
<section class="section white"><div class="wrap">
<h2>Get to know Northside</h2>
<div class="cards">{card_html}</div>
</div></section>
<section class="section"><div class="wrap"><div class="panel band">
<div><h2>Join Northside — no experience needed</h2>
<p class="lede">All training is included. 18+, valid NJ driver’s license, and 6 months’ residency in Tinton Falls or a neighboring town. Junior program for under 18.</p></div>
<a class="btn btn-light" href="join-northside.html">How to join</a>
</div></div></section>
<section class="section"><div class="wrap split">
<div><span class="eyebrow">Annual Fund Drive</span><h2>Support your volunteer firefighters.</h2>
<p class="lede">Donate securely online. Every dollar keeps our trucks and crews ready. Follow our latest news on <a href="{FB}">Facebook</a>.</p>
<a class="btn btn-primary" href="donate.html">More ways to give</a></div>
<div class="embed"><iframe src="{ZEFFY}" title="Donation form" loading="lazy" allowpaymentrequest></iframe></div>
</div></section>
</main>''' + FOOTER + "</body></html>"
(OUT / "index.html").write_text(home)

# ---------------- ABOUT ----------------
page("about-us.html", "About Northside", f'''
<p class="lede">Northside Engine Company (NSEC) is a group of volunteers from the community that has been a part of the Borough of Tinton Falls’ fire protection since 1955. Northside is one of the four Tinton Falls fire departments — and the youngest.</p>
<p>We respond to 300+ calls every year no matter the day or time. Our members have on average 15 years of experience, and attend monthly drills and annual training events to maintain the skills necessary to operate the equipment and protect the borough in the event of an emergency. We are all proud to be here, to serve our neighbors when they call.</p>
{fig("tintonlogo_orig.jpg")}
<h2>Around Northside</h2>
<div class="cards" style="grid-template-columns:repeat(2,1fr)">
<a class="card" href="history.html">{img("published/6970060-orig.jpeg","History")}<div><h3>History</h3></div></a>
<a class="card" href="officers--admin.html">{img("published/off.jpeg","Officers")}<div><h3>Officers & Admin</h3></div></a>
<a class="card" href="fire-scene-images.html">{img("editor/ye2.jpeg","Fire scenes")}<div><h3>Fire Scene Images</h3></div></a>
<a class="card" href="around-station-4.html">{img("editor/night.jpeg","Station 4")}<div><h3>Around Station 4</h3></div></a>
<a class="card" href="northside-fire-apparatus.html">{img("editor/491_2.jpeg","Ladder 491")}<div><h3>Our Trucks</h3></div></a>
</div>''', "About Us", ABOUT_GROUP)

charter = ["Leonard Dean", "Harrison Hubbard", "Russell Pendell", "William Metler", "William Cook Sr.", "Charles Utley", "David E. Smith",
           "George Watts", "Robert Vogel", "Walter Huhn", "Dominic Trocchia", "Robert L. Cook Sr.", "Frank Citarella", "Dan W. Blalock",
           "Eugene E. Kodadik", "Stephen P. Lusciano", "Julius Lanyi", "Arthur Jurman", "Frank Mazza", "William Stubbs", "Salvator Tola"]
page("history.html", "History", f'''
<h2>Northside at the Beginning</h2>
<p class="lede">Northside was chartered in New Shrewsbury on February 28, 1955.</p>
<h3>Charter members</h3>
<ul class="people">{"".join(f"<li>{n}</li>" for n in charter)}</ul>
<h2>Ex-Chiefs’ & Ex-Presidents’ Dinner</h2>
<p>Northside follows some traditions, including an annual dinner for ex-Chiefs and ex-Presidents. Here are some pictures from years past.</p>
{gallery(["1.jpg", "5.jpg"])}''', "About / History", ABOUT_GROUP)

def off(rows):
    return '<div class="officers">' + "".join(f"<div><span>{r}</span><b>{n}</b></div>" for r, n in rows) + "</div>"
page("officers--admin.html", "Officers & Admin", f'''
<h2>Line Officers</h2>
{off([("Chief","Zachary Neis"),("Assistant Chief","Ronald Neis"),("Captain","Cole Vandevelde"),("Chief Engineer","Mason Lewis"),("First Asst. Engineer","Emmanuel Roman"),("Second Asst. Engineer","Matteo Siano Jr."),("Third Asst. Engineer","Robert Gray")])}
<h2>Administration</h2>
{off([("President","Cooper Lewis"),("Vice President","Larry Neis"),("Treasurer","Mason Lewis"),("Secretary","Michael Lee")])}
<h3>Trustees</h3>
{off([("2021–2023","Larry Neis"),("2022–2024","Robert Gray"),("2023–2025","Matteo Siano Jr.")])}
{fig("off_1.jpg")}''', "About / Officers & Admin", ABOUT_GROUP)

page("fire-scene-images.html", "Fire Scene Images", f'''
<p class="lede">Selected images from Northside fire scenes.</p>
<h2>2017</h2>
<p>From <a href="http://www.nj.com/monmouth/index.ssf/2017/03/2-alarm_blaze_badly_damages_monmouth_county_house.html">NJ.com</a>: A two-alarm blaze badly damaged a Monmouth County house and drew fire companies from several towns to bring it under control. The fire in the two-story house on Shafto Road near Route 33 was reported around 4 p.m., and firefighters found the house fully engulfed on arrival. No injuries were reported; a backhoe helped demolish part of the structure to expose lingering hot spots.</p>
{fig("17264402-1451349631596343-7795168321000928384-n_2.jpg")}
<h2>2009</h2>
{gallery([("9802287.jpg","Memory Lanes: Northside provided mutual aid to Shrewsbury during the Memory Lanes bowling alley fire."),("2481082.jpg","Local basement fire.")])}
<h2>2006 & 2008</h2>
{gallery([("3613848-orig.jpg","2006"),("1106284-orig.jpg","2008")])}''', "About / Fire Scene Images", ABOUT_GROUP)

page("around-station-4.html", "Around Station 4", f'''
{fig("northside-766-shrews_orig.jpg")}
<h2>Tinton Falls Fire Departments Visit TF Solar</h2>
{fig("8463987.jpg")}
<p>Tinton Falls fire departments were given a tour of the solar site on Shafto Road. Tours of businesses and facilities in the borough help firefighters become familiar with sites in case of emergencies. For information on the solar project visit <a href="http://en.wikipedia.org/wiki/Tinton_Falls_Solar_Farm">Wikipedia</a>.</p>
<hr class="rule">
<h2>Memorial Day 2013</h2>
{fig("4982353.jpg")}
<p>Northside members — father and son Zach and Ron Neis — at the Memorial Day celebration and new location of the Tinton Falls Veterans Memorial at Sycamore Soccer Fields. Zach’s Eagle Scout project was to coordinate the move from the borough green to the new location.</p>
<hr class="rule">
<h2>2001</h2>
{fig("4205481.jpg")}
<p><strong>Kneeling, L–R:</strong> Kevin Kenney, Paul Nelson, Ron Neis, Scott Reed, Roy Latham<br><strong>Standing, L–R:</strong> Larry Neis, Tom Libbin, Mark Wood, Butch Neis, Dave Reed, Ed Breidenbach, Dan Tierney, Joe Corson</p>
<hr class="rule">
<h2>2009 Drill</h2>
{gallery([("4547270.jpg","477 in action"),("9558257.jpg","477 in action"),("3415284.jpg","490 — “Is that supposed to do that?”")])}
<hr class="rule">
<h2>Memorial Day 2009</h2>
{fig("5748725.jpg","1st Sgt Richardson and Ex-Chief Neis")}
<p>Ex-Chief Larry Neis took a moment at the 2009 Tinton Falls Memorial Day Service to thank First Sergeant Reginald Richardson for his service to our country. First Sgt Richardson serves in the Central Jersey Recruiting Company of Fort Monmouth.</p>
<hr class="rule">
<h2>196?</h2>
{gallery([("525982.jpg",""),("9548883.jpg","Name that intersection!")])}
<h2>Congrats to Ryan!</h2>
<p>Ryan completed his Firefighter training and graduated from Monmouth County Fire Academy on 8/11. He was subsequently officially soaked.</p>
<h2>Members Continue to Make an Impression</h2>
{fig("6165351.jpg")}
<p>Exemplary effort by member Greg in bringing his own tools to Northside drills. Unfortunately, the “little tyke” didn’t share well and needed a time out.</p>
<h2>Northside Weather Expert</h2>
{fig("3013919.jpg")}
<p>You’ve heard of Punxsutawney Phil? Well here is Northside’s own Fairweather Fred, sought by all the local news stations for his expert opinions during weather emergencies. Thank you, Fairweather Fred.</p>
<h2>Community Day Smoke Tent and Thermal Camera</h2>
<p>Northside participated in Tinton Falls Community Day in 2009, using our smoke tent to show residents how the thermal imaging camera allows us to see through smoke. The tent also shows how difficult it is to see in a smoky environment.</p>
{fig("5607143.jpg")}''', "About / Around Station 4", ABOUT_GROUP)

page("northside-fire-apparatus.html", "Our Apparatus", f'''
<p class="lede">Northside Engine Company runs several types of fire apparatus; each unit provides unique capabilities on the fire scene.</p>
<h3>Ladder 36-491</h3><p>A 2009 Seagrave 100' stick with a 500-gallon water tank, 2000 gpm pump and an 8-person cab. (Also see <a href="building-491.html">Building 491</a> and <a href="491-wetdown.html">491 Wetdown</a>.)</p>
<h3>Engine 36-477</h3><p>A 1994 Seagrave engine with a 750-gallon tank and 1500 gpm pump. It also has a 1500 gpm deck gun and a 10-person cab.</p>
<h3>Brush 36-494</h3><p>Our repurposed military 6x6 cargo truck (220 horsepower, 44,000 lb rear tandems, 20,000 lb front axle), now a brush truck for wooded areas within the borough and neighboring towns. It has protected seating in the cargo area, an 800-gallon water tank, an on-board pump and hose reel, and woodland fire suppression tools.</p>
<h3>Rescue 36-486</h3><p>An International/E-One with a cascade air tank resupply system, fire scene support material and a personnel rehabilitation area.</p>
{gallery(["7265418-orig.jpg","8471437-orig.jpg","5037580-orig.jpg","4216239-orig.jpg","5165697-orig.jpg","6961583-orig_1.jpg"])}
<h3>Santa Run</h3><p>Every year our members and trucks escort Santa around our response area, taking pictures and giving out candy canes.</p>
<h3>Holiday Parade</h3><p>491 visited Wallington, NJ — home of its sister truck — for their annual holiday parade.</p>
{gallery(["1919270-325138334276808-7554318691090785458-n.jpg","1_2.jpg"])}
<h3>Our previous ladder truck</h3><p>36-490, a 1989 Seagrave 75' ladder with a 300-gallon tank and 1500 gpm pump. Retired 2010.</p>
{fig("lad3.jpg","36-490")}
<h3>Historic equipment</h3><p>Our 1972 Ford Telesquirt was in service with Northside until 1993. It then served at the Meadowlands for a period.</p>
{fig("5609426.jpg","1972 Ford Telesquirt")}''', "About / Our Apparatus", ABOUT_GROUP)

page("building-491.html", "Building 491", f'''
<p class="lede">491 is our newest ladder apparatus: a Seagrave truck equipped with a 100-ft ladder, and usually our go-to apparatus. Here is how it came together in 2009.</p>
{gallery(["5396125-orig.jpg","9045097-orig.jpg"])}
<h2>May 2009</h2>{fig("1779760.jpg")}
<h2>June – July 2009</h2>
<p>Making very fast progress. Our ladder is mounted on an old fire truck and tested before it gets mounted on 491. Lots of shelf space. The back of the truck is now upright, and the body has been mounted. It’s been a very busy month when you compare the start of July to the end.</p>
{gallery(["4212413-orig.jpg","3994008-orig.jpg","5016775-orig.jpg","9934474-orig.jpg"])}
<h2>August</h2>
<p>Things are getting “put together.” Testing the ladder — notice the pictures are taken from a safe distance. Experience counts! Almost ready to roll.</p>
{gallery(["376205-orig.jpg","6514265-orig.jpg","4989111-orig.jpg"])}
<h2>September</h2>
{gallery(["1752465-orig.jpg","31421-orig.jpg","1918942-orig.jpg","156596-orig.jpg","1833024-orig.jpg","7496330-orig.jpg","9704151-orig.jpg","5414328-orig.jpg","7154795-orig.jpg"])}''', "About / Building 491", ABOUT_GROUP)

wet_attend = [("6671512-orig.jpg","Belford, Middletown Township"),("6514973-orig.jpg","36-491"),("4327732-orig.jpg","East Keansburg"),("7790379-orig.jpg","Fair Haven"),
 ("7713754-orig.jpg","Farmingdale"),("7755033-orig.jpg","Highland Park"),("4261599-orig.jpg","Holmdel"),("5633877-orig.jpg","Ocean FD"),("457060-orig.jpg","Tinton Falls Company No. 1"),
 ("388988-orig.jpg","US Forest Service"),("5764843-orig.jpg","Ramtown, Howell Township"),("9916792-orig.jpg","Sea Bright H&L"),("9933325-orig.jpg","Wallington, the model for 491"),
 ("6310257-orig.jpg","Jackson Mills"),("5524939-orig.jpg","Shrewsbury Hose Company"),("1849496-orig.jpg","Southard, Howell Township"),("506247-orig.jpg","Morganville 1"),
 ("7876949-orig.jpg","Morganville 2"),("1784665-orig.jpg","Spring Lake Heights FD"),("9202375-orig.jpg","Pine Brook, Tinton Falls Station 3"),("6598896-orig.jpg","Oceanport Ladder"),("6953581-orig.jpg","Oceanport Pumper")]
wet_day = [("258692-orig.jpg","…and packed down this way too"),("6255881-orig.jpg",""),("533381-orig.jpg",""),("5505261-orig.jpg","Springdale was packed"),("209469-orig.jpg",""),
 ("8059683-orig.jpg",""),("1042083-orig.jpg",""),("9204411-orig_1.jpg",""),("1943881-orig.jpg",""),("270225-orig.jpg",""),("4838531-orig.jpg","Image on Fair Haven Ladder Truck"),
 ("1230635-orig_1.jpg","…and the band played on"),("9301822-orig.jpg",""),("1396898-orig.jpg",""),("8149876-orig.jpg","")]
page("491-wetdown.html", "491 Wetdown", f'''
<p class="lede">We commissioned 491 by holding a wetdown and celebrated with neighboring departments.</p>
<h2>Attendees from Nearby Departments</h2>{gallery(wet_attend)}
<h2>Photos from Throughout the Day</h2>{gallery(wet_day)}
<p>Thanks for contributions to Jason Schramm — <a href="http://www.jschramm.com/photography/">Jason Schramm Photography</a>.</p>''', "About / 491 Wetdown", ABOUT_GROUP)

def logos(items):
    return '<div class="logo-grid">' + "".join(f'<a href="{u}" target="_blank" rel="noopener">{img(i, t)}<span>{t}</span></a>' for i, u, t in items) + "</div>"
page("dashboard.html", "Member Dashboard", f'''
<h2>Operations</h2>
{logos([("editor/370102801.png","https://dashboard.iamresponding.com/","IamResponding"),("editor/932996363.jpg","https://wiki.radioreference.com/index.php/Monmouth_County_(NJ)_Fire_Stations","Monmouth County Fire Stations"),
("editor/347787611.jpg","https://www.mcsonj.org/marp/marp-plans/","MARP Plans"),("editor/350790897.jpg","https://www.mcsonj.org/divisions/emergency-management/","MCSO Emergency Management"),
("published/574729183.png","https://login.emergencyreporting.com/","Emergency Reporting"),("published/346117857.png","https://app.halligan.io/login","Halligan"),
("editor/528622473.png","http://www.ready.nj.gov/","Ready NJ"),("published/504003925.png","https://www.fema.gov/","FEMA")])}
<h2>Training</h2>
{logos([("editor/579431359.jpg","https://www.visitmonmouth.com/page.aspx","Monmouth County Fire Academy"),("128127096_orig.jpg","http://www.middletownfireacademy.com/","Middletown Fire Academy"),
("editor/229770378.jpg","http://www.middlesexcountynj.gov/government/departments/psh/pages/fire-academy.aspx","Middlesex County Fire Academy"),("published/342631336.jpg","http://www.tomsriverfire.org/fire-academy/","Toms River Fire Academy"),
("601345759_orig.png","https://www.allhandsfire.com/Get-Trained","All Hands Fire"),("591766484_orig.png","https://www.keanfiresafety.com/","Kean Fire Safety")])}
<h2>Tinton Falls Districts & Fire Companies</h2>
{logos([("342127728_orig.png","https://www.tintonfallsfiredistrict2.com/","TF Fire District 2"),("published/210050470.png","http://www.tintonfallsfire.org/","Tinton Falls Fire"),
("published/985095324.jpg","https://www.waysidefirecompany.com/","Wayside Fire Company"),("published/847025001.jpg","https://www.tintonfallsfiredistrict1.com/","TF Fire District 1")])}''', "Resources / Dashboard", RES_GROUP)

page("join-northside.html", "Join Northside", f'''
<div class="recruit-banner"><b>Northside is looking for volunteers.</b> No experience needed. Training is free. <a href="#interest">Tell us you’re interested →</a></div>
<p class="lede">Northside Engine Company No. 4 has protected Tinton Falls since 1955, and every member is a volunteer. We answer 300+ calls a year, and we need neighbors who want to learn real skills, make a difference close to home, and be part of a crew that has each other’s backs.</p>
<div class="stat-band">
<div><b>62%</b><span>of U.S. firefighters are volunteers</span></div>
<div><b>3×</b><span>more calls than 40 years ago</span></div>
<div><b>635,100</b><span>volunteer firefighters in 2023, a record low</span></div>
</div>
<p class="src-note">Source: <a href="https://www.nvfc.org/wp-content/uploads/2026/02/2026-Fire-Service-Infographic.pdf">National Volunteer Fire Council, 2026 Fire Service Fact Sheet</a></p>

<h2>What You Get</h2>
<div class="benefit-grid">
<div><h3>Real-world skills</h3><p>Fire suppression, rescue, ladders, ropes, hazmat awareness, CPR and incident command — skills that help keep you and your family safe.</p></div>
<div><h3>Free state certification</h3><p>New Jersey Firefighter I training at the county fire academy at no cost to you.</p></div>
<div><h3>A second family</h3><p>Drills, meals, parades, Memorial Day, wetdowns. The friendships are a big reason members stay for decades.</p></div>
<div><h3>Retirement money (LOSAP)</h3><p>Tax-deferred contributions toward retirement for active volunteers.</p></div>
<div><h3>Life insurance</h3><p>A district-supplied life insurance policy once you qualify.</p></div>
<div><h3>Tuition and fee waivers</h3><p>Up to $600 a year in Tinton Falls tuition waivers for you and your family, plus up to $300 in borough fee waivers.</p></div>
</div>
<p><a href="#benefits">Full benefit details ↓</a></p>

<h2>Ways To Serve</h2>
<div class="role-list">
<div><h3>Firefighter</h3><p>Respond to fires, crashes, alarms and rescues. You’ll train to Firefighter I, then keep building skills — driver/operator, officer and specialty training as you gain experience.</p></div>
<div><h3>Junior member (under 18)</h3><p>Start learning early. Under New Jersey law, juniors under 16 attend meetings and non-hazardous training; at 16 and up they can join recruit firefighter training with parent permission and close supervision. Juniors never face the same hazards as adult members.</p></div>
</div>

<h2>Who Can Join</h2>
<ol><li>At least 18 years old (or ask about the junior program)</li><li>Hold a valid NJ driver’s license</li><li>A resident of the Borough of Tinton Falls, Shrewsbury Township, Red Bank, Lincroft, Shrewsbury or Eatontown for at least 6 months</li></ol>
<p>Firefighting isn’t just for one kind of person. Members come from all walks of life, and we welcome women, people of every background, and people who have never set foot in a firehouse.</p>

<h2>How It Works</h2>
<ol class="steps">
<li><b>Tell us you’re interested.</b> Use the form below, call or email. A member will reach out.</li>
<li><b>Visit Station 4.</b> Meet the members, see the trucks, ask anything.</li>
<li><b>Apply.</b> Fill out the membership application and pass the background checks.</li>
<li><b>Investigating committee.</b> A few members get to know you and make a recommendation.</li>
<li><b>Probation (6 months).</b> Start drilling and responding alongside experienced members.</li>
<li><b>Firefighter I.</b> Complete New Jersey Firefighter I at the Monmouth County Fire Academy — more than 100 hours of state-certified training at no cost.</li>
<li><b>Full member.</b> After probation, the active members vote on your membership based on your performance and the line officers’ recommendations.</li>
</ol>

<h2>Common Questions</h2>
<div class="faq">
<details><summary>Do I need any experience?</summary><p>No. We train you from day one. Many of our members had never fought a fire before joining.</p></details>
<details><summary>How much time does it take?</summary><p>Plan on regular drills and meetings, plus calls when you’re available. Firefighter I is the biggest commitment up front: more than 100 hours of classes and drills, usually spread over evenings and weekends. Ask us about our current drill schedule and minimums.</p></details>
<details><summary>Do I have to answer every call?</summary><p>No. Nobody makes every call. Members respond when they can, and many with day jobs cover nights and weekends.</p></details>
<details><summary>Can I join if I work full-time or have kids?</summary><p>Yes. Many of our members do. Volunteering is built around real lives, and families are part of the firehouse too.</p></details>
<details><summary>What does it cost?</summary><p>Nothing. Training at the county fire academy is free, and the district provides your protective gear.</p></details>
<details><summary>What does Firefighter I training involve?</summary><p>It’s New Jersey’s state certification course, covering ladders, hose, safety, search and rescue, hazardous materials awareness, incident command and more. You’ll need a physician’s medical evaluation before the academy, and you must be 18 to take part in live-fire training.</p></details>
<details><summary>What if I’m worried about the physical or emotional side?</summary><p>That’s a fair question and a common one. You’ll train at your own pace with experienced members, and you won’t be asked to do anything you haven’t been trained for. Firefighters look out for each other, on scene and after. Ask us about the support available.</p></details>
<details><summary>I don’t live in your area. Where can I volunteer?</summary><p>Use our <a href="find-a-fd-to-join.html">fire department finder</a>, or search <a href="https://www.makemeafirefighter.org/">MakeMeAFirefighter.org</a>, the National Volunteer Fire Council’s national listing of volunteer opportunities.</p></details>
</div>

<p><a class="download" href="images/joint_district_application_-_update_20210304.pdf">📄 Download the membership application (PDF, 126 KB)</a></p>
<h2 id="interest">Tell Us You’re Interested</h2>
<p>Fill this out and a member will reach out to answer your questions and set up a time to visit Station 4. It only takes a minute.</p>
<form class="join-form" id="join-form" action="https://formsubmit.co/{EMAIL}" method="POST">
<input type="hidden" name="_subject" value="New interest from northsideenginecompany.org">
<input type="hidden" name="_template" value="table">
<input type="hidden" name="_next" value="https://www.northsideenginecompany.org/join-northside.html?sent=1#interest">
<input type="text" name="_honey" class="sr" tabindex="-1" autocomplete="off" aria-hidden="true">
<div class="jf-grid">
<label>Full name<input name="name" required autocomplete="name"></label>
<label>Phone<input name="phone" type="tel" required autocomplete="tel"></label>
<label>Email<input name="email" type="email" required autocomplete="email"></label>
<label>Town you live in<select name="town" required><option value="">Choose…</option><option>Tinton Falls</option><option>Shrewsbury Township</option><option>Shrewsbury</option><option>Red Bank</option><option>Lincroft</option><option>Eatontown</option><option>Other</option></select></label>
<label>I’m interested in<select name="interest"><option>Firefighting</option><option>Junior program (under 18)</option><option>Fire police / support</option><option>Not sure yet</option></select></label>
<label>Best time to reach you<input name="best_time" placeholder="e.g. weekday evenings"></label>
</div>
<label>Anything you want us to know? <span class="opt">(optional)</span><textarea name="message" rows="4" placeholder="Prior experience, questions, etc."></textarea></label>
<label class="jf-check"><input type="checkbox" name="age_18_plus" value="Yes"> I’m 18 or older</label>
<button class="btn btn-primary" type="submit">Send</button>
<p class="jf-status" id="jf-status" role="status" aria-live="polite"></p>
</form>
<p class="jf-alt">Prefer email? Write to <a href="mailto:{EMAIL}?subject=Joining%20Northside">{EMAIL}</a> or call 732.741.3205.</p>
<script>
(function(){{
var f=document.getElementById("join-form"),st=document.getElementById("jf-status");
if(/[?&]sent=1/.test(location.search)){{st.textContent="Thanks! We got your info and will be in touch soon.";st.className="jf-status ok"}}
f.addEventListener("submit",function(e){{
  if(!window.fetch)return;e.preventDefault();
  var b=f.querySelector("button");b.disabled=true;st.className="jf-status";st.textContent="Sending…";
  var data={{}};new FormData(f).forEach(function(v,k){{data[k]=v}});
  fetch("https://formsubmit.co/ajax/{EMAIL}",{{method:"POST",headers:{{"Content-Type":"application/json","Accept":"application/json"}},body:JSON.stringify(data)}})
  .then(function(r){{return r.json().then(function(j){{if(!r.ok||String(j.success)!=="true")throw 0}})}})
  .then(function(){{f.reset();st.className="jf-status ok";st.textContent="Thanks! We got your info and will be in touch soon."}})
  .catch(function(){{st.className="jf-status err";st.textContent="Something went wrong. Please email {EMAIL} or call 732.741.3205."}})
  .finally(function(){{b.disabled=false}});
}});
}})();
</script>
<p><a class="download" href="images/joint_district_application_-_update_20210304.pdf">📄 Download the membership application (PDF, 126 KB)</a></p>
<h2 id="benefits">Benefit Details</h2>
<h3>Length of Service Award Program (LOSAP)</h3><p>A statewide program established in 1998 that lets communities provide retirement savings contributions to volunteer emergency responders. <a href="http://www.state.nj.us/dca/lgs/losap/program_info/about_losap.pdf">Learn more from the State</a>.</p>
<h3>Life Insurance</h3><p>District-supplied life insurance policy once qualified.</p>
<h3>Training</h3><p>Members are trained in fireground operations, safety, ladders, ropes, wildland fire suppression, electrical and chemical hazards, and incident command. Training starts with Firefighter I & II at the Monmouth County, Middletown, or Middlesex County Fire Academy, and continues throughout your career as you progress in experience and command responsibilities.</p>
<ul><li><a href="http://www.monmouthcountyfireacademy.org/">Monmouth County Fire Academy</a></li><li><a href="http://www.middletownfireacademy.com/">Middletown Fire Academy</a></li><li><a href="http://www.middlesexcountynj.gov/Government/Departments/PSH/Pages/Fire-Academy.aspx">Middlesex County Fire Academy</a></li></ul>
<h3>Tuition Assistance</h3><p>The Borough of Tinton Falls provides tuition waivers for volunteer emergency responders up to $600 per year, covering the volunteer, their spouse and dependent children. It starts after your first year of service, with additional credit for each emergency service organization you belong to.</p>
<h3>Municipal Fee Waiver</h3><p>(2-18A.4) Exemption from Tinton Falls Borough fees for recreation activities, training programs, licenses and permits, and use of Borough buildings and facilities, up to $300 per year, for the personal and nonprofit use of members in good standing.</p>
<h3>Jury Duty</h3><p>Active volunteer firefighters may request to be excused from jury duty with verification of active membership. See the <a href="http://www.judiciary.state.nj.us/juryreporting/juryfqa.pdf">state website</a>.</p>
<h2>Learn More</h2>
<ul class="src-list">
<li><a href="https://www.nvfc.org/RR-Research">NVFC volunteer firefighter recruitment and retention research</a></li>
<li><a href="https://www.makemeafirefighter.org/">Make Me A Firefighter</a> — national volunteer opportunity search</li>
<li><a href="https://mcsonj.org/firefighter-1-2/">Monmouth County Fire Academy — Firefighter 1 &amp; 2 program</a></li>
<li><a href="https://www.nvfc.org/?p=22467">NVFC: volunteer roles beyond firefighting</a></li>
</ul>
{fig("firelogo_orig.gif")}''', "Join / Join Northside", JOIN_GROUP)

# Fire departments for the finder map. lat/lng from OpenStreetMap; phone "" = none published.
FIRE_DEPTS = [
    # name, town, address, phone, website, lat, lng
    ("Northside Engine Company No. 4", "Tinton Falls", "35 Springdale Ave, Tinton Falls, NJ 07724", "732-741-3205", "join-northside.html", 40.33559, -74.08247),
    ("Tinton Falls Fire Company No. 1", "Tinton Falls", "695 Tinton Ave, Tinton Falls, NJ 07724", "732-542-4422", "https://www.facebook.com/TFFC1/", 40.30424, -74.09916),
    ("Wayside Fire Company", "Tinton Falls", "2 Volunteer Way, Tinton Falls, NJ 07753", "", "https://www.waysidefirecompany.com/", 40.24494, -74.09499),
    ("Pine Brook Fire Company", "Tinton Falls", "70 Hamilton Rd, Tinton Falls, NJ 07724", "", "https://www.facebook.com/PineBrookFireCo/", 40.28700, -74.09609),
    ("Eatontown Fire Department", "Eatontown", "47 Broad St, Eatontown, NJ 07724", "", "https://eatontownfd.com/", 40.30587, -74.05828),
    ("Shrewsbury Hose Company No. 1", "Shrewsbury", "783 Broad St, Shrewsbury, NJ 07702", "", "http://www.shrewsburyhosecompany.com/", 40.32572, -74.06176),
    ("Red Bank Fire Department", "Red Bank", "7-9 Mechanic St, Red Bank, NJ 07701", "732-530-2700", "https://www.redbankfire.org/", 40.35145, -74.06491),
    ("Little Silver Fire Company", "Little Silver", "543 Prospect Ave, Little Silver, NJ 07739", "", "https://www.littlesilverfd.org/", 40.33724, -74.04003),
    ("Oceanport Hook & Ladder Company", "Oceanport", "21 Main St, Oceanport, NJ 07757", "732-542-6928", "https://www.ophl.org/", 40.31303, -74.03302),
    ("Port-Au-Peck Chemical Hose Company", "Oceanport", "433 Myrtle Ave, Oceanport, NJ 07757", "732-229-9771", "https://www.portaupeckfire.org/", 40.32046, -74.01631),
    ("West Long Branch Fire Company No. 1", "West Long Branch", "385 Monmouth Rd, West Long Branch, NJ 07764", "", "", 40.28411, -74.01929),
    ("Oakhurst Independent Hose Company", "Ocean Township", "72 Larkin Pl, Oakhurst, NJ 07755", "732-222-4624", "https://www.facebook.com/OakhurstIndependentHoseCompanyNo.1/", 40.26832, -74.01977),
    ("Wanamassa Fire Company", "Ocean Township", "2001 Sunset Ave, Ocean Township, NJ 07712", "732-775-9784", "https://www.wanamassafirecompany.com/", 40.23166, -74.02478),
    ("Hamilton Fire Company", "Neptune", "2420 Heck Ave, Neptune, NJ 07753", "", "", 40.21058, -74.08543),
    ("Liberty Fire Company", "Neptune", "1518 Monroe Ave, Neptune, NJ 07753", "", "", 40.22092, -74.03052),
    ("Unexcelled Fire Company", "Neptune", "1120 Corlies Ave, Neptune, NJ 07753", "", "", 40.21053, -74.01782),
    ("Shark River Hills Fire Company", "Neptune", "200 Brighton Ave, Neptune, NJ 07753", "", "", 40.20135, -74.05368),
    ("Colts Neck Fire Company No. 1", "Colts Neck", "123 County Rd 537, Colts Neck, NJ 07722", "", "https://www.cnfd.org/", 40.28580, -74.18270),
    ("Colts Neck Fire Company No. 2", "Colts Neck", "50 Conover Rd, Colts Neck, NJ 07722", "", "https://www.cnfd.org/", 40.31540, -74.19040),
    ("Lincroft Fire Company", "Middletown", "601 Newman Springs Rd, Lincroft, NJ 07738", "", "https://www.lfc10.org/", 40.33130, -74.11755),
    ("Middletown Fire Company No. 1", "Middletown", "336 Route 35, Middletown, NJ 07701", "732-890-0378", "https://www.middletownnj.org/mtfd", 40.36900, -74.08501),
    ("River Plaza Hose Company", "Middletown", "26 Applegate St, Middletown, NJ 07701", "732-890-0378", "https://www.middletownnj.org/mtfd", 40.35005, -74.08591),
    ("Old Village Fire Company", "Middletown", "1340 Route 35, Middletown, NJ 07748", "732-890-0378", "https://www.middletownnj.org/mtfd", 40.40038, -74.12208),
    ("Navesink Hook & Ladder Company", "Middletown", "141 Jackson St, Atlantic Highlands, NJ 07716", "732-890-0378", "https://www.navesinkfire.org/", 40.40027, -74.02879),
    ("Belford Engine Company", "Middletown", "739 Main St, Belford, NJ 07718", "732-890-0378", "https://www.middletownnj.org/mtfd", 40.42215, -74.08971),
    ("Independent Fire Company", "Middletown", "536 Route 36, Belford, NJ 07718", "732-890-0378", "https://www.middletownnj.org/mtfd", 40.42137, -74.09457),
    ("Community Fire Company", "Middletown", "85 Appleton Ave, Leonardo, NJ 07737", "732-890-0378", "https://www.middletownnj.org/mtfd", 40.41499, -74.06573),
    ("Brevent Park & Leonardo Fire Company", "Middletown", "38 Center Ave, Leonardo, NJ 07737", "732-890-0378", "https://www.middletownnj.org/mtfd", 40.41835, -74.05484),
    ("Port Monmouth Fire Company", "Middletown", "125 Main St, Port Monmouth, NJ 07758", "732-890-0378", "https://www.middletownnj.org/mtfd", 40.43017, -74.09807),
    ("East Keansburg Fire Company", "Middletown", "214 Thompson Ave, North Middletown, NJ 07748", "732-890-0378", "https://www.middletownnj.org/mtfd", 40.43606, -74.11315),
    ("Fair Haven Fire Company No. 1", "Fair Haven", "645 River Rd, Fair Haven, NJ 07704", "", "https://fhfd.org/", 40.36207, -74.04075),
    ("Rumson Fire Company", "Rumson", "140 E River Rd, Rumson, NJ 07760", "", "", 40.37175, -73.99926),
    ("Oceanic Hook & Ladder Company", "Rumson", "45 W River Rd, Rumson, NJ 07760", "", "", 40.37501, -74.01214),
    ("Holmdel Fire & Rescue Company No. 2", "Holmdel", "11-13 Centerville Rd, Holmdel, NJ 07733", "", "https://hfrc2.org/", 40.40886, -74.15685),
]
_fd_json = json.dumps([dict(zip(["name", "town", "addr", "phone", "web", "lat", "lng"], d)) for d in FIRE_DEPTS])
_fd_rows = "".join(
    f'<tr><td><b>{html.escape(n)}</b></td><td>{html.escape(t)}</td><td>{html.escape(a)}</td>'
    f'<td>{f"<a href=tel:+1{ph.replace(chr(45), str())}>{ph}</a>" if ph else "—"}</td>'
    f'<td>{f"<a href={w!r}>Website</a>" if w else "—"}</td></tr>'
    for n, t, a, ph, w, _, _ in sorted(FIRE_DEPTS, key=lambda d: (d[1], d[0])))
page("find-a-fd-to-join.html", "Find A Fire Department", f'''
<p class="lede">Most fire departments across the country depend on dedicated volunteers from their local communities, and we are no different. If you’re interested in getting involved, we’d love to meet you.</p>
<p>One important factor when joining is how close the department is to your home or job. No one expects you to make every call, but you need to be able to respond in a reasonable time. Most people choose a department near home; some with flexible jobs respond during the day.</p>
<div class="recruit-banner"><b>Almost every company on this map relies on volunteers.</b> In a national survey, nearly two-thirds of people weren’t sure their local fire department was looking for help. <a href="https://www.nvfc.org/RR-Research">They are.</a></div>
<p>No experience is needed, training is free, and there are roles for people who never go inside a burning building: fire police, fundraising, fire safety education and support. <a href="join-northside.html">See what joining Northside looks like →</a></p>
<h2>Find The Closest Department</h2>
<p>Enter your home or work address to see the volunteer fire companies nearest you. Each department is set up and run a little differently, so reaching out to the one you’re interested in is the best way to learn more.</p>
<form class="fd-search" id="fd-form" role="search">
<label for="fd-q" class="sr">Your address</label>
<input id="fd-q" type="text" placeholder="Street address, town or ZIP" autocomplete="street-address" required>
<button class="btn btn-primary" type="submit">Search</button>
<button class="btn btn-outline" type="button" id="fd-loc">Use my location</button>
</form>
<p class="fd-status" id="fd-status" aria-live="polite"></p>
<div class="fd-map" id="fd-map" role="region" aria-label="Map of fire departments"></div>
<div class="fd-results" id="fd-results"></div>
<h2>All Departments</h2>
<div class="fd-table-wrap"><table class="fd-table"><thead><tr><th>Department</th><th>Town</th><th>Address</th><th>Phone</th><th>Website</th></tr></thead><tbody>{_fd_rows}</tbody></table></div>
<p class="fd-note">Don’t see your town? Search <a href="https://www.makemeafirefighter.org/">MakeMeAFirefighter.org</a>, the National Volunteer Fire Council’s national listing of volunteer opportunities, or call your town hall’s non-emergency line.</p>
<details class="fd-suggest" id="suggest"><summary>Know of a department we missed or a detail that changed? Let us know</summary>
<form class="join-form" id="fd-suggest-form" action="https://formsubmit.co/{EMAIL}" method="POST">
<input type="hidden" name="_subject" value="Fire department map correction">
<input type="hidden" name="_template" value="table">
<input type="hidden" name="_next" value="https://www.northsideenginecompany.org/find-a-fd-to-join.html?sent=1#suggest">
<input type="text" name="_honey" class="sr" tabindex="-1" autocomplete="off" aria-hidden="true">
<div class="jf-grid">
<label>Fire department<input name="department" required placeholder="e.g. Wall Township Fire Co."></label>
<label>Town<input name="town" required></label>
</div>
<label>What should we add or change?<textarea name="details" rows="3" required placeholder="Address, phone, website, or what’s wrong"></textarea></label>
<label>Your email <span class="opt">(optional, if you’d like a reply)</span><input name="email" type="email" autocomplete="email"></label>
<button class="btn btn-primary" type="submit">Send</button>
<p class="jf-status" id="fs-status" role="status" aria-live="polite"></p>
</form></details>
<script>
(function(){{
var f=document.getElementById("fd-suggest-form"),st=document.getElementById("fs-status"),d=document.getElementById("suggest");
if(/[?&]sent=1/.test(location.search)){{d.open=true;st.className="jf-status ok";st.textContent="Thanks! We’ll take a look and update the map."}}
f.addEventListener("submit",function(e){{
  if(!window.fetch)return;e.preventDefault();
  var b=f.querySelector("button");b.disabled=true;st.className="jf-status";st.textContent="Sending…";
  var data={{}};new FormData(f).forEach(function(v,k){{data[k]=v}});
  fetch("https://formsubmit.co/ajax/{EMAIL}",{{method:"POST",headers:{{"Content-Type":"application/json","Accept":"application/json"}},body:JSON.stringify(data)}})
  .then(function(r){{return r.json().then(function(j){{if(!r.ok||String(j.success)!=="true")throw 0}})}})
  .then(function(){{f.reset();st.className="jf-status ok";st.textContent="Thanks! We’ll take a look and update the map."}})
  .catch(function(){{st.className="jf-status err";st.textContent="Something went wrong. Please email {EMAIL} instead."}})
  .finally(function(){{b.disabled=false}});
}});
}})();
</script>
{video("eR98LQtCyiQ")}
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" integrity="sha256-p4NxAoJBhIIN+hmNHrzRCf9tD/miZyoHS5obTRR9BMY=" crossorigin="">
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js" integrity="sha256-20nQCchB9co0qIjJZRGuk2/Z9VM+kNiyxNV1lvTlZBo=" crossorigin=""></script>
<script>
(function(){{
var D={_fd_json};
var map=L.map("fd-map",{{scrollWheelZoom:false}}).setView([40.285,-74.07],11);
L.tileLayer("https://{{s}}.tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png",{{maxZoom:18,attribution:'&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'}}).addTo(map);
var pin=function(home){{return L.divIcon({{className:"fd-pin"+(home?" fd-home":""),html:home?'<img src="images/northside-patch.png" alt="">':"",iconSize:home?[34,40]:[18,18],iconAnchor:home?[17,20]:[9,9]}})}};
function esc(s){{return String(s).replace(/[&<>"']/g,function(c){{return{{"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}}[c]}})}}
function dirs(d){{return "https://www.google.com/maps/dir/?api=1&destination="+encodeURIComponent(d.addr)}}
function card(d,mi){{
  var tel=d.phone?'<a class="btn btn-outline" href="tel:+1'+d.phone.replace(/-/g,"")+'">Call '+esc(d.phone)+'</a>':"";
  var web=d.web?'<a class="btn btn-outline" href="'+esc(d.web)+'"'+(d.web.indexOf("http")===0?' target="_blank" rel="noopener"':"")+'>'+(d.name.indexOf("Northside")===0?"Join Northside":"Website")+'</a>':"";
  return '<div class="fd-card'+(d.name.indexOf("Northside")===0?" fd-card-home":"")+'"><div class="fd-card-top"><h3>'+esc(d.name)+'</h3>'+(mi!=null?'<span class="fd-dist">'+mi.toFixed(1)+' mi</span>':"")+'</div><p>'+esc(d.addr)+'</p><div class="fd-actions">'+tel+web+'<a class="btn btn-outline" href="'+dirs(d)+'" target="_blank" rel="noopener">Directions</a></div></div>';
}}
D.forEach(function(d){{d.m=L.marker([d.lat,d.lng],{{icon:pin(d.name.indexOf("Northside")===0),title:d.name}}).addTo(map).bindPopup(card(d))}});
map.fitBounds(L.latLngBounds(D.map(function(d){{return[d.lat,d.lng]}})),{{padding:[20,20]}});
var you=null,st=document.getElementById("fd-status"),res=document.getElementById("fd-results");
function miles(a,b,c,e){{var R=3958.8,r=Math.PI/180,x=(c-a)*r,y=(e-b)*r,h=Math.sin(x/2)*Math.sin(x/2)+Math.cos(a*r)*Math.cos(c*r)*Math.sin(y/2)*Math.sin(y/2);return 2*R*Math.asin(Math.sqrt(h))}}
function show(lat,lng,label){{
  if(you)map.removeLayer(you);
  you=L.circleMarker([lat,lng],{{radius:9,color:"#24324A",weight:3,fillColor:"#fff",fillOpacity:1}}).addTo(map).bindTooltip("You",{{permanent:false}});
  var list=D.map(function(d){{return{{d:d,mi:miles(lat,lng,d.lat,d.lng)}}}}).sort(function(a,b){{return a.mi-b.mi}}).slice(0,5);
  st.textContent="Closest departments to "+label+" (straight-line distance):";
  res.innerHTML=list.map(function(x){{return card(x.d,x.mi)}}).join("");
  map.fitBounds(L.latLngBounds([[lat,lng]].concat(list.slice(0,3).map(function(x){{return[x.d.lat,x.d.lng]}}))),{{padding:[40,40],maxZoom:14}});
  if(list[0].mi>15)st.textContent="That address is outside our area. These are the closest departments we list, but there is likely one closer to you.";
}}
document.getElementById("fd-form").addEventListener("submit",function(e){{
  e.preventDefault();var q=document.getElementById("fd-q").value.trim();if(!q)return;
  st.textContent="Searching…";res.innerHTML="";
  var url="https://nominatim.openstreetmap.org/search?format=json&limit=1&countrycodes=us&q="+encodeURIComponent(/\\bnj\\b|new jersey/i.test(q)?q:q+", New Jersey");
  fetch(url,{{headers:{{"Accept-Language":"en"}}}}).then(function(r){{return r.json()}}).then(function(j){{
    if(!j.length){{st.textContent="We couldn’t find that address. Try adding the town or ZIP code.";return}}
    show(+j[0].lat,+j[0].lon,j[0].display_name.split(",").slice(0,3).join(","));
  }}).catch(function(){{st.textContent="Address search is unavailable right now. Use the map or the list below."}});
}});
document.getElementById("fd-loc").addEventListener("click",function(){{
  if(!navigator.geolocation){{st.textContent="Your browser can’t share its location.";return}}
  st.textContent="Finding your location…";
  navigator.geolocation.getCurrentPosition(function(p){{show(p.coords.latitude,p.coords.longitude,"your location")}},function(){{st.textContent="Location wasn’t shared. Type your address instead."}},{{timeout:10000}});
}});
}})();
</script>''', "Join / Find A Fire Department", JOIN_GROUP)

page("donate.html", "Donate", f'''
<span class="eyebrow">Annual Fund Drive</span>
<h2>Support your volunteer firefighters</h2>
<p class="lede">We have started our annual fund drive and hope you can support us. Donating is easy — give securely online below.</p>
<div class="embed" style="margin:24px 0 32px"><iframe src="{ZEFFY}" title="Donation form" loading="lazy" allowpaymentrequest style="height:760px"></iframe></div>
<p>Prefer PayPal? Northside is registered with PayPal, the secure online payment service.</p>
<p><a class="btn btn-outline" href="https://www.paypal.com/donate/">Donate with PayPal</a></p>
<p>Thank you for your support!</p>''', "Donate")

page("interesting-stuff.html", "Interesting Stuff", f'''
<h2>Items of Interest</h2>
<p>For the first time ever, the FDNY used a drone to help fight a building fire (03-06-2017).</p>
{video("jXE365WENhQ")}{video("v6sQQVlY6VE")}
<h3>Drive carefully! Ladder positioning is everything!</h3>
{video("fwVHbegmdRg")}
<h3>I’m not saying this is one of us, but it could be!</h3>
{video("LAzo4bpC8vs")}''', "Resources / Interesting Stuff", RES_GROUP)

page("contact-us.html", "Contact Us", f'''
<div class="alert">For emergencies call 9-1-1</div>
<div class="contact-card" style="margin-top:28px"><dl>
<dt>Email</dt><dd><a href="mailto:{EMAIL}">{EMAIL}</a></dd>
<dt>Phone (non-emergency)</dt><dd><a href="tel:+17327413205">732.741.3205</a></dd>
<dt>Address</dt><dd>35 Springdale Ave<br>Tinton Falls, NJ 07724</dd>
<dt>Social</dt><dd><a href="{FB}">Facebook</a> · <a href="{IG}">Instagram</a></dd>
</dl></div>
<div class="video" style="aspect-ratio:16/10"><iframe src="https://www.google.com/maps?q=35+Springdale+Ave,+Tinton+Falls,+NJ+07724&output=embed" title="Map" loading="lazy"></iframe></div>''', "Contact Us")

# ---------------- LINKS (Linktree-style page for social bios) ----------------
LINKS = [
    ("join-northside.html#interest", "Join Northside", "Become a volunteer firefighter", True),
    ("find-a-fd-to-join.html", "Find A Fire Department", "Find a volunteer company near you", False),
    ("donate.html", "Donate to Northside", "Support your volunteer firefighters", False),
    (VENMO, "Venmo", "@northsidefire", False),
    (IG, "Instagram", "@northsideengineco4", False),
    (FB, "Facebook", "Northside Engine Company", False),
    ("./", "Our Website", "northsideenginecompany.org", False),
    (f"mailto:{EMAIL}", "Email Us", EMAIL, False),
]
_ICONS = {
    "donate": '<path d="M12 21s-7.5-4.6-9.6-9.2C.9 8.4 3 5 6.4 5c2 0 3.6 1.1 4.6 2.6C12 6.1 13.6 5 15.6 5 19 5 21.1 8.4 19.6 11.8 17.5 16.4 12 21 12 21z"/>',
    "join": '<circle cx="9" cy="8" r="4"/><path d="M2 21c0-3.9 3.1-7 7-7s7 3.1 7 7"/><path d="M19 8v6M16 11h6"/>',
    "instagram": '<rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.5" cy="6.5" r="1" fill="currentColor"/>',
    "facebook": '<path d="M14 8h3V4h-3c-2.8 0-4 1.7-4 4.3V11H7v4h3v6h4v-6h3l1-4h-4V8.6c0-.4.3-.6.6-.6z"/>',
    "venmo": '<path d="M17.5 3.5c.7 1.2 1 2.4 1 3.9 0 4.9-4.2 11.2-7.6 15.6H5.3L3 5.2l5-.5 1.3 10.2c1.2-2 2.7-5.1 2.7-7.2 0-1.2-.2-2-.5-2.6z"/>',
    "text": '<path d="M4 5h16a1 1 0 0 1 1 1v10a1 1 0 0 1-1 1H9l-5 4V6a1 1 0 0 1 1-1z"/><path d="M8 10h8M8 13h5"/>',
    "contact": '<rect x="4" y="3" width="16" height="18" rx="2"/><circle cx="12" cy="10" r="3"/><path d="M7.5 17.5c.8-2 2.5-3 4.5-3s3.7 1 4.5 3"/>',
    "drive": '<path d="M12 3c1 3 4.5 4.6 4.5 9.2A4.5 4.5 0 0 1 12 17a4.5 4.5 0 0 1-4.5-4.8c0-2 1.2-3.3 2-4.2.3 1.6 1 2.4 2 2.7C11 8.6 11.4 5.5 12 3z"/><path d="M5 21h14"/>',
    "pin": '<path d="M12 21s-6.5-6-6.5-11a6.5 6.5 0 0 1 13 0c0 5-6.5 11-6.5 11z"/><circle cx="12" cy="10" r="2.5"/>',
    "web": '<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c2.5 2.7 3.8 5.7 3.8 9s-1.3 6.3-3.8 9c-2.5-2.7-3.8-5.7-3.8-9S9.5 5.7 12 3z"/>',
    "truck": '<path d="M2 16V8h11v8M13 11h4l4 4v1h-8"/><circle cx="6.5" cy="17.5" r="2"/><circle cx="17.5" cy="17.5" r="2"/>',
    "history": '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
    "email": '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3 7l9 6 9-6"/>',
    "phone": '<path d="M5 3h4l2 5-2.5 1.5a11 11 0 0 0 6 6L16 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 5a2 2 0 0 1 2-2z"/>',
}
_icon_keys = ["join", "pin", "donate", "venmo", "instagram", "facebook", "web", "email"]
def _svg(k):
    return f'<svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">{_ICONS[k]}</svg>'
_link_items = "".join(
    f'<a class="lt-link{" lt-primary" if pri else ""}" href="{h}"{" target=_blank rel=noopener" if h.startswith("http") else ""}>'
    f'<span class="lt-ico">{_svg(k)}</span><span class="lt-txt"><b>{html.escape(t)}</b><small>{html.escape(d)}</small></span><span class="lt-arrow" aria-hidden="true">→</span></a>'
    for (h, t, d, pri), k in zip(LINKS, _icon_keys))
_link_items += (f'<div class="lt-link lt-split"><span class="lt-ico">{_svg("phone")}</span>'
    '<span class="lt-txt"><b>Call Or Text</b><small>732.741.3205</small></span>'
    '<span class="lt-btns"><a href="tel:+17327413205">Call</a><a href="sms:+17327413205">Text</a></span></div>'
    f'<a class="lt-link" href="northside.vcf" download="Northside Engine Co 4.vcf"><span class="lt-ico">{_svg("contact")}</span><span class="lt-txt"><b>Save Our Contact</b><small>Add Northside to your phone</small></span><span class="lt-arrow" aria-hidden="true">↓</span></a>')
(OUT / "links.html").write_text(HEAD.format(title="Northside Engine Co. No. 4 | Join, Donate & Connect", desc=DESC).replace("images/background-images/1218312023.jpg", "images/og-links.jpg").replace("<body>", '<body class="lt-body">') + f'''
<main id="main" class="lt">
<div class="lt-cover">{img("background-images/1218312023.jpg", "Northside fire apparatus outside Station 4")}</div>
<div class="lt-card">
<div class="lt-avatar">{img("northside-patch.png", "Northside Engine Co. patch")}</div>
<h1>Northside Engine Co. No. 4</h1>
<p class="lt-sub">Volunteer firefighters serving Tinton Falls, NJ since 1955</p>
<div class="lt-social"><a href="{IG}" target="_blank" rel="noopener" aria-label="Instagram">{_svg("instagram")}</a><a href="{FB}" target="_blank" rel="noopener" aria-label="Facebook">{_svg("facebook")}</a><a href="{VENMO}" target="_blank" rel="noopener" aria-label="Venmo">{_svg("venmo")}</a><a href="mailto:{EMAIL}" aria-label="Email">{_svg("email")}</a><a href="tel:+17327413205" aria-label="Call">{_svg("phone")}</a><a href="sms:+17327413205" aria-label="Text">{_svg("text")}</a></div>
<nav class="lt-links" aria-label="Northside links"><a class="lt-link lt-primary lt-drive" id="fund-drive" href="donate.html" hidden><span class="lt-ico">{_svg("drive")}</span><span class="lt-txt"><b>Annual Fund Drive</b><small>Your gift keeps Station 4 running</small></span><span class="lt-arrow" aria-hidden="true">→</span></a>{_link_items}</nav>
<div class="lt-alert">For emergencies, always call 9-1-1</div>
<p class="lt-foot">35 Springdale Ave · Tinton Falls, NJ 07724</p>
</div>
</main>
<script>
// Fund drive: show the Fund Drive link Dec 26 - Feb 28 (Eastern time); add ?drive=1 to preview it any time
(function(){{
var d=new Date(new Date().toLocaleString("en-US",{{timeZone:"America/New_York"}})),m=d.getMonth()+1,day=d.getDate();
var on=(m===12&&day>=26)||m===1||m===2||/[?&]drive=1/.test(location.search);
if(on)document.getElementById("fund-drive").hidden=false;
}})();
</script></body></html>''')

# 404 + favicon + CNAME + assets
(OUT / "404.html").write_text(HEAD.format(title="Page not found | Northside Engine Company No. 4", desc=DESC) + nav("") +
    '<main id="main"><section class="page-head"><div class="wrap"><h1>Page not found</h1></div></section><div class="wrap" style="padding:72px 24px"><p class="lede">Sorry, that page doesn’t exist.</p><a class="btn btn-primary" href="/">Back to home</a></div></main>' + FOOTER + "</body></html>")
(OUT / "styles.css").write_text((ROOT / "src/styles.css").read_text())
(OUT / "CNAME").write_text("www.northsideenginecompany.org\n")
_pages = sorted(p.name for p in OUT.glob("*.html") if p.name != "404.html")
(OUT / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "".join(f"  <url><loc>https://www.northsideenginecompany.org/{'' if n == 'index.html' else n}</loc></url>\n" for n in _pages) + "</urlset>\n")
(OUT / "robots.txt").write_text("User-agent: *\nAllow: /\nSitemap: https://www.northsideenginecompany.org/sitemap.xml\n")
(OUT / ".nojekyll").write_text("\n")
os.makedirs(OUT / "images", exist_ok=True)
(OUT / "images/favicon.svg").write_text('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect x="2" y="2" width="60" height="60" rx="16" fill="#A63A2E"/><text x="32" y="45" font-family="Arial,sans-serif" font-weight="700" font-size="38" text-anchor="middle" fill="#fff">4</text></svg>')
print("built", sorted(p.name for p in OUT.glob("*.html")))
