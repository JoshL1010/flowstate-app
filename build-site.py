import base64, os, subprocess

MEDIA = "site/media"

# Clips are referenced as files, not inlined.
#
# They used to be base64 data URIs, which made index.html 2.04 MB — 1.16 MB of video plus
# the third base64 adds — and every byte of it blocking the first paint. The lazy loading
# underneath (preload="none", src assigned on scroll) was doing nothing at all, because the
# bytes had already arrived inside the HTML. The same files are published beside the page
# and served from the same origin, so pointing at them cuts the document to about 30 KB and
# makes the deferred loading real.
def src(name):
    return f"media/{name}"

def shape(name):
    """The clip's own aspect ratio, so its frame occupies the right space before it loads
    and the page does not jump when it does."""
    try:
        out = subprocess.run(
            ["ffprobe", "-v", "error", "-select_streams", "v:0",
             "-show_entries", "stream=width,height", "-of", "csv=p=0",
             os.path.join(MEDIA, f"{name}.mp4")],
            capture_output=True, text=True, check=True).stdout.strip()
        w, h = (int(v) for v in out.split(",")[:2])
        return f"{w} / {h}"
    except Exception:
        return "16 / 10"

CLIPS = ("reveal", "launch", "configure", "appearance")
SHAPE = {n: shape(n) for n in CLIPS}
ICON = "media/icon.png"

