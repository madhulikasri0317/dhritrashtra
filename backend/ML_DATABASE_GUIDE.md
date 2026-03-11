# Dhritrashtra ML & Database Documentation

## Overview

This document provides comprehensive information about the machine learning model and PostgreSQL database schema for the Dhritrashtra water-borne disease prediction system.

---

## Machine Learning Model

### Overview
The Dhritrashtra system uses a **Random Forest Classifier** from scikit-learn to predict disease outbreak risk levels based on environmental and epidemiological features.

**Model Type:** RandomForestClassifier (scikit-learn)
**Classes:** 3 (Low, Medium, High Risk)
**Features:** 4 input variables
**Output:** Risk probability, predicted cases, attack rate

### Input Features

| Feature | Type | Range | Description |
|---------|------|-------|-------------|
| rainfall | float | 0-300 mm | Precipitation in millimeters |
| temperature | float | 15-40°C | Temperature in Celsius |
| previous_cases | int | 0-1000+ | Number of cases in previous period |
| population_density | float | 100-10000 /sq km | Population per square kilometer |

### Output Variables

| Variable | Type | Range | Description |
|----------|------|-------|-------------|
| risk_level | string | low/medium/high | Categorical risk classification |
| risk_score | float | 0-1 | Probability of outbreak (0=no risk, 1=certain) |
| predicted_cases | int | 0+ | Estimated number of cases |
| attack_rate | float | 0-1 | Proportion of population affected |
| confidence | float | 0-1 | Model confidence in prediction |

### Model Architecture

```python
RandomForestClassifier(
    n_estimators=150,        # 150 decision trees
    max_depth=15,            # Maximum tree depth
    min_samples_split=5,     # Minimum samples to split node
    min_samples_leaf=2,      # Minimum samples per leaf
    random_state=42,         # Reproducibility
    class_weight='balanced'  # Handle class imbalance
)
```

### Training Data

The model is trained on:
- **Historical disease case data** from the `disease_cases` table
- **Environmental data** (rainfall, temperature)
- **Epidemiological data** (previous cases, population density)

### Feature Importance

After training, feature importance scores indicate which features most influence predictions:

```
Feature Importance Example:
  - previous_cases: 0.3892
  - temperature: 0.2847
  - population_density: 0.1923
  - rainfall: 0.1338
```

### Risk Level Thresholds

```
Risk Level Classification:
├── Low Risk:    risk_score < 0.4   → Attack rate 0.03 per capita
├── Medium Risk: 0.4 ≤ risk_score < 0.7  → Attack rate 0.08 per capita
└── High Risk:   risk_score ≥ 0.7   → Attack rate 0.15 per capita
```

### Prediction Example

**Input:**
```python
features = [
    rainfall=250,           # Heavy rain
    temperature=32,         # High temperature
    previous_cases=500,     # Significant outbreak
    population_density=7000 # High density
]
population = 20000

predictor.predict_risk_level(features)
→ {
    'risk_probability': 0.875,
    'risk_level': 'high',
    'confidence': 0.92
}

predictor.predict_cases(features, population)
→ {
    'predicted_cases': 2625,
    'attack_rate': 0.1313,
    'severity': 'high'
}
```

---

## Database Schema

### Tables Overview

The PostgreSQL schema consists of 8 main tables:

```
locations
├── disease_cases
├── predictions
├── alerts
├── risk_maps
├── epidemic_curves
└── model_performance
```

### 1. Locations Table

**Purpose:** Geographic regions being monitored

**Columns:**
```sql
id              SERIAL PRIMARY KEY
name            VARCHAR(255) - Location name
latitude        FLOAT - Geographic latitude
longitude       FLOAT - Geographic longitude
region          VARCHAR(255) - Administrative region
district        VARCHAR(255) - District name
created_at      TIMESTAMP - Creation date
```

**Example:**
```sql
INSERT INTO locations (name, latitude, longitude, region, district)
VALUES ('New Delhi', 28.6139, 77.2090, 'North', 'New Delhi');
```

### 2. Disease Cases Table

**Purpose:** Record historical disease case data

