# Dhritrashtra Frontend - Complete Guide

## Overview

The Dhritrashtra frontend is a modern React dashboard UI built with:
- **React 18** - UI library
- **Vite** - Fast build tool
- **TailwindCSS 3.3** - Utility-first CSS framework
- **Leaflet.js** - Interactive map visualization
- **Axios** - HTTP client for API communication

## Project Structure

```
frontend/
├── src/
│   ├── pages/
│   │   ├── Dashboard.jsx      # Main dashboard with predictions & stats
│   │   ├── RiskMap.jsx        # Geographic heat map visualization
│   │   └── Alerts.jsx         # Alert management and monitoring
│   ├── components/
│   │   ├── Navbar.jsx         # Top navigation with menu
│   │   ├── PredictionTable.jsx # Risk predictions table
│   │   └── AlertPanel.jsx     # Alert notifications panel
│   ├── App.jsx                # Main app component
│   ├── index.js               # Entry point
│   ├── index.css              # Global Tailwind styles
│   └── App.css                # App-specific styles
├── public/
├── index.html                 # HTML template
├── tailwind.config.js         # TailwindCSS configuration
├── vite.config.js             # Vite configuration
├── package.json               # Project dependencies
└── Dockerfile                 # Docker container config
```

## Components Overview

### 1. Navbar Component
**File:** `src/components/Navbar.jsx`

Sticky navigation bar with responsive design.

**Features:**
- Brand logo and title
- Desktop and mobile navigation menus
- Real-time status indicator
- Active page highlighting
- Hamburger menu for mobile devices

**Props:**
- `currentPage` (string) - Currently active page
- `setCurrentPage` (function) - Callback to change page

**Example:**
```jsx
<Navbar currentPage="dashboard" setCurrentPage={setCurrentPage} />
```

### 2. Dashboard Page
**File:** `src/pages/Dashboard.jsx`

Main dashboard showing predictions and alerts overview.

**Features:**
- 4 statistics cards (Predictions, High Risk Areas, Active Alerts, Predicted Cases)
- Responsive grid layout
- Prediction table integration
- Alert panel integration
- System status information

**Statistics Displayed:**
- Current Predictions: Total number of predictions
- High Risk Areas: Count of high-risk zones
- Active Alerts: Number of active alerts
- Predicted Cases: Total forecasted cases

### 3. PredictionTable Component
**File:** `src/components/PredictionTable.jsx`

Displays prediction data in an interactive table format.

**Features:**
- Sortable columns
- Color-coded risk levels
- Risk score progress bars
- Risk percentage display
- Predicted cases count
- Responsive overflow handling

**Table Columns:**
| Column | Type | Description |
|--------|------|-------------|
| Location | string | Geographic area |
| Disease | string | Disease name |
| Risk Score | number | 0-1 probability |
| Risk Level | enum | High/Medium/Low |
| Predicted Cases | number | Case forecast |
| Date | date | Prediction timestamp |

