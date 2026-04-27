from flask import Flask, jsonify
from flask_cors import CORS
import requests
from textblob import TextBlob
from collections import defaultdict
import os
from datetime import datetime, timedelta
import time

app = Flask(__name__)
CORS(app)

NEWS_API_KEY = os.environ.get("NEWS_API_KEY", "YOUR_KEY_HERE")

# Country name → ISO 3166-1 alpha-3 code mapping
COUNTRY_MAP = {
    "us": "USA", "united states": "USA", "america": "USA",
    "uk": "GBR", "britain": "GBR", "england": "GBR", "united kingdom": "GBR",
    "china": "CHN", "chinese": "CHN",
    "russia": "RUS", "russian": "RUS",
    "india": "IND", "indian": "IND",
    "germany": "DEU", "german": "DEU",
    "france": "FRA", "french": "FRA",
    "brazil": "BRA", "brazilian": "BRA",
    "canada": "CAN", "canadian": "CAN",
    "australia": "AUS", "australian": "AUS",
    "japan": "JPN", "japanese": "JPN",
    "israel": "ISR", "israeli": "ISR",
    "iran": "IRN", "iranian": "IRN",
    "ukraine": "UKR", "ukrainian": "UKR",
    "pakistan": "PAK", "pakistani": "PAK",
    "mexico": "MEX", "mexican": "MEX",
    "south korea": "KOR", "korean": "KOR",
    "saudi arabia": "SAU", "saudi": "SAU",
    "turkey": "TUR", "turkish": "TUR",
    "italy": "ITA", "italian": "ITA",
    "spain": "ESP", "spanish": "ESP",
    "indonesia": "IDN", "indonesian": "IDN",
    "nigeria": "NGA", "nigerian": "NGA",
    "south africa": "ZAF",
    "argentina": "ARG", "argentine": "ARG",
    "egypt": "EGY", "egyptian": "EGY",
    "poland": "POL", "polish": "POL",
    "sweden": "SWE", "swedish": "SWE",
    "netherlands": "NLD", "dutch": "NLD",
    "venezuela": "VEN", "venezuelan": "VEN",
    "colombia": "COL", "colombian": "COL",
    "ethiopia": "ETH", "ethiopian": "ETH",
    "afghanistan": "AFG", "afghan": "AFG",
    "iraq": "IRQ", "iraqi": "IRQ",
    "syria": "SYR", "syrian": "SYR",
    "north korea": "PRK",
    "taiwan": "TWN", "taiwanese": "TWN",
    "vietnam": "VNM", "vietnamese": "VNM",
    "thailand": "THA", "thai": "THA",
    "malaysia": "MYS", "malaysian": "MYS",
    "philippines": "PHL", "philippine": "PHL",
    "new zealand": "NZL",
    "portugal": "PRT", "portuguese": "PRT",
    "greece": "GRC", "greek": "GRC",
    "hungary": "HUN", "hungarian": "HUN",
    "czech": "CZE",
    "romania": "ROU", "romanian": "ROU",
    "chile": "CHL", "chilean": "CHL",
    "peru": "PER", "peruvian": "PER",
    "kenya": "KEN", "kenyan": "KEN",
    "ghana": "GHA", "ghanaian": "GHA",
    "bangladesh": "BGD", "bangladeshi": "BGD",
    "myanmar": "MMR", "burmese": "MMR",
    "sudan": "SDN", "sudanese": "SDN",
    "somalia": "SOM", "somali": "SOM",
    "libya": "LBY", "libyan": "LBY",
    "morocco": "MAR", "moroccan": "MAR",
    "algeria": "DZA", "algerian": "DZA",
    "tunisia": "TUN", "tunisian": "TUN",
    "jordan": "JOR", "jordanian": "JOR",
    "lebanon": "LBN", "lebanese": "LBN",
    "cuba": "CUB", "cuban": "CUB",
    "haiti": "HTI", "haitian": "HTI",
    "bolivia": "BOL", "bolivian": "BOL",
    "ecuador": "ECU", "ecuadorian": "ECU",
    "paraguay": "PRY", "paraguayan": "PRY",
    "uruguay": "URY", "uruguayan": "URY",
    "norway": "NOR", "norwegian": "NOR",
    "denmark": "DNK", "danish": "DNK",
    "finland": "FIN", "finnish": "FIN",
    "switzerland": "CHE", "swiss": "CHE",
    "austria": "AUT", "austrian": "AUT",
    "belgium": "BEL", "belgian": "BEL",
    "ireland": "IRL", "irish": "IRL",
    "singapore": "SGP", "singaporean": "SGP",
    "hong kong": "HKG",
    "cambodia": "KHM", "cambodian": "KHM",
    "laos": "LAO",
    "mongolia": "MNG", "mongolian": "MNG",
    "nepal": "NPL", "nepalese": "NPL",
    "sri lanka": "LKA",
    "qatar": "QAT", "qatari": "QAT",
    "uae": "ARE", "emirates": "ARE",
    "kuwait": "KWT", "kuwaiti": "KWT",
    "bahrain": "BHR",
    "oman": "OMN", "omani": "OMN",
    "yemen": "YEM", "yemeni": "YEM",
    "zimbabwe": "ZWE", "zimbabwean": "ZWE",
    "tanzania": "TZA", "tanzanian": "TZA",
    "uganda": "UGA", "ugandan": "UGA",
    "cameroon": "CMR", "cameroonian": "CMR",
    "ivory coast": "CIV",
    "senegal": "SEN", "senegalese": "SEN",
    "mali": "MLI", "malian": "MLI",
    "niger": "NER",
    "chad": "TCD",
    "congo": "COD",
    "angola": "AGO", "angolan": "AGO",
    "mozambique": "MOZ",
    "zambia": "ZMB", "zambian": "ZMB",
    "madagascar": "MDG",
    "guatemala": "GTM", "guatemalan": "GTM",
    "honduras": "HND", "honduran": "HND",
    "nicaragua": "NIC", "nicaraguan": "NIC",
    "costa rica": "CRI",
    "panama": "PAN", "panamanian": "PAN",
    "dominican republic": "DOM",
    "jamaica": "JAM", "jamaican": "JAM",
    "trinidad": "TTO",
    "iceland": "ISL", "icelander": "ISL",
    "luxembourg": "LUX",
    "slovakia": "SVK", "slovak": "SVK",
    "croatia": "HRV", "croatian": "HRV",
    "serbia": "SRB", "serbian": "SRB",
    "bosnia": "BIH",
    "albania": "ALB", "albanian": "ALB",
    "north macedonia": "MKD",
    "moldova": "MDA",
    "belarus": "BLR", "belarusian": "BLR",
    "georgia": "GEO", "georgian": "GEO",
    "armenia": "ARM", "armenian": "ARM",
    "azerbaijan": "AZE", "azerbaijani": "AZE",
    "kazakhstan": "KAZ", "kazakh": "KAZ",
    "uzbekistan": "UZB", "uzbek": "UZB",
    "tajikistan": "TJK",
    "kyrgyzstan": "KGZ",
    "turkmenistan": "TKM",
    "estonia": "EST", "estonian": "EST",
    "latvia": "LVA", "latvian": "LVA",
    "lithuania": "LTU", "lithuanian": "LTU",
    "slovenia": "SVN", "slovenian": "SVN",
    "bulgaria": "BGR", "bulgarian": "BGR",
    "cyprus": "CYP", "cypriot": "CYP",
    "malta": "MLT", "maltese": "MLT",
    "israel": "ISR",
    "palestine": "PSE", "palestinian": "PSE",
}

