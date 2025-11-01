export default function ProcessingStatus() {
  return (
    <div className="mt-8 bg-white rounded-lg shadow-lg p-8">
      <div className="flex items-center justify-center space-x-4">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600"></div>
        <div className="text-center">
          <h3 className="text-xl font-semibold text-gray-800">
            Processing your image...
          </h3>
          <p className="text-gray-600 mt-2">
            Detecting edges and generating mathematical expressions
          </p>
        </div>
      </div>
    </div>
  )
}
