export default function EmptyState({ icon: Icon, title, description }) {
  return (
    <div className="flex flex-col items-center justify-center rounded-lg border border-dashed border-navy-200 bg-navy-50/40 px-6 py-16 text-center">
      {Icon && (
        <div className="mb-4 flex h-12 w-12 items-center justify-center rounded-full bg-white shadow-subtle">
          <Icon size={22} className="text-navy-400" strokeWidth={1.75} />
        </div>
      )}
      <p className="text-sm font-medium text-navy-700">{title}</p>
      {description && <p className="mt-1 max-w-sm text-sm text-navy-400">{description}</p>}
    </div>
  )
}
