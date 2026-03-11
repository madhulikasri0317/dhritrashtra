# React Components Reference Guide

## Complete Component Documentation

---

## 1. Navbar Component

**Location:** `src/components/Navbar.jsx`

### Purpose
Top navigation bar with responsive design, brand logo, and navigation menu for page switching.

### Props
```javascript
interface NavbarProps {
  currentPage: string;        // Currently active page ID
  setCurrentPage: (page: string) => void;  // Function to change page
}
```

### State
```javascript
const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
```

### Features
- ✅ Sticky positioning (stays at top when scrolling)
- ✅ Responsive design (desktop menu + mobile hamburger)
- ✅ Active page highlighting
- ✅ Real-time status indicator (green dot)
- ✅ Last updated timestamp
- ✅ Smooth transitions and hover effects

### Structure
```
Navbar (nav.sticky.top-0)
├── Logo Section (brand)
├── Desktop Menu (hidden on mobile)
│   ├── Dashboard
│   ├── Risk Map
│   └── Alerts
├── Status Section (time + indicator)
└── Mobile Menu Button (visible on mobile)
    └── Mobile Navigation
        ├── Dashboard
        ├── Risk Map
        └── Alerts
```

### Usage Example
```jsx
import Navbar from './components/Navbar';

function App() {
  const [currentPage, setCurrentPage] = useState('dashboard');

  return (
    <div>
      <Navbar currentPage={currentPage} setCurrentPage={setCurrentPage} />
      {/* Main content */}
    </div>
  );
}
```

### Styling Details
**Active State:**
```jsx
currentPage === item.id
  ? 'bg-blue-100 text-blue-700 border-b-2 border-blue-600'
  : 'text-gray-700 hover:bg-gray-100'
```

**Responsive Breakpoints:**
- Mobile: Hamburger menu
- `md` (768px): Desktop navigation
- `lg` (1024px): Full status section visible

---

## 2. PredictionTable Component

**Location:** `src/components/PredictionTable.jsx`

### Purpose
Displays prediction data in a responsive, sortable table with color-coded risk levels.

### Props
```javascript
interface PredictionTableProps {
  predictions: Prediction[];
}

interface Prediction {
  id: number;
  location: string;
  disease: string;
  riskScore: number;        // 0-1
  riskLevel: 'High' | 'Medium' | 'Low';
  predictedCases: number;
  timestamp: string;
}
```

### Features
- ✅ Responsive table (horizontal scroll on mobile)
- ✅ Color-coded rows by risk level
- ✅ Risk score progress bars
- ✅ Risk percentage display
- ✅ Hover effects for better UX
- ✅ Predicted cases count
- ✅ Timestamp display

### Color Mapping
```javascript
const getRiskColor = (riskLevel) => {
  switch(riskLevel.toLowerCase()) {
    case 'high':
      return { bg: 'bg-red-50', text: 'text-red-700', badge: 'bg-red-100' };
    case 'medium':
      return { bg: 'bg-yellow-50', text: 'text-yellow-700', badge: 'bg-yellow-100' };
    case 'low':
      return { bg: 'bg-green-50', text: 'text-green-700', badge: 'bg-green-100' };
  }
};
```

### Structure
```
table
├── thead (bg-gray-50)
│   └── tr
│       ├── th: Location
│       ├── th: Disease
│       ├── th: Risk Score
│       ├── th: Risk Level
│       ├── th: Predicted Cases
│       └── th: Date
└── tbody (divide-y)
    └── tr (per prediction)
        ├── td: location
        ├── td: disease
        ├── td: progress bar + percentage
        ├── td: badge
        ├── td: case count
        └── td: timestamp
```

### Usage Example
```jsx
import PredictionTable from './components/PredictionTable';

function Dashboard() {
  const [predictions, setPredictions] = useState([
    {
      id: 1,
      location: 'New Delhi',
      disease: 'Cholera',
      riskScore: 0.85,
      riskLevel: 'High',
      predictedCases: 45,
      timestamp: '2026-03-10'
    }
  ]);

  return <PredictionTable predictions={predictions} />;
}
```

### Progress Bar Implementation
```jsx
<div className="w-24 h-2 bg-gray-200 rounded-full overflow-hidden">
  <div
    className={`h-full ${barColor} transition-all duration-300`}
    style={{ width: `${prediction.riskScore * 100}%` }}
  ></div>
</div>
```

---

## 3. AlertPanel Component

**Location:** `src/components/AlertPanel.jsx`

### Purpose
Compact alert notification display showing active health alerts with severity indicators.

### Props
```javascript
interface AlertPanelProps {
  alerts: Alert[];
}

interface Alert {
  id: number;
  title: string;
  region: string;
  severity: 'high' | 'medium' | 'low';
  affectedPopulation: number;
  timestamp: string;
}
```

