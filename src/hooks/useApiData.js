import { useEffect, useState, useCallback } from 'react'

/**
 * Generic hook to call an async fetcher function and expose
 * loading / error / data / refetch state.
 *
 * @param {() => Promise<any>} fetcher
 * @param {Array} deps
 */
export function useApiData(fetcher, deps = []) {
  const [data, setData] = useState(null)
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState(null)

  const load = useCallback(() => {
    let isMounted = true
    setIsLoading(true)
    setError(null)

    fetcher()
      .then((result) => {
        if (isMounted) setData(result)
      })
      .catch((err) => {
        if (isMounted) setError(err)
      })
      .finally(() => {
        if (isMounted) setIsLoading(false)
      })

    return () => {
      isMounted = false
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, deps)

  useEffect(() => {
    const cleanup = load()
    return cleanup
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [load])

  return { data, isLoading, error, refetch: load }
}
