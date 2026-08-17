import StatusBadge from './StatusBadge'
import { formatDate } from '../utils/formatters'

export default function RiskCard({ risk }) {
  const { title, severity, reason, date_detected, recommended_action } = risk

  return (
    <div className="card p-5">
      <div className="flex items-start justify-between gap-3">
        <h3 className="text-sm font-semibold text-navy-900">{title}</h3>
        <StatusBadge status={severity} />
      </div>

      {reason && <p className="mt-2 text-sm leading-relaxed text-navy-500">{reason}</p>}

      {date_detected && (
        <p className="mt-2 text-xs text-navy-400">Detected {formatDate(date_detected)}</p>
      )}

      {recommended_action && (
        <div className="mt-3 rounded-md bg-navy-50/60 px-3 py-2.5">
          <p className="text-xs font-semibold uppercase tracking-wide text-navy-500">
            Recommended Action
          </p>
          <p className="mt-1 text-sm text-navy-700">{recommended_action}</p>
        </div>
      )}
    </div>
  )
}
