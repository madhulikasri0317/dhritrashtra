-- Dhritrashtra PostgreSQL Database Schema
-- Water Borne Disease Prediction System

-- ================== Location Table ==================
CREATE TABLE IF NOT EXISTS locations (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    latitude FLOAT NOT NULL,
    longitude FLOAT NOT NULL,
    region VARCHAR(255),
    district VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_locations_district ON locations(district);
CREATE INDEX idx_locations_region ON locations(region);

-- ================== Disease Cases Table ==================
-- Historical records of disease cases in districts
CREATE TABLE IF NOT EXISTS disease_cases (
    id SERIAL PRIMARY KEY,
    location_id INTEGER REFERENCES locations(id),
    district VARCHAR(255) NOT NULL,
    disease VARCHAR(100) NOT NULL,
    cases INTEGER DEFAULT 0,
    deaths INTEGER DEFAULT 0,
    recovered INTEGER DEFAULT 0,
    date DATE NOT NULL,
    week INTEGER,
    month INTEGER,
    year INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_disease_cases_district ON disease_cases(district);
CREATE INDEX idx_disease_cases_disease ON disease_cases(disease);
CREATE INDEX idx_disease_cases_date ON disease_cases(date);
CREATE INDEX idx_disease_cases_created_at ON disease_cases(created_at);
CREATE UNIQUE INDEX idx_disease_cases_unique ON disease_cases(district, disease, date);

-- ================== Predictions Table ==================
-- ML model predictions for disease outbreaks
CREATE TABLE IF NOT EXISTS predictions (
    id SERIAL PRIMARY KEY,
    location_id INTEGER REFERENCES locations(id),
    district VARCHAR(255) NOT NULL,
    disease VARCHAR(100) NOT NULL,
    risk_level VARCHAR(20) NOT NULL,
    risk_score FLOAT,
    predicted_cases INTEGER,
    attack_rate FLOAT,
    confidence FLOAT,

    -- Input features
    rainfall FLOAT,
    temperature FLOAT,
    previous_cases INTEGER,
    population_density FLOAT,

    -- Metadata
    model_version VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    prediction_date DATE NOT NULL
);

CREATE INDEX idx_predictions_district ON predictions(district);
CREATE INDEX idx_predictions_disease ON predictions(disease);
CREATE INDEX idx_predictions_risk_level ON predictions(risk_level);
CREATE INDEX idx_predictions_created_at ON predictions(created_at);
CREATE INDEX idx_predictions_prediction_date ON predictions(prediction_date);

-- ================== Alerts Table ==================
-- Disease outbreak alerts based on predictions
CREATE TABLE IF NOT EXISTS alerts (
    id SERIAL PRIMARY KEY,
    location_id INTEGER REFERENCES locations(id),
    district VARCHAR(255) NOT NULL,
    disease VARCHAR(100) NOT NULL,
    title VARCHAR(255) NOT NULL,
    message TEXT,
    risk_level VARCHAR(20) NOT NULL,
    affected_population INTEGER,
    severity VARCHAR(20),
    is_active BOOLEAN DEFAULT TRUE,

    -- Alert lifecycle
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    dismissed_at TIMESTAMP,
    expires_at TIMESTAMP,

    -- Related prediction
    prediction_id INTEGER REFERENCES predictions(id)
);

CREATE INDEX idx_alerts_district ON alerts(district);
CREATE INDEX idx_alerts_disease ON alerts(disease);
CREATE INDEX idx_alerts_risk_level ON alerts(risk_level);
CREATE INDEX idx_alerts_is_active ON alerts(is_active);
CREATE INDEX idx_alerts_created_at ON alerts(created_at);

-- ================== Risk Maps Table ==================
-- Risk map visualization data points
CREATE TABLE IF NOT EXISTS risk_maps (
    id SERIAL PRIMARY KEY,
    latitude FLOAT NOT NULL,
    longitude FLOAT NOT NULL,
    district VARCHAR(255),
    disease VARCHAR(100),
    risk_score FLOAT,
    intensity VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_risk_maps_coordinates ON risk_maps(latitude, longitude);
CREATE INDEX idx_risk_maps_created_at ON risk_maps(created_at);

-- ================== Epidemic Curves Table ==================
-- Time series data for epidemic curves
CREATE TABLE IF NOT EXISTS epidemic_curves (
    id SERIAL PRIMARY KEY,
    district VARCHAR(255) NOT NULL,
    disease VARCHAR(100) NOT NULL,
    date DATE NOT NULL,
    daily_cases INTEGER,
    cumulative_cases INTEGER,
    weekly_growth_rate FLOAT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_epidemic_curves_district_disease ON epidemic_curves(district, disease);
CREATE INDEX idx_epidemic_curves_date ON epidemic_curves(date);

-- ================== Model Performance Table ==================
-- Track ML model performance metrics
CREATE TABLE IF NOT EXISTS model_performance (
    id SERIAL PRIMARY KEY,
    model_version VARCHAR(50) NOT NULL,
    accuracy FLOAT,
    precision FLOAT,
    recall FLOAT,
    f1_score FLOAT,
    training_samples INTEGER,
    evaluation_date TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_model_performance_version ON model_performance(model_version);

-- ================== Sample Data Insertion ==================
-- Insert sample locations
INSERT INTO locations (name, latitude, longitude, region, district) VALUES
('New Delhi', 28.6139, 77.2090, 'North', 'New Delhi'),
('Mumbai', 19.0760, 72.8777, 'West', 'Mumbai'),
('Bangalore', 12.9716, 77.5946, 'South', 'Bangalore'),
('Kolkata', 22.5726, 88.3639, 'East', 'Kolkata'),
('Chennai', 13.0827, 80.2707, 'South', 'Chennai')
ON CONFLICT DO NOTHING;

-- ================== Views for Analytics ==================

-- View: Active Alerts Summary
CREATE OR REPLACE VIEW active_alerts_summary AS
SELECT
    district,
    disease,
    COUNT(*) as alert_count,
    SUM(affected_population) as total_affected,
    MAX(created_at) as latest_alert
FROM alerts
WHERE is_active = TRUE
GROUP BY district, disease;

-- View: Risk Assessment by District
CREATE OR REPLACE VIEW risk_assessment_by_district AS
SELECT
    p.district,
    p.disease,
    COUNT(*) as prediction_count,
    AVG(p.risk_score) as avg_risk_score,
    MAX(p.risk_score) as max_risk_score,
    COUNT(CASE WHEN p.risk_level = 'high' THEN 1 END) as high_risk_count,
    COUNT(CASE WHEN p.risk_level = 'medium' THEN 1 END) as medium_risk_count,
    COUNT(CASE WHEN p.risk_level = 'low' THEN 1 END) as low_risk_count
FROM predictions p
WHERE p.created_at >= CURRENT_DATE - INTERVAL '30 days'
GROUP BY p.district, p.disease;

-- View: Disease Trend Analysis
CREATE OR REPLACE VIEW disease_trends AS
SELECT
    dc.district,
    dc.disease,
    dc.date,
    dc.cases,
    SUM(dc.cases) OVER (
        PARTITION BY dc.district, dc.disease
        ORDER BY dc.date
        ROWS BETWEEN 7 PRECEDING AND CURRENT ROW
    ) as cases_7day_rolling,
    LAG(dc.cases) OVER (
        PARTITION BY dc.district, dc.disease
        ORDER BY dc.date
    ) as previous_day_cases
FROM disease_cases dc
WHERE dc.date >= CURRENT_DATE - INTERVAL '90 days';

-- ================== Database Info ==================
-- Run these queries to check database structure:
--   \d disease_cases
--   \d predictions
--   \d alerts
--   SELECT table_name FROM information_schema.tables WHERE table_schema='public';

-- Index statistics:
--   SELECT * FROM pg_stat_user_indexes;
