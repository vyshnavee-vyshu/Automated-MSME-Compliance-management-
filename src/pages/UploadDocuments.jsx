import PageHeader from '../components/PageHeader'
import FileUploader from '../components/FileUploader'

export default function UploadDocuments() {
  return (
    <div>
      <PageHeader
        title="Upload Documents"
        subtitle="Upload licenses, certificates, notices and other compliance documents for review."
      />
      <div className="max-w-2xl">
        <FileUploader />
      </div>
    </div>
  )
}
