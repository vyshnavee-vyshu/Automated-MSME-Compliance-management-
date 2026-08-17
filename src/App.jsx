import { Routes, Route } from 'react-router-dom'
import Layout from './components/Layout'
import Dashboard from './pages/Dashboard'
import UploadDocuments from './pages/UploadDocuments'
import LatestNews from './pages/LatestNews'
import ComplianceChatbot from './pages/ComplianceChatbot'
import RiskAnalysis from './pages/RiskAnalysis'
import ComplianceCalendar from './pages/ComplianceCalendar'

export default function App() {
  return (
    <Routes>
      <Route element={<Layout />}>
        <Route path="/" element={<Dashboard />} />
        <Route path="/upload-documents" element={<UploadDocuments />} />
        <Route path="/latest-news" element={<LatestNews />} />
        <Route path="/compliance-chatbot" element={<ComplianceChatbot />} />
        <Route path="/risk-analysis" element={<RiskAnalysis />} />
        <Route path="/compliance-calendar" element={<ComplianceCalendar />} />
      </Route>
    </Routes>
  )
}
