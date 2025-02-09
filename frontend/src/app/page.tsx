'use client'
import { useState } from 'react'
import axios from 'axios'

interface ResultComponents {
  base_rate: number
  risk_premium: number
}

interface Result {
  interest_rate: number
  default_probability: number
  components: ResultComponents
}

export default function Home() {
  const [inputs, setInputs] = useState({
    loan_amount: 500,
    business_type: 'Agriculture',
    location: 'Rural',
    season: 'Planting',
    repayment_history: 70,
    existing_debt_ratio: 30
  })
  
  const [result, setResult] = useState<Result | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)
    try {
      const response = await axios.post('/api/predict', {
        ...inputs,
        repayment_history: inputs.repayment_history / 100,
        existing_debt_ratio: inputs.existing_debt_ratio / 100
      })
      setResult(response.data)
      setError('')
    } catch {
      setError('Failed to calculate rate. Please check inputs.')
    }
    setLoading(false)
  }

  return (
    <div className="max-w-2xl mx-auto p-6">
      <h1 className="text-3xl font-bold text-primary mb-8">
        Microfinance Rate Optimizer
      </h1>
      
      <form onSubmit={handleSubmit} className="space-y-6 bg-white p-8 rounded-lg shadow-lg">
        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700">
              Loan Amount ($)
            </label>
            <input
              type="number"
              value={inputs.loan_amount}
              onChange={(e) => setInputs({...inputs, loan_amount: +e.target.value})}
              className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary focus:ring-primary sm:text-sm"
              min="50"
              max="2000"
              required
              placeholder = "Enter loan amount"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700">
              Business Type
            </label>
            <select
              aria-label="Business Type"
              value={inputs.business_type}
              onChange={(e) => setInputs({...inputs, business_type: e.target.value})}
              className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary focus:ring-primary sm:text-sm"
            >
              <option>Agriculture</option>
              <option>Retail</option>
              <option>Handicraft</option>
              <option>Livestock</option>
            </select>
          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-primary hover:bg-secondary focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary"
          >
            {loading ? 'Calculating...' : 'Calculate Rate'}
          </button>
        </div>
      </form>

      {error && (
        <div className="mt-6 p-4 bg-red-50 text-red-700 rounded-lg">
          {error}
        </div>
      )}

      {result && (
        <div className="mt-8 p-6 bg-white rounded-lg shadow-md">
          <h2 className="text-xl font-semibold mb-4">Results</h2>
          <div className="space-y-2">
            <div className="flex justify-between">
              <span className="font-medium">Interest Rate:</span>
              <span className="text-primary font-bold">
                {result.interest_rate.toFixed(1)}%
              </span>
            </div>
            <div className="flex justify-between">
              <span>Default Probability:</span>
              <span>{(result.default_probability * 100).toFixed(1)}%</span>
            </div>
            <div className="pt-4 border-t mt-4">
              <h3 className="font-medium mb-2">Breakdown:</h3>
              <div className="space-y-1">
                <div className="flex justify-between">
                  <span>Base Rate:</span>
                  <span>{result.components.base_rate.toFixed(1)}%</span>
                </div>
                <div className="flex justify-between">
                  <span>Risk Premium:</span>
                  <span>{result.components.risk_premium.toFixed(1)}%</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}