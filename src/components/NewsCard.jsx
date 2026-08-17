import { ExternalLink } from 'lucide-react'
import { formatDate } from '../utils/formatters'

export default function NewsCard({ news }) {
  const { title, authority, category, published_date, effective_date, summary, source_url, impact } = news

  return (
    <div className="card p-5 sm:p-6">
      <div className="flex flex-wrap items-center gap-2">
        {category && (
          <span className="rounded-full bg-navy-50 px-2.5 py-0.5 text-xs font-medium text-navy-600">
            {category}
          </span>
        )}
        {authority && <span className="text-xs text-navy-400">{authority}</span>}
      </div>

      <h3 className="mt-3 text-[15px] font-semibold leading-snug text-navy-900">{title}</h3>

      {summary && <p className="mt-2 text-sm leading-relaxed text-navy-500">{summary}</p>}

      <div className="mt-4 flex flex-wrap items-center justify-between gap-3 border-t border-navy-100 pt-3">
        <div className="flex flex-wrap gap-4 text-xs text-navy-400">
          {published_date && <span>Published {formatDate(published_date)}</span>}
          {effective_date && <span>Effective {formatDate(effective_date)}</span>}
          {impact && <span>Impact: {impact}</span>}
        </div>
        {source_url && (
          <a
            href={source_url}
            target="_blank"
            rel="noreferrer"
            className="inline-flex items-center gap-1 text-xs font-medium text-navy-700 hover:text-navy-900"
          >
            Source <ExternalLink size={12} />
          </a>
        )}
      </div>
    </div>
  )
}
