// Signed tokens (HMAC-SHA256) for magic links and session cookies.
// Works in both Vercel Functions (Node) and Routing Middleware (Edge).
const enc = new TextEncoder();
export const COOKIE = "ns_session";
export const SESSION_DAYS = 30;

const b64u = (buf) =>
  btoa(String.fromCharCode(...new Uint8Array(buf))).replace(/\+/g, "-").replace(/\//g, "_").replace(/=+$/, "");
const unb64u = (s) => Uint8Array.from(atob(s.replace(/-/g, "+").replace(/_/g, "/")), (c) => c.charCodeAt(0));

async function key() {
  const secret = process.env.AUTH_SECRET;
  if (!secret || secret.length < 32) throw new Error("AUTH_SECRET missing or too short");
  return crypto.subtle.importKey("raw", enc.encode(secret), { name: "HMAC", hash: "SHA-256" }, false, ["sign", "verify"]);
}

export async function sign(payload) {
  const body = b64u(enc.encode(JSON.stringify(payload)));
  const sig = await crypto.subtle.sign("HMAC", await key(), enc.encode(body));
  return `${body}.${b64u(sig)}`;
}

export async function verify(token, type) {
  try {
    const [body, sig] = String(token || "").split(".");
    if (!body || !sig) return null;
    const ok = await crypto.subtle.verify("HMAC", await key(), unb64u(sig), enc.encode(body));
    if (!ok) return null;
    const p = JSON.parse(new TextDecoder().decode(unb64u(body)));
    if (p.t !== type || !p.exp || Date.now() > p.exp) return null;
    if (!isMember(p.e)) return null; // removing someone from the list signs them out
    return p;
  } catch {
    return null;
  }
}

export function members() {
  return (process.env.MEMBER_EMAILS || "")
    .split(/[\s,;]+/)
    .map((e) => e.trim().toLowerCase())
    .filter(Boolean);
}
export const isMember = (email) => !!email && members().includes(String(email).toLowerCase());

export function getCookie(request, name) {
  const m = (request.headers.get("cookie") || "").match(new RegExp(`(?:^|;\\s*)${name}=([^;]+)`));
  return m ? decodeURIComponent(m[1]) : null;
}

export const safeNext = (n) => (typeof n === "string" && /^\/members(\/|$)/.test(n) && !n.startsWith("//") ? n : "/members/");
