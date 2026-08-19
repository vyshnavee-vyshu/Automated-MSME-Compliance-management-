import { Newspaper } from 'lucide-react'
import PageHeader from '../components/PageHeader'
import NewsCard from '../components/NewsCard'
import LoadingState from '../components/LoadingState'
import EmptyState from '../components/EmptyState'
import { useApiData } from '../hooks/useApiData'
import { getLatestNews } from '../services/newsApi'

export default function LatestNews() {
  
  const { data, isLoading, error } = useApiData(getLatestNews, [])
  const items = Array.isArray(data) ? data : []

  return (
    <div>
      <PageHeader
        title="Latest Regulatory Updates"
        subtitle="Stay informed about government notifications and regulatory changes."
      />

      {isLoading && <LoadingState label="Fetching regulatory updates..." />}

      {!isLoading && (error || items.length === 0) && (
        <EmptyState
          icon={Newspaper}
          title="Regulatory updates will appear here."
          description={
            error
              ? 'We could not reach the compliance service. Please try again shortly.'
              : 'New regulatory notifications and government updates will be listed as soon as they are published.'
          }
        />
      )}

      {!isLoading && !error && items.length > 0 && (
        <div className="grid grid-cols-1 gap-4 lg:grid-cols-2">
          {items.map((item, index) => (
            <NewsCard key={item.id || index} news={item} />
          ))}
        </div>
      )}
    </div>
  )
}
