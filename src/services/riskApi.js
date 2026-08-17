import apiClient from './apiClient'

/**
 * Fetches the current compliance risk analysis.
 * Backend endpoint (to be implemented): GET /api/risk
 *
 * Expected response shape:
 * {
 *   overall_score: number,
 *   risk_level: 'Critical' | 'High' | 'Medium' | 'Low',
 *   factors: [
 *     {
 *       title: string,
 *       severity: 'Critical' | 'High' | 'Medium' | 'Low',
 *       reason: string,
 *       date_detected: string,
 *       recommended_action: string
 *     }
 *   ]
 * }
 */
export async function getRiskAnalysis() {
  const response = await apiClient.get('/api/risk')
  return response.data
}
