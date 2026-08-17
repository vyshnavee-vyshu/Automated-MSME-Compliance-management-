import apiClient from './apiClient'

/**
 * Uploads a compliance document to the backend.
 * Backend endpoint (to be implemented): POST /api/documents/upload
 * Expects multipart/form-data with a "file" field.
 *
 * @param {File} file
 * @param {(progress: number) => void} onUploadProgress
 * @returns {Promise<any>}
 */
export async function uploadDocument(file, onUploadProgress) {
  const formData = new FormData()
  formData.append('file', file)

  const response = await apiClient.post('/api/documents/upload', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
    onUploadProgress: (event) => {
      if (onUploadProgress && event.total) {
        const percent = Math.round((event.loaded * 100) / event.total)
        onUploadProgress(percent)
      }
    },
  })

  return response.data
}

/**
 * Fetches the list of previously uploaded documents.
 * Backend endpoint (to be implemented): GET /api/documents
 */
export async function getDocuments() {
  const response = await apiClient.get('/api/documents')
  return response.data
}
