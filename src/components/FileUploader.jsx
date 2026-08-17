import { useCallback, useRef, useState } from 'react'
import { UploadCloud, FileText, X, CheckCircle2, AlertCircle } from 'lucide-react'
import { formatFileSize, MAX_FILE_SIZE_BYTES, ACCEPTED_DOCUMENT_EXTENSIONS } from '../utils/formatters'
import { uploadDocument } from '../services/documentApi'

const ACCEPT_STRING = ACCEPTED_DOCUMENT_EXTENSIONS.join(',')

export default function FileUploader() {
  const [isDragging, setIsDragging] = useState(false)
  const [file, setFile] = useState(null)
  const [status, setStatus] = useState('idle') // idle | uploading | success | error
  const [progress, setProgress] = useState(0)
  const [errorMessage, setErrorMessage] = useState('')
  const inputRef = useRef(null)

  const validateAndSetFile = useCallback((selected) => {
    if (!selected) return

    const extension = `.${selected.name.split('.').pop().toLowerCase()}`
    if (!ACCEPTED_DOCUMENT_EXTENSIONS.includes(extension)) {
      setErrorMessage('Unsupported file type. Please upload a PDF, PNG, JPG or DOCX file.')
      setStatus('error')
      return
    }

    if (selected.size > MAX_FILE_SIZE_BYTES) {
      setErrorMessage('File exceeds the 10 MB size limit.')
      setStatus('error')
      return
    }

    setErrorMessage('')
    setStatus('idle')
    setProgress(0)
    setFile(selected)
  }, [])

  const handleDrop = useCallback(
    (event) => {
      event.preventDefault()
      setIsDragging(false)
      const dropped = event.dataTransfer.files?.[0]
      validateAndSetFile(dropped)
    },
    [validateAndSetFile],
  )

  const handleBrowse = (event) => {
    const selected = event.target.files?.[0]
    validateAndSetFile(selected)
  }

  const handleRemove = () => {
    setFile(null)
    setStatus('idle')
    setProgress(0)
    setErrorMessage('')
    if (inputRef.current) inputRef.current.value = ''
  }

  const handleUpload = async () => {
    if (!file) return
    setStatus('uploading')
    setProgress(0)

    try {
      await uploadDocument(file, setProgress)
      setStatus('success')
    } catch (err) {
      setStatus('error')
      setErrorMessage(
        err?.response?.data?.message || 'Upload failed. Please check your connection and try again.',
      )
    }
  }

  return (
    <div className="card p-6 sm:p-8">
      <h2 className="text-[15px] font-semibold tracking-tight text-navy-900">
        Upload Compliance Document
      </h2>
      <p className="mt-1 text-sm text-navy-500">
        Drag and drop your file here or browse from your computer.
      </p>

      {!file && (
        <div
          onDragOver={(e) => {
            e.preventDefault()
            setIsDragging(true)
          }}
          onDragLeave={() => setIsDragging(false)}
          onDrop={handleDrop}
          className={`mt-6 flex flex-col items-center justify-center rounded-lg border-2 border-dashed px-6 py-14 text-center transition-colors ${
            isDragging ? 'border-navy-400 bg-navy-50' : 'border-navy-200 bg-navy-50/40'
          }`}
        >
          <div className="mb-4 flex h-12 w-12 items-center justify-center rounded-full bg-white shadow-subtle">
            <UploadCloud size={22} className="text-navy-500" strokeWidth={1.75} />
          </div>
          <p className="text-sm font-medium text-navy-700">
            Drop your file here, or{' '}
            <button
              type="button"
              onClick={() => inputRef.current?.click()}
              className="font-semibold text-navy-900 underline decoration-navy-300 underline-offset-2 hover:decoration-navy-600"
            >
              browse
            </button>
          </p>
          <p className="mt-2 text-xs text-navy-400">
            Supports PDF, PNG, JPG, DOCX &middot; Max file size 10 MB
          </p>
          <input
            ref={inputRef}
            type="file"
            accept={ACCEPT_STRING}
            onChange={handleBrowse}
            className="hidden"
          />
        </div>
      )}

      {errorMessage && !file && (
        <div className="mt-4 flex items-start gap-2 rounded-md border border-red-200 bg-red-50 px-3.5 py-3 text-sm text-red-700">
          <AlertCircle size={16} className="mt-0.5 shrink-0" />
          <span>{errorMessage}</span>
        </div>
      )}

      {file && (
        <div className="mt-6 rounded-lg border border-navy-100 bg-navy-50/40 p-4">
          <div className="flex items-start justify-between gap-3">
            <div className="flex items-start gap-3">
              <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-md bg-white shadow-subtle">
                <FileText size={18} className="text-navy-500" />
              </div>
              <div className="min-w-0">
                <p className="truncate text-sm font-medium text-navy-800">{file.name}</p>
                <p className="mt-0.5 text-xs text-navy-400">{formatFileSize(file.size)}</p>
              </div>
            </div>

            {status !== 'uploading' && (
              <button
                onClick={handleRemove}
                aria-label="Remove file"
                className="rounded-md p-1.5 text-navy-400 hover:bg-white hover:text-navy-600"
              >
                <X size={16} />
              </button>
            )}
          </div>

          {status === 'uploading' && (
            <div className="mt-4">
              <div className="h-1.5 w-full overflow-hidden rounded-full bg-navy-100">
                <div
                  className="h-full rounded-full bg-navy-700 transition-all duration-200"
                  style={{ width: `${progress}%` }}
                />
              </div>
              <p className="mt-2 text-xs text-navy-400">Uploading... {progress}%</p>
            </div>
          )}

          {status === 'success' && (
            <div className="mt-4 flex items-center gap-2 rounded-md border border-emerald-200 bg-emerald-50 px-3.5 py-2.5 text-sm text-emerald-700">
              <CheckCircle2 size={16} />
              Upload successful
            </div>
          )}

          {status === 'error' && (
            <div className="mt-4 flex items-start gap-2 rounded-md border border-red-200 bg-red-50 px-3.5 py-2.5 text-sm text-red-700">
              <AlertCircle size={16} className="mt-0.5 shrink-0" />
              <span>{errorMessage || 'Upload failed. Please try again.'}</span>
            </div>
          )}

          {(status === 'idle' || status === 'error') && (
            <div className="mt-4 flex gap-2">
              <button onClick={handleUpload} className="btn-primary">
                Upload Document
              </button>
              <button onClick={handleRemove} className="btn-secondary">
                Cancel
              </button>
            </div>
          )}

          {status === 'success' && (
            <button onClick={handleRemove} className="btn-secondary mt-4">
              Upload Another Document
            </button>
          )}
        </div>
      )}
    </div>
  )
}
