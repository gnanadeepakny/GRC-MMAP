// ui/app/page.tsx
'use client'; // CRITICAL: Marks this component to run in the browser (needed for useEffect/useState)

import React, { useState, useEffect } from 'react';
import axios from 'axios'; // Import the HTTP client
import { List } from 'postcss/lib/list'; // Ensure List is imported for type hints

// Define the expected structure of the risk data from the FastAPI backend
interface RiskData {
  rating: string;
  count: number;
}
interface ControlData {
  control_name: string;
  finding_count: number;
}

const DashboardSummary = () => {
  const [riskData, setRiskData] = useState<RiskData[]>([]);
  const [controlData, setControlData] = useState<ControlData[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    // NOTE: Your FastAPI backend is running on port 8000
    const API_URL = 'http://127.0.0.1:8000/dashboard/summary'; 
    
    axios.get(API_URL)
      .then(response => {
        // Ensure the data structure matches the backend's /dashboard/summary endpoint
        setRiskData(response.data.risks_by_rating);
        setControlData(response.data.control_maturity);
        setLoading(false);
      })
      .catch(err => {
        console.error("API Fetch Error:", err);
        setError("Failed to fetch dashboard data. Check Docker containers (API/DB) and API URL.");
        setLoading(false);
      });
  }, []);

  if (loading) return <div className="text-xl p-10 text-gray-700">Loading GRC Data...</div>;
  if (error) return <div className="text-xl p-10 text-red-600">Error: {error}</div>;

  return (
    <main className="min-h-screen p-8 bg-gray-50">
      <h1 className="text-3xl font-bold mb-8 text-indigo-800 border-b pb-2">
        Project GRC-MMAP Dashboard Overview
      </h1>
      
      {/* 1. Risk Status Cards (Using Tailwind CSS for styling) */}
      <h2 className="text-2xl font-semibold mb-4 text-gray-700">Risk Status by Rating</h2>
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-10">
        {riskData.map((item) => (
          <div 
            key={item.rating} 
            className={`p-6 shadow-xl rounded-lg border-l-4 
              ${item.rating === 'Critical' ? 'border-red-600 bg-red-50' : 
                item.rating === 'High' ? 'border-orange-600 bg-orange-50' : 
                'border-green-600 bg-white'
              }`}
          >
            <p className="text-sm text-gray-500">{item.rating} Risks</p>
            <p className="text-4xl font-extrabold text-gray-900 mt-1">
              {item.count}
            </p>
          </div>
        ))}
      </div>

      {/* 2. Control Maturity / Compliance List */}
      <h2 className="text-2xl font-semibold mb-4 text-gray-700">
        Control Maturity Status (Compliance Footprint)
      </h2>
      <div className="bg-white shadow-xl rounded-lg p-6">
        <ul className="space-y-3">
          {controlData.map((item, index) => (
            <li key={index} className="flex justify-between items-center border-b pb-2">
              <span className="font-medium text-gray-800">{item.control_name}</span>
              <span className="text-sm text-indigo-600">
                {item.finding_count} Findings Attached
              </span>
            </li>
          ))}
        </ul>
      </div>

      {/* Trend Data (You can implement the chart visualization later) */}
      <div className="mt-8 text-center text-sm text-gray-500">
        *Finding Trend data loaded successfully (ready for chart visualization)*
      </div>
    </main>
  );
};

export default DashboardSummary;