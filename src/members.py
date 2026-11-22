# Members-only pages. Run by build.py (shares its helpers).
# Everything under /members/ is guarded by middleware.js on Vercel.
# Edit the content below, then run `python3 src/build.py`.

ANNOUNCEMENTS = [
    # (date, title, text) — newest first
    ("Nov 22, 2026", "Welcome To The Members Area", "This private section is for active Northside members only. Check back here for announcements, documents and the drill calendar."),
]

DOCUMENTS = [
    # (section, title, link) — link can be a file in docs/members/files/ or a shared Google Drive link
    ("Forms", "Membership Application (PDF)", "/images/joint_district_application_-_update_20210304.pdf"),
]

CALENDAR_EMBED = ""  # paste a Google Calendar "embed" URL here to show the drill/duty calendar

def ann_html(items):
    return "".join(f'<div class="contact-card" style="margin:0 0 16px"><span class="eyebrow">{html.escape(d)}</span><h3 style="margin:.3em 0">{html.escape(t)}</h3><p style="margin:0">{html.escape(x)}</p></div>' for d, t, x in items)

def docs_html(items):
    out, sections = [], {}
    for sec, t, u in items:
        sections.setdefault(sec, []).append((t, u))
    for sec, rows in sections.items():
        out.append(f"<h2>{html.escape(sec)}</h2><ul>" + "".join(f'<li><a href="{html.escape(u)}" target="_blank" rel="noopener">{html.escape(t)}</a></li>' for t, u in rows) + "</ul>")
    return "".join(out) or "<p>No documents yet.</p>"

page("members/index.html", "Member Dashboard", f'''
<p class="lede">Welcome, Northside. This area is private to signed-in members.</p>
<h2>Latest Announcement</h2>
{ann_html(ANNOUNCEMENTS[:1])}
<p><a href="members/announcements.html">All announcements →</a> · <a href="members/documents.html">Documents →</a> · <a href="members/calendar.html">Calendar →</a></p>
{LINKS}''', "Members", MEM_GROUP, base=True)

page("members/announcements.html", "Announcements", ann_html(ANNOUNCEMENTS), "Members / Announcements", MEM_GROUP, base=True)
page("members/documents.html", "Documents", docs_html(DOCUMENTS), "Members / Documents", MEM_GROUP, base=True)
page("members/calendar.html", "Calendar",
     f'<div class="video" style="aspect-ratio:4/3"><iframe src="{html.escape(CALENDAR_EMBED)}" title="Calendar" loading="lazy"></iframe></div>' if CALENDAR_EMBED
     else "<p>The drill and duty calendar will appear here once a calendar is connected.</p>", "Members / Calendar", MEM_GROUP, base=True)

page("login.html", "Member Sign In", '''
<p class="lede">Enter the email address on file with Northside and we’ll send you a sign-in link.</p>
<form id="login" class="contact-card" style="max-width:480px">
<label for="email" style="font-weight:500">Email</label>
<input id="email" name="email" type="email" required autocomplete="email" style="display:block;width:100%;margin:8px 0 16px;padding:12px 14px;font:inherit;border:1px solid var(--line);border-radius:10px">
<button class="btn btn-primary" type="submit">Email me a sign-in link</button>
<p id="msg" role="status" style="margin:16px 0 0"></p>
</form>
<p>Not on the list yet? Ask an officer, or email <a href="mailto:info@nsec4.org">info@nsec4.org</a>.</p>
<script>
const q=new URLSearchParams(location.search);
if(q.get("e")==="expired")document.getElementById("msg").textContent="That link expired or was already used. Request a new one.";
document.getElementById("login").addEventListener("submit",async e=>{e.preventDefault();
const m=document.getElementById("msg");m.textContent="Sending…";
try{const r=await fetch("/api/login",{method:"POST",headers:{"content-type":"application/json"},body:JSON.stringify({email:document.getElementById("email").value,next:q.get("next")||"/members/"})});
m.textContent=r.ok?"If that email is on the member list, a sign-in link is on its way. It expires in 15 minutes.":"Something went wrong. Please try again.";}
catch(_){m.textContent="Something went wrong. Please try again.";}});
</script>''', "Member Sign In", base=True)

# Old public dashboard URL now points into the members area
(OUT / "dashboard.html").write_text('<!doctype html><meta charset="utf-8"><meta http-equiv="refresh" content="0;url=/members/"><link rel="canonical" href="/members/"><title>Member Dashboard</title><a href="/members/">Member Dashboard</a>')
