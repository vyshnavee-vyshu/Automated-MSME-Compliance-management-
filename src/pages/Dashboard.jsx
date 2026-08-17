import { UploadCloud, Newspaper, MessageSquare, ShieldAlert, CalendarDays } from 'lucide-react'
import FeatureCard from '../components/FeatureCard'

const FEATURES = [
  {
    icon: UploadCloud,
    title: 'Upload Documents',
    description: 'Upload licenses, certificates, notices and other compliance documents.',
    buttonLabel: 'Upload Documents',
    to: '/upload-documents',
  },
  {
    icon: Newspaper,
    title: 'Latest News',
    description: 'Stay updated with important government and regulatory changes.',
    buttonLabel: 'View Latest News',
    to: '/latest-news',
  },
  {
    icon: MessageSquare,
    title: 'Compliance Chatbot',
    description: 'Ask questions about applicable compliance requirements.',
    buttonLabel: 'Open Assistant',
    to: '/compliance-chatbot',
  },
  {
    icon: ShieldAlert,
    title: 'Risk Analysis',
    description: 'Identify and understand compliance risks.',
    buttonLabel: 'View Risk Analysis',
    to: '/risk-analysis',
  },
  {
    icon: CalendarDays,
    title: 'Compliance Calendar',
    description: 'Track compliance deadlines and upcoming activities.',
    buttonLabel: 'Open Calendar',
    to: '/compliance-calendar',
  },
]

export default function Dashboard() {
  return (
    <div>
      <h1 className="text-2xl font-semibold tracking-tight text-navy-900 sm:text-[28px]">
        MSME Compliance
      </h1>
      <p className="mt-2 max-w-xl text-sm text-navy-500 sm:text-[15px]">
        Manage documents, regulatory updates, risks and compliance deadlines in one place.
      </p>

      <div className="mt-8 grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-3">
        {FEATURES.map((feature) => (
          <FeatureCard key={feature.to} {...feature} />
        ))}
      </div>
    </div>
  )
}