HEAD = f'''<meta charset="utf-8">
<title>FlowState for Mac</title>
<meta name="description" content="A native macOS workspace launcher. Opens the editor, terminal, repository and pages a project needs — arranged — in one keystroke. Free while in beta.">
<link rel="icon" href="{ICON}">
<link rel="apple-touch-icon" href="{ICON}">
<meta property="og:type" content="website">
<meta property="og:title" content="FlowState for Mac">
<meta property="og:description" content="Every project you own, one keystroke away. A macOS workspace launcher that waits at the edge of your screen.">
<meta property="og:image" content="https://flowstatemac.com/media/og.jpg">
<meta property="og:url" content="https://flowstatemac.com/">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="FlowState for Mac">
<meta name="twitter:description" content="Every project you own, one keystroke away.">
<meta name="twitter:image" content="https://flowstatemac.com/media/og.jpg">
<meta name="theme-color" content="#0E6DB2">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Instrument+Sans:wght@400;500;600;700&family=IBM+Plex+Mono:wght@400;500&display=swap">
<style>
:root{{
  --paper:#F7F8F7;--raised:#FFF;--sunk:#ECEFEC;
  --ink:#080D10;--ink2:#525C5F;--ink3:#8A9396;
  --rule:#E2E6E2;--rule2:#C6CBC6;
  --live:#0E6DB2;--live-soft:#E3F0F8;
  --sa:#102A38;
  --sh:0 2px 4px rgba(8,13,16,.04),0 24px 60px rgba(8,13,16,.12);
  --sh-lift:0 3px 8px rgba(8,13,16,.06),0 36px 84px rgba(8,13,16,.17);
  --glow:rgba(14,109,178,.13);
  --ease:cubic-bezier(.22,.9,.28,1);
}}
@media (prefers-color-scheme:dark){{:root:not([data-theme="light"]){{
  --paper:#070B0D;--raised:#10161A;--sunk:#0B1113;
  --ink:#EDEFEB;--ink2:#98A2A5;--ink3:#667073;
  --rule:#1C2326;--rule2:#313A3E;
  --live:#5CBBF2;--live-soft:#0B2839;
  --sh:0 2px 4px rgba(0,0,0,.5),0 28px 70px rgba(0,0,0,.6);
  --sh-lift:0 3px 8px rgba(0,0,0,.55),0 40px 96px rgba(0,0,0,.7);
  --glow:rgba(92,187,242,.10);
}}}}
:root[data-theme="dark"]{{
  --paper:#070B0D;--raised:#10161A;--sunk:#0B1113;
  --ink:#EDEFEB;--ink2:#98A2A5;--ink3:#667073;
  --rule:#1C2326;--rule2:#313A3E;
  --live:#5CBBF2;--live-soft:#0B2839;
  --sh:0 2px 4px rgba(0,0,0,.5),0 28px 70px rgba(0,0,0,.6);
  --sh-lift:0 3px 8px rgba(0,0,0,.55),0 40px 96px rgba(0,0,0,.7);
  --glow:rgba(92,187,242,.10);
}}
*{{box-sizing:border-box}}
html{{scroll-behavior:smooth}}
body{{margin:0;background:var(--paper);color:var(--ink);overflow-x:hidden;
  font-family:"Instrument Sans",ui-sans-serif,-apple-system,system-ui,sans-serif;
  font-size:17px;line-height:1.6;-webkit-font-smoothing:antialiased}}
.wrap{{width:min(100% - 44px,1180px);margin-inline:auto}}
h1,h2,h3{{margin:0;font-weight:600;letter-spacing:-.032em;line-height:1.04;text-wrap:balance}}
p{{margin:0}}
a{{color:var(--live)}}
a:focus-visible{{outline:2px solid var(--live);outline-offset:3px;border-radius:4px}}
kbd{{font-family:"IBM Plex Mono",monospace;font-size:.78em;border:1px solid var(--rule2);
  border-radius:4px;padding:.1em .4em;white-space:nowrap}}
.mono{{font-family:"IBM Plex Mono",monospace}}

/* Keyboard users reach the download without tabbing the whole page first. */
.skip{{position:absolute;left:-9999px;top:0;z-index:100;background:var(--ink);color:var(--paper);
  padding:12px 20px;border-radius:0 0 9px 0;font-weight:600;text-decoration:none}}
.skip:focus{{left:0}}

.rv{{opacity:0;transition:opacity .85s var(--ease),transform .85s var(--ease);
  transition-delay:calc(var(--i,0)*95ms)}}
.rv-u{{transform:translateY(30px)}}
.rv-l{{transform:translateX(-60px)}}
.rv-r{{transform:translateX(60px)}}
.rv-s{{transform:scale(.95)}}
.rv.in{{opacity:1;transform:none}}

nav{{position:fixed;inset:0 0 auto;z-index:60;border-bottom:1px solid transparent;
  transition:background .35s,border-color .35s}}
nav.stuck{{background:color-mix(in srgb,var(--paper) 88%,transparent);backdrop-filter:blur(16px);
  border-bottom-color:var(--rule)}}
.nav-in{{display:flex;align-items:center;gap:16px;padding:16px 0}}
.logo{{display:flex;align-items:center;gap:10px;font-weight:600;letter-spacing:-.02em;
  text-decoration:none;color:var(--ink)}}
.logo-mark{{width:26px;height:26px;flex:none;border-radius:6px;
  background-image:url("{ICON}");background-size:cover}}
.nav-links{{margin-left:auto;display:flex;align-items:center;gap:22px}}
.nav-links a.plain{{color:var(--ink2);text-decoration:none;font-size:14.5px;font-weight:500;
  transition:color .2s}}
.nav-links a.plain:hover{{color:var(--ink)}}
@media (max-width:620px){{.nav-links a.plain{{display:none}}}}
.btn{{display:inline-flex;align-items:center;gap:9px;border:1px solid transparent;font-weight:600;
  font-size:15px;padding:11px 20px;border-radius:9px;text-decoration:none;cursor:pointer;
  transition:transform .18s var(--ease),box-shadow .18s,border-color .18s}}
.btn-solid{{background:var(--ink);color:var(--paper)}}
.btn-solid:hover{{transform:translateY(-2px);box-shadow:0 10px 26px rgba(8,13,16,.26)}}
.btn-line{{background:transparent;color:var(--ink);border-color:var(--rule2)}}
.btn-line:hover{{border-color:var(--ink);transform:translateY(-2px)}}
.btn-lg{{font-size:16px;padding:15px 30px;border-radius:11px}}

/* A single soft light behind the headline. The hero was a flat field with type on it,
   which made a product about a glowing panel look like a text document. */
.hero{{padding:clamp(104px,14vw,180px) 0 0;position:relative;isolation:isolate}}
.hero::before{{content:"";position:absolute;z-index:-1;inset:-10% -20% auto auto;
  width:min(900px,90vw);aspect-ratio:1;pointer-events:none;
  background:radial-gradient(circle at 65% 35%,var(--glow),transparent 62%)}}
.hero h1{{font-size:clamp(2.9rem,7.8vw,6.4rem);max-width:13ch;letter-spacing:-.04em}}
.hero h1 .soft{{color:var(--ink3)}}
.hero .sub{{margin-top:30px;font-size:clamp(17px,1.75vw,19.5px);color:var(--ink2);max-width:45ch}}
.cta{{display:flex;flex-wrap:wrap;gap:15px 18px;align-items:center;margin-top:38px}}
.note{{font-family:"IBM Plex Mono",monospace;font-size:12px;color:var(--ink3)}}

/* video frames — the product, shown rather than described */
.screen{{position:relative;border-radius:14px;overflow:hidden;border:1px solid var(--rule2);
  box-shadow:var(--sh);background:var(--sa);line-height:0;
  transition:transform .5s var(--ease),box-shadow .5s var(--ease)}}
.screen:hover{{transform:translateY(-4px);box-shadow:var(--sh-lift)}}
.screen video{{width:100%;height:auto;display:block;background:var(--sa)}}
.hero-screen{{margin-top:clamp(44px,5.5vw,72px)}}
/* Says what is being shown. A silent looping clip with no label leaves the reader
   working out what they are looking at while it is already halfway through. */
.cap{{margin-top:14px;font-family:"IBM Plex Mono",monospace;font-size:11.5px;
  letter-spacing:.04em;color:var(--ink3);line-height:1.5}}

.story{{padding:clamp(76px,10vw,132px) 0}}
.story+.story{{border-top:1px solid var(--rule)}}
.sgrid{{display:grid;grid-template-columns:1fr 1.35fr;gap:clamp(34px,6vw,86px);align-items:center}}
.story.flip .scopy{{order:2}}
.scopy h2{{font-size:clamp(1.85rem,3.6vw,2.8rem);max-width:14ch}}
.scopy p{{margin-top:20px;color:var(--ink2);max-width:40ch}}
.step{{font-family:"IBM Plex Mono",monospace;font-size:11px;letter-spacing:.2em;
  color:var(--ink3);margin-bottom:20px}}
@media (max-width:880px){{.sgrid{{grid-template-columns:1fr;gap:34px}}.story.flip .scopy{{order:0}}}}

.quiet{{padding:clamp(70px,9vw,124px) 0;background:var(--sunk);border-block:1px solid var(--rule)}}
.lede{{max-width:54ch}}
.lede h2{{font-size:clamp(1.95rem,3.9vw,3rem);letter-spacing:-.034em}}
.lede p{{margin-top:20px;color:var(--ink2);font-size:18px}}
table{{width:100%;border-collapse:collapse;margin-top:40px;font-size:15.5px}}
th,td{{text-align:left;padding:14px 0;border-bottom:1px solid var(--rule);vertical-align:baseline}}
th{{font-family:"IBM Plex Mono",monospace;font-weight:400;font-size:11px;letter-spacing:.1em;
  text-transform:uppercase;color:var(--ink3);width:196px;padding-right:26px}}
td{{color:var(--ink2)}}
@media (max-width:640px){{th{{width:124px}}}}

.price{{padding:clamp(76px,10vw,132px) 0}}
.pgrid{{display:grid;grid-template-columns:1fr 1fr;gap:clamp(32px,5vw,72px);align-items:start;margin-top:46px}}
@media (max-width:820px){{.pgrid{{grid-template-columns:1fr}}}}
.amount{{display:flex;align-items:baseline;gap:10px}}
.amount b{{font-size:clamp(3.4rem,7.5vw,5rem);font-weight:600;letter-spacing:-.05em;line-height:1}}
.amount span{{color:var(--ink3);font-size:16px}}
.incl{{list-style:none;margin:28px 0 0;padding:0;display:grid;gap:13px}}
.incl li{{display:flex;gap:13px;align-items:baseline;color:var(--ink2);font-size:15.5px}}
.incl li::before{{content:"";width:5px;height:5px;border-radius:50%;background:var(--live);
  flex:none;transform:translateY(-3px)}}
.fine{{margin-top:28px;font-size:13.5px;color:var(--ink3);line-height:1.65;max-width:42ch}}

.close{{text-align:center;padding:clamp(84px,11vw,150px) 0}}
.close h2{{font-size:clamp(2.1rem,5.4vw,4rem);max-width:15ch;margin-inline:auto;letter-spacing:-.038em}}
.close p{{margin-top:22px;color:var(--ink2);max-width:44ch;margin-inline:auto}}
.close .cta{{justify-content:center;margin-top:36px}}
footer{{border-top:1px solid var(--rule);padding:32px 0 68px;color:var(--ink3);font-size:13px;
  font-family:"IBM Plex Mono",monospace}}
footer a{{color:var(--ink3)}}
footer a:hover{{color:var(--ink2)}}

@media (prefers-reduced-motion:reduce){{
  html{{scroll-behavior:auto}}
  *,*::before,*::after{{transition-duration:.01ms!important;animation:none!important}}
  .rv{{opacity:1;transform:none}}
  .screen:hover{{transform:none}}
}}
</style>
'''