### Features
- ✅ Color-coded by severity
- ✅ Severity icons (🔴 🟡 🟢)
- ✅ Affected population display
- ✅ Timestamp information
- ✅ Empty state message
- ✅ Hover effects
- ✅ Compact vertical layout

### Severity Colors
```javascript
const getSeverityColors = (severity) => {
  switch(severity.toLowerCase()) {
    case 'high':
      return { bg: 'bg-red-50', border: 'border-l-4 border-red-500', icon: '🔴' };
    case 'medium':
      return { bg: 'bg-yellow-50', border: 'border-l-4 border-yellow-500', icon: '🟡' };
    case 'low':
      return { bg: 'bg-green-50', border: 'border-l-4 border-green-500', icon: '🟢' };
  }
};
```

### Structure
```
div (space-y-3)
├── Empty State (if length === 0)
└── Alert Items (for each alert)
    ├── Icon (severity emoji)
    ├── Content
    │   ├── Title (h4)
    │   ├── Region (xs text)
    │   └── Affected population (xs text)
    └── Timestamp (xs text)
```

### Usage Example
```jsx
import AlertPanel from './components/AlertPanel';

function Dashboard() {
  const [alerts, setAlerts] = useState([
    {
      id: 1,
      title: 'High Cholera Risk',
      region: 'New Delhi',
      severity: 'high',
      affectedPopulation: 10000,
      timestamp: '2 hours ago'
    }
  ]);

  return <AlertPanel alerts={alerts} />;
}
```

---

## 4. Dashboard Page

**Location:** `src/pages/Dashboard.jsx`

### Purpose
Main dashboard view displaying predictions, alerts, and statistics overview.

### State
```javascript
const [predictions, setPredictions] = useState([...]);
const [alerts, setAlerts] = useState([...]);
```

### Features
- ✅ 4 statistics cards (Predictions, High Risk, Active Alerts, Cases)
- ✅ Responsive grid layout
- ✅ Prediction table embedded
- ✅ Alert panel embedded
- ✅ System status information
- ✅ Real-time data display

### Computed Values
```javascript
const highRiskCount = predictions.filter(p => p.riskLevel === 'High').length;
const totalCases = predictions.reduce((sum, p) => sum + p.predictedCases, 0);
```

### Structure
```
div (space-y-8)
├── Header
│   ├── h1: Dashboard title
│   └── p: Subtitle
├── Statistics Grid (grid-cols-1 md:grid-cols-2 lg:grid-cols-4)
│   ├── StatCard: Predictions
│   ├── StatCard: High Risk Areas
│   ├── StatCard: Active Alerts
│   └── StatCard: Predicted Cases
├── Main Content (grid-cols-1 lg:grid-cols-3)
│   ├── PredictionTable (lg:col-span-2)
│   └── AlertPanel (lg:col-span-1)
└── Footer Info Box
```

### StatCard Component (Inline)
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
```

---

## 5. RiskMap Page

**Location:** `src/pages/RiskMap.jsx`

### Purpose
Interactive geographic map visualization showing disease outbreak risk distribution.

### State
```javascript
const mapContainer = useRef(null);
const map = useRef(null);
```

### Features
- ✅ Leaflet.js integration
- ✅ OpenStreetMap tile layer
- ✅ Circle markers for locations
- ✅ Color-coded risk levels
- ✅ Interactive popups
- ✅ Legend with explanations
- ✅ Zoom and pan controls
- ✅ Responsive container

### Map Initialization
```javascript
map.current = L.map(mapContainer.current).setView([28.7041, 77.1025], 10);
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
  attribution: '© OpenStreetMap contributors'
}).addTo(map.current);
```

### Marker Configuration
```javascript
const riskLocations = [
  { lat: 28.6139, lon: 77.2090, risk: 0.85, disease: 'Cholera' },
  // ...
];

riskLocations.forEach(location => {
  const riskColor = location.risk > 0.7 ? '#dc2626' :
                    location.risk > 0.4 ? '#f59e0b' : '#10b981';

  L.circleMarker([location.lat, location.lon], {
    radius: 10,
    fillColor: riskColor,
    color: '#000',
    weight: 2,
    fillOpacity: 0.8
  }).addTo(map.current);
});
```

### Structure
```
div (space-y-6)
├── Header (title + subtitle)
├── Legend Box
│   ├── High Risk (>70%)
│   ├── Medium Risk (40-70%)
│   └── Low Risk (<40%)
├── Map Container
│   └── div#map (h-96 md:h-[500px] lg:h-[600px])
└── Info Box
```

---

## 6. Alerts Page

**Location:** `src/pages/Alerts.jsx`

### Purpose
Comprehensive alert management interface with severity filtering and dismissal functionality.

### State
```javascript
const [alerts, setAlerts] = useState([...]);
```

### Features
- ✅ Severity-based styling
- ✅ Summary statistics cards
- ✅ Detailed alert cards
- ✅ Dismiss functionality
- ✅ Affected population display
- ✅ Time tracking
- ✅ Empty state handling
- ✅ Responsive layout

### Alert Dismissal
```javascript
const dismissAlert = (id) => {
  setAlerts(alerts.filter(alert => alert.id !== id));
};
```

### Structure
```
div (space-y-8)
├── Header (title + subtitle)
├── Summary Stats (grid-cols-1 md:grid-cols-3)
│   ├── High Severity Count
│   ├── Medium Severity Count
│   └── Low Severity Count
├── Alerts List (space-y-4)
│   ├── Empty State (if no alerts)
│   └── Alert Cards
│       ├── Header Section
│       │   ├── Title
│       │   └── Severity Badge
│       ├── Body Section
│       │   ├── Region
│       │   ├── Message
│       │   └── Stats Grid
│       └── Footer (Dismiss Button)
└── Info Box
```

---

## Component Hierarchy

```
App
├── Navbar
│   └── Navigation Items
└── Main Content (based on currentPage)
    ├── Dashboard
    │   ├── Statistics Cards
    │   ├── PredictionTable
    │   └── AlertPanel
    ├── RiskMap
    │   ├── Legend
    │   └── Leaflet Map
    └── Alerts
        ├── Summary Cards
        └── Alert Cards
```

---

## Styling Guidelines

### TailwindCSS Classes Organization

**Layout:**
- `flex`, `grid`, `space-y-*`, `gap-*`

**Colors:**
- Text: `text-gray-900`, `text-gray-600`, `text-blue-700`
- Background: `bg-white`, `bg-gray-50`, `bg-red-50`
- Borders: `border`, `border-t-4`, `border-gray-200`

**Effects:**
- Shadows: `shadow-md`, `shadow-lg`, `hover:shadow-lg`
- Rounded: `rounded`, `rounded-lg`, `rounded-full`
- Transitions: `transition-colors`, `transition-shadow`, `duration-200`

### Common Patterns

**Card Layout:**
```jsx
<div className="bg-white rounded-lg shadow-md p-6">
  {/* content */}
</div>
```

**Grid Responsive:**
```jsx
<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
```

**Badge:**
```jsx
<span className="px-3 py-1 rounded-full text-xs font-bold bg-red-100 text-red-800">
  HIGH
</span>
```

---

## Data Flow

### How Data Flows Through Components

```
Backend API
    ↓
Dashboard useState (predictions, alerts)
    ↓
    ├─→ PredictionTable (props: predictions)
    │       ↓
    │   Renders: Table rows with color coding
    │
    └─→ AlertPanel (props: alerts)
            ↓
        Renders: Alert cards
```

### Event Flow

```
User clicks "Dismiss Alert"
    ↓
AlertPanel captures click
    ↓
Calls dismissAlert(id)
    ↓
Updates Alerts state
    ↓
Component re-renders
    ↓
Alert removed from UI
```

---

## Performance Considerations

### Memoization
```jsx
const PredictionTable = React.memo(({ predictions }) => {
  // Only re-renders if predictions prop changes
});
```

### useCallback
```jsx
const handleDismiss = useCallback((id) => {
  setAlerts(alerts.filter(a => a.id !== id));
}, [alerts]);
```

### useEffect Dependencies
```jsx
useEffect(() => {
  // Fetch data only on mount
  fetchPredictions();
}, []); // Empty dependency array
```

---

## CSS Classes Reference

### Tailwind Utilities Used

| Purpose | Classes |
|---------|---------|
| Spacing | `p-4`, `m-2`, `space-y-4`, `gap-6` |
| Typography | `font-bold`, `text-lg`, `text-center` |
| Colors | `text-red-700`, `bg-blue-50`, `border-green-500` |
| Responsive | `md:grid-cols-2`, `lg:col-span-2` |
| Interactions | `hover:shadow-lg`, `transition-colors` |
| Sizing | `w-full`, `h-screen`, `max-w-7xl` |
| Positioning | `sticky`, `fixed`, `relative` |
| Shadows | `shadow-md`, `shadow-lg` |
| Rounded | `rounded-lg`, `rounded-full`, `rounded-t` |

---

## Debugging Tips

### Console Logging
```javascript
console.log('Component rendered');
console.log('Props:', props);
console.log('State:', state);
```

### React DevTools
- Inspect component tree
- View props and state
- Track re-renders

### Network Debugging
- Open DevTools → Network tab
- Make API calls
- Inspect request/response

---

**Last Updated:** March 10, 2026
**Version:** 1.0.0
