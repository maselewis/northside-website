// GET /api/logout → clears the session cookie.
import { COOKIE } from "./_lib/auth.js";

export function GET(request) {
  return new Response(null, {
    status: 302,
    headers: {
      Location: new URL("/", request.url).toString(),
      "Set-Cookie": `${COOKIE}=; Path=/; Max-Age=0; HttpOnly; Secure; SameSite=Lax`,
    },
  });
}