def screen(name, caption, cls=""):
    return (f'<div class="screen {cls}" style="aspect-ratio:{SHAPE[name]}">'
            f'<video muted playsinline loop preload="none" '
            f'poster="{src(name + ".jpg")}" data-src="{src(name + ".mp4")}" '
            f'aria-label="{caption}"></video></div>'
            f'<p class="cap">{caption}</p>')

DOWNLOAD = "https://github.com/JoshL1010/flowstate-app/releases/latest/download/FlowState.dmg"
RELEASES = "https://github.com/JoshL1010/flowstate-app/releases"

# Where /buy sends people. Sandbox today; the live account will issue a different one on a
# different host, and this is the single line that changes — which is the whole reason the
# application opens /buy rather than a Paddle URL compiled into a notarized binary.
CHECKOUT = "https://sandbox-pay.paddle.io/hsc_01m12xm209gkv3y916s4b07bgs_bpgzfw0awwn8hebn90dthk835p6rrmv0"

# The service that turns a completed checkout into a signed licence.
LICENCE_SERVICE = "https://flowstate-licence.flowstate-app.workers.dev"

BODY = f'''
<a class="skip" href="#get">Skip to download</a>

<nav id="nav"><div class="wrap nav-in">
  <a class="logo" href="#top"><span class="logo-mark"></span> FlowState</a>
  <span class="nav-links">
    <a class="plain" href="#pricing">Pricing</a>
    <a class="plain" href="{RELEASES}">Release notes</a>
    <a class="btn btn-line" href="{DOWNLOAD}">Download</a>
  </span>
</div></nav>

<div id="top" class="hero"><div class="wrap">
  <h1 class="rv rv-u">Every project you own,<br><span class="soft">one keystroke away.</span></h1>
  <p class="sub rv rv-u" style="--i:1">
    FlowState waits at the edge of your screen. Call it and it opens the editor, the terminal,
    the repository and the pages a project needs — arranged, and gone again before you have
    finished thinking.
  </p>
  <div class="cta rv rv-u" style="--i:2">
    <a class="btn btn-solid btn-lg" href="{DOWNLOAD}">Download for macOS</a>
    <span class="note">Free in beta · macOS 15 or later · 2.9 MB</span>
  </div>
  <div class="hero-screen rv rv-s" style="--i:3">
    {screen("launch", "One keystroke: the editor, the terminal and the project&#8217;s pages, arranged.")}
  </div>
</div></div>

<div class="story"><div class="wrap sgrid">
  <div class="scopy rv rv-l">
    <div class="step">01 — REVEAL</div>
    <h2>No window to manage.</h2>
    <p>Rest the pointer against the side of the screen, or press a shortcut you choose.
      There is no Dock icon and nothing to arrange. It appears when you want it and is gone
      the moment you look away.</p>
  </div>
  <div class="rv rv-r" style="--i:1">
    {screen("reveal", "The panel arriving at the screen edge, and leaving again.")}
  </div>
</div></div>

<div class="story flip"><div class="wrap sgrid">
  <div class="scopy rv rv-r">
    <div class="step">02 — SET IT UP</div>
    <h2>You decide what opens.</h2>
    <p>Everything a project needs sits in one list — the app, the terminal, the repository,
      the pages, the files. A switch beside each one says whether it opens with Launch, and a
      panel reads back exactly what will happen, in the order it will happen.</p>
  </div>
  <div class="rv rv-l" style="--i:1">
    {screen("configure", "Setting up a project, with the Launch plan updating as you edit.")}
  </div>
</div></div>

<div class="story"><div class="wrap sgrid">
  <div class="scopy rv rv-l">
    <div class="step">03 — MAKE IT YOURS</div>
    <h2>Built to sit on your screen all day.</h2>
    <p>Eight palettes or your own colours, with width, spacing, text size, typeface, corners
      and how see-through the panel is. Every option shows you what it does before you pick
      it, and a look you like can be saved and handed to someone else.</p>
  </div>
  <div class="rv rv-r" style="--i:1">
    {screen("appearance", "Appearance Studio, where each option previews itself.")}
  </div>
</div></div>

<div class="quiet"><div class="wrap">
  <div class="lede rv rv-u">
    <h2>It never phones home, because there is no home to phone.</h2>
    <p>No account, no analytics, no telemetry, no third-party SDKs and no server of any kind.
      Your projects, paths and preferences are files in your own Application Support folder.</p>
  </div>
  <table class="rv rv-u" style="--i:1"><tbody>
    <tr><th scope="row">Accessibility</th><td>Optional. Lets FlowState move and resize windows — decline it and everything else still works, it simply stops rearranging anything.</td></tr>
    <tr><th scope="row">Automation</th><td>Optional. Requested only if you ask a workspace link to open in a new Safari or Chrome window on your current desktop.</td></tr>
    <tr><th scope="row">Network</th><td>None while FlowState is free. A paid subscription checks its licence against FlowState&rsquo;s own service about once a month, and sends nothing else &mdash; no projects, no paths, no usage. <a href="privacy/">Full detail</a>.</td></tr>
    <tr><th scope="row">Signature</th><td>Developer ID, notarized by Apple. Both permissions revocable at any time in System Settings.</td></tr>
  </tbody></table>
</div></div>

<div class="price" id="pricing"><div class="wrap">
  <div class="lede rv rv-u">
    <h2>Free right now. $7 a month when it is finished.</h2>
    <p>FlowState is in open beta with every feature unlocked, nothing to buy and no card to
      enter. Here is what it will cost afterwards, so nobody is surprised by it later.</p>
  </div>
  <div class="pgrid">
    <div class="rv rv-l" style="--i:1">
      <div class="amount"><b>$7</b><span>/ month, after launch</span></div>
      <ul class="incl">
        <li>Unlimited projects, workspaces and shortcuts</li>
        <li>Window arrangement and workspace restore</li>
        <li>Appearance Studio with saved, shareable themes</li>
        <li>AI handoff to any assistant you use</li>
        <li>Every update while your subscription is active</li>
      </ul>
    </div>
    <div class="rv rv-r" style="--i:2">
      <h3 style="font-size:1.2rem;margin-bottom:14px">Why a subscription</h3>
      <p style="color:var(--ink2);font-size:15.5px;max-width:40ch">
        FlowState is one person's work and macOS changes every year. A subscription is what
        pays for it to keep working on the next version instead of being abandoned, which is
        what happens to most small Mac utilities eventually.
      </p>
      <p class="fine">
        Seven-day free trial, no card up front. Cancel whenever you like and it keeps working
        until the period you have paid for ends. Beta testers keep full access for the whole
        beta, with plenty of warning before anything changes.
      </p>
    </div>
  </div>
</div></div>

<div class="close" id="get"><div class="wrap">
  <h2 class="rv rv-u">Try it on the project you are most behind on.</h2>
  <p class="rv rv-u" style="--i:1">
    That is the only real test. If it has not saved you anything by the third day, tell me —
    that is far more useful than a compliment.
  </p>
  <div class="cta rv rv-u" style="--i:2">
    <a class="btn btn-solid btn-lg" href="{DOWNLOAD}">Download FlowState</a>
    <span class="note">macOS 15+ · Apple silicon &amp; Intel · 2.9 MB</span>
  </div>
</div></div>

<footer><div class="wrap" style="display:flex;flex-wrap:wrap;gap:8px 26px">
  <span>FlowState 0.2.5 beta</span>
  <a href="terms/">Terms</a>
  <a href="refunds/">Refunds</a>
  <a href="privacy/">Privacy</a>
  <a href="{RELEASES}">Release notes</a>
  <span>Made for macOS</span>
</div></footer>

<script>
(function(){{
  var reduce = matchMedia("(prefers-reduced-motion: reduce)").matches;
  // Someone on a metered connection gets the poster frames and nothing else.
  var thrifty = matchMedia("(prefers-reduced-data: reduce)").matches;

  var rv = document.querySelectorAll(".rv");
  if (reduce) rv.forEach(function(el){{ el.classList.add("in"); }});
  else {{
    var o = new IntersectionObserver(function(es){{
      es.forEach(function(e){{ if(e.isIntersecting){{ e.target.classList.add("in"); o.unobserve(e.target); }} }});
    }},{{threshold:.14,rootMargin:"0px 0px -6% 0px"}});
    rv.forEach(function(el){{ o.observe(el); }});
  }}

  var nav=document.getElementById("nav");
  addEventListener("scroll",function(){{ nav.classList.toggle("stuck", scrollY>10); }},{{passive:true}});

  // Each clip is fetched and started only once it is actually on screen, and paused again
  // when it leaves. Now that the files are not inlined in this document, that defers real
  // bytes rather than only deferring the decode.
  if (thrifty) return;
  var vids=[].slice.call(document.querySelectorAll("video[data-src]"));
  var vo=new IntersectionObserver(function(es){{
    es.forEach(function(e){{
      var v=e.target;
      if(e.isIntersecting){{
        if(!v.src){{ v.src=v.dataset.src; }}
        if(!reduce){{ var p=v.play(); if(p&&p.catch){{ p.catch(function(){{}}); }} }}
      }} else if(!v.paused){{ v.pause(); }}
    }});
  }},{{threshold:.25}});
  vids.forEach(function(v){{ vo.observe(v); }});
}})();
</script>
'''