# Cache to avoid hitting API too often
_cache = {"data": None, "timestamp": None}
CACHE_TTL = 300  # 5 minutes


def fetch_and_analyze():
    """Fetch news, score sentiment, aggregate by country."""
    global _cache

    now = datetime.utcnow()
    if _cache["data"] and _cache["timestamp"]:
        age = (now - _cache["timestamp"]).total_seconds()
        if age < CACHE_TTL:
            return _cache["data"]

    country_scores = defaultdict(list)
    country_headlines = defaultdict(list)

    # Top world news queries
    queries = [
        "world news",
        "geopolitics",
        "international",
        "conflict war",
        "economy trade",
        "climate environment",
        "election government",
        "sanctions protest",
    ]

    headers = {"X-Api-Key": NEWS_API_KEY}
    from_date = (datetime.utcnow() - timedelta(days=2)).strftime("%Y-%m-%d")

    for query in queries[:4]:  # limit to 4 queries to save API calls
        try:
            url = (
                f"https://newsapi.org/v2/everything"
                f"?q={query}&language=en&sortBy=publishedAt"
                f"&from={from_date}&pageSize=20"
            )
            resp = requests.get(url, headers=headers, timeout=8)
            if resp.status_code != 200:
                continue
            articles = resp.json().get("articles", [])

            for article in articles:
                title = article.get("title", "") or ""
                desc = article.get("description", "") or ""
                text = f"{title} {desc}".lower()

                # Find countries mentioned
                found = set()
                for keyword, iso3 in COUNTRY_MAP.items():
                    if keyword in text:
                        found.add(iso3)

                if not found:
                    continue

                # Score sentiment
                blob = TextBlob(f"{title} {desc}")
                polarity = blob.sentiment.polarity  # -1 to +1

                for iso3 in found:
                    country_scores[iso3].append(polarity)
                    if len(country_headlines[iso3]) < 5:
                        country_headlines[iso3].append({
                            "title": title[:120],
                            "url": article.get("url", ""),
                            "source": (article.get("source") or {}).get("name", ""),
                            "sentiment": round(polarity, 3),
                        })

        except Exception as e:
            print(f"Error fetching {query}: {e}")
            continue

    # Build result
    result = {}
    for iso3, scores in country_scores.items():
        avg = sum(scores) / len(scores)
        result[iso3] = {
            "score": round(avg, 4),
            "count": len(scores),
            "headlines": country_headlines[iso3],
        }

    # If no API key or no results, return demo data
    if not result or NEWS_API_KEY == "YOUR_KEY_HERE":
        result = get_demo_data()

    _cache["data"] = result
    _cache["timestamp"] = now
    return result


