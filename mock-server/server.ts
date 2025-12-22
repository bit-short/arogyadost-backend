import express from 'express';
import cors from 'cors';
import { healthCategories, recommendedActions, healthMetrics, healthReportMetrics } from './data/health.js';
import { dailyRoutine, weeklyRoutine } from './data/routines.js';
import { chatThreads, chatSpaces, chatVoices } from './data/chat.js';
import { userProfiles, dataSources } from './data/settings.js';
import { allCardiologists } from './data/doctors.js';
import { labs, testTypeLabels } from './data/labs.js';
import { biomarkerData } from './data/biomarkers.js';
import { metricDetails } from './data/metrics.js';
import { actionDetails } from './data/actions.js';

const app = express();
const PORT = process.env.PORT || 3001;

// Middleware
app.use(cors());
app.use(express.json());

// Add delay to simulate real API
const delay = (ms: number) => new Promise(resolve => setTimeout(resolve, ms));

// Health endpoints
app.get('/api/health/biomarkers', async (req, res) => {
  await delay(300);
  res.json(healthCategories);
});

app.get('/api/health/recommendations', async (req, res) => {
  await delay(200);
  res.json(recommendedActions);
});

app.get('/api/health/metrics', async (req, res) => {
  await delay(250);
  res.json(healthReportMetrics);
});

app.get('/api/health/status', async (req, res) => {
  await delay(300);
  res.json(healthMetrics);
});

app.get('/api/biomarkers/:id', async (req, res) => {
  await delay(400);
  const { id } = req.params;
  const data = biomarkerData[id];
  
  if (!data) {
    return res.status(404).json({ error: 'Biomarker not found' });
  }
  
  res.json(data);
});

app.get('/api/metrics/:id', async (req, res) => {
  await delay(350);
  const { id } = req.params;
  const data = metricDetails[id];
  
  if (!data) {
    return res.status(404).json({ error: 'Metric not found' });
  }
  
  res.json(data);
});

// Routines endpoints
app.get('/api/routines/daily', async (req, res) => {
  await delay(200);
  res.json(dailyRoutine);
});

app.get('/api/routines/weekly', async (req, res) => {
  await delay(200);
  res.json(weeklyRoutine);
});

// Chat endpoints
app.get('/api/chat/threads', async (req, res) => {
  await delay(150);
  res.json(chatThreads);
});

app.get('/api/chat/spaces', async (req, res) => {
  await delay(150);
  res.json(chatSpaces);
});

app.get('/api/chat/voices', async (req, res) => {
  await delay(100);
  res.json(chatVoices);
});

// Settings endpoints
app.get('/api/settings/profiles', async (req, res) => {
  await delay(100);
  res.json(userProfiles);
});

app.get('/api/settings/data-sources', async (req, res) => {
  await delay(200);
  res.json(dataSources);
});

// Search endpoints
app.get('/api/doctors/cardiologists', async (req, res) => {
  await delay(500);
  res.json(allCardiologists);
});

app.get('/api/labs', async (req, res) => {
  await delay(400);
  const { testType } = req.query;
  
  let filteredLabs = labs;
  
  if (testType && testTypeLabels[testType as string]) {
    // Filter labs that support the specific test type
    filteredLabs = labs.filter(lab => 
      lab.specialties.some(specialty => 
        specialty.toLowerCase().includes(testType as string) ||
        specialty.toLowerCase().includes('blood work') ||
        specialty.toLowerCase().includes('full panels')
      )
    );
  }
  
  res.json(filteredLabs);
});

// Actions endpoints
app.get('/api/actions/:id', async (req, res) => {
  await delay(300);
  const { id } = req.params;
  const data = actionDetails[id];
  
  if (!data) {
    return res.status(404).json({ error: 'Action not found' });
  }
  
  res.json(data);
});

// Health check endpoint
app.get('/api/health', (req, res) => {
  res.json({ status: 'OK', timestamp: new Date().toISOString() });
});

// Error handling middleware
app.use((err: any, req: express.Request, res: express.Response, next: express.NextFunction) => {
  console.error(err.stack);
  res.status(500).json({ error: 'Something went wrong!' });
});

// 404 handler
app.use('*', (req, res) => {
  res.status(404).json({ error: 'Endpoint not found' });
});

app.listen(PORT, () => {
  console.log(`🚀 Mock API server running on http://localhost:${PORT}`);
  console.log(`📊 Health check: http://localhost:${PORT}/api/health`);
});

export default app;