# ── Small pages ────────────────────────────────────────────────────────────────────────
#
# /buy and /thanks are the two ends of a purchase. They are separate files rather than
# sections of the landing page because Paddle redirects to one of them by URL, and because
# the landing page's 18 KB of CSS is not worth loading to show a sentence and a licence.

# One level down from the site root, so assets and links need a parent-relative path.
# Absolute paths would work on GitHub Pages, where the site lives under /flowstate-app/, and
# break locally, where it does not — and this is exactly where that difference is easy to
# ship without noticing, because the landing page keeps working either way.
PAGE_ICON = "../media/icon.png"
PAGE_HOME = "../"

PAGE_STYLE = f"""<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex">
<link rel="icon" href="{PAGE_ICON}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Instrument+Sans:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap">
<style>
:root{{--paper:#F7F8F7;--ink:#080D10;--ink2:#525C5F;--ink3:#8A9396;--rule:#E2E6E2;
  --live:#0E6DB2;--raised:#FFF;--warn:#8A5A00;--warn-bg:#FFF6E5}}
@media (prefers-color-scheme:dark){{:root{{--paper:#070B0D;--ink:#EDEFEB;--ink2:#98A2A5;
  --ink3:#667073;--rule:#1C2326;--live:#5CBBF2;--raised:#10161A;--warn:#F0C97A;--warn-bg:#2A2011}}}}
*{{box-sizing:border-box}}
body{{margin:0;min-height:100vh;display:flex;align-items:center;justify-content:center;
  background:var(--paper);color:var(--ink);padding:32px 22px;
  font-family:"Instrument Sans",ui-sans-serif,-apple-system,system-ui,sans-serif;
  font-size:16.5px;line-height:1.6;-webkit-font-smoothing:antialiased}}
main{{width:min(100%,560px)}}
h1{{margin:0 0 14px;font-size:clamp(1.7rem,4vw,2.3rem);font-weight:600;letter-spacing:-.03em;
  line-height:1.1}}
p{{margin:0 0 16px;color:var(--ink2)}}
.mono{{font-family:"IBM Plex Mono",monospace}}
.brand{{display:flex;align-items:center;gap:10px;margin-bottom:30px;font-weight:600;
  text-decoration:none;color:var(--ink);letter-spacing:-.02em}}
.brand span{{width:24px;height:24px;border-radius:6px;background-image:url("{PAGE_ICON}");
  background-size:cover}}
.card{{background:var(--raised);border:1px solid var(--rule);border-radius:13px;padding:20px}}
.licence{{font-family:"IBM Plex Mono",monospace;font-size:11.5px;line-height:1.55;
  word-break:break-all;user-select:all;color:var(--ink)}}
.btn{{display:inline-flex;align-items:center;gap:8px;background:var(--ink);color:var(--paper);
  border:0;font:inherit;font-weight:600;font-size:15px;padding:12px 22px;border-radius:9px;
  text-decoration:none;cursor:pointer}}
.btn.secondary{{background:transparent;color:var(--ink);border:1px solid var(--rule)}}
.row{{display:flex;flex-wrap:wrap;gap:10px;margin-top:18px}}
.note{{font-size:13.5px;color:var(--ink3);margin-top:22px}}
.warn{{background:var(--warn-bg);color:var(--warn);border-radius:9px;padding:13px 15px;
  font-size:14px;margin-top:18px}}
a{{color:var(--live)}}
.spin{{display:inline-block;width:15px;height:15px;border:2px solid var(--rule);
  border-top-color:var(--live);border-radius:50%;animation:s .8s linear infinite;
  vertical-align:-2px;margin-right:8px}}
@keyframes s{{to{{transform:rotate(360deg)}}}}
@media (prefers-reduced-motion:reduce){{.spin{{animation:none}}}}
</style>
"""

