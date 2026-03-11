# Frontend Quick Start Guide

## 🚀 Get Started in 5 Minutes

### Step 1: Install Dependencies
```bash
cd frontend
npm install
```

### Step 2: Start Development Server
```bash
npm run dev
```

Open your browser: **http://localhost:5173**

### Step 3: Explore the Dashboard
- 📊 **Dashboard**: View predictions and statistics
- 🗺️ **Risk Map**: See geographic risk distribution
- 🚨 **Alerts**: Monitor active health alerts

---

## 📁 Project Files Quick Reference

### Pages (Main Views)
| File | Purpose | Features |
|------|---------|----------|
| `pages/Dashboard.jsx` | Main dashboard | Stats, predictions, alerts |
| `pages/RiskMap.jsx` | Map visualization | Leaflet.js map with markers |
| `pages/Alerts.jsx` | Alert management | Filter, dismiss alerts |

### Components (Reusable)
| File | Purpose | Props |
|------|---------|-------|
| `components/Navbar.jsx` | Navigation | currentPage, setCurrentPage |
| `components/PredictionTable.jsx` | Data table | predictions (array) |
| `components/AlertPanel.jsx` | Alert display | alerts (array) |

### Configuration
- `tailwind.config.js` - TailwindCSS configuration
- `vite.config.js` - Build tool configuration
- `package.json` - Dependencies and scripts

---

## 🎨 TailwindCSS Classes Used

### Layout
```jsx
<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
<div className="flex items-center justify-between">
<div className="border-t-4 border-blue-500">
```

### Colors
```jsx
className="text-red-700 bg-red-50 border-red-500"  // High Risk
className="text-yellow-700 bg-yellow-50 border-yellow-500"  // Medium Risk
className="text-green-700 bg-green-50 border-green-500"  // Low Risk
```

### Utilities
```jsx
className="rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow"
className="font-bold text-lg text-gray-900"
className="space-y-4"  // Vertical spacing
```

---

## 📊 Displaying Data

### Example: Add New Prediction
```jsx
const newPrediction = {
  id: 4,
  location: 'Chennai',
  disease: 'Cholera',
  riskScore: 0.75,
  riskLevel: 'Medium',
  predictedCases: 32,
  timestamp: new Date().toLocaleDateString()
};

setPredictions([...predictions, newPrediction]);
```

### Example: Add New Alert
```jsx
const newAlert = {
  id: 4,
  title: 'Typhoid Risk Alert',
  region: 'Pune',
  severity: 'medium',
  affectedPopulation: 3500,
  timestamp: '30 minutes ago'
};

setAlerts([...alerts, newAlert]);
```

---

## 🔌 API Integration

### Setup Environment File
Create `frontend/.env.local`:
```
VITE_API_URL=http://localhost:5000
```

### Fetch Data from Backend
```jsx
import axios from 'axios';

useEffect(() => {
  const fetchData = async () => {
    try {
      const response = await axios.get(`${import.meta.env.VITE_API_URL}/api/predictions/list`);
      setPredictions(response.data);
    } catch (error) {
      console.error('Error:', error);
    }
  };
  fetchData();
}, []);
```

### Make Prediction Request
```jsx
const predictDisease = async () => {
  try {
    const response = await axios.post(
      `${import.meta.env.VITE_API_URL}/api/predictions/predict`,
      {
        district: 'New Delhi',
        rainfall: 250,
        temperature: 32,
        previous_cases: 150,
        population_density: 5000
      }
    );
    console.log('Prediction:', response.data);
  } catch (error) {
    console.error('Error:', error);
  }
};
```

---

## 🎯 Common Tasks

### Change a Component's Color
Find the component file and update className:
```jsx
// Before
className="border-blue-500"

// After
className="border-red-500"
```

### Add a New Statistic Card
Edit `pages/Dashboard.jsx`:
```jsx
<StatCard
  icon="🏥"
  label="Hospitals Alerted"
  value={50}
  color="border-purple-500"
/>
```

### Update Alert Data
Edit `pages/Alerts.jsx` in the useState:
```jsx
const [alerts, setAlerts] = React.useState([
  {
    id: 4,
    title: 'New Alert',
    region: 'Kolkata',
    severity: 'low',
    message: 'Low dengue risk',
    affectedPopulation: 1000,
    timestamp: 'Just now'
  }
]);
```

### Add Navigation Item
Edit `components/Navbar.jsx`:
```jsx
const navItems = [
  { id: 'dashboard', label: 'Dashboard', icon: '📊' },
  { id: 'map', label: 'Risk Map', icon: '🗺️' },
  { id: 'alerts', label: 'Alerts', icon: '🚨' },
  { id: 'reports', label: 'Reports', icon: '📈' }  // New item
];
```

---

## 🧪 Testing Components

### Test in Browser Console
```javascript
// Check if Navbar renders
console.log(document.querySelector('nav'));

// Check predictions data
console.log(predictions);
```

### View Network Requests
1. Open DevTools (F12)
2. Go to Network tab
3. Make API calls and watch requests

---

## 📦 Build for Production

```bash
npm run build
```

Creates optimized build in `dist/` folder.

### Deploy to Server
```bash
# Copy dist folder to web server
cp -r dist/* /var/www/dhritrashtra/
```

---

## 🐛 Troubleshooting

### Styles not showing?
```bash
# Clear cache and reinstall
npm install
```

### API not connecting?
1. Check backend is running (npm run dev in backend folder)
2. Verify VITE_API_URL in .env.local
3. Check CORS is enabled in Flask app

### Map not displaying?
```jsx
// Make sure this import is present
import 'leaflet/dist/leaflet.css';
```

### Port already in use?
```bash
npm run dev -- --port 5174
```

---

## 📚 Learn More

- **TailwindCSS**: https://tailwindcss.com/docs
- **React Hooks**: https://react.dev/reference/react
- **Leaflet Maps**: https://leafletjs.com
- **Axios HTTP**: https://axios-http.com

---

## 🚀 Next Steps

1. ✅ Run development server
2. ✅ Explore all three pages
3. ✅ Check console for any errors
4. ✅ Connect to backend API
5. ✅ Customize colors and layouts
6. ✅ Deploy to production

---

**Happy Coding! 🎉**

For help, check `FRONTEND_GUIDE.md` for detailed documentation.
