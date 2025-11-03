import React from 'react';
import { createRoot } from 'react-dom/client';
import './styles.css';
import OnboardProDashboard from './components/OnboardProDashboard.jsx';

createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <OnboardProDashboard />
  </React.StrictMode>
);