BUY = PAGE_STYLE + f"""<title>Get FlowState Pro</title>
<meta http-equiv="refresh" content="0;url={CHECKOUT}">
<main>
  <a class="brand" href="{PAGE_HOME}"><span></span> FlowState</a>
  <h1>Taking you to checkout…</h1>
  <p>Payment is handled by Paddle, who are the merchant of record for FlowState.</p>
  <p><a href="{CHECKOUT}">Continue to checkout</a> if this page does not move on its own.</p>
</main>
<script>location.replace("{CHECKOUT}");</script>
"""

THANKS = PAGE_STYLE + f"""<title>Thank you — FlowState</title>
<main>
  <a class="brand" href="{PAGE_HOME}"><span></span> FlowState</a>
  <div id="view">
    <h1><span class="spin"></span>Setting up your licence…</h1>
    <p>This usually takes a few seconds. Leave this page open.</p>
  </div>
</main>
<script>
(function(){{
  var view = document.getElementById("view");
  var txn = new URLSearchParams(location.search).get("_ptxn");
  var SERVICE = "{LICENCE_SERVICE}";

  function escapeText(value) {{
    var node = document.createElement("div");
    node.textContent = value;
    return node.innerHTML;
  }}

  function showLicence(licence) {{
    view.innerHTML =
      '<h1>You&rsquo;re all set.</h1>' +
      '<p>Open FlowState and paste this licence into Settings, or press the button below ' +
      'and FlowState will take it for you.</p>' +
      '<div class="card"><div class="licence" id="lic">' + escapeText(licence) + '</div></div>' +
      '<div class="row">' +
      '<a class="btn" href="flowstate://licence?token=' + encodeURIComponent(licence) + '">Open in FlowState</a>' +
      '<button class="btn secondary" id="copy">Copy licence</button>' +
      '</div>' +
      '<p class="note">Keep this licence somewhere safe. It is also in your receipt email, ' +
      'and FlowState renews it on its own while your subscription is active.</p>';
    document.getElementById("copy").addEventListener("click", function(){{
      navigator.clipboard.writeText(licence).then(function(){{
        document.getElementById("copy").textContent = "Copied";
      }});
    }});
  }}

  // `paid` matters. The reassurance is for somebody whose money has left their account and
  // whose licence has not arrived. Showing it to a person who wandered onto this page
  // without buying anything tells them they have been charged, which is alarming and false.
  function showProblem(title, detail, paid) {{
    view.innerHTML = '<h1>' + title + '</h1><p>' + detail + '</p>' +
      (paid
        ? '<div class="warn">Your payment went through — this is only about delivering ' +
          'the licence. Nothing has been charged twice.</div>' +
          '<p class="note">Your receipt email also carries the licence. If it has not ' +
          'arrived, reply to it and it will be sorted out by hand.</p>'
        : '<p class="note"><a href="{PAGE_HOME}">Back to FlowState</a></p>');
  }}

  if (!txn) {{
    showProblem("Nothing to set up here",
      "This page is where Paddle sends you after a purchase, and it was opened without one.",
      false);
    return;
  }}

  // Paddle's webhook and this redirect race each other, and the browser often wins. 202
  // means the purchase has not reached the licence service yet, so this waits rather than
  // reporting a failure that is really just a few seconds of lag.
  var attempts = 0;
  (function poll(){{
    attempts += 1;
    fetch(SERVICE + "/licence?txn=" + encodeURIComponent(txn))
      .then(function(response){{
        if (response.status === 202) {{
          if (attempts > 20) {{
            showProblem("This is taking longer than it should",
              "Your licence has not come through yet. It will arrive by email shortly.", true);
            return;
          }}
          setTimeout(poll, 2000);
          return;
        }}
        if (!response.ok) {{
          showProblem("Something went wrong",
            "The licence service could not complete your purchase.", true);
          return;
        }}
        return response.json().then(function(body){{
          if (body && body.licence) showLicence(body.licence);
          else showProblem("Something went wrong", "No licence came back.", true);
        }});
      }})
      .catch(function(){{
        if (attempts > 20) {{
          showProblem("Could not reach FlowState",
            "Check your connection. Your licence is also in your receipt email.", true);
          return;
        }}
        setTimeout(poll, 2000);
      }});
  }})();
}})();
</script>
"""

