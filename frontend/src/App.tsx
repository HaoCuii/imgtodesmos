import { useState } from 'react'
import ImageUploader from './components/ImageUploader'
import EquationDisplay from './components/EquationDisplay'
import ProcessingStatus from './components/ProcessingStatus'

interface ProcessedResult {
  equations: string[]
  edgesImage: string
  equationCount: number
}

function App() {
  const [result, setResult] = useState<ProcessedResult | null>(null)
  const [isProcessing, setIsProcessing] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const handleImageProcessed = (data: ProcessedResult) => {
    setResult(data)
    setIsProcessing(false)
    setError(null)
  }

  const handleProcessingStart = () => {
    setIsProcessing(true)
    setError(null)
    setResult(null)
  }

  const handleError = (errorMessage: string) => {
    setError(errorMessage)
    setIsProcessing(false)
  }

  const handleReset = () => {
    setResult(null)
    setError(null)
    setIsProcessing(false)
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      <div className="container mx-auto px-4 py-8">
        <header className="text-center mb-12">
          <h1 className="text-5xl font-bold text-gray-800 mb-4">
            Image 2 Desmos
          </h1>
          <p className="text-xl text-gray-600">
            Convert your images into mathematical expressions for Desmos
          </p>
        </header>

        <div className="max-w-6xl mx-auto">
          {error && (
            <div className="mb-6 bg-red-50 border border-red-200 text-red-700 px-6 py-4 rounded-lg">
              <div className="flex items-center">
                <svg className="w-6 h-6 mr-3" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
                </svg>
                <span>{error}</span>
              </div>
            </div>
          )}

          <ImageUploader
            onImageProcessed={handleImageProcessed}
            onProcessingStart={handleProcessingStart}
            onError={handleError}
          />

          {isProcessing && <ProcessingStatus />}

          {result && (
            <div className="mt-8">
              <div className="flex justify-between items-center mb-6">
                <h2 className="text-2xl font-bold text-gray-800">
                  Results ({result.equationCount} equations)
                </h2>
                <button
                  onClick={handleReset}
                  className="px-6 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition-colors"
                >
                  Process Another Image
                </button>
              </div>

              <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
                <div className="bg-white rounded-lg shadow-lg p-6">
                  <h3 className="text-xl font-semibold text-gray-800 mb-4">
                    Edge Detection Preview
                  </h3>
                  <img
                    src={result.edgesImage}
                    alt="Edge detection result"
                    className="w-full rounded-lg border border-gray-200"
                  />
                </div>

                <EquationDisplay equations={result.equations} />
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

export default App
