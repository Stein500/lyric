import os
import json
from flask import Flask, request, jsonify, send_from_directory

app = Flask(__name__)

LYRIC_DIR = "/home/user/lyric"
AUDIO_FILE = "i'm not dying 1 Techstein.mp3"
LYRIC_FILE = "i'm not dying 1.txt"

@app.route('/')
def index():
    # Read the lyric file and parse lines
    lines = []
    lyric_path = os.path.join(LYRIC_DIR, LYRIC_FILE)
    if os.path.exists(lyric_path):
        with open(lyric_path, 'r', encoding='utf-8') as f:
            for line in f:
                line_str = line.strip()
                if line_str:
                    lines.append(line_str)
    
    # Generate HTML
    html_content = """
    <!DOCTYPE html>
    <html lang="fr">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Daïsky Pro - Lyric Synchronizer</title>
        <script src="https://cdn.tailwindcss.com"></script>
        <style>
            body {
                background: radial-gradient(circle at center, #1e1b4b, #090514);
                color: #f3f4f6;
            }
            .scrollbar-hide::-webkit-scrollbar {
                display: none;
            }
            .scrollbar-hide {
                -ms-overflow-style: none;
                scrollbar-width: none;
            }
        </style>
    </head>
    <body class="min-h-screen flex flex-col items-center justify-between p-4 font-sans selection:bg-amber-500 selection:text-black">
        <header class="w-full max-w-4xl flex items-center justify-between py-4 border-b border-gray-800">
            <div class="flex items-center space-x-3">
                <span class="text-2xl font-black bg-gradient-to-r from-amber-400 to-orange-500 bg-clip-text text-transparent">DAÏSKY PRO</span>
                <span class="text-xs bg-gray-800 text-gray-400 px-2 py-1 rounded">TechStein</span>
            </div>
            <h1 class="text-lg font-bold text-amber-400 tracking-wider">I'M NOT DYING - SYNC TOOL</h1>
            <div class="text-sm text-gray-400">Tempo: 120 BPM</div>
        </header>

        <main class="w-full max-w-4xl flex flex-col md:flex-row gap-6 my-6 flex-1 overflow-hidden h-[60vh]">
            <!-- Lyrics list -->
            <div class="flex-1 bg-black/40 border border-gray-800/80 rounded-2xl p-6 flex flex-col h-full overflow-hidden">
                <h2 class="text-sm font-semibold uppercase text-gray-400 mb-4 tracking-wider">Paroles (Cliquez pour marquer le début)</h2>
                <div id="lyrics-container" class="flex-1 overflow-y-auto space-y-3 pr-2 scrollbar-hide">
                    <!-- Lines injected here -->
                </div>
            </div>

            <!-- Controls and output -->
            <div class="w-full md:w-80 bg-black/40 border border-gray-800/80 rounded-2xl p-6 flex flex-col justify-between">
                <div>
                    <h2 class="text-sm font-semibold uppercase text-gray-400 mb-4 tracking-wider">Contrôles</h2>
                    <div class="space-y-4">
                        <button id="btn-play-pause" class="w-full py-3 bg-gradient-to-r from-amber-500 to-orange-600 text-black font-black rounded-xl hover:from-amber-400 hover:to-orange-500 transition shadow-lg shadow-orange-500/20 active:scale-95">
                            PLAY / PAUSE (Espace)
                        </button>
                        <div class="text-xs text-gray-400 leading-relaxed">
                            <p class="font-semibold text-amber-400/80">Raccourcis :</p>
                            <p>• <kbd class="bg-gray-800 px-1 rounded text-white">Espace</kbd> : Play/Pause</p>
                            <p>• <kbd class="bg-gray-800 px-1 rounded text-white">Entrée</kbd> : Valider la ligne courante au temps actuel</p>
                            <p>• <kbd class="bg-gray-800 px-1 rounded text-white">←</kbd> / <kbd class="bg-gray-800 px-1 rounded text-white">→</kbd> : Reculer/Avancer de 2s</p>
                            <p>• <kbd class="bg-gray-800 px-1 rounded text-white">R</kbd> : Réinitialiser la ligne sélectionnée</p>
                        </div>
                    </div>
                </div>

                <div class="mt-6 pt-6 border-t border-gray-800/80 space-y-4">
                    <div class="flex justify-between items-center bg-gray-950 p-3 rounded-lg">
                        <span class="text-xs text-gray-500 uppercase">Temps</span>
                        <span id="current-time" class="font-mono text-xl font-bold text-amber-400">00:00.00</span>
                    </div>
                    <button id="btn-save" class="w-full py-3 bg-emerald-600 text-white font-bold rounded-xl hover:bg-emerald-500 transition shadow-lg shadow-emerald-500/20 active:scale-95">
                        SAUVEGARDER LA SYNCHRO
                    </button>
                </div>
            </div>
        </main>

        <footer class="w-full max-w-4xl py-4 border-t border-gray-800 text-center text-xs text-gray-500">
            Daïsky Pro (TechStein) © 2026 - Wolof TechStein beat wê!
        </footer>

        <!-- Audio element -->
        <audio id="audio-player" class="hidden" src="/audio.mp3"></audio>

        <script>
            const lyricsData = """ + json.dumps(lines) + """;
            let syncedLines = lyricsData.map((text, index) => ({
                id: index,
                text: text,
                time: null,
                isSection: text.startsWith('[') && text.endsWith(']')
            }));

            let activeIndex = 0;
            const audio = document.getElementById('audio-player');
            const lyricsContainer = document.getElementById('lyrics-container');
            const timeDisplay = document.getElementById('current-time');
            const playPauseBtn = document.getElementById('btn-play-pause');
            const saveBtn = document.getElementById('btn-save');

            // Render lyrics
            function renderLyrics() {
                lyricsContainer.innerHTML = '';
                syncedLines.forEach((line, index) => {
                    const el = document.createElement('div');
                    el.id = `line-${index}`;
                    
                    if (line.isSection) {
                        el.className = `p-2 mt-4 text-xs font-bold tracking-widest text-orange-400 uppercase select-none border-b border-orange-500/10`;
                        el.innerText = line.text;
                    } else {
                        const timeStr = line.time !== null ? formatTime(line.time) : '--:--.--';
                        const isActive = index === activeIndex;
                        const isSynced = line.time !== null;
                        
                        el.className = `p-3 rounded-xl cursor-pointer transition flex justify-between items-center group ` +
                            (isActive ? 'bg-amber-500/20 border border-amber-500 text-white font-semibold' : 
                             isSynced ? 'bg-gray-900/40 text-gray-300 hover:bg-gray-900/60' : 'bg-transparent text-gray-600 hover:bg-gray-900/20');
                        
                        el.innerHTML = `
                            <span class="flex-1">${line.text}</span>
                            <span class="font-mono text-xs ${isActive ? 'text-amber-400' : isSynced ? 'text-gray-400' : 'text-gray-700'} group-hover:underline">${timeStr}</span>
                        `;
                        el.addEventListener('click', () => {
                            selectLine(index);
                            if (audio.currentTime > 0) {
                                setLineTime(index, audio.currentTime);
                            }
                        });
                    }
                    lyricsContainer.appendChild(el);
                });
            }

            function selectLine(index) {
                while (index < syncedLines.length && syncedLines[index].isSection) {
                    index++;
                }
                if (index < syncedLines.length) {
                    activeIndex = index;
                    renderLyrics();
                    const activeEl = document.getElementById(`line-${activeIndex}`);
                    if (activeEl) {
                        activeEl.scrollIntoView({ behavior: 'smooth', block: 'center' });
                    }
                }
            }

            function setLineTime(index, time) {
                syncedLines[index].time = time;
                renderLyrics();
                let next = index + 1;
                while (next < syncedLines.length && syncedLines[next].isSection) {
                    next++;
                }
                if (next < syncedLines.length) {
                    activeIndex = next;
                    renderLyrics();
                    const activeEl = document.getElementById(`line-${activeIndex}`);
                    if (activeEl) {
                        activeEl.scrollIntoView({ behavior: 'smooth', block: 'center' });
                    }
                }
            }

            function formatTime(seconds) {
                const m = Math.floor(seconds / 60).toString().padStart(2, '0');
                const s = Math.floor(seconds % 60).toString().padStart(2, '0');
                const ms = Math.floor((seconds % 1) * 100).toString().padStart(2, '0');
                return `${m}:${s}.${ms}`;
            }

            audio.addEventListener('timeupdate', () => {
                timeDisplay.innerText = formatTime(audio.currentTime);
            });

            playPauseBtn.addEventListener('click', togglePlay);
            function togglePlay() {
                if (audio.paused) {
                    audio.play();
                    playPauseBtn.innerText = "PAUSE (Espace)";
                    playPauseBtn.className = "w-full py-3 bg-amber-500 text-black font-black rounded-xl hover:bg-amber-400 transition shadow-lg active:scale-95";
                } else {
                    audio.pause();
                    playPauseBtn.innerText = "PLAY (Espace)";
                    playPauseBtn.className = "w-full py-3 bg-gradient-to-r from-amber-500 to-orange-600 text-black font-black rounded-xl hover:from-amber-400 hover:to-orange-500 transition shadow-lg active:scale-95";
                }
            }

            window.addEventListener('keydown', (e) => {
                if (e.code === 'Space') {
                    e.preventDefault();
                    togglePlay();
                } else if (e.code === 'Enter') {
                    e.preventDefault();
                    if (activeIndex < syncedLines.length) {
                        setLineTime(activeIndex, audio.currentTime);
                    }
                } else if (e.code === 'ArrowLeft') {
                    audio.currentTime = Math.max(0, audio.currentTime - 2);
                } else if (e.code === 'ArrowRight') {
                    audio.currentTime = Math.min(audio.duration, audio.currentTime + 2);
                } else if (e.code === 'KeyR') {
                    if (activeIndex < syncedLines.length) {
                        syncedLines[activeIndex].time = null;
                        renderLyrics();
                    }
                }
            });

            saveBtn.addEventListener('click', () => {
                fetch('/save-sync', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(syncedLines)
                })
                .then(res => res.json())
                .then(data => {
                    alert('Synchronisation sauvegardée avec succès !');
                })
                .catch(err => {
                    console.error(err);
                    alert('Erreur lors de la sauvegarde.');
                });
            });

            renderLyrics();
            selectLine(0);
        </script>
    </body>
    </html>
    """
    return html_content