# ── Legal ──────────────────────────────────────────────────────────────────────────────
#
# Paddle requires a seller to publish terms, a refund policy and a support route before it
# will verify the account, and these are also the pages a customer reads when something has
# gone wrong. Written for New Zealand, where FlowState is sold from.
#
# THREE VALUES BELOW ARE YOURS TO CONFIRM. They are deliberately real and working rather
# than obvious placeholders, because a legal page published with "YOUR_COMPANY_HERE" in it
# is worse than one naming a person accurately.

# The legal entity behind FlowState. A sole trader trades under their own name; change this
# if FlowState is ever put into a company, because the entity named here is the one a
# customer would have a contract with.
LEGAL_ENTITY = "Joshua Lafrentz"

# Where support reaches a human. Move this to an address on the FlowState domain once one
# exists — but never leave it pointing somewhere unmonitored, because Paddle checks it and
# customers use it.
LEGAL_CONTACT = "support@flowstatemac.com"

LEGAL_UPDATED = "28 August 2026"

# PAGE_STYLE is already-evaluated f-string output, so its braces are single here. Matching
# on the doubled form silently matches nothing, and the page keeps the vertical centring
# meant for a one-sentence page while carrying two thousand words.
LEGAL_STYLE = PAGE_STYLE.replace(
    "body{margin:0;min-height:100vh;display:flex;align-items:center;justify-content:center;",
    "body{margin:0;min-height:100vh;display:block;",
) + """<style>
body{padding:0}
main{width:min(100%,720px);margin:0 auto;padding:44px 22px 90px}
h2{margin:38px 0 12px;font-size:1.22rem;font-weight:600;letter-spacing:-.02em;line-height:1.25}
h2:first-of-type{margin-top:30px}
p,li{color:var(--ink2)}
ul{margin:0 0 16px;padding-left:20px}
li{margin-bottom:7px}
strong{color:var(--ink);font-weight:600}
.updated{font-family:"IBM Plex Mono",monospace;font-size:12px;color:var(--ink3);
  margin-bottom:0}
.lede{font-size:17.5px;color:var(--ink2)}
.box{background:var(--raised);border:1px solid var(--rule);border-radius:11px;
  padding:16px 18px;margin:20px 0}
.box p:last-child{margin-bottom:0}
footer{margin-top:52px;padding-top:22px;border-top:1px solid var(--rule);
  font-family:"IBM Plex Mono",monospace;font-size:12.5px;color:var(--ink3)}
footer a{color:var(--ink3);margin-right:18px}
</style>
"""

LEGAL_FOOTER = f"""<footer>
  <a href="{PAGE_HOME}">FlowState</a>
  <a href="../terms/">Terms</a>
  <a href="../refunds/">Refunds</a>
  <a href="../privacy/">Privacy</a>
</footer>"""

