import { useEffect, useRef, useState } from 'react'
import { Send, MessageSquare, ShieldCheck, AlertCircle } from 'lucide-react'
import { sendChatMessage } from '../services/chatbotApi'

const SUGGESTED_QUESTIONS = [
  'What compliances apply to my business?',
  'What filings are due?',
  'Has any regulation changed?',
  'What documents are required?',
  'Why is there a compliance risk?',
]

export default function ComplianceChatbot() {
  const [messages, setMessages] = useState([])
  const [input, setInput] = useState('')
  const [isSending, setIsSending] = useState(false)
  const [errorMessage, setErrorMessage] = useState('')
  const scrollRef = useRef(null)

  useEffect(() => {
    scrollRef.current?.scrollTo({ top: scrollRef.current.scrollHeight, behavior: 'smooth' })
  }, [messages, isSending])

  const handleSend = async (text) => {
    const question = (text ?? input).trim()
    if (!question || isSending) return

    setMessages((prev) => [...prev, { role: 'user', content: question }])
    setInput('')
    setErrorMessage('')
    setIsSending(true)

    try {
      const response = await sendChatMessage(question)
      setMessages((prev) => [
        ...prev,
        { role: 'assistant', content: response.answer, sources: response.sources || [] },
      ])
    } catch (err) {
      setErrorMessage(
        err?.response?.data?.message || 'The compliance assistant is unavailable right now.',
      )
    } finally {
      setIsSending(false)
    }
  }

  return (
    <div className="flex h-[calc(100vh-8rem)] flex-col">
      <div className="mb-6">
        <h1 className="text-2xl font-semibold tracking-tight text-navy-900">Compliance Assistant</h1>
        <p className="mt-1.5 text-sm text-navy-500">
          Ask questions about GST, PF, ESI, labour and environmental compliance.
        </p>
      </div>

      <div className="flex flex-1 flex-col overflow-hidden rounded-lg border border-navy-100 bg-white shadow-subtle">
        <div ref={scrollRef} className="flex-1 space-y-5 overflow-y-auto px-5 py-6 sm:px-8">
          {messages.length === 0 && (
            <div className="flex h-full flex-col items-center justify-center text-center">
              <div className="mb-4 flex h-12 w-12 items-center justify-center rounded-full bg-navy-50">
                <MessageSquare size={22} className="text-navy-500" strokeWidth={1.75} />
              </div>
              <p className="text-sm font-medium text-navy-700">
                Ask a question to get started
              </p>
              <p className="mt-1 max-w-sm text-sm text-navy-400">
                The assistant can help you understand compliance requirements, filing deadlines and applicable regulations.
              </p>
            </div>
          )}

          {messages.map((message, index) => (
            <div
              key={index}
              className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}
            >
              <div
                className={`max-w-[85%] rounded-lg px-4 py-3 text-sm leading-relaxed sm:max-w-[70%] ${
                  message.role === 'user'
                    ? 'bg-navy-900 text-white'
                    : 'border border-navy-100 bg-navy-50/50 text-navy-800'
                }`}
              >
                <p>{message.content}</p>

                {message.role === 'assistant' && message.sources?.length > 0 && (
                  <div className="mt-3 border-t border-navy-200 pt-2.5">
                    <div className="flex items-center gap-1.5 text-xs font-semibold text-navy-500">
                      <ShieldCheck size={13} />
                      Verified Sources
                    </div>
                    <ul className="mt-1.5 space-y-1">
                      {message.sources.map((source, sourceIndex) => (
                        <li key={sourceIndex} className="text-xs text-navy-500">
                          {typeof source === 'string' ? source : source.title || source.url}
                        </li>
                      ))}
                    </ul>
                  </div>
                )}
              </div>
            </div>
          ))}

          {isSending && (
            <div className="flex justify-start">
              <div className="flex items-center gap-1.5 rounded-lg border border-navy-100 bg-navy-50/50 px-4 py-3">
                <span className="h-1.5 w-1.5 animate-bounce rounded-full bg-navy-400 [animation-delay:-0.3s]" />
                <span className="h-1.5 w-1.5 animate-bounce rounded-full bg-navy-400 [animation-delay:-0.15s]" />
                <span className="h-1.5 w-1.5 animate-bounce rounded-full bg-navy-400" />
              </div>
            </div>
          )}

          {errorMessage && (
            <div className="flex items-start gap-2 rounded-md border border-red-200 bg-red-50 px-3.5 py-2.5 text-sm text-red-700">
              <AlertCircle size={16} className="mt-0.5 shrink-0" />
              <span>{errorMessage}</span>
            </div>
          )}
        </div>

        {messages.length === 0 && (
          <div className="border-t border-navy-100 px-5 py-4 sm:px-8">
            <p className="section-label mb-2.5">Suggested Questions</p>
            <div className="flex flex-wrap gap-2">
              {SUGGESTED_QUESTIONS.map((question) => (
                <button
                  key={question}
                  onClick={() => handleSend(question)}
                  className="rounded-full border border-navy-200 bg-white px-3.5 py-1.5 text-xs font-medium text-navy-600 transition-colors hover:border-navy-300 hover:bg-navy-50"
                >
                  {question}
                </button>
              ))}
            </div>
          </div>
        )}

        <form
          onSubmit={(e) => {
            e.preventDefault()
            handleSend()
          }}
          className="flex items-center gap-3 border-t border-navy-100 px-5 py-4 sm:px-8"
        >
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Ask a compliance question..."
            className="input-field"
            disabled={isSending}
          />
          <button
            type="submit"
            disabled={isSending || !input.trim()}
            aria-label="Send message"
            className="btn-primary shrink-0 px-3.5"
          >
            <Send size={16} />
          </button>
        </form>
      </div>
    </div>
  )
}
