import React from 'react';
import { Routes, Route } from 'react-router-dom';
import { Box } from '@mui/material';

import Layout from './components/Layout.tsx';
import Dashboard from './pages/Dashboard.tsx';
import StoryGeneration from './pages/StoryGeneration.tsx';
import EmotionAnalysis from './pages/EmotionAnalysis.tsx';
import CulturalAnalysis from './pages/CulturalAnalysis.tsx';
import AgentManagement from './pages/AgentManagement.tsx';
import WorkflowManagement from './pages/WorkflowManagement.tsx';
import Analytics from './pages/Analytics.tsx';

function App() {
  return (
    <Box sx={{ display: 'flex', minHeight: '100vh' }}>
      <Layout>
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/stories" element={<StoryGeneration />} />
          <Route path="/emotions" element={<EmotionAnalysis />} />
          <Route path="/cultural" element={<CulturalAnalysis />} />
          <Route path="/agents" element={<AgentManagement />} />
          <Route path="/workflows" element={<WorkflowManagement />} />
          <Route path="/analytics" element={<Analytics />} />
        </Routes>
      </Layout>
    </Box>
  );
}

export default App;