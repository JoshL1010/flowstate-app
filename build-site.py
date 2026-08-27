import base64, os, re

MEDIA = "site/media"
def uri(name):
    ext = name.rsplit(".",1)[1]
    mime = "video/mp4" if ext=="mp4" else "image/jpeg"
    with open(os.path.join(MEDIA,name),"rb") as f:
        return f"data:{mime};base64," + base64.b64encode(f.read()).decode()

V = {n: uri(f"{n}.mp4") for n in ("reveal","launch","configure","appearance")}
P = {n: uri(f"{n}.jpg") for n in ("reveal","launch","configure","appearance")}
ICON = uri("icon.png")

HEAD = f'''<title>FlowState for Mac</title>
<meta name="description" content="A native macOS workspace launcher. Opens the editor, terminal, repository and pages a project needs \u2014 arranged \u2014 in one keystroke. Free while in beta.">
<link rel="icon" href="{ICON}">
<link rel="apple-touch-icon" href="{ICON}">
<meta property="og:type" content="website">
<meta property="og:title" content="FlowState for Mac">
<meta property="og:description" content="Every project you own, one keystroke away. A macOS workspace launcher that waits at the edge of your screen.">
<meta property="og:image" content="https://joshl1010.github.io/flowstate-app/media/og.jpg">
<meta property="og:url" content="https://joshl1010.github.io/flowstate-app/">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="FlowState for Mac">
<meta name="twitter:description" content="Every project you own, one keystroke away.">
<meta name="twitter:image" content="https://joshl1010.github.io/flowstate-app/media/og.jpg">
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
  --ease:cubic-bezier(.22,.9,.28,1);
}}
@media (prefers-color-scheme:dark){{:root:not([data-theme="light"]){{
  --paper:#070B0D;--raised:#10161A;--sunk:#0B1113;
  --ink:#EDEFEB;--ink2:#98A2A5;--ink3:#667073;
  --rule:#1C2326;--rule2:#313A3E;
  --live:#5CBBF2;--live-soft:#0B2839;
  --sh:0 2px 4px rgba(0,0,0,.5),0 28px 70px rgba(0,0,0,.6);
}}}}
:root[data-theme="dark"]{{
  --paper:#070B0D;--raised:#10161A;--sunk:#0B1113;
  --ink:#EDEFEB;--ink2:#98A2A5;--ink3:#667073;
  --rule:#1C2326;--rule2:#313A3E;
  --live:#5CBBF2;--live-soft:#0B2839;
  --sh:0 2px 4px rgba(0,0,0,.5),0 28px 70px rgba(0,0,0,.6);
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
.nav-in{{display:flex;align-items:center;padding:16px 0}}
.logo{{display:flex;align-items:center;gap:10px;font-weight:600;letter-spacing:-.02em;
  text-decoration:none;color:var(--ink)}}
.logo-mark{{width:26px;height:26px;flex:none;border-radius:6px;
  background-image:url("{ICON}");background-size:cover}}
.btn{{display:inline-flex;align-items:center;gap:9px;border:1px solid transparent;font-weight:600;
  font-size:15px;padding:11px 20px;border-radius:9px;text-decoration:none;cursor:pointer;
  transition:transform .18s var(--ease),box-shadow .18s,border-color .18s}}
.btn-solid{{background:var(--ink);color:var(--paper)}}
.btn-solid:hover{{transform:translateY(-2px);box-shadow:0 10px 26px rgba(8,13,16,.26)}}
.btn-line{{background:transparent;color:var(--ink);border-color:var(--rule2)}}
.btn-line:hover{{border-color:var(--ink);transform:translateY(-2px)}}
.btn-lg{{font-size:16px;padding:15px 30px;border-radius:11px}}
nav .btn{{margin-left:auto}}

.hero{{padding:clamp(104px,14vw,180px) 0 0}}
.hero h1{{font-size:clamp(2.9rem,7.8vw,6.4rem);max-width:13ch;letter-spacing:-.04em}}
.hero h1 .soft{{color:var(--ink3)}}
.hero .sub{{margin-top:30px;font-size:clamp(17px,1.75vw,19.5px);color:var(--ink2);max-width:45ch}}
.cta{{display:flex;flex-wrap:wrap;gap:15px 18px;align-items:center;margin-top:38px}}
.note{{font-family:"IBM Plex Mono",monospace;font-size:12px;color:var(--ink3)}}

/* video frames — the product, shown rather than described */
.screen{{position:relative;border-radius:14px;overflow:hidden;border:1px solid var(--rule2);
  box-shadow:var(--sh);background:var(--sa);line-height:0}}
.screen video{{width:100%;height:auto;display:block}}
.hero-screen{{margin-top:clamp(44px,5.5vw,72px)}}

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
  font-family:"IBM Plex Mono",monospace;display:flex;flex-wrap:wrap;gap:8px 26px}}

@media (prefers-reduced-motion:reduce){{
  html{{scroll-behavior:auto}}
  *,*::before,*::after{{transition-duration:.01ms!important;animation:none!important}}
  .rv{{opacity:1;transform:none}}
}}
</style>
'''

