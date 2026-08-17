import apiClient from './apiClient'

/**
 * Sends a user message to the compliance chatbot.
 * Backend endpoint (to be implemented): POST /api/chat
 *
 * Request body: { message: string }
 * Response body: { answer: string, sources: Array }
 *
 * @param {string} message
 */
export async function sendChatMessage(message) {
  const response = await apiClient.post('/api/chat', { message })
  return response.data
}
