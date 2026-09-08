import os, sqlite3, statistics
from datetime import datetime
from flask import Flask, request, jsonify, render_template
import requests
DB=os.getenv('DB_PATH','jetx.db'); BOT_TOKEN=os.getenv('BOT_TOKEN',''); app=Flask(__name__)
def db():
 c=sqlite3.connect(DB); c.row_factory=sqlite3.Row; return c
def init_db():
 c=db(); c.execute('CREATE TABLE IF NOT EXISTS rounds(id INTEGER PRIMARY KEY AUTOINCREMENT,multiplier REAL NOT NULL,created_at TEXT NOT NULL)'); c.commit(); c.close()
def add_round(x):
 c=db(); c.execute('INSERT INTO rounds(multiplier,created_at) VALUES(?,?)',(float(x),datetime.utcnow().isoformat(timespec='seconds'))); c.commit(); c.close()
def stats(limit=50):
 c=db(); rows=c.execute('SELECT multiplier FROM rounds ORDER BY id DESC LIMIT ?',(limit,)).fetchall(); c.close(); vals=[r['multiplier'] for r in rows]
 if not vals:return {'count':0,'average':0,'median':0,'under2':0,'over5':0,'values':[]}
 return {'count':len(vals),'average':round(statistics.mean(vals),2),'median':round(statistics.median(vals),2),'under2':sum(v<2 for v in vals),'over5':sum(v>=5 for v in vals),'values':list(reversed(vals))}
def telegram_send(text,chat_id=None):
 if not BOT_TOKEN:return
 target=chat_id or os.getenv('TELEGRAM_CHAT_ID')
 if not target:return
 try: requests.post(f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage',json={'chat_id':target,'text':text},timeout=5)
 except requests.RequestException: pass
@app.route('/')
def index():return render_template('index.html')
@app.route('/api/rounds',methods=['GET'])
def get_rounds():return jsonify(stats(int(request.args.get('limit',50))))
@app.route('/api/rounds',methods=['POST'])
def post_round():
 data=request.get_json(silent=True) or {}
 try:x=float(data['multiplier'])
 except (KeyError,TypeError,ValueError):return jsonify({'error':'multiplier invalide'}),400
 if x<1:return jsonify({'error':'le multiplicateur doit être >= 1'}),400
 add_round(x); s=stats()
 if s['count']>=10:
  signal='PRUDENCE' if s['under2']>=7 else 'ANALYSE NORMALE'; telegram_send(f'JetX — analyse: {signal}\nDernier: {x:.2f}x\nMoyenne (50): {s["average"]}x')
 return jsonify(s)
@app.route('/telegram',methods=['POST'])
def telegram():
 update=request.get_json(silent=True) or {}; msg=update.get('message',{}); text=(msg.get('text') or '').strip(); chat_id=msg.get('chat',{}).get('id')
 if text=='/start':reply='Envoie un multiplicateur, ex. 1.72'
 elif text=='/stats':
  s=stats(); reply=f'Statistiques\nMoyenne: {s["average"]}x\nMédiane: {s["median"]}x\n<2x: {s["under2"]}/{s["count"]}\n>=5x: {s["over5"]}/{s["count"]}'
 else:
  try:
   x=float(text.replace(',','.').lower().replace('x','').strip())
   if x<1:raise ValueError
   add_round(x); s=stats(); reply=f'Ajouté: {x:.2f}x\nMoyenne: {s["average"]}x\nMédiane: {s["median"]}x\n<2x: {s["under2"]}/{s["count"]}\n>=5x: {s["over5"]}/{s["count"]}'
  except ValueError:reply='Format attendu: 1.72 (ou 1,72 / 1.72x)'
 telegram_send(reply,chat_id); return 'ok'
init_db()
if __name__=='__main__':app.run(host='0.0.0.0',port=int(os.getenv('PORT',5000)))
