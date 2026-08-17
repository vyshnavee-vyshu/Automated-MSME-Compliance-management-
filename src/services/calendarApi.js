import apiClient from './apiClient'

/**
 * Fetches compliance calendar events.
 * Backend endpoint (to be implemented): GET /api/compliance/calendar
 *
 * Expected response item shape:
 * {
 *   compliance_name: string,
 *   category: string,
 *   due_date: string,
 *   status: 'Completed' | 'Upcoming' | 'Due Soon' | 'Overdue',
 *   priority: string
 * }
 */
export async function getComplianceCalendar() {
  const response = await apiClient.get('/api/compliance/calendar')
  return response.data
}
