// Vercel Routing Middleware: everything under /members/ requires a valid member session.
import { next } from "@vercel/functions";
import { verify, getCookie, COOKIE } from "./api/_lib/auth.js";

export const config = { matcher: ["/members", "/members/:path*"] };

export default async function middleware(request) {
  const session = await verify(getCookie(request, COOKIE), "sess");
  if (session) return next({ headers: { "Cache-Control": "private, no-store" } });

  const url = new URL(request.url);
  const login = new URL("/login.html", url);
  login.searchParams.set("next", url.pathname);
  return Response.redirect(login, 302);
}
