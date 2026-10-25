#!/usr/bin/env python3
"""Builds the Northside Engine Company static site into ../site/"""
import html, os, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "docs"
OUT.mkdir(exist_ok=True)

FB = "https://www.facebook.com/northsideenginecompany/"
IG = "https://www.instagram.com/northsideengineco4/"
EMAIL = "info@nsec4.org"
ZEFFY = "https://www.zeffy.com/en-US/embed/donation-form/0aa583fd-22ea-407d-ae3f-dafd78c17bf9"

ABOUT_GROUP = [("about-us.html", "About Us"), ("history.html", "History"),
               ("officers--admin.html", "Officers & Admin"), ("fire-scene-images.html", "Fire Scene Images"),
               ("around-station-4.html", "Around Station 4"), ("northside-fire-apparatus.html", "Our Apparatus"),
               ("building-491.html", "Building 491"), ("491-wetdown.html", "491 Wetdown")]
JOIN_GROUP = [("join-northside.html", "Join Northside"), ("find-a-fd-to-join.html", "Find a FD to Join")]
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
<a class="brand" href="./"><span class="badge">4</span><span><b>Northside Engine Co.</b><small>No. 4 · Tinton Falls, NJ</small></span></a>
<button class="menu-toggle" aria-expanded="false" aria-controls="nav">Menu</button>
<ul class="nav" id="nav">
<li><a href="./"{" aria-current=page" if cur == "index.html" else ""}>Home</a></li>
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
<link href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@600;700&family=Source+Sans+3:wght@400;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="styles.css">
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
<section class="hero"><div class="wrap">
<div class="kicker">Tinton Falls · Est. 1955</div>
<h1>Serving the community since 1955.</h1>
<p>Northside Engine Company No. 4 is an all-volunteer fire company protecting the Borough of Tinton Falls — answering 300+ calls a year, any day, any hour.</p>
<div class="actions"><a class="btn btn-primary" href="join-northside.html">Join Northside</a><a class="btn btn-light" href="donate.html">Donate</a></div>
</div></section>
<section class="stats"><div class="wrap">
<div><b>1955</b><span>Chartered</span></div><div><b>300+</b><span>Calls per year</span></div>
<div><b>15 yrs</b><span>Average member experience</span></div><div><b>100%</b><span>Volunteer</span></div>
</div></section>
<section class="section"><div class="wrap split">
<div><span class="eyebrow">Who we are</span><h2>Neighbors protecting neighbors.</h2>
<p class="lede">Northside Engine Company (NSEC) is one of the four Tinton Falls fire departments — and the youngest. Our members average 15 years of experience and train monthly to keep the borough safe. We are proud to serve our neighbors when they call.</p>
<a class="btn btn-outline" href="about-us.html">About Us</a></div>
<div class="rounded">{img("northside-766-shrews_orig.jpg", "Northside apparatus")}</div>
</div></section>
<section class="section white"><div class="wrap">
<span class="eyebrow">Around Northside</span><h2>Explore the company</h2>
<div class="cards">{card_html}</div>
</div></section>
<section class="section dark"><div class="wrap band">
<div><span class="eyebrow">No experience needed</span><h2>Join Northside. All training included.</h2>
<p class="lede">18+, valid NJ driver’s license, and 6 months’ residency in Tinton Falls or a neighboring town. Junior program available for under 18.</p></div>
<a class="btn btn-primary" href="join-northside.html">How to Join</a>
</div></section>
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
{fig("editor/memberstar.jpg")}
<h2>Interested in joining NSEC?</h2>
<p class="lede">Interested in helping your community? Working as part of the fire company is a great way to help — and pick up a couple of extras while you’re at it. <strong>No experience is needed, and all training is included!</strong></p>
<h3>You need to be</h3>
<ol><li>At least 18 years old</li><li>Hold a valid NJ driver’s license</li><li>A resident of the Borough of Tinton Falls, Shrewsbury Township, Red Bank, Lincroft, Shrewsbury or Eatontown for at least 6 months</li></ol>
<h3>The rest is easy</h3>
<ul><li>Complete the application</li><li>Pass the background checks</li><li>Receive a favorable recommendation from the investigating committee</li></ul>
<p>You then become a probationary member for 6 months. After that, the active members vote to accept your membership based on your performance and the recommendations of the line officers.</p>
<p><a class="btn btn-primary" href="mailto:{EMAIL}?subject=Joining%20Northside">Email us to get started</a></p>
<p><a class="download" href="images/joint_district_application_-_update_20210304.pdf">📄 Download the membership application (PDF, 126 KB)</a></p>
<h2>Junior Program</h2>
{fig("editor/fire-dog.jpeg")}
<p>We also have a junior program for individuals under 18. <a href="contact-us.html">Contact us</a> for more info!</p>
<h2>Benefits</h2>
<h3>Length of Service Award Program (LOSAP)</h3><p>A statewide program established in 1998 that lets communities provide retirement savings contributions to volunteer emergency responders. <a href="http://www.state.nj.us/dca/lgs/losap/program_info/about_losap.pdf">Learn more from the State</a>.</p>
<h3>Life Insurance</h3><p>District-supplied life insurance policy once qualified.</p>
<h3>Training</h3><p>Members are trained in fireground operations, safety, ladders, ropes, wildland fire suppression, electrical and chemical hazards, and incident command. Training starts with Firefighter I & II at the Monmouth County, Middletown, or Middlesex County Fire Academy, and continues throughout your career as you progress in experience and command responsibilities.</p>
<ul><li><a href="http://www.monmouthcountyfireacademy.org/">Monmouth County Fire Academy</a></li><li><a href="http://www.middletownfireacademy.com/">Middletown Fire Academy</a></li><li><a href="http://www.middlesexcountynj.gov/Government/Departments/PSH/Pages/Fire-Academy.aspx">Middlesex County Fire Academy</a></li></ul>
<h3>Tuition Assistance</h3><p>The Borough of Tinton Falls provides tuition waivers for volunteer emergency responders up to $600 per year, covering the volunteer, their spouse and dependent children. It starts after your first year of service, with additional credit for each emergency service organization you belong to.</p>
<h3>Municipal Fee Waiver</h3><p>(2-18A.4) Exemption from Tinton Falls Borough fees for recreation activities, training programs, licenses and permits, and use of Borough buildings and facilities, up to $300 per year, for the personal and nonprofit use of members in good standing.</p>
<h3>Jury Duty</h3><p>Active volunteer firefighters may request to be excused from jury duty with verification of active membership. See the <a href="http://www.judiciary.state.nj.us/juryreporting/juryfqa.pdf">state website</a>.</p>
{fig("firelogo_orig.gif")}''', "Join / Join Northside", JOIN_GROUP)

deps = [("Tinton Falls Fire Company No. 1","https://www.facebook.com/TFFC1/"),("Wayside","https://www.waysidefirecompany.com/"),("Pine Brook","https://www.facebook.com/PineBrookFireCo/"),
        ("Northside Engine Company No. 4","join-northside.html"),("Shrewsbury","http://www.shrewsburyhosecompany.com/"),("Red Bank","https://www.redbankfire.org/"),
        ("Lincroft","https://www.lfc10.org/"),("Eatontown","https://eatontownfd.com/"),("Colts Neck","https://www.cnfd.org/"),("Oakhurst","https://www.facebook.com/OakhurstIndependentHoseCompanyNo.1/")]
page("find-a-fd-to-join.html", "Become a Firefighter", f'''
<p class="lede">Most fire departments across the country depend on dedicated volunteers from their local communities, and we are no different. If you’re interested in getting involved, we’d love to meet you.</p>
<p>There are many fire departments around the Tinton Falls area, and finding the right one usually starts with finding the closest. Each department is set up and run a little differently, so contacting the one you’re interested in is the best way to learn more.</p>
<h2>Find Your Local Fire Department</h2>
<p>One important factor when joining is how close the department is to your home or job. No one expects you to make every call, but you need to be able to respond in a reasonable time. Most people choose a department near home; some with flexible jobs respond during the day.</p>
<h3>Nearby fire departments</h3>
<ul>{"".join(f'<li><a href="{u}">{n}</a></li>' for n, u in deps)}</ul>
{video("eR98LQtCyiQ")}
<h2>Fire Departments in Tinton Falls</h2>
<p>Tinton Falls has four fire departments, so anyone who lives in Tinton Falls has a department nearby.</p>''', "Join / Find a FD to Join", JOIN_GROUP)

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

# 404 + favicon + CNAME + assets
(OUT / "404.html").write_text(HEAD.format(title="Page not found | Northside Engine Company No. 4", desc=DESC) + nav("") +
    '<main id="main"><section class="page-head"><div class="wrap"><h1>Page not found</h1></div></section><div class="wrap" style="padding:72px 24px"><p class="lede">Sorry, that page doesn’t exist.</p><a class="btn btn-primary" href="/">Back to home</a></div></main>' + FOOTER + "</body></html>")
(OUT / "styles.css").write_text((ROOT / "src/styles.css").read_text())
# custom domain is set in GitHub Pages settings
(OUT / ".nojekyll").write_text("")
os.makedirs(OUT / "images", exist_ok=True)
(OUT / "images/favicon.svg").write_text('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><circle cx="32" cy="32" r="30" fill="#B3121B" stroke="#C9A227" stroke-width="3"/><text x="32" y="45" font-family="Arial Narrow,Arial,sans-serif" font-weight="700" font-size="38" text-anchor="middle" fill="#fff">4</text></svg>')
print("built", sorted(p.name for p in OUT.glob("*.html")))
