import re, json, base64
from io import BytesIO
import streamlit as st
import streamlit.components.v1 as components
from PIL import Image
from model import chat_stream, pil_to_base64_url, text_message, image_message, get_api_key_display

st.set_page_config(page_title="Ask DeX", page_icon="✨", layout="wide", initial_sidebar_state="collapsed")

for k, v in [("messages",[]),("pending_prompt",""),("pending_img_b64","")]:
    if k not in st.session_state: st.session_state[k] = v

def pil_from_b64(b64):
    _, data = b64.split(",",1)
    return Image.open(BytesIO(base64.b64decode(data)))

st.markdown("""<style>
html,body,[data-testid="stAppViewContainer"],[data-testid="stMain"],.main,.block-container,
[data-testid="stVerticalBlock"],[data-testid="stVerticalBlockBorderWrapper"]{
  background:#0d1117!important;padding:0!important;margin:0!important;}
.block-container{max-width:100%!important;}
#MainMenu,footer,header,[data-testid="stToolbar"],[data-testid="stDecoration"],
[data-testid="stStatusWidget"],section[data-testid="stSidebar"],
[data-testid="collapsedControl"],[data-testid="stBottom"]{display:none!important;}
div[data-testid="stVerticalBlock"]>div{padding:0!important;gap:0!important;}
</style>""", unsafe_allow_html=True)

if st.session_state.pending_prompt:
    prompt, img_b64 = st.session_state.pending_prompt, st.session_state.pending_img_b64
    st.session_state.pending_prompt = st.session_state.pending_img_b64 = ""
    img_url = None
    if img_b64:
        try: img_url = pil_to_base64_url(pil_from_b64(img_b64))
        except: img_url = img_b64
    st.session_state.messages.append({"role":"user","content":prompt,"image_url":img_url})
    api_hist = [image_message(m["role"],m["content"],m["image_url"]) if m.get("image_url")
                else text_message(m["role"],m["content"]) for m in st.session_state.messages]
    full = ""
    try:
        for chunk in chat_stream(api_hist): full += chunk
    except Exception as e: full = f"⚠️ Error: {e}"
    st.session_state.messages.append({"role":"assistant","content":full})

msgs_json = json.dumps([{"role":m["role"],"content":m["content"],"image_url":m.get("image_url","")}
                         for m in st.session_state.messages], ensure_ascii=False)
api_key = get_api_key_display()

