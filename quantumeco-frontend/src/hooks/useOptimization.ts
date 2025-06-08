import { useState } from 'react'
import { type OptimizationResponse } from '../Services/types'

export default function useOptimization() {
  const [result, setResult] = useState<OptimizationResponse | null>(null)
  const [loading, setLoading] = useState(false)

  const optimizeRoutes = async (locations: any[]) => {
    setLoading(true)
    try {
      // Replace with actual API call
      const response = await fetch('/api/routes/optimize', {
        method: 'POST',
        body: JSON.stringify({ locations })
      })
      const data = await response.json()
      setResult(data)
    } finally {
      setLoading(false)
    }
  }

  return { result, loading, optimizeRoutes }
}