**Risk Colors:**
- High (>0.7): Red (#dc2626)
- Medium (0.4-0.7): Yellow (#f59e0b)
- Low (<0.4): Green (#10b981)

### 4. AlertPanel Component
**File:** `src/components/AlertPanel.jsx`

Compact alert notification display.

**Features:**
- Color-coded severity levels
- Affected population display
- Timestamp information
- Icon indicators
- Empty state display

**Props:**
- `alerts` (array) - Array of alert objects

**Alert Object Structure:**
```javascript
{
  id: number,
  title: string,
  region: string,
  severity: 'high' | 'medium' | 'low',
  affectedPopulation: number,
  timestamp: string
}
```

### 5. RiskMap Page
**File:** `src/pages/RiskMap.jsx`

Interactive geographic map with risk visualization.

**Features:**
- Leaflet.js integration
- OpenStreetMap tile layer
- Circle markers for disease locations
- Color-coded risk indicators
- Interactive popups with details
- Legend explanation
- Zoom and pan controls

**Marker Colors:**
- High Risk (>70%): Red
- Medium Risk (40-70%): Yellow
- Low Risk (<40%): Green

### 6. Alerts Page
**File:** `src/pages/Alerts.jsx`

Comprehensive alert management interface.

**Features:**
- Severity-based card styling
- Affected population metrics
- Time tracking
- Dismiss functionality
- Severity summary statistics
- Empty state handling
- Alert filtering by severity

**Alert Sections:**
- Alert title and severity badge
- Region information
- Detailed message
- Affected population count
- Time since alert
- Dismiss button

## Styling with TailwindCSS

### Color Palette

**Risk Levels:**
- High Risk: `text-red-700`, `bg-red-50`, `border-red-500`
- Medium Risk: `text-yellow-700`, `bg-yellow-50`, `border-yellow-500`
- Low Risk: `text-green-700`, `bg-green-50`, `border-green-500`

**UI Elements:**
- Primary: `blue-500` (navigation, primary action)
- Text: `gray-900` (headings), `gray-600` (body)
- Background: `gray-50` (main), `white` (cards)
- Border: `gray-200` (dividers)

### Responsive Design

Tailwind breakpoints used:
- `sm` - Small devices (640px)
- `md` - Medium devices (768px)
- `lg` - Large devices (1024px)

**Grid System:**
```jsx
// Single column → 2 columns on medium → 4 columns on large
<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
```

### Utility Classes

**Common Patterns:**
- Spacing: `p-6`, `m-4`, `space-y-4`
- Typography: `font-bold`, `text-lg`, `text-gray-900`
- Shadows: `shadow-md`, `shadow-lg`
- Borders: `border-t-4`, `rounded-lg`
- Transitions: `transition-colors`, `duration-200`

## Data Flow

### Dashboard Data Flow

```
┌─────────────────┐
│  Backend API    │
│ /api/predictions│
│  /api/alerts    │
└────────┬────────┘
         │
         ↓
┌─────────────────┐
│   useState      │
│  predictions[]  │
│    alerts[]     │
└────────┬────────┘
         │
    ┌────┴────┐
    ↓         ↓
┌─────────────────┐  ┌──────────────┐
│PredictionTable  │  │ AlertPanel   │
│   Display       │  │  Display     │
└─────────────────┘  └──────────────┘
```

### API Integration

**Endpoints Used:**

1. **Get Predictions**
```
GET /api/predictions/list
Response: Array of prediction objects
```

2. **Make Prediction**
```
POST /api/predictions/predict
Payload: { district, rainfall, temperature, previous_cases, population_density }
Response: { risk_level, predicted_cases, confidence, ... }
```

3. **Get Alerts**
```
GET /api/alerts/list
Response: Array of alert objects
```

4. **Risk Map Data**
```
GET /api/maps/risk-data
Response: Array of geographic risk points
```

## Setup & Installation

### Prerequisites
- Node.js 16+
- npm or yarn

### Installation Steps

1. **Install Dependencies**
```bash
cd frontend
npm install
```

2. **Configure Environment**
```bash
# Copy example config
cp .env.example .env.local

# Edit .env.local with your backend URL
VITE_API_URL=http://localhost:5000
```

3. **Start Development Server**
```bash
npm run dev
```

Server runs at: `http://localhost:5173`

4. **Build for Production**
```bash
npm run build
```

Output: `dist/` folder

## Usage Examples

### Adding a New Statistic Card

```jsx
const StatCard = ({ icon, label, value, color }) => (
  <div className={`bg-white rounded-lg shadow-md p-6 border-t-4 ${color}`}>
    <div className="flex items-center justify-between">
      <div>
        <p className="text-gray-600 text-sm font-medium">{label}</p>
        <p className="text-3xl font-bold text-gray-900 mt-2">{value}</p>
      </div>
      <div className="text-4xl">{icon}</div>
    </div>
  </div>
);

// Usage in Dashboard
<StatCard
  icon="📊"
  label="Predictions"
  value={predictions.length}
  color="border-blue-500"
/>
```

### Fetching Data from API

```jsx
import axios from 'axios';

useEffect(() => {
  const fetchPredictions = async () => {
    try {
      const response = await axios.get('/api/predictions/list');
      setPredictions(response.data);
    } catch (error) {
      console.error('Error fetching predictions:', error);
    }
  };

  fetchPredictions();
}, []);
```

### Making API Prediction Request

```jsx
const makePrediction = async (data) => {
  try {
    const response = await axios.post('/api/predictions/predict', {
      district: data.district,
      rainfall: data.rainfall,
      temperature: data.temperature,
      previous_cases: data.previous_cases,
      population_density: data.population_density
    });

    console.log('Prediction:', response.data);
  } catch (error) {
    console.error('Error making prediction:', error);
  }
};
```

## Performance Optimization

### 1. Code Splitting
Components are automatically code-split by Vite:
```jsx
// Lazy load pages for better initial load
const Dashboard = lazy(() => import('./pages/Dashboard'));
const RiskMap = lazy(() => import('./pages/RiskMap'));
```

### 2. Memoization
Prevent unnecessary re-renders:
```jsx
const PredictionTable = React.memo(({ predictions }) => {
  // Component code
});
```

### 3. Image Optimization
Use appropriate image formats and sizes.

### 4. Caching
Configure API response caching:
```javascript
const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL,
  timeout: 10000,
});
```

## Testing

### Unit Tests
```bash
npm run test
```

### E2E Tests
```bash
npm run test:e2e
```

### Accessibility Testing
- Keyboard navigation
- Screen reader compatibility
- Color contrast verification

## Deployment

### Docker Deployment

**Build Docker image:**
```bash
docker build -t dhritrashtra-frontend .
```

**Run container:**
```bash
docker run -p 3000:3000 dhritrashtra-frontend
```

### Environment Configuration

**Development:**
```
VITE_API_URL=http://localhost:5000
```

**Production:**
```
VITE_API_URL=https://api.dhritrashtra.com
```

## Common Issues & Solutions

### Issue 1: Styles not applying
**Solution:** Ensure TailwindCSS is properly configured in `tailwind.config.js`

### Issue 2: Map not displaying
**Solution:** Check that Leaflet CSS is imported: `import 'leaflet/dist/leaflet.css'`

### Issue 3: API calls failing
**Solution:** Verify backend is running and CORS is configured

### Issue 4: Build errors
**Solution:** Clear node_modules and reinstall:
```bash
rm -rf node_modules package-lock.json
npm install
```

## Best Practices

1. **Component Organization**
   - Separate presentational and container components
   - Keep components focused and reusable
   - Use meaningful names

2. **State Management**
   - Use useState for local state
   - Keep state as close as possible to where it's used
   - Consider Context API for shared state

3. **Performance**
   - Use React.memo for pure components
   - Lazy load heavy components
   - Optimize re-renders

4. **Accessibility**
   - Semantic HTML elements
   - ARIA labels where needed
   - Keyboard navigation support

5. **Error Handling**
   - Graceful error messages
   - Fallback UI states
   - Logging for debugging

## Browser Support

- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

## Resources

- [React Documentation](https://react.dev)
- [TailwindCSS Docs](https://tailwindcss.com/docs)
- [Leaflet Documentation](https://leafletjs.com)
- [Axios Documentation](https://axios-http.com)
- [Vite Documentation](https://vitejs.dev)

## Security Considerations

1. **API Communication**
   - Use HTTPS in production
   - Validate all user inputs
   - Implement CORS properly

2. **Data Privacy**
   - Don't store sensitive data in localStorage
   - Use secure session management
   - Encrypt sensitive API payloads

3. **XSS Prevention**
   - React escapes content by default
   - Use dangerouslySetInnerHTML carefully
   - Sanitize HTML if needed

## Version History

- **1.0.0** (2026-03-10): Initial release with Dashboard, RiskMap, and Alerts pages

## Support & Contribution

For issues, questions, or contributions, please contact the development team.

---

**Last Updated:** March 10, 2026
**Status:** ✅ Production Ready