def screen(name, cls=""):
    return (f'<div class="screen {cls}">'
            f'<video muted playsinline loop preload="none" poster="{P[name]}" '
            f'data-src="{V[name]}"></video></div>')

BODY = f'''
<nav id="nav"><div class="wrap nav-in">
  <a class="logo" href="#top"><span class="logo-mark"></span> FlowState</a>
  <a class="btn btn-line" href="https://github.com/JoshL1010/flowstate-app/releases/download/v0.2.0/FlowState-0.2.0.dmg">Download</a>
</div></nav>

<div id="top" class="hero"><div class="wrap">
  <h1 class="rv rv-u">Every project you own,<br><span class="soft">one keystroke away.</span></h1>
  <p class="sub rv rv-u" style="--i:1">
    FlowState waits at the edge of your screen. Call it and it opens the editor, the terminal,
    the repository and the pages a project needs — arranged, and gone again before you have
    finished thinking.
  </p>
  <div class="cta rv rv-u" style="--i:2">
    <a class="btn btn-solid btn-lg" href="https://github.com/JoshL1010/flowstate-app/releases/download/v0.2.0/FlowState-0.2.0.dmg">Download for macOS</a>
    <span class="note">Free in beta · macOS 15 or later · 2.7 MB</span>
  </div>
  <div class="hero-screen rv rv-s" style="--i:3">{screen("reveal")}</div>
</div></div>

<div class="story"><div class="wrap sgrid">
  <div class="scopy rv rv-l">
    <div class="step">01 — REVEAL</div>
    <h2>No window to manage.</h2>
    <p>Rest the pointer against the side of the screen, or press a shortcut you choose.
      There is no Dock icon and nothing to arrange. It appears when you want it and is gone
      the moment you look away.</p>
  </div>
  <div class="rv rv-r" style="--i:1">{screen("launch")}</div>
</div></div>

<div class="story flip"><div class="wrap sgrid">
  <div class="scopy rv rv-r">
    <div class="step">02 — LAUNCH</div>
    <h2>One action opens all of it.</h2>
    <p>The editor at the right folder. Terminal already in the working directory. The
      repository and the pages you keep reopening — every one of them, in the order you set,
      with the main windows arranged side by side.</p>
  </div>
  <div class="rv rv-l" style="--i:1">{screen("configure")}</div>
</div></div>

<div class="story"><div class="wrap sgrid">
  <div class="scopy rv rv-l">
    <div class="step">03 — MAKE IT YOURS</div>
    <h2>Built to sit on your screen all day.</h2>
    <p>Eight palettes or your own colours, with width, density, text size, corners and motion
      to match. The preview updates as you drag, and a theme you like can be saved and handed
      to someone else.</p>
  </div>
  <div class="rv rv-r" style="--i:1">{screen("appearance")}</div>
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
    <tr><th scope="row">Network</th><td>None. FlowState makes no network requests.</td></tr>
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
    <a class="btn btn-solid btn-lg" href="https://github.com/JoshL1010/flowstate-app/releases/download/v0.2.0/FlowState-0.2.0.dmg">Download FlowState 0.2.0</a>
    <span class="note">macOS 15+ · Apple silicon &amp; Intel · 2.7 MB</span>
  </div>
</div></div>

<footer><div class="wrap" style="display:flex;flex-wrap:wrap;gap:8px 26px">
  <span>FlowState 0.2.0 beta</span><span>Swift &amp; SwiftUI</span><span>Made for macOS</span>
</div></footer>

<script>
(function(){{
  var reduce = matchMedia("(prefers-reduced-motion: reduce)").matches;

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

  // Clips are heavy, so each one is attached and started only when it is actually on
  // screen, and paused again when it leaves. Nothing downloads until it is needed.
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

open("site/index.html","w").write(HEAD + BODY)
size = os.path.getsize("site/index.html")
print(f"  site/index.html written: {size/1_000_000:.2f} MB")
