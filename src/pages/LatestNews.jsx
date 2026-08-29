import React, { useState, useEffect } from "react";

export default function LatestNews() {
  const [activeTab, setActiveTab] = useState("taxation");
  const [loading, setLoading] = useState(true);
  const [dataStore, setDataStore] = useState({
    taxation: [],
    environment: [],
    labour: [],
    industry: [],
  });

  // Safe API caller with built-in 3-second timeout guard
  const fetchCategoryData = async (category) => {
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), 3000); // Stop waiting after 3s

    try {
      // Replace this URL with your actual backend endpoint
      const response = await fetch(`/api/v1/compliance/regulatory-updates?category=${category}`, {
        signal: controller.signal,
        headers: { "Content-Type": "application/json" },
      });

      clearTimeout(timeoutId);

      if (!response.ok) return [];

      const result = await response.json();

      // Flexible extraction matching your JSON response keys (tax_rate_changes, data, etc.)
      if (Array.isArray(result)) return result;
      if (Array.isArray(result?.tax_rate_changes)) return result.tax_rate_changes;
      if (Array.isArray(result?.data)) return result.data;
      if (Array.isArray(result?.results)) return result.results;

      return [];
    } catch (err) {
      // Gracefully catch CORS, network failures, or timeouts without looping
      return [];
    }
  };

  useEffect(() => {
    let isMounted = true;

    const loadDataOnPageMount = async () => {
      setLoading(true);

      // Concurrently query all 4 categories on page load
      const [taxation, environment, labour, industry] = await Promise.all([
        fetchCategoryData("taxation"),
        fetchCategoryData("environment"),
        fetchCategoryData("labour"),
        fetchCategoryData("industry"),
      ]);

      if (isMounted) {
        setDataStore({
          taxation: taxation || [],
          environment: environment || [],
          labour: labour || [],
          industry: industry || [],
        });
        setLoading(false); // Guarantees loading state ends
      }
    };

    loadDataOnPageMount();

    return () => {
      isMounted = false;
    };
  }, []);

  const categories = [
    { id: "taxation", label: "Taxation Data" },
    { id: "environment", label: "Environment Standards" },
    { id: "labour", label: "Labour Laws" },
    { id: "industry", label: "Industry Regulations" },
  ];

  const currentRecords = Array.isArray(dataStore[activeTab]) ? dataStore[activeTab] : [];

  return (
    <div className="w-full min-h-screen bg-[#F8FAFC] p-8 text-slate-800 font-sans">
      {/* Title Header */}
      <div className="mb-6">
        <h1 className="text-2xl font-bold text-slate-900">Latest Regulatory Updates</h1>
        <p className="text-sm text-slate-500 mt-1">
          Stay informed about government notifications and regulatory changes across key domains.
        </p>
      </div>

      {/* Category Tabs */}
      <div className="flex items-center space-x-2 bg-slate-100 p-1.5 rounded-xl mb-6 w-fit">
        {categories.map((cat) => {
          const isActive = activeTab === cat.id;
          const count = (dataStore[cat.id] || []).length;

          return (
            <button
              key={cat.id}
              onClick={() => setActiveTab(cat.id)}
              className={`flex items-center space-x-2 px-4 py-2.5 rounded-lg text-sm font-medium transition-all ${
                isActive
                  ? "bg-[#0F172A] text-white shadow-sm"
                  : "text-slate-600 hover:text-slate-900 hover:bg-slate-200/60"
              }`}
            >
              <span>{cat.label}</span>
              {!loading && (
                <span
                  className={`ml-1 px-2 py-0.5 text-xs rounded-full ${
                    isActive ? "bg-slate-700 text-slate-100" : "bg-slate-200 text-slate-600"
                  }`}
                >
                  {count}
                </span>
              )}
            </button>
          );
        })}
      </div>

      {/* Content Rendering */}
      {loading ? (
        <div className="flex flex-col items-center justify-center p-16 bg-white border border-slate-200 rounded-xl">
          <div className="w-6 h-6 border-2 border-slate-600 border-t-transparent rounded-full animate-spin mb-3"></div>
          <p className="text-sm text-slate-500 font-medium">Fetching regulatory data...</p>
        </div>
      ) : currentRecords.length === 0 ? (
        /* Soft Empty/No-Data Message matching your layout */
        <div className="flex flex-col items-center justify-center p-16 bg-white border border-dashed border-slate-300 rounded-xl text-center">
          <div className="w-10 h-10 bg-slate-100 rounded-full flex items-center justify-center mb-3 text-slate-400 font-semibold text-sm">
            📄
          </div>
          <h3 className="text-sm font-semibold text-slate-700">No Regulatory Updates Available</h3>
          <p className="text-xs text-slate-400 mt-1 max-w-sm">
            New regulatory notifications and government updates will be listed here as soon as they are published.
          </p>
        </div>
      ) : (
        /* Item List */
        <div className="grid grid-cols-1 gap-4">
          {currentRecords.map((item, index) => (
            <div
              key={item.id || item.notification_number || index}
              className="bg-white border border-slate-200 rounded-xl p-5 hover:border-slate-300 transition-all shadow-sm"
            >
              <div className="flex items-start justify-between">
                <div className="flex-1">
                  <div className="flex items-center space-x-3 mb-2">
                    <span className="inline-flex items-center px-2.5 py-0.5 rounded-md text-xs font-semibold bg-slate-100 text-slate-800">
                      {item.notification_number || item.notificationNo || "N/A"}
                    </span>
                    <span className="text-xs text-slate-400">•</span>
                    <span className="text-xs font-medium text-slate-500">
                      {item.issued_by || item.issuedBy || "Government Authority"}
                    </span>
                  </div>
                  <h3 className="text-base font-semibold text-slate-900 leading-snug">
                    {item.title || "Regulatory Notification"}
                  </h3>
                </div>

                {(item.source_url || item.sourceUrl) && (
                  <a
                    href={item.source_url || item.sourceUrl}
                    target="_blank"
                    rel="noreferrer"
                    className="px-3 py-1.5 bg-slate-50 border border-slate-200 rounded-lg text-xs font-medium text-slate-700 hover:bg-slate-100 transition-colors ml-4 shrink-0"
                  >
                    View Document
                  </a>
                )}
              </div>

              <div className="mt-4 pt-4 border-t border-slate-100 grid grid-cols-1 md:grid-cols-3 gap-4 text-xs">
                <div className="text-slate-600 truncate">
                  <strong>Legal Basis:</strong> {item.legal_basis || item.legalBasis || "N/A"}
                </div>

                <div className="text-slate-600">
                  <strong>Issued:</strong> {item.date_issued || item.dateIssued || "N/A"} |{" "}
                  <strong>Effective:</strong> {item.effective_date || item.effectiveDate || "N/A"}
                </div>

                <div className="flex items-center justify-end space-x-2">
                  <span className="text-slate-400">Status:</span>
                  <span className="inline-block w-2 h-2 rounded-full bg-emerald-500"></span>
                  <span className="font-semibold text-slate-700">
                    {item.status || "Active"}
                  </span>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}