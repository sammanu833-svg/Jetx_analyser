# JetX Analyzer — Telegram + site web

## Ce que fait cette V1
- Enregistre manuellement les multiplicateurs.
- Affiche moyenne, médiane, fréquence des résultats <2x et >=5x.
- Affiche un graphique des 50 dernières manches.
- Permet d'envoyer un multiplicateur au bot Telegram.
- Envoie une alerte statistique de prudence lorsque certaines conditions sont réunies.

**Important :** ce programme ne prédit pas le prochain multiplicateur et ne garantit aucun gain.

## Installation locale

Python 3.10+ recommandé.

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
```

Copie `.env.example` vers `.env` et renseigne `BOT_TOKEN`.

Lance ensuite :

```bash
python app.py
```

Le site sera disponible sur `http://127.0.0.1:5000`.

## Telegram

1. Dans Telegram, ouvre BotFather.
2. Crée un bot avec `/newbot`.
3. Copie le token dans `BOT_TOKEN`.
4. Pour un déploiement public, configure le webhook vers :
   `https://TON-DOMAINE/telegram`

Exemple d'appel webhook :

```bash
curl -X POST "https://api.telegram.org/bot<TOKEN>/setWebhook" \
  -d "url=https://TON-DOMAINE/telegram"
```

Le bot accepte des messages comme `1.72`, `2.15x` ou `1,72`.

## Étape suivante
Déployer le serveur sur un hébergeur, puis sécuriser le webhook et ajouter une authentification au site.
