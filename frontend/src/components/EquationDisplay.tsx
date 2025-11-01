import { useState } from 'react'

interface EquationDisplayProps {
  equations: string[]
}

export default function EquationDisplay({ equations }: EquationDisplayProps) {
  const [copied, setCopied] = useState(false)

  const handleCopyAll = () => {
    const allEquations = equations.join('\n')
    navigator.clipboard.writeText(allEquations)
    setCopied(true)
    setTimeout(() => setCopied(false), 2000)
  }

  const handleCopyOne = (equation: string) => {
    navigator.clipboard.writeText(equation)
  }

  const handleDownload = () => {
    const allEquations = equations.join('\n')
    const blob = new Blob([allEquations], { type: 'text/plain' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = 'desmos-equations.txt'
    document.body.appendChild(a)
    a.click()
    document.body.removeChild(a)
    URL.revokeObjectURL(url)
  }

  return (
    <div className="bg-white rounded-lg shadow-lg p-6">
      <div className="flex justify-between items-center mb-4">
        <h3 className="text-xl font-semibold text-gray-800">
          Desmos Equations
        </h3>
        <div className="flex gap-2">
          <button
            onClick={handleCopyAll}
            className="px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors text-sm"
          >
            {copied ? 'Copied!' : 'Copy All'}
          </button>
          <button
            onClick={handleDownload}
            className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors text-sm"
          >
            Download
          </button>
        </div>
      </div>

      <div className="space-y-2 max-h-96 overflow-y-auto">
        {equations.map((equation, index) => (
          <div
            key={index}
            className="group flex items-center justify-between p-3 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors"
          >
            <code className="text-sm text-gray-700 flex-1 font-mono break-all">
              {equation}
            </code>
            <button
              onClick={() => handleCopyOne(equation)}
              className="ml-2 p-2 text-gray-500 hover:text-indigo-600 opacity-0 group-hover:opacity-100 transition-opacity"
              title="Copy equation"
            >
              <svg
                className="w-5 h-5"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z"
                />
              </svg>
            </button>
          </div>
        ))}
      </div>

      <div className="mt-4 p-4 bg-blue-50 border border-blue-200 rounded-lg">
        <p className="text-sm text-blue-800">
          <strong>Tip:</strong> Copy these equations and paste them directly into{' '}
          <a
            href="https://www.desmos.com/calculator"
            target="_blank"
            rel="noopener noreferrer"
            className="underline hover:text-blue-600"
          >
            Desmos Calculator
          </a>{' '}
          to visualize your image!
        </p>
      </div>
    </div>
  )
}
