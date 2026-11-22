// POST /api/login  { email, next }  → emails a 15-minute sign-in link if the email is on MEMBER_EMAILS.
import { sign, isMember, safeNext } from "./_lib/auth.js";

export async function POST(request) {
  let email = "", next = "/members/";
  try {
    const b = await request.json();
    email = String(b.email || "").trim().toLowerCase();
    next = safeNext(b.next);
  } catch {}

  // Same reply whether or not the email is a member, so the list can't be probed.
  const reply = Response.json({ ok: true });
  if (!isMember(email)) return reply;

  const token = await sign({ t: "link", e: email, n: next, exp: Date.now() + 15 * 60 * 1000 });
  const origin = process.env.SITE_URL || new URL(request.url).origin;
  const link = `${origin}/api/verify?token=${encodeURIComponent(token)}`;

  const r = await fetch("https://api.resend.com/emails", {
    method: "POST",
    headers: { Authorization: `Bearer ${process.env.RESEND_API_KEY}`, "Content-Type": "application/json" },
    body: JSON.stringify({
      from: process.env.MAIL_FROM || "Northside Engine Co. No. 4 <onboarding@resend.dev>",
      to: email,
      subject: "Your Northside Member Sign-In Link",
      text: `Use this link to sign in to the Northside members area. It expires in 15 minutes.\n\n${link}\n\nIf you didn't ask for this, you can ignore this email.`,
      html: `<p>Use the button below to sign in to the Northside members area. It expires in 15 minutes.</p><p><a href="${link}" style="background:#A63A2E;color:#fff;padding:12px 20px;border-radius:8px;text-decoration:none;display:inline-block">Sign in</a></p><p style="color:#666">If you didn't ask for this, you can ignore this email.</p>`,
    }),
  });
  if (!r.ok) {
    console.error("Resend error", r.status, await r.text());
    return Response.json({ ok: false }, { status: 502 });
  }
  return reply;
}
