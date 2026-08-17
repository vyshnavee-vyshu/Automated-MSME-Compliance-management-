import { useState } from 'react'
import { Search, Bell, Menu } from 'lucide-react'

export default function Header({ onMenuClick }) {
  const [isSearchFocused, setIsSearchFocused] = useState(false)

  return (
    <header className="sticky top-0 z-30 flex h-16 items-center gap-3 border-b border-navy-100 bg-white/95 px-4 backdrop-blur sm:px-6">
      <button
        onClick={onMenuClick}
        aria-label="Open navigation"
        className="rounded-md p-2 text-navy-600 hover:bg-navy-50 lg:hidden"
      >
        <Menu size={20} />
      </button>

      <span className="font-display text-[15px] font-semibold tracking-tight text-navy-900 lg:hidden">
        MSME Compliance
      </span>

      <div className="ml-auto flex items-center gap-2 sm:gap-3">
        <div
          className={`hidden items-center gap-2 rounded-md border px-3 py-2 transition-colors sm:flex ${
            isSearchFocused ? 'border-navy-300 bg-white' : 'border-navy-100 bg-navy-50'
          }`}
        >
          <Search size={16} className="text-navy-400" />
          <input
            type="text"
            placeholder="Search compliance records..."
            onFocus={() => setIsSearchFocused(true)}
            onBlur={() => setIsSearchFocused(false)}
            className="w-56 bg-transparent text-sm text-navy-800 placeholder:text-navy-400 focus:outline-none"
          />
        </div>

        <button
          aria-label="Search"
          className="rounded-md p-2 text-navy-600 hover:bg-navy-50 sm:hidden"
        >
          <Search size={19} />
        </button>

        <button
          aria-label="Notifications"
          className="relative rounded-md p-2 text-navy-600 hover:bg-navy-50"
        >
          <Bell size={19} />
          <span className="absolute right-1.5 top-1.5 h-1.5 w-1.5 rounded-full bg-amber-500" />
        </button>

        <div className="h-8 w-8 shrink-0 rounded-full border border-navy-100 bg-navy-100" />
      </div>
    </header>
  )
}