@app.route('/audio.mp3')
def get_audio():
    return send_from_directory(LYRIC_DIR, AUDIO_FILE)

@app.route('/download-assets')
def download_assets():
    return send_from_directory(LYRIC_DIR, "daiskypro_im_not_dying.zip", as_attachment=True)

@app.route('/download-new-assets')
def download_new_assets():
    return send_from_directory(LYRIC_DIR, "daiskypro_fancy_new_assets.zip", as_attachment=True)

@app.route('/download-hq-assets')
def download_hq_assets():
    return send_from_directory(LYRIC_DIR, "daiskypro_fancy_HQ_assets.zip", as_attachment=True)

@app.route('/save-sync', methods=['POST'])
def save_sync():
    data = request.json
    sync_file = os.path.join(LYRIC_DIR, "synced_lyrics.json")
    with open(sync_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    
    lrc_file = os.path.join(LYRIC_DIR, "i'm not dying 1.lrc")
    with open(lrc_file, 'w', encoding='utf-8') as f:
        for item in data:
            if item.get('isSection'):
                f.write(f"\n# {item['text']}\n")
            elif item.get('time') is not None:
                t = item['time']
                m = int(t // 60)
                s = int(t % 60)
                ms = int((t % 1) * 100)
                f.write(f"[{m:02d}:{s:02d}.{ms:02d}]{item['text']}\n")
            else:
                f.write(f"{item['text']}\n")

    return jsonify({"status": "success", "message": "Saved synced_lyrics.json and i'm not dying 1.lrc"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True)
