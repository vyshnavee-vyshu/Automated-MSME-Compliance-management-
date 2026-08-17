# MSME Compliance — Frontend

Frontend-only dashboard for an MSME Compliance Management Platform. Built with React, Vite, Tailwind CSS, and Lucide icons. This project contains **no backend, no database, and no mock/fake data** — every feature is wired to a documented REST endpoint that a FastAPI backend can implement later.

## Features

1. **Upload Documents** — drag-and-drop uploader for PDF, PNG, JPG, DOCX (max 10 MB)
2. **Latest News** — regulatory update feed with an empty state until real data is connected
3. **Compliance Chatbot** — enterprise-style assistant UI with suggested questions and verified sources
4. **Risk Analysis** — risk score and risk factor layout ready for backend data
5. **Compliance Calendar** — Month / Week / List views for compliance deadlines

## Tech Stack

- React 18 + JavaScript (no TypeScript)
- Vite
- Tailwind CSS
- React Router
- Axios
- Lucide React icons
- Recharts (available for future charting needs)

## Getting Started

```bash
npm install
npm run dev
```

The app runs at `http://localhost:5173`.

To create a production build:

```bash
npm run build
npm run preview
```

## Environment Variables

Copy `.env.example` to `.env` and set the backend URL:

```bash
cp .env.example .env
```

```
VITE_API_BASE_URL=http://localhost:8000
```

## Backend Integration

This frontend expects a FastAPI (or any REST) backend exposing the following endpoints. Service wrappers already exist in `src/services/`.

| Feature | Method | Endpoint | Service file |
|---|---|---|---|
| Upload Documents | POST | `/api/documents/upload` (multipart/form-data) | `src/services/documentApi.js` |
| Latest News | GET | `/api/news` | `src/services/newsApi.js` |
| Compliance Chatbot | POST | `/api/chat` | `src/services/chatbotApi.js` |
| Risk Analysis | GET | `/api/risk` | `src/services/riskApi.js` |
| Compliance Calendar | GET | `/api/compliance/calendar` | `src/services/calendarApi.js` |

See each service file's JSDoc comments for expected request/response shapes.

## Project Structure

```
src/
├── components/     # Reusable UI components (Sidebar, Header, Calendar, etc.)
├── pages/          # One page per feature
├── services/       # Axios-based API wrappers (frontend-only, no backend logic)
├── hooks/          # Shared hooks (useApiData)
├── utils/          # Formatters and calendar helpers
├── App.jsx         # Route definitions
├── main.jsx        # App entry point
└── index.css       # Tailwind base + design tokens
```

## Notes

- No fake/mock data is used anywhere. Every data-driven page (News, Chatbot, Risk Analysis, Calendar) shows a loading state while fetching and a clean empty state when no backend is connected or no data is returned.
- Fully responsive: collapsible sidebar drawer on mobile/tablet, fixed sidebar on desktop.