def get_demo_data():
    """Realistic demo data when no API key is present."""
    return {
        "USA": {"score": 0.05, "count": 142, "headlines": [
            {"title": "Federal Reserve holds rates steady amid inflation concerns", "url": "#", "source": "Reuters", "sentiment": 0.02},
            {"title": "Congress passes bipartisan infrastructure amendment", "url": "#", "source": "AP", "sentiment": 0.18},
            {"title": "Tech sector layoffs continue as AI reshapes workforce", "url": "#", "source": "Bloomberg", "sentiment": -0.12},
        ]},
        "CHN": {"score": -0.08, "count": 98, "headlines": [
            {"title": "Trade tensions escalate as tariffs reach record highs", "url": "#", "source": "FT", "sentiment": -0.22},
            {"title": "China GDP growth slows to 4.6% in latest quarter", "url": "#", "source": "WSJ", "sentiment": -0.08},
            {"title": "Belt and Road Initiative expands across Southeast Asia", "url": "#", "source": "Reuters", "sentiment": 0.04},
        ]},
        "RUS": {"score": -0.31, "count": 87, "headlines": [
            {"title": "Ceasefire negotiations stall as conflict enters third year", "url": "#", "source": "BBC", "sentiment": -0.41},
            {"title": "Western sanctions tighten on energy sector", "url": "#", "source": "Guardian", "sentiment": -0.28},
            {"title": "Humanitarian corridor discussions resume in Geneva", "url": "#", "source": "Reuters", "sentiment": 0.06},
        ]},
        "UKR": {"score": -0.24, "count": 76, "headlines": [
            {"title": "Reconstruction efforts face continued disruption", "url": "#", "source": "AP", "sentiment": -0.32},
            {"title": "NATO allies pledge continued military support", "url": "#", "source": "BBC", "sentiment": 0.08},
            {"title": "Civilian displacement reaches 6 million across Europe", "url": "#", "source": "UNHCR", "sentiment": -0.48},
        ]},
        "IND": {"score": 0.12, "count": 93, "headlines": [
            {"title": "India overtakes Japan as third-largest economy", "url": "#", "source": "Bloomberg", "sentiment": 0.34},
            {"title": "Tech investment surge drives record FDI inflows", "url": "#", "source": "FT", "sentiment": 0.28},
            {"title": "Monsoon season brings flooding to northeastern states", "url": "#", "source": "Reuters", "sentiment": -0.18},
        ]},
        "GBR": {"score": 0.03, "count": 71, "headlines": [
            {"title": "Bank of England cuts rates for second time this year", "url": "#", "source": "Guardian", "sentiment": 0.12},
            {"title": "NHS waiting list reaches record 7.8 million patients", "url": "#", "source": "BBC", "sentiment": -0.28},
            {"title": "UK-EU trade framework negotiations advance", "url": "#", "source": "FT", "sentiment": 0.18},
        ]},
        "DEU": {"score": 0.01, "count": 64, "headlines": [
            {"title": "German industrial output falls for fourth consecutive quarter", "url": "#", "source": "Reuters", "sentiment": -0.24},
            {"title": "Berlin coalition reaches agreement on energy transition", "url": "#", "source": "DW", "sentiment": 0.16},
            {"title": "Volkswagen announces 35,000 job reduction plan", "url": "#", "source": "Bloomberg", "sentiment": -0.14},
        ]},
        "FRA": {"score": 0.04, "count": 58, "headlines": [
            {"title": "Paris Olympic legacy drives tourism record", "url": "#", "source": "AFP", "sentiment": 0.32},
            {"title": "French parliament passes pension reform extension", "url": "#", "source": "Le Monde", "sentiment": -0.08},
        ]},
        "BRA": {"score": -0.06, "count": 52, "headlines": [
            {"title": "Amazon deforestation reaches decade low under new policy", "url": "#", "source": "Reuters", "sentiment": 0.22},
            {"title": "Brazilian real hits record low against dollar", "url": "#", "source": "Bloomberg", "sentiment": -0.28},
        ]},
        "CAN": {"score": 0.08, "count": 47, "headlines": [
            {"title": "Bank of Canada cuts rates to 3.0% supporting growth", "url": "#", "source": "Globe and Mail", "sentiment": 0.18},
            {"title": "Housing affordability crisis deepens in major cities", "url": "#", "source": "CBC", "sentiment": -0.22},
        ]},
        "ISR": {"score": -0.38, "count": 83, "headlines": [
            {"title": "Ceasefire negotiations continue amid humanitarian concerns", "url": "#", "source": "AP", "sentiment": -0.28},
            {"title": "International court hearings on conflict continue in Hague", "url": "#", "source": "Reuters", "sentiment": -0.42},
        ]},
        "IRN": {"score": -0.21, "count": 61, "headlines": [
            {"title": "Nuclear talks resume in Vienna with EU mediators", "url": "#", "source": "Reuters", "sentiment": 0.06},
            {"title": "New sanctions target oil exports and financial sector", "url": "#", "source": "Bloomberg", "sentiment": -0.32},
        ]},
        "JPN": {"score": 0.09, "count": 54, "headlines": [
            {"title": "Bank of Japan raises rates for first time since 2007", "url": "#", "source": "Nikkei", "sentiment": 0.14},
            {"title": "Japan AI investment surges to record $12 billion", "url": "#", "source": "FT", "sentiment": 0.28},
        ]},
        "KOR": {"score": 0.06, "count": 43, "headlines": [
            {"title": "Samsung posts record semiconductor earnings", "url": "#", "source": "Reuters", "sentiment": 0.32},
        ]},
        "AUS": {"score": 0.11, "count": 39, "headlines": [
            {"title": "Australia records strongest GDP growth in three years", "url": "#", "source": "AFR", "sentiment": 0.24},
        ]},
        "ZAF": {"score": -0.09, "count": 36, "headlines": [
            {"title": "Load shedding crisis eases as new power capacity comes online", "url": "#", "source": "Reuters", "sentiment": 0.14},
            {"title": "South Africa unemployment remains at 33%", "url": "#", "source": "Bloomberg", "sentiment": -0.28},
        ]},
        "NGA": {"score": -0.14, "count": 34, "headlines": [
            {"title": "Nigerian naira stabilizes after central bank intervention", "url": "#", "source": "Reuters", "sentiment": 0.08},
            {"title": "Security concerns persist in northern regions", "url": "#", "source": "AFP", "sentiment": -0.36},
        ]},
        "PAK": {"score": -0.18, "count": 41, "headlines": [
            {"title": "IMF approves $7 billion bailout for Pakistan economy", "url": "#", "source": "Reuters", "sentiment": 0.12},
            {"title": "Political tensions rise ahead of elections", "url": "#", "source": "Dawn", "sentiment": -0.28},
        ]},
        "SAU": {"score": 0.07, "count": 38, "headlines": [
            {"title": "Saudi Vision 2030 investment reaches $1.3 trillion milestone", "url": "#", "source": "Bloomberg", "sentiment": 0.28},
            {"title": "OPEC+ agrees to extend production cuts through 2025", "url": "#", "source": "Reuters", "sentiment": 0.06},
        ]},
        "TUR": {"score": -0.04, "count": 37, "headlines": [
            {"title": "Turkish inflation falls to 45% from record 85%", "url": "#", "source": "Reuters", "sentiment": 0.08},
            {"title": "Erdogan meets Putin for energy cooperation talks", "url": "#", "source": "AFP", "sentiment": -0.08},
        ]},
        "MEX": {"score": 0.02, "count": 33, "headlines": [
            {"title": "Mexico becomes top US trading partner displacing China", "url": "#", "source": "Bloomberg", "sentiment": 0.22},
        ]},
        "ARG": {"score": -0.16, "count": 31, "headlines": [
            {"title": "Milei austerity measures cut deficit but recession deepens", "url": "#", "source": "Reuters", "sentiment": -0.18},
        ]},
        "VNM": {"score": 0.14, "count": 28, "headlines": [
            {"title": "Vietnam attracts record semiconductor investment from Intel", "url": "#", "source": "FT", "sentiment": 0.32},
        ]},
        "IDN": {"score": 0.08, "count": 29, "headlines": [
            {"title": "Indonesia moves capital to Nusantara as construction advances", "url": "#", "source": "Reuters", "sentiment": 0.18},
        ]},
        "ETH": {"score": -0.22, "count": 27, "headlines": [
            {"title": "Peace talks on Tigray conflict show fragile progress", "url": "#", "source": "AFP", "sentiment": -0.14},
        ]},
        "EGY": {"score": -0.11, "count": 26, "headlines": [
            {"title": "Egypt secures $35 billion UAE investment package", "url": "#", "source": "Reuters", "sentiment": 0.24},
            {"title": "IMF conditions weigh on Egyptian pound", "url": "#", "source": "Bloomberg", "sentiment": -0.28},
        ]},
        "POL": {"score": 0.06, "count": 24, "headlines": [
            {"title": "Poland strengthens eastern NATO flank with new bases", "url": "#", "source": "Reuters", "sentiment": 0.08},
        ]},
        "SWE": {"score": 0.09, "count": 22, "headlines": [
            {"title": "Sweden's NATO integration progresses as defense spending rises", "url": "#", "source": "Reuters", "sentiment": 0.12},
        ]},
        "NLD": {"score": 0.05, "count": 21, "headlines": [
            {"title": "ASML semiconductor controls dominate global chip supply", "url": "#", "source": "FT", "sentiment": 0.24},
        ]},
        "NOR": {"score": 0.16, "count": 19, "headlines": [
            {"title": "Norway sovereign wealth fund reaches $1.8 trillion", "url": "#", "source": "Bloomberg", "sentiment": 0.32},
        ]},
        "CHE": {"score": 0.12, "count": 18, "headlines": [
            {"title": "Swiss franc strengthens as safe haven demand rises", "url": "#", "source": "Reuters", "sentiment": 0.08},
        ]},
        "SGP": {"score": 0.18, "count": 17, "headlines": [
            {"title": "Singapore emerges as Asia Pacific AI hub", "url": "#", "source": "FT", "sentiment": 0.34},
        ]},
        "QAT": {"score": 0.09, "count": 16, "headlines": [
            {"title": "Qatar mediates Gaza ceasefire talks in Doha", "url": "#", "source": "Reuters", "sentiment": 0.06},
        ]},
    }


@app.route("/api/sentiment")
def sentiment():
    data = fetch_and_analyze()
    return jsonify({
        "data": data,
        "updated": datetime.utcnow().isoformat(),
        "source": "NewsAPI + TextBlob sentiment analysis",
        "total_countries": len(data),
    })


@app.route("/api/health")
def health():
    return jsonify({"status": "ok", "time": datetime.utcnow().isoformat()})


@app.route("/")
def index():
    return jsonify({"message": "Geopolitical Sentiment Engine", "endpoints": ["/api/sentiment", "/api/health"]})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
