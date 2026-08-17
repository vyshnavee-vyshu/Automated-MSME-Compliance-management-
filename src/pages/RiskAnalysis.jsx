import { ShieldAlert } from 'lucide-react'
import PageHeader from '../components/PageHeader'
import RiskCard from '../components/RiskCard'
import LoadingState from '../components/LoadingState'
import EmptyState from '../components/EmptyState'
import { useApiData } from '../hooks/useApiData'
import { getRiskAnalysis } from '../services/riskApi'

const RISK_LEVELS = ['Critical', 'High', 'Medium', 'Low']

export default function RiskAnalysis() {
  const { data, isLoading, error } = useApiData(getRiskAnalysis, [])

  const overallScore = data?.overall_score
  const factors = Array.isArray(data?.factors) ? data.factors : []
  const hasData = !isLoading && !error && data

  return (
    <div>
      <PageHeader
        title="Risk Analysis"
        subtitle="Identify and understand compliance risks across your business."
      />

      {isLoading && <LoadingState label="Analyzing compliance risk..." />}

      {!isLoading && (error || !data) && (
        <EmptyState
          icon={ShieldAlert}
          title="Risk analysis will appear here once compliance data is available."
          description={
            error
              ? 'We could not reach the risk analysis service. Please try again shortly.'
              : 'Upload documents and connect your compliance data to generate a risk assessment.'
          }
        />
      )}

      {hasData && (
        <div className="space-y-6">
          <div className="grid grid-cols-1 gap-5 sm:grid-cols-2">
            <div className="card flex flex-col items-center justify-center p-8">
              <p className="section-label">Overall Risk Score</p>
              <p className="mt-3 font-display text-4xl font-semibold text-navy-900">
                {overallScore ?? '--'}
                <span className="text-lg font-normal text-navy-400"> / 100</span>
              </p>
            </div>

            <div className="card p-6">
              <p className="section-label mb-4">Risk Levels</p>
              <div className="grid grid-cols-2 gap-3">
                {RISK_LEVELS.map((level) => (
                  <div
                    key={level}
                    className="flex items-center justify-between rounded-md border border-navy-100 px-3 py-2.5"
                  >
                    <span className="text-sm text-navy-600">{level}</span>
                    <span className="text-sm font-semibold text-navy-900">
                      {factors.filter((f) => f.severity === level).length}
                    </span>
                  </div>
                ))}
              </div>
            </div>
          </div>

          <div>
            <p className="section-label mb-3">Risk Factors</p>
            {factors.length === 0 ? (
              <EmptyState
                icon={ShieldAlert}
                title="No risk factors identified."
                description="Detected risk factors will be listed here as compliance data is analyzed."
              />
            ) : (
              <div className="grid grid-cols-1 gap-4 lg:grid-cols-2">
                {factors.map((factor, index) => (
                  <RiskCard key={index} risk={factor} />
                ))}
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  )
}
