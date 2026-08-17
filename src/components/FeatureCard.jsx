import { Link } from 'react-router-dom'
import { ArrowRight } from 'lucide-react'

export default function FeatureCard({ icon: Icon, title, description, buttonLabel, to }) {
  return (
    <div className="card group flex flex-col justify-between p-6 transition-all hover:shadow-card">
      <div>
        <div className="mb-5 flex h-11 w-11 items-center justify-center rounded-md bg-navy-900">
          <Icon size={20} className="text-white" strokeWidth={1.8} />
        </div>
        <h3 className="text-[15px] font-semibold tracking-tight text-navy-900">{title}</h3>
        <p className="mt-2 text-sm leading-relaxed text-navy-500">{description}</p>
      </div>

      <Link
        to={to}
        className="mt-6 inline-flex items-center gap-1.5 text-sm font-medium text-navy-700 transition-colors group-hover:text-navy-900"
      >
        {buttonLabel}
        <ArrowRight size={15} className="transition-transform group-hover:translate-x-0.5" />
      </Link>
    </div>
  )
}
