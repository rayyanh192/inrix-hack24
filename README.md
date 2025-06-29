# EmergenSee 🚑✨

> Every second counts. EmergenSee reduces emergency-vehicle response times by predicting traffic congestion in real-time and alerting drivers ahead of approaching ambulances.

---

## Overview

- **Purpose / Goal** Provide real-time traffic-congestion analytics and proactive alerts so that civilian drivers can quickly clear a path for ambulances, fire trucks, and other emergency vehicles.
- **Intended Users**
  - Emergency-service dispatchers & fleet managers
  - Civilian drivers receiving in-car or mobile alerts
  - City traffic-management agencies evaluating congestion hotspots.
- **Problem Solved**
  Traditional sirens/lights are often missed in noisy, insulated vehicles—especially in gridlock. EmergenSee augments audible warnings with digital alerts backed by live traffic-camera analysis and congestion scoring.

## Features

- 🔴 **Real-time Camera Ingestion** – Pulls the nearest INRIX traffic-camera feed every few minutes.
- 🧠 **AI Image Analysis** – Uses Amazon Bedrock (Llama 3) to count vehicles & classify congestion level (0-100).
- 📍 **Geospatial Selection** – Finds the camera closest to the target coordinates via vector distance.
- 🛣️ **Route Distance Estimation** – Google Maps Distance Matrix calculates miles & ETA between ambulance and drivers.
- 🚨 **Driver Alerts** – Triggers notifications when congestion exceeds a configurable threshold & ambulance is within 10 mi.
- 🌐 **Modern Web Front-end** – Next.js + Tailwind dashboard that live-updates congestion scores & imagery.
- 🎛️ **REST API** – Flask endpoints for token retrieval, camera lookup, image download, rating, and alert orchestration.
- ✨ **Infrastructure-light** – Runs locally or on a small EC2 instance; no heavyweight queue or database required.

## Tech Stack

| Layer        | Technology                                                                                  |
| ------------ | ------------------------------------------------------------------------------------------- |
| Front-end    | Next.js (React 18), TypeScript, Tailwind CSS                                                |
| Back-end     | Python 3.12, Flask 2, AWS Bedrock (Llama 3 via `boto3`), Google Maps & Distance Matrix APIs |
| Data Sources | INRIX Traffic Cameras & Security Token API                                                  |
| Tooling      | Bun (📦 front-end package manager), pip / virtualenv (🐍 back-end), dotenv for secrets      |

**Architectural Notes**

- Clean separation between `frontend` (Next.js app) and `backend` (Flask micro-service).
- Stateless REST design; front-end polls periodically for updates.
- AI inference is on-demand to keep costs predictable.

## How It Works

1. Front-end obtains user/ambulance coordinates and calls `/start-check` on the Flask API.
2. API exchanges credentials for an INRIX security token.
3. Nearest operational traffic camera ID is calculated (`vector distance`).
4. Camera snapshot is fetched, saved locally, and fed to Bedrock Llama 3 for vehicle counting & congestion scoring.
5. Google Distance Matrix estimates remaining distance between ambulance and drivers on the same route.
6. If `congestion_score > threshold` **AND** `distance ≤ 10 mi`, an alert payload is returned; the UI displays a prominent "Move over – ambulance incoming!" banner.

## Setup and Installation

### Prerequisites

- **Node ≥ 20** & **Bun ≥ 1.0** (front-end)
- **Python ≥ 3.10** (back-end)
- AWS credentials with Bedrock access (`AWS_ACCESS_KEY_ID` / `AWS_SECRET_ACCESS_KEY`).
- Google Maps API key (`API_KEY`).
- INRIX developer account (token endpoint access).

### Backend (Flask)

```bash
# 1. clone
git clone https://github.com/rayyanh192/inrix-hack24 && cd inrix-hack24/backend

# 2. install deps
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.local.example .env.local   # fill in API_KEY and AWS keys

# 3. run server
python server.py  # starts on http://127.0.0.1:5000
```

### Frontend (Next.js)

```bash
cd inrix-hack24/emergensee
bun install
bun dev  # http://localhost:3000
```

## Usage Examples

#### Fetch INRIX Token

```bash
curl http://localhost:5000/token
```

#### Get Congestion Rating & Alert Decision

```bash
curl "http://localhost:5000/start-check?lat=37.458781&lon=-123.213041"
```

Example response:

```json
{
  "congestion_rating": 82,
  "distance_mi": 3.4,
  "should_alert": true
}
```

## Project Structure

```
inrix-hack24/
├── README.md                # ← You are here
├── backend/                 # Flask micro-service
│   ├── server.py            # Main API (entry point)
│   ├── main.py, ape.py      # algorithm prototypes
│   └── requirements.txt
└── emergensee/              # Next.js 14 front-end
    ├── src/app/             # ├─ pages, components
    ├── tailwind.config.ts
    ├── package.json
    └── ...
```

_Main entry points:_ `backend/server.py` (API) and `emergensee/src/app/page.tsx` (UI landing page).

## Challenges and Learnings

- **Noisy Camera Feeds** – Many INRIX images were blurry or outdated; added vector-based filtering & fallback logic.
- **LLM Output Parsing** – Llama occasionally returned explanatory text; regex sanitization was implemented to extract pure JSON.
- **Sparse Update Frequency** – INRIX cameras refresh every 5 min; we cache tokens and only call Bedrock when new images arrive to control cost.
- **AWS Bedrock Familiarity** – Gained hands-on experience invoking Bedrock Runtime and handling multi-modal inputs.
- **Vector Math Refresher** – Calculated Euclidean distance in lat/long space to pick the closest camera efficiently.

## Future Improvements

- 🔔 **Push Notifications** – Send alerts to iOS and Android devices via APNs and Firebase.
- 📈 **SageMaker Model** – Train on historical congestion images to achieve higher accuracy.
- 🗺️ **Navigation-App Integration** – Automatically reroute drivers through Google Maps and Waze.
- ⚡ **Streaming Video** – Add support for live INRIX camera feeds as they become available.
- 🪄 **Serverless Deployment** – Migrate the API to AWS Lambda backed by API Gateway.

## Credits and Inspiration

- Built during the **AWS × INRIX AI Hackathon 2024** – see full story on [Devpost](https://devpost.com/software/emergensee-p34rk9).
- INRIX Traffic Cameras & Security Token APIs.
- Google Maps Platform (Distance Matrix).
- Amazon Bedrock (Llama 3 multi-modal).
- Icons & fonts courtesy of Vercel's Geist.

---

> Built with ❤️, caffeine, and a mission to clear the road for lifesavers.