PAGE = f"""<!DOCTYPE html><html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Ask DeX</title>
<link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>✨</text></svg>">
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
*{{box-sizing:border-box;margin:0;padding:0;}}
:root{{--bg:#0d1117;--sf:#161b22;--bd:#21262d;--bd2:#30363d;--tx:#e6edf3;--mt:#8b949e;--ac:#29b6f6;--ub:#1f6feb;}}
html,body{{background:var(--bg);color:var(--tx);font-family:'Inter',sans-serif;height:100vh;overflow:hidden;display:flex;flex-direction:column;}}
#main{{flex:1;overflow-y:auto;display:flex;flex-direction:column;align-items:center;padding-bottom:90px;scrollbar-width:thin;scrollbar-color:var(--bd) transparent;}}
#main::-webkit-scrollbar{{width:4px;}}#main::-webkit-scrollbar-thumb{{background:var(--bd);border-radius:4px;}}
#hero{{display:flex;flex-direction:column;align-items:center;justify-content:center;flex:1;min-height:calc(100vh - 90px);width:100%;padding:0 20px;}}
.logo{{display:flex;align-items:center;gap:12px;margin-bottom:10px;}}
.logo-icon{{font-size:2.6rem;line-height:1;}}
.logo-text{{font-size:2.7rem;font-weight:700;letter-spacing:-0.5px;}}
.logo-sub{{color:var(--mt);font-size:.97rem;margin-bottom:32px;}}
.cards{{display:grid;grid-template-columns:1fr 1fr;gap:10px;width:640px;max-width:92vw;}}
.card{{background:var(--sf);border:1px solid var(--bd);border-radius:12px;padding:16px 18px 14px;cursor:pointer;transition:border-color .18s,background .18s,transform .14s;user-select:none;}}
.card:hover{{border-color:var(--ac);background:#1a2233;transform:translateY(-2px);}}
.card-title{{font-size:.88rem;font-weight:600;display:flex;align-items:center;gap:7px;margin-bottom:5px;}}
.card-desc{{font-size:.79rem;color:var(--mt);line-height:1.45;}}
#chat{{display:none;flex-direction:column;gap:20px;width:660px;max-width:92vw;padding:28px 0 4px;}}
.row{{display:flex;align-items:flex-start;gap:10px;}}
.row.user{{flex-direction:row-reverse;}}.row.ai{{flex-direction:row;}}
.ai-avatar{{width:36px;height:36px;background:var(--sf);border:1px solid var(--bd);border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:1.1rem;flex-shrink:0;margin-top:2px;}}
.bubble{{border-radius:16px;padding:10px 15px;font-size:.875rem;line-height:1.65;max-width:80%;word-break:break-word;}}
.bubble.user{{background:var(--ub);color:#fff;border-radius:18px 18px 5px 18px;}}
.bubble.ai{{background:var(--sf);border:1px solid var(--bd);border-radius:5px 18px 18px 18px;}}
.bubble.ai code{{background:var(--bg);border:1px solid var(--bd2);border-radius:4px;padding:1px 5px;font-size:.82em;}}
.bubble.ai pre{{background:var(--bg);border:1px solid var(--bd2);border-radius:8px;padding:12px;overflow-x:auto;margin:8px 0;font-size:.82em;}}
.bubble img{{max-width:220px;border-radius:8px;display:block;margin-bottom:6px;}}
.dots{{display:flex;gap:5px;padding:4px 2px;}}
.dots span{{width:7px;height:7px;background:var(--ac);border-radius:50%;animation:pulse 1.2s infinite;}}
.dots span:nth-child(2){{animation-delay:.2s;}}.dots span:nth-child(3){{animation-delay:.4s;}}
@keyframes pulse{{0%,80%,100%{{opacity:.2;transform:scale(.8);}}40%{{opacity:1;transform:scale(1);}}}}
#bar{{position:fixed;bottom:0;left:0;right:0;background:var(--bg);padding:10px 0 14px;display:flex;flex-direction:column;align-items:center;z-index:200;}}
#img-preview{{display:none;width:660px;max-width:92vw;background:var(--sf);border:1px solid var(--bd);border-radius:8px;padding:6px 14px;margin-bottom:8px;font-size:.77rem;color:var(--mt);align-items:center;gap:10px;}}
#img-preview img{{height:40px;border-radius:5px;object-fit:cover;}}
#img-preview .rm{{margin-left:auto;background:none;border:none;color:var(--mt);cursor:pointer;font-size:1rem;transition:color .15s;}}
#img-preview .rm:hover{{color:#f85149;}}
.pill{{width:660px;max-width:92vw;background:var(--sf);border:1px solid var(--bd2);border-radius:40px;display:flex;align-items:center;padding:5px 5px 5px 16px;gap:8px;transition:border-color .2s,box-shadow .2s;}}
.pill:focus-within{{border-color:var(--ac);box-shadow:0 0 0 3px rgba(41,182,246,.1);}}
.attach{{background:none;border:none;color:var(--mt);cursor:pointer;display:flex;align-items:center;padding:4px;flex-shrink:0;transition:color .15s;}}
.attach:hover{{color:var(--ac);}}
#txt{{flex:1;background:none;border:none;outline:none;color:var(--tx);font-size:.93rem;font-family:'Inter',sans-serif;caret-color:var(--ac);}}
#txt::placeholder{{color:#484f58;}}
.send{{width:34px;height:34px;background:var(--ac);border:none;border-radius:50%;cursor:pointer;flex-shrink:0;display:flex;align-items:center;justify-content:center;transition:background .15s,transform .15s;}}
.send:hover{{background:#7dd3fc;transform:scale(1.08);}}.send svg{{fill:#0d1117;display:block;}}
</style></head><body>

<div id="main">
  <div id="hero">
    <div class="logo">
      <span class="logo-icon">✨</span>
      <span class="logo-text">Ask DeX</span>
    </div>
    <div class="logo-sub">What can I help you with?</div>
    <div class="cards">
      <div class="card" onclick="useCard(this)">
        <div class="card-title">🧠 Creative Vision</div>
        <div class="card-desc">Describe a scene and suggest improvements.</div>
        <span class="card-prompt" style="display:none">Describe this scene and suggest creative improvements.</span>
      </div>
      <div class="card" onclick="useCard(this)">
        <div class="card-title">🖹 OCR Extract</div>
        <div class="card-desc">Turn a document photo into clean text.</div>
        <span class="card-prompt" style="display:none">Extract and clean all text from this image.</span>
      </div>
      <div class="card" onclick="useCard(this)">
        <div class="card-title">🔧 Debug Code</div>
        <div class="card-desc">Analyze a screenshot to find the error.</div>
        <span class="card-prompt" style="display:none">Analyze this screenshot and identify the bug or error.</span>
      </div>
      <div class="card" onclick="useCard(this)">
        <div class="card-title">📊 Data Insights</div>
        <div class="card-desc">Explain the trends in this chart.</div>
        <span class="card-prompt" style="display:none">Explain the trends and key insights in this chart.</span>
      </div>
    </div>
  </div>
  <div id="chat"></div>
</div>

<div id="bar">
  <div id="img-preview">
    <img id="prev-img" src="" alt="">
    <span id="prev-name"></span>
    <button class="rm" onclick="clearImg()">✕</button>
  </div>
  <div class="pill">
    <button class="attach" onclick="document.getElementById('file-in').click()" title="Attach image">
      <svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <path d="M21.44 11.05l-9.19 9.19a6 6 0 01-8.49-8.49l9.19-9.19a4 4 0 015.66 5.66L9.41 17.41a2 2 0 01-2.83-2.83l8.49-8.48"/>
      </svg>
    </button>
    <input id="txt" type="text" placeholder="Ask anything" autocomplete="off"
           onkeydown="if(event.key==='Enter'&&!event.shiftKey){{event.preventDefault();send();}}">
    <button class="send" onclick="send()">
      <svg width="14" height="14" viewBox="0 0 24 24"><path d="M2 21l21-9L2 3v7l15 2-15 2z"/></svg>
    </button>
  </div>
  <input id="file-in" type="file" accept="image/*" style="display:none" onchange="handleFile(this)">
</div>

<input type="hidden" id="_ak" value="{api_key}">

<script>
const MSGS={msgs_json};
const heroEl=document.getElementById('hero'), chatEl=document.getElementById('chat'),
      mainEl=document.getElementById('main'), txtEl=document.getElementById('txt');
let pendingImg='', streaming=false;

(function init(){{
  if(!MSGS.length) return;
  heroEl.style.display='none'; chatEl.style.display='flex';
  MSGS.forEach(m=>addBubble(m.role,m.content,m.image_url));
  scrollEnd();
}})();

function fmt(t){{
  t=t.replace(/<think>[\s\S]*?<\/think>/g,'').trim();
  t=t.replace(/```[a-z]*\\n?([\\s\\S]*?)```/g,'<pre><code>$1</code></pre>');
  t=t.replace(/`([^`]+)`/g,'<code>$1</code>');
  t=t.replace(/\*\*(.*?)\*\*/g,'<strong>$1</strong>');
  return t.replace(/\\n/g,'<br>');
}}

function addBubble(role,content,imgUrl){{
  const row=document.createElement('div'); row.className='row '+role;
  if(role==='ai'){{ const av=document.createElement('div'); av.className='ai-avatar'; av.textContent='✨'; row.appendChild(av); }}
  const bub=document.createElement('div'); bub.className='bubble '+role;
  if(imgUrl){{ const img=document.createElement('img'); img.src=imgUrl; bub.appendChild(img); }}
  if(role==='ai') bub.innerHTML+=fmt(content);
  else {{ const s=document.createElement('span'); s.textContent=content; bub.appendChild(s); }}
  row.appendChild(bub); chatEl.appendChild(row); return bub;
}}

function showTyping(){{
  const row=document.createElement('div'); row.id='typing-row'; row.className='row ai';
  const av=document.createElement('div'); av.className='ai-avatar'; av.textContent='✨';
  const bub=document.createElement('div'); bub.className='bubble ai';
  bub.innerHTML='<div class="dots"><span></span><span></span><span></span></div>';
  row.appendChild(av); row.appendChild(bub); chatEl.appendChild(row); scrollEnd();
}}
function rmTyping(){{ const el=document.getElementById('typing-row'); if(el) el.remove(); }}

// Fix: read prompt from hidden span inside card, set in txt, focus
function useCard(card){{
  const prompt=card.querySelector('.card-prompt').textContent;
  txtEl.value=prompt;
  txtEl.focus();
  // Scroll pill into view
  document.getElementById('bar').scrollIntoView({{behavior:'smooth'}});
}}

function handleFile(inp){{
  const f=inp.files[0]; if(!f) return;
  const r=new FileReader();
  r.onload=e=>{{ pendingImg=e.target.result;
    document.getElementById('prev-img').src=pendingImg;
    document.getElementById('prev-name').textContent=f.name;
    document.getElementById('img-preview').style.display='flex'; }};
  r.readAsDataURL(f);
}}
function clearImg(){{ pendingImg=''; document.getElementById('img-preview').style.display='none'; document.getElementById('file-in').value=''; }}

async function send(){{
  if(streaming) return;
  const text=txtEl.value.trim(); if(!text) return;
  txtEl.value=''; const img=pendingImg; clearImg();
  heroEl.style.display='none'; chatEl.style.display='flex';
  addBubble('user',text,img); scrollEnd();
  streaming=true; showTyping();
  const history=[...MSGS,{{role:'user',content:text,image_url:img||''}}];
  const apiMsgs=history.map(m=>m.image_url
    ? {{role:m.role==='ai'?'assistant':m.role,content:[{{type:'text',text:m.content}},{{type:'image_url',image_url:{{url:m.image_url}}}}]}}
    : {{role:m.role==='ai'?'assistant':m.role,content:[{{type:'text',text:m.content}}]}});
  const sys={{role:'system',content:'You are Ask DeX, a powerful multimodal AI assistant built by Madhanadeva D. If asked who created you, answer "Madhanadeva D.". Analyze images, solve STEM, perform OCR, convert UI to code. Be accurate and concise.'}};
  const ak=document.getElementById('_ak').value;
  let full='';
  try{{
    const resp=await fetch('https://openrouter.ai/api/v1/chat/completions',{{
      method:'POST',
      headers:{{'Content-Type':'application/json','Authorization':'Bearer '+ak,'HTTP-Referer':window.location.href,'X-Title':'AskDeX'}},
      body:JSON.stringify({{model:'qwen/qwen3-vl-235b-a22b-thinking',messages:[sys,...apiMsgs],max_tokens:2048,temperature:0.7,stream:true}})
    }});
    rmTyping();
    const row=document.createElement('div'); row.className='row ai';
    const av=document.createElement('div'); av.className='ai-avatar'; av.textContent='✨';
    const bub=document.createElement('div'); bub.className='bubble ai';
    row.appendChild(av); row.appendChild(bub); chatEl.appendChild(row);
    const reader=resp.body.getReader(); const dec=new TextDecoder();
    while(true){{
      const {{done,value}}=await reader.read(); if(done) break;
      for(const line of dec.decode(value).split('\\n')){{
        const l=line.trim();
        if(!l||l==='data: [DONE]') continue;
        if(l.startsWith('data: ')){{
          try{{ const d=JSON.parse(l.slice(6)); const c=d?.choices?.[0]?.delta?.content||''; if(c){{full+=c;bub.innerHTML=fmt(full);scrollEnd();}} }}catch(e){{}}
        }}
      }}
    }}
    MSGS.push({{role:'user',content:text,image_url:img||''}});
    MSGS.push({{role:'ai',content:full,image_url:''}});
  }}catch(e){{ rmTyping(); addBubble('ai','⚠️ Error: '+e.message,''); }}
  streaming=false; scrollEnd();
}}

function scrollEnd(){{ setTimeout(()=>mainEl.scrollTop=mainEl.scrollHeight,30); }}
</script></body></html>"""

components.html(PAGE, height=620, scrolling=False)