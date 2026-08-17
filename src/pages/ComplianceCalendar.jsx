import PageHeader from '../components/PageHeader'
import Calendar from '../components/Calendar'
import LoadingState from '../components/LoadingState'
import { useApiData } from '../hooks/useApiData'
import { getComplianceCalendar } from '../services/calendarApi'

export default function ComplianceCalendar() {
  const { data, isLoading } = useApiData(getComplianceCalendar, [])
  const events = Array.isArray(data) ? data : []

  return (
    <div>
      <PageHeader
        title="Compliance Calendar"
        subtitle="Track compliance deadlines and upcoming activities."
      />

      {isLoading ? <LoadingState label="Loading compliance calendar..." /> : <Calendar events={events} />}
    </div>
  )
}
