# Northside Engine Company No. 4 — website

Static site for https://www.northsideenginecompany.org, hosted on GitHub Pages (served from `/docs`).

- Edit page content in `src/build.py` and styles in `src/styles.css`, then run `python3 src/build.py` to regenerate `docs/`.
- Or edit the HTML files in `docs/` directly.
- Design source: Figma file "Northside Engine Co. No. 4 – Website".
- `assets.txt` + the "Copy images from old Weebly site" Action pulled the original photos from Weebly (one-time).

## Hosting on Vercel (project: `northside`)

Vercel serves `docs/` as static files and also runs:
- `middleware.js` — blocks everything under `/members/` unless the visitor is signed in.
- `api/login.js`, `api/verify.js`, `api/logout.js` — email sign-in links (no passwords).

Members pages are built from `src/members.py` (announcements, documents, calendar).

### Environment variables (Vercel → northside → Settings → Environment Variables)
| Name | What it is |
|---|---|
| `AUTH_SECRET` | Long random string (32+ chars) used to sign sign-in links and sessions |
| `MEMBER_EMAILS` | Comma-separated list of approved member emails. Remove an email to revoke access. |
| `RESEND_API_KEY` | API key from resend.com, used to send the sign-in emails |
| `MAIL_FROM` | Sender, e.g. `Northside Engine Co. No. 4 <members@northsideenginecompany.org>` (domain must be verified in Resend) |
| `SITE_URL` | Optional. e.g. `https://www.northsideenginecompany.org` |

After cutover to Vercel, turn off GitHub Pages so `/members/` is not also served publicly from `docs/`.
