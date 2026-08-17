import apiClient from './apiClient'

/**
 * Fetches the latest regulatory news updates.
 * Backend endpoint (to be implemented): GET /api/news
 *
 * Expected response item shape:
 * {
 *   title: string,
 *   authority: string,
 *   category: string,
 *   published_date: string,
 *   effective_date: string,
 *   summary: string,
 *   source_url: string,
 *   impact: string
 * }
 */
export async function getLatestNews() {
  const response = await apiClient.get('/api/news')
  return response.data
}