**Columns:**
```sql
id                  SERIAL PRIMARY KEY
location_id         INTEGER FK → locations
district            VARCHAR(255) - District where cases occurred
disease             VARCHAR(100) - Type of disease
cases               INTEGER - Number of confirmed cases
deaths              INTEGER - Number of deaths
recovered           INTEGER - Number recovered
date                DATE - Date of record
week                INTEGER - ISO week number
month               INTEGER - Month number
year                INTEGER - Year
created_at          TIMESTAMP - Record creation date
updated_at          TIMESTAMP - Last update date
```

**Example:**
```sql
INSERT INTO disease_cases (district, disease, cases, deaths, recovered, date)
VALUES ('New Delhi', 'Cholera', 125, 5, 95, '2026-03-10');
```

**Indexes:**
- district
- disease
- date
- created_at
- Unique: (district, disease, date)

### 3. Predictions Table

**Purpose:** Store ML model predictions

**Columns:**
```sql
id                  SERIAL PRIMARY KEY
location_id         INTEGER FK → locations
district            VARCHAR(255) - Target district
disease             VARCHAR(100) - Predicted disease
risk_level          VARCHAR(20) - low/medium/high
risk_score          FLOAT - Probability (0-1)
predicted_cases     INTEGER - Estimated cases
attack_rate         FLOAT - Attack rate (0-1)
confidence          FLOAT - Model confidence
rainfall            FLOAT - Input feature
temperature         FLOAT - Input feature
previous_cases      INTEGER - Input feature
population_density  FLOAT - Input feature
model_version       VARCHAR(50) - Model version
created_at          TIMESTAMP - Prediction timestamp
prediction_date     DATE - Date of prediction
```

**Example:**
```sql
INSERT INTO predictions
(district, disease, risk_level, risk_score, predicted_cases,
 rainfall, temperature, previous_cases, population_density, prediction_date)
VALUES
('New Delhi', 'Cholera', 'high', 0.85, 750,
 250, 32, 500, 7000, '2026-03-10');
```

**Indexes:**
- district
- disease
- risk_level
- created_at
- prediction_date

### 4. Alerts Table

**Purpose:** Disease outbreak alerts generated based on risk levels

**Columns:**
```sql
id                  SERIAL PRIMARY KEY
location_id         INTEGER FK → locations
district            VARCHAR(255) - Affected district
disease             VARCHAR(100) - Disease type
title               VARCHAR(255) - Alert title
message             TEXT - Alert message
risk_level          VARCHAR(20) - Associated risk level
affected_population INTEGER - Estimated affected population
severity            VARCHAR(20) - low/medium/high
is_active           BOOLEAN - Active status
created_at          TIMESTAMP - Alert issued date
dismissed_at        TIMESTAMP - When alert was dismissed
expires_at          TIMESTAMP - Alert expiration date
prediction_id       INTEGER FK → predictions
```

**Example:**
```sql
INSERT INTO alerts
(district, disease, title, message, risk_level, severity, is_active, prediction_id)
VALUES
('New Delhi', 'Cholera', 'High Cholera Risk Detected',
 'High risk detected in New Delhi', 'high', 'high', TRUE, 1);
```

**Indexes:**
- district
- disease
- risk_level
- is_active
- created_at

### 5. Risk Maps Table

**Purpose:** Geographic data for visualization

**Columns:**
```sql
id              SERIAL PRIMARY KEY
latitude        FLOAT - Latitude coordinate
longitude       FLOAT - Longitude coordinate
district        VARCHAR(255) - District
disease         VARCHAR(100) - Disease type
risk_score      FLOAT - Risk value
intensity       VARCHAR(20) - low/medium/high
created_at      TIMESTAMP - Record date
updated_at      TIMESTAMP - Last update
```

### 6. Epidemic Curves Table

**Purpose:** Time series data for trend analysis

**Columns:**
```sql
id                  SERIAL PRIMARY KEY
district            VARCHAR(255) - District
disease             VARCHAR(100) - Disease type
date                DATE - Date of record
daily_cases         INTEGER - Cases on this date
cumulative_cases    INTEGER - Total cases to date
weekly_growth_rate  FLOAT - Week-over-week growth
created_at          TIMESTAMP - Record date
```

### 7. Model Performance Table

**Purpose:** Track model accuracy metrics

