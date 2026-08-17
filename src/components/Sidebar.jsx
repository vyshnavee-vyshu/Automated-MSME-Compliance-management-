import { NavLink } from 'react-router-dom'
import {
  LayoutGrid,
  UploadCloud,
  Newspaper,
  MessageSquare,
  ShieldAlert,
  CalendarDays,
  X,
  ShieldCheck,
} from 'lucide-react'

const NAV_ITEMS = [
  { to: '/', label: 'Dashboard', icon: LayoutGrid, end: true },
  { to: '/upload-documents', label: 'Upload Documents', icon: UploadCloud },
  { to: '/latest-news', label: 'Latest News', icon: Newspaper },
  { to: '/compliance-chatbot', label: 'Compliance Chatbot', icon: MessageSquare },
  { to: '/risk-analysis', label: 'Risk Analysis', icon: ShieldAlert },
  { to: '/compliance-calendar', label: 'Compliance Calendar', icon: CalendarDays },
]

function SidebarContent({ onNavigate }) {
  return (
    <div className="flex h-full flex-col">
      <div className="flex items-center gap-2.5 px-6 py-6">
        <div className="flex h-8 w-8 items-center justify-center rounded-md bg-navy-900">
          <ShieldCheck className="h-4.5 w-4.5 text-white" strokeWidth={2} size={18} />
        </div>
        <span className="font-display text-[15px] font-semibold tracking-tight text-navy-900">
          MSME Compliance
        </span>
      </div>

      <nav className="flex-1 space-y-0.5 px-3">
        {NAV_ITEMS.map(({ to, label, icon: Icon, end }) => (
          <NavLink
            key={to}
            to={to}
            end={end}
            onClick={onNavigate}
            className={({ isActive }) =>
              `flex items-center gap-3 rounded-md px-3 py-2.5 text-sm transition-colors ${
                isActive
                  ? 'bg-navy-900 font-medium text-white'
                  : 'text-navy-600 hover:bg-navy-50 hover:text-navy-900'
              }`
            }
          >
            <Icon size={17} strokeWidth={2} />
            {label}
          </NavLink>
        ))}
      </nav>

      <div className="border-t border-navy-100 px-6 py-4">
        <p className="text-xs leading-relaxed text-navy-400">
          Document, monitor and manage MSME regulatory compliance.
        </p>
      </div>
    </div>
  )
}

export default function Sidebar({ isMobileOpen, onClose }) {
  return (
    <>
      {/* Desktop sidebar */}
      <aside className="hidden w-64 shrink-0 border-r border-navy-100 bg-white lg:block">
        <SidebarContent />
      </aside>

      {/* Mobile drawer */}
      {isMobileOpen && (
        <div className="fixed inset-0 z-40 lg:hidden">
          <div
            className="absolute inset-0 bg-navy-950/40"
            onClick={onClose}
            aria-hidden="true"
          />
          <div className="absolute inset-y-0 left-0 w-72 bg-white shadow-raised">
            <div className="flex justify-end px-4 pt-4">
              <button
                onClick={onClose}
                aria-label="Close navigation"
                className="rounded-md p-1.5 text-navy-500 hover:bg-navy-50"
              >
                <X size={18} />
              </button>
            </div>
            <SidebarContent onNavigate={onClose} />
          </div>
        </div>
      )}
    </>
  )
}
