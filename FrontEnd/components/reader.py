import json
from config import paper_bg, paper_ink, paper_border, cyan_color, accent_color

def build_reader_html(text: str) -> str:
    # Clean the text safely for JS injection
    clean_text = text.replace('*', '').replace('#', '').replace('\n', ' ')
    safe_text = json.dumps(clean_text)

    # Added the KeepAlive Interval to stop Google Chrome from glitching out on long reads!
    return f"""
    <html>
    <head>
    <style>
        @font-face {{ font-family: 'OpenDyslexic'; src: url('https://cdn.jsdelivr.net/gh/antijingoist/opendyslexic@master/compiled/OpenDyslexic-Regular.otf') format('opentype'); }}
        body {{ font-family: 'OpenDyslexic', sans-serif; background-color: {paper_bg}; color: {paper_ink}; padding: 20px 24px; border-radius: 10px; margin: 0; border: 1px solid {paper_border}; }}
        .highlight {{ background-color: {cyan_color}; color: #0E1117; font-weight: bold; border-radius: 4px; padding: 2px 4px; box-shadow: 0 0 8px rgba(0,229,255,0.5); transition: background-color 0.1s ease; }}
        #progress-container {{ width: 100%; background-color: {paper_border}; border-radius: 8px; margin-bottom: 16px; height: 8px; overflow: hidden; }}
        #progress-bar {{ width: 0%; height: 100%; background-color: {accent_color}; transition: width 0.1s linear; }}
        .controls {{ margin-bottom: 16px; display: flex; gap: 12px; align-items: center; font-family: 'Segoe UI', sans-serif; }}
        button {{ background-color: {cyan_color}; color: #0E1117; border: none; padding: 6px 14px; border-radius: 16px; font-family: 'Segoe UI', sans-serif; font-weight: bold; cursor: pointer; transition: 0.2s; font-size: 0.85rem; }}
        button:hover {{ background-color: {accent_color}; }}
        #status {{ font-family: 'Segoe UI', sans-serif; font-size: 0.85rem; }}
    </style>
    </head>
    <body>
    <div id="progress-container"><div id="progress-bar"></div></div>
    <div class="controls">
        <button id="play-pause-btn" onclick="togglePlayPause()">⏸️ Pause Reading</button>
        <span id="status" style="color: #4E7A67; font-weight: bold;">🔊 Speaking...</span>
    </div>
    <div id="text-display" style="font-size: 20px; line-height: 1.8;"></div>

    <script>
        const rawText = {safe_text};
        const display = document.getElementById("text-display");
        const progressBar = document.getElementById("progress-bar");
        const status = document.getElementById("status");
        const playPauseBtn = document.getElementById("play-pause-btn");

        const words = rawText.split(/(\\s+)/); 
        display.innerHTML = words.map((w, i) => `<span id="word-${{i}}">${{w}}</span>`).join('');

        const synth = window.parent.speechSynthesis || window.speechSynthesis;
        synth.cancel();

        let msg = new SpeechSynthesisUtterance(rawText);
        msg.lang = 'en-US';
        msg.rate = 0.9; 
        
        let keepAlive; // 🚨 Fixes the Chrome 15-second cut-off glitch

        msg.onstart = () => {{
            // Resets Chrome's internal TTS timer every 10 seconds
            keepAlive = setInterval(() => {{
                synth.pause();
                synth.resume();
            }}, 10000);
        }};

        msg.onboundary = (event) => {{
            if(event.name === 'word') {{
                const pct = (event.charIndex / rawText.length) * 100;
                progressBar.style.width = pct + "%";

                let charCount = 0;
                for (let i = 0; i < words.length; i++) {{
                    charCount += words[i].length;
                    if (charCount > event.charIndex) {{
                        document.querySelectorAll('.highlight').forEach(el => el.classList.remove('highlight'));
                        const activeWord = document.getElementById(`word-${{i}}`);
                        if(activeWord && activeWord.innerText.trim().length > 0) {{
                            activeWord.classList.add('highlight');
                            // Ensure the word scrolls into view
                            activeWord.scrollIntoView({{ behavior: "smooth", block: "center" }});
                        }}
                        break;
                    }}
                }}
            }}
        }};

        msg.onend = () => {{
            clearInterval(keepAlive);
            progressBar.style.width = "100%";
            status.innerText = "✅ Finished";
            playPauseBtn.style.display = "none"; 
            document.querySelectorAll('.highlight').forEach(el => el.classList.remove('highlight'));
        }};
        
        msg.onerror = () => {{
            clearInterval(keepAlive);
        }};

        synth.speak(msg);

        function togglePlayPause() {{
            if (synth.paused) {{
                synth.resume();
                playPauseBtn.innerText = "⏸️ Pause Reading";
                status.innerText = "🔊 Speaking...";
            }} else if (synth.speaking) {{
                synth.pause();
                playPauseBtn.innerText = "▶️ Resume Reading";
                status.innerText = "⏸️ Paused";
            }}
        }}
    </script>
    </body>
    </html>
    """