**Columns:**
```sql
id                  SERIAL PRIMARY KEY
model_version       VARCHAR(50) - Model version identifier
accuracy            FLOAT - Overall accuracy (0-1)
precision           FLOAT - Precision score (0-1)
recall              FLOAT - Recall score (0-1)
f1_score            FLOAT - F1 score (0-1)
training_samples    INTEGER - Number of training samples
evaluation_date     TIMESTAMP - Evaluation date
created_at          TIMESTAMP - Record date
```

---

## Database Relationships

```
locations (1)
├── disease_cases (M)
├── predictions (M)
└── alerts (M)
    └── predictions (1)
```

---

## Useful SQL Queries

### Query 1: Get Recent Predictions by Risk Level
```sql
SELECT district, disease, risk_level, COUNT(*) as count
FROM predictions
WHERE created_at >= CURRENT_DATE - INTERVAL '7 days'
GROUP BY district, disease, risk_level
ORDER BY count DESC;
```

### Query 2: Active High-Risk Alerts
```sql
SELECT id, district, disease, title, created_at
FROM alerts
WHERE is_active = TRUE AND risk_level = 'high'
ORDER BY created_at DESC;
```

### Query 3: Disease Trends Over Time
```sql
SELECT date, disease, SUM(cases) as total_cases
FROM disease_cases
WHERE date >= CURRENT_DATE - INTERVAL '30 days'
GROUP BY date, disease
ORDER BY date DESC;
```

### Query 4: Model Performance Comparison
```sql
SELECT model_version, accuracy, precision, recall, f1_score
FROM model_performance
ORDER BY evaluation_date DESC
LIMIT 10;
```

### Query 5: At-Risk Populations
```sql
SELECT district, SUM(affected_population) as total_at_risk
FROM alerts
WHERE is_active = TRUE
GROUP BY district
ORDER BY total_at_risk DESC;
```

---

## Data Import/Export

### Import sample data
```bash
python data/generate_sample_data.py
```

### PostgreSQL Schema Setup
```bash
psql -h localhost -U user -d dhritrashtra -f backend/DATABASE_SCHEMA.sql
```

### Backup Database
```bash
pg_dump -h localhost -U user dhritrashtra > backup.sql
```

### Restore Database
```bash
psql -h localhost -U user dhritrashtra < backup.sql
```

---

## Training the Model

### Step 1: Generate or Prepare Training Data
```python
from models.train_model import generate_synthetic_training_data
X_train, y_train = generate_synthetic_training_data(n_samples=500)
```

### Step 2: Train the Model
```bash
cd backend/models
python train_model.py
```

### Step 3: Verify Model Performance
```python
from disease_model import DiseasePredictor
predictor = DiseasePredictor(model_path='trained_model.pkl')
info = predictor.get_model_info()
print(info['feature_importance'])
```

---

## Performance Optimization

### Database Indexes
All critical columns are indexed:
- `disease_cases`: district, disease, date
- `predictions`: district, disease, risk_level
- `alerts`: district, disease, is_active

### Query Optimization Tips
1. Use `WHERE` clauses with indexed columns
2. Partition large tables by date
3. Archive old records (> 2 years)
4. Create materialized views for complex queries

### Model Optimization
1. Regular retraining (monthly or quarterly)
2. Monitor accuracy metrics
3. Update feature engineering if needed
4. Experiment with hyperparameters

---

## Maintenance

### Weekly Tasks
- Monitor alert creation rate
- Check active alert count
- Verify data ingestion

### Monthly Tasks
- Retrain model with new data
- Update performance metrics
- Review model accuracy

### Quarterly Tasks
- Archive old records
- Optimize database indices
- Evaluate feature importance

---

## Support Files

- `train_model.py` - Model training script
- `generate_sample_data.py` - Sample data generator
- `disease_model.py` - ML model implementation
- `db.py` - SQLAlchemy ORM models
- `DATABASE_SCHEMA.sql` - SQL schema definition

---

## References

- **Scikit-learn:** https://scikit-learn.org/
- **PostgreSQL:** https://www.postgresql.org/
- **Random Forest:** https://en.wikipedia.org/wiki/Random_forest
- **Flask-SQLAlchemy:** https://flask-sqlalchemy.palletsprojects.com/
