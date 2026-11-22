// GET /api/verify?token=…  → checks the emailed link and sets a 30-day session cookie.
import { sign, verify, safeNext, COOKIE, SESSION_DAYS } from "./_lib/auth.js";

export async function GET(request) {
  const url = new URL(request.url);
  const p = await verify(url.searchParams.get("token"), "link");
  if (!p) return Response.redirect(new URL("/login.html?e=expired", url), 302);

  const maxAge = SESSION_DAYS * 24 * 60 * 60;
  const session = await sign({ t: "sess", e: p.e, exp: Date.now() + maxAge * 1000 });
  return new Response(null, {
    status: 302,
    headers: {
      Location: new URL(safeNext(p.n), url).toString(),
      "Set-Cookie": `${COOKIE}=${encodeURIComponent(session)}; Path=/; Max-Age=${maxAge}; HttpOnly; Secure; SameSite=Lax`,
      "Cache-Control": "no-store",
    },
  });
}
