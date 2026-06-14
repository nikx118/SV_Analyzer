CSS = open("style.css", encoding="utf-8").read()

HEAD = f"""<!DOCTYPE html>
<html><head><meta charset="utf-8">
{CSS}
<style>
html, body {{ margin:0; overflow:hidden; }}
.stApp {{ padding: 28px 40px; min-height: 100vh; box-sizing: border-box; }}
.tabs {{ display:flex; gap:28px; border-bottom:1px solid rgba(255,255,255,0.1); margin-bottom:24px; }}
.tab {{ padding-bottom:10px; font-weight:600; font-size:0.95rem; color:#9ca3af; }}
.tab.active {{ color:#ff4b4b; border-bottom:2px solid #ff4b4b; }}
h3.section-title {{ color:#e8eaf6; font-weight:700; margin-bottom:4px; }}
p.section-sub {{ color:#9ca3af; font-size:0.9rem; margin-top:0; }}
.bar-row {{ display:flex; align-items:center; margin-bottom:14px; }}
.bar-label {{ width:160px; text-align:right; padding-right:14px; color:#e8eaf6; font-size:0.85rem; }}
.bar-track {{ flex:1; position:relative; height:26px; }}
.bar-fill {{ height:26px; border-radius:3px; display:flex; align-items:center; }}
.bar-val {{ margin-left:10px; color:#e8eaf6; font-size:0.85rem; font-weight:600; }}
.axis {{ display:flex; margin-left:160px; padding-left:14px; color:#9ca3af; font-size:0.78rem; justify-content:space-between; max-width:520px; padding-top:6px; border-top:1px solid rgba(255,255,255,0.08); }}
</style>
</head><body><div class="stApp">
"""

TAIL = "</div></body></html>"

HEADER_BANNER = """
<div class="main-header">
  <h1>🏡 Site Visit Analyzer</h1>
  <p>AI-powered real estate sales coaching &amp; Voice of Customer intelligence</p>
  <span class="property-badge">📍 Sunrise Residences · Whitefield, Bangalore</span>
</div>
"""