TERMS = LEGAL_STYLE + f"""<title>Terms of Service — FlowState</title>
<main>
  <a class="brand" href="{PAGE_HOME}"><span></span> FlowState</a>
  <h1>Terms of Service</h1>
  <p class="updated">Last updated {LEGAL_UPDATED}</p>

  <p class="lede">These terms cover your use of FlowState, a macOS application provided by
  {LEGAL_ENTITY}, a sole trader based in New Zealand. Installing or using FlowState means
  you accept them.</p>

  <div class="box">
    <p><strong>Who you buy from.</strong> FlowState is sold through Paddle.com Market Ltd,
    which acts as the <strong>merchant of record</strong>. Your purchase contract is with
    Paddle, and Paddle appears on your bank statement. Paddle handles payment, sales tax and
    VAT, refunds and chargebacks under its own
    <a href="https://www.paddle.com/legal/checkout-buyer-terms">Buyer Terms</a>.
    {LEGAL_ENTITY} licenses the software to you and provides support for it.</p>
  </div>

  <h2>Your licence</h2>
  <p>While your subscription is active you have a personal, non-exclusive, non-transferable
  licence to install and use FlowState on Macs you own or control. The licence is for you;
  it is not sold, and it does not transfer with a resold computer.</p>

  <h2>What you may not do</h2>
  <ul>
    <li>Share, resell, sublicense or publish your licence key. It identifies your
      subscription, and a shared key can be revoked.</li>
    <li>Remove or work around the licensing in the application.</li>
    <li>Use FlowState in a way that breaks New Zealand law, or the law where you are.</li>
  </ul>
  <p>You may inspect the application on your own machine, and you may keep using it after a
  subscription ends within the limits of the free tier described below.</p>

  <h2>Subscription and billing</h2>
  <ul>
    <li>FlowState Pro is <strong>US$7 per month</strong>, billed by Paddle until cancelled.</li>
    <li>A free trial runs inside the application before any payment, and needs no card.</li>
    <li>Cancel at any time. Your subscription keeps working until the end of the period you
      have already paid for; it is not cut short.</li>
    <li>Prices may change. Existing subscribers get at least 30 days' notice by email
      before a change takes effect, and may cancel instead.</li>
  </ul>

  <h2>What happens when a subscription ends</h2>
  <p><strong>Nothing you made is taken away.</strong> Your projects, shortcuts, themes and
  preferences are files on your own Mac and remain yours and readable. FlowState continues
  to run with its free tier: a limited number of projects, and without window arrangement,
  Appearance Studio or AI handoff.</p>

  <h2>Availability and support</h2>
  <p>FlowState is made by one person. Support is by email at
  <a href="mailto:{LEGAL_CONTACT}">{LEGAL_CONTACT}</a>, usually answered within a few working
  days. There is no guaranteed response time and no uptime commitment for the licensing
  service, though it is designed so that a paid copy of FlowState keeps working while that
  service is unreachable.</p>

  <h2>Your rights under New Zealand law</h2>
  <div class="box">
    <p>If you are a consumer in New Zealand, the <strong>Consumer Guarantees Act 1993</strong>
    gives you guarantees that cannot be excluded, and nothing in these terms limits them.
    The <strong>Fair Trading Act 1986</strong> applies as well. Where those Acts conflict
    with anything written here, those Acts win.</p>
    <p>If you acquire FlowState for the purposes of a business, sections 9, 12A, 13 and 14(1)
    of the Fair Trading Act and the Consumer Guarantees Act do not apply, to the extent the
    law permits that agreement.</p>
  </div>

  <h2>Liability</h2>
  <p>Subject to the section above, and to the extent New Zealand law allows: FlowState is
  provided as it is, and {LEGAL_ENTITY}'s total liability for any claim relating to it is
  limited to the amount you paid in the twelve months before the claim. FlowState arranges
  windows and opens applications on your Mac; it does not modify or delete your documents,
  but you remain responsible for your own backups.</p>

  <h2>Ending this agreement</h2>
  <p>You may stop using FlowState at any time. Your licence may be ended if these terms are
  breached — for example by publishing a licence key — in which case a fair portion of any
  unused subscription is refunded.</p>

  <h2>Changes</h2>
  <p>These terms may change as FlowState does. Material changes are announced by email to
  subscribers and dated here. Continuing to use FlowState after a change means accepting it.</p>

  <h2>Governing law</h2>
  <p>These terms are governed by New Zealand law, and the New Zealand courts have
  non-exclusive jurisdiction. If you are a consumer elsewhere, this does not remove any
  protection you have under the law of your own country.</p>

  <h2>Contact</h2>
  <p>{LEGAL_ENTITY} · <a href="mailto:{LEGAL_CONTACT}">{LEGAL_CONTACT}</a><br>
  For billing, refunds or an invoice, contact
  <a href="https://paddle.net">Paddle</a>, who processed the payment.</p>

  {LEGAL_FOOTER}
</main>
"""

REFUNDS = LEGAL_STYLE + f"""<title>Refund Policy — FlowState</title>
<main>
  <a class="brand" href="{PAGE_HOME}"><span></span> FlowState</a>
  <h1>Refund Policy</h1>
  <p class="updated">Last updated {LEGAL_UPDATED}</p>

  <p class="lede">FlowState has a free trial that needs no card, so you can find out whether
  it suits you before paying anything. If you paid and it did not work out, ask and you will
  get your money back.</p>

  <div class="box">
    <p><strong>Refunds are handled by Paddle</strong>, who is the merchant of record for
    every FlowState purchase and the company that charged you. The fastest route is
    <a href="https://paddle.net">paddle.net</a>, where you can find your order using the
    email address you paid with.</p>
  </div>

  <h2>The short version</h2>
  <ul>
    <li><strong>Within 14 days of a payment</strong> — full refund, no reason needed. This
      is Paddle's standard buyer refund window and applies to a first payment or a renewal.</li>
    <li><strong>A renewal you did not intend</strong> — if a subscription renewed and you had
      meant to cancel, say so and it will be refunded. Nobody wants money for a month you
      did not want.</li>
    <li><strong>FlowState does not work on your Mac</strong> — refunded whenever you tell us,
      inside 14 days or not.</li>
  </ul>

  <h2>How to ask</h2>
  <ul>
    <li>Go to <a href="https://paddle.net">paddle.net</a> and look up your order, or</li>
    <li>Email <a href="mailto:{LEGAL_CONTACT}">{LEGAL_CONTACT}</a> and it will be arranged
      for you.</li>
  </ul>
  <p>Refunds go back to the card or account you paid from, and usually appear within five to
  ten working days depending on your bank.</p>

  <h2>Cancelling instead</h2>
  <p>Cancelling stops the next payment and is not the same as a refund. Your subscription
  keeps working until the end of the period you have already paid for, and FlowState then
  returns to its free tier. Nothing you have created is removed.</p>

  <h2>Your rights under New Zealand law</h2>
  <div class="box">
    <p>Nothing here limits your rights under the <strong>Consumer Guarantees Act 1993</strong>.
    If FlowState is faulty, does not match how it was described, or is not fit for the purpose
    it was sold for, you are entitled to a remedy under that Act regardless of the 14 days
    above — and if the failure is substantial, you may choose a refund.</p>
    <p>If you bought from outside New Zealand, your own consumer law may give you further
    rights, including a statutory right of withdrawal in the EU and UK. Those apply on top of
    this policy, not instead of it.</p>
  </div>

  <h2>Contact</h2>
  <p>{LEGAL_ENTITY} · <a href="mailto:{LEGAL_CONTACT}">{LEGAL_CONTACT}</a></p>

  {LEGAL_FOOTER}
</main>
"""

