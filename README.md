# Dhritrashtra - Water Borne Disease Prediction System

Dhritrashtra is an intelligent AI system designed to predict water-borne diseases and visualize risk maps in real-time. It combines machine learning, geospatial analysis, and data visualization to help public health authorities monitor and respond to disease outbreaks.

## 🎯 Features

- **Disease Risk Prediction**: ML-based predictions for water-borne diseases (Cholera, Typhoid, Dengue)
- **Interactive Risk Maps**: Real-time visualization of disease risk using Leaflet.js
- **Alert System**: Automated outbreak alerts based on risk thresholds
- **Historical Data**: Track predictions over time for trend analysis
- **Geographic Analysis**: Region-based risk assessment and population impact estimation

## 🏗️ Project Structure

```
dhritrashtra/
├── backend/              # Flask Python API
│   ├── app.py           # Main Flask application
│   ├── routes/          # API endpoints
│   │   ├── predictions.py   # Disease prediction routes
│   │   ├── alerts.py        # Alert management routes
│   │   └── maps.py          # Risk map data routes
│   ├── models/          # ML models
│   │   └── disease_model.py # scikit-learn predictor
│   ├── database/        # Database models
│   │   └── db.py        # SQLAlchemy models
│   ├── data/            # Training data
│   ├── requirements.txt  # Python dependencies
│   └── .env.example     # Environment variables template
│
├── frontend/            # React + Tailwind UI
│   ├── src/
│   │   ├── pages/       # Page components
│   │   │   ├── Dashboard.jsx
│   │   │   ├── RiskMap.jsx
│   │   │   └── Alerts.jsx
│   │   ├── components/  # Reusable components
│   │   │   ├── Navbar.jsx
│   │   │   ├── PredictionTable.jsx
│   │   │   └── AlertPanel.jsx
│   │   ├── styles/      # CSS stylesheets
│   │   ├── App.jsx      # Main App component
│   │   ├── index.js     # Entry point
│   │   └── index.css    # Global styles
│   ├── package.json     # Frontend dependencies
│   ├── vite.config.js   # Vite configuration
│   ├── tailwind.config.js # Tailwind CSS config
│   ├── index.html       # HTML template
│   └── .env.example     # Environment variables template
│
└── README.md            # This file

```

## 🛠️ Tech Stack

### Backend
- **Framework**: Flask (Python)
- **Database**: PostgreSQL
- **ML**: scikit-learn
- **ORM**: SQLAlchemy
- **API**: RESTful with Flask-CORS

### Frontend
- **Framework**: React 18
- **Styling**: Tailwind CSS
- **Maps**: Leaflet.js
- **Build Tool**: Vite
- **HTTP Client**: Axios

### Infrastructure
- **Database**: PostgreSQL
- **Deployment**: Containerized with Docker (optional)

## 🚀 Getting Started

### Prerequisites
- Python 3.9+
- Node.js 16+
- PostgreSQL 12+

### Backend Setup

1. **Navigate to backend directory**
```bash
cd backend
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure environment**
```bash
cp .env.example .env
# Edit .env with your database credentials
```

5. **Initialize database**
```bash
python
>>> from app import app, db
>>> with app.app_context():
...     db.create_all()
>>> exit()
```

6. **Run Flask server**
```bash
python app.py
```

Backend will be available at `http://localhost:5000`

### Frontend Setup

1. **Navigate to frontend directory**
```bash
cd frontend
```

2. **Install dependencies**
```bash
npm install
```

3. **Configure environment**
```bash
cp .env.example .env
# Edit .env if needed
```

4. **Start development server**
```bash
npm run dev
```

Frontend will be available at `http://localhost:3000`

## 📡 API Endpoints

### Predictions
- `GET /api/predictions` - Get all predictions
- `POST /api/predictions` - Create new prediction
- `GET /api/predictions/<id>` - Get specific prediction
- `GET /api/predictions/history?location=<location>` - Get historical data

### Alerts
- `GET /api/alerts` - Get active alerts
- `POST /api/alerts` - Create new alert
- `DELETE /api/alerts/<id>` - Dismiss alert

### Maps
- `GET /api/maps/risk-data` - Get risk data for visualization
- `GET /api/maps/heatmap` - Get heatmap layer data
- `GET /api/maps/regions` - Get region statistics

## 🤖 Machine Learning Model

The disease prediction model uses a Random Forest classifier trained on:
- Water quality metrics
- Temperature data
- Humidity levels
- Rainfall patterns
- Population density

**Features:**
- 5 input features
- 100 decision trees
- Preprocessing with StandardScaler
- Probability-based risk scoring

## 📊 Database Schema

### Tables
- **locations** - Geographic locations being monitored
- **predictions** - Disease risk predictions
- **alerts** - Outbreak alerts
- **risk_maps** - Risk data points for visualization

## 🔧 Configuration

### Environment Variables

**Backend (.env)**
```
FLASK_ENV=development
DATABASE_URL=postgresql://user:password@localhost:5432/dhritrashtra
SECRET_KEY=your-secret-key
DEBUG=True
```

**Frontend (.env)**
```
VITE_API_URL=http://localhost:5000/api
VITE_APP_NAME=Dhritrashtra
```

## 📈 Development

### Adding New Features

1. **Backend Route**
   - Create route file in `backend/routes/`
   - Import and register in `app.py`

2. **Frontend Component**
   - Create component in `frontend/src/components/`
   - Import and use in pages/App

3. **Database Model**
   - Add model class in `backend/database/db.py`
   - Run migration

### Testing

```bash
# Backend
python -m pytest tests/

# Frontend
npm test
```

## 📝 License

Copyright (c) 2026 madhulikasri0317. All Rights Reserved.

This project is proprietary. No part of the code may be reproduced, distributed, or used without prior written permission from the owner. See the [LICENSE](LICENSE) file for full terms.

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📧 Support

For support, email support@dhritrashtra.dev or open an issue in the repository.

## 🙏 Acknowledgments

- OpenStreetMap for map data
- scikit-learn team for ML tools
- React and Tailwind communities
- Flask framework

---

**Dhritrashtra** - Predicting Disease, Saving Lives
