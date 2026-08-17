export default function LoadingState({ label = 'Loading...' }) {
  return (
    <div className="flex flex-col items-center justify-center gap-3 rounded-lg border border-navy-100 bg-white px-6 py-16">
      <div className="h-6 w-6 animate-spin rounded-full border-2 border-navy-200 border-t-navy-700" />
      <p className="text-sm text-navy-400">{label}</p>
    </div>
  )
}