PRIVACY = LEGAL_STYLE + f"""<title>Privacy Policy — FlowState</title>
<main>
  <a class="brand" href="{PAGE_HOME}"><span></span> FlowState</a>
  <h1>Privacy Policy</h1>
  <p class="updated">Last updated {LEGAL_UPDATED}</p>

  <p class="lede">FlowState is built to know as little about you as possible. The application
  has no account, no analytics and no telemetry, and your projects never leave your Mac.
  This page says exactly what does exist, because a privacy policy that only makes promises
  is not much use.</p>

  <h2>What stays on your Mac</h2>
  <p>Everything you create in FlowState — projects, folder paths, shortcuts, websites,
  themes and preferences — is stored in files in your own Application Support folder. It is
  never uploaded, never synced, and never seen by anyone else. Deleting FlowState and that
  folder removes it completely.</p>

  <h2>What FlowState sends, and when</h2>
  <ul>
    <li><strong>Without a subscription: nothing.</strong> A free or trial copy of FlowState
      makes no network requests of its own at all.</li>
    <li><strong>With a subscription:</strong> FlowState contacts its own licensing service to
      renew your licence, roughly once a month. It sends the licence it already holds, and
      nothing else — no projects, no paths, no usage.</li>
  </ul>
  <p>Opening a link or launching a workspace opens your own browser and applications. Those
  connections are between you and those sites, exactly as if you had opened them yourself.</p>

  <h2>The licensing service</h2>
  <p>When you subscribe, a small service run for FlowState stores the minimum needed to know
  that your subscription is live:</p>
  <ul>
    <li>Your Paddle customer and subscription identifiers</li>
    <li>The email address you used at checkout</li>
    <li>Whether the subscription is active, and when that was last updated</li>
  </ul>
  <p>It holds <strong>no card details, no address and no name</strong> — Paddle has those,
  and does not pass them on. The service runs on Cloudflare Workers. The records are kept
  while your subscription exists and removed when it has been over for 90 days.</p>

  <h2>Payment</h2>
  <p>Payments are taken by <strong>Paddle.com Market Ltd</strong>, the merchant of record for
  FlowState. Your card details go to Paddle and never to {LEGAL_ENTITY} — they are never seen
  by, or stored on, anything FlowState runs. Paddle's handling of your information is covered
  by its own <a href="https://www.paddle.com/legal/privacy">Privacy Notice</a>.</p>

  <h2>The website and downloads</h2>
  <p>This site has no analytics, no cookies and no trackers. It is hosted on GitHub Pages,
  and downloads come from GitHub Releases; both keep standard server logs, including IP
  addresses, under <a href="https://docs.github.com/site-policy/privacy-policies/github-privacy-statement">GitHub's
  privacy statement</a>. The site loads fonts from Google Fonts, which sees the request for
  the font file.</p>

  <h2>Permissions FlowState asks for</h2>
  <ul>
    <li><strong>Accessibility</strong> — to move and resize windows on your screen. It reads
      window positions to put them back afterwards. Nothing is recorded or sent, and
      declining it leaves everything else working.</li>
    <li><strong>Automation</strong> — asked for only if you have FlowState open a workspace
      link in a new Safari or Chrome window. It sends that browser a URL and nothing more.</li>
  </ul>
  <p>Both can be withdrawn at any time in System Settings, and FlowState keeps running.</p>

  <h2>Your rights</h2>
  <div class="box">
    <p>FlowState is operated from New Zealand and follows the <strong>Privacy Act 2020</strong>.
    You may ask what information is held about you, ask for it to be corrected, or ask for it
    to be deleted — email <a href="mailto:{LEGAL_CONTACT}">{LEGAL_CONTACT}</a> and you will
    have an answer within 20 working days.</p>
    <p>If you are not satisfied with the response, you may complain to the
    <a href="https://www.privacy.org.nz">Office of the Privacy Commissioner</a>. If you are in
    the EU or UK, you have equivalent rights under the GDPR, and Paddle acts as the controller
    for payment information.</p>
  </div>

  <h2>Changes</h2>
  <p>This page is dated, and is revised whenever FlowState starts or stops sending anything.
  Material changes are announced by email to subscribers.</p>

  <h2>Contact</h2>
  <p>{LEGAL_ENTITY} · <a href="mailto:{LEGAL_CONTACT}">{LEGAL_CONTACT}</a></p>

  {LEGAL_FOOTER}
</main>
"""

# Explicit encoding on both ends: the document declares UTF-8 in its first bytes and is
# written as UTF-8 regardless of the locale of the machine building it. The page carried
# neither before and rendered only because GitHub Pages happens to send a charset header —
# opened from a file, or served by anything that does not, every em dash broke.
with open("site/index.html", "w", encoding="utf-8") as f:
    f.write(HEAD + BODY)

# Directories rather than buy.html, so /buy and /buy/ both resolve on GitHub Pages without
# depending on its extension-guessing.
for name, page in (("buy", BUY), ("thanks", THANKS),
                   ("terms", TERMS), ("refunds", REFUNDS), ("privacy", PRIVACY)):
    os.makedirs(f"site/{name}", exist_ok=True)
    with open(f"site/{name}/index.html", "w", encoding="utf-8") as f:
        f.write(page)
    print(f"  site/{name}/index.html written")
size = os.path.getsize("site/index.html")
print(f"  site/index.html written: {size/1024:.1f} KB")
