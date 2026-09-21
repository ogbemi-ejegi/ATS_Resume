import { useState } from 'react'

function App() {
  const [jobDescription, setJobDescription] = useState('')
  const [file, setFile] = useState(null)
  const [isLoading, setIsLoading] = useState(false)

  const handleSubmit = async (e) => {
    e.preventDefault()
    if (!file || !jobDescription) return alert("Please provide both a resume and a job description.")

    setIsLoading(true)

    const formData = new FormData()
    formData.append('job_description', jobDescription)
    formData.append('resume', file)

    try {
      // This automatically uses your Render URL online, or localhost when you are testing on your PC
      const API_URL = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000';

      const response = await fetch(`${API_URL}/api/optimize`, {
        method: 'POST',
        body: formData,
      })

      if (!response.ok) throw new Error("Server error processing request")

      const blob = await response.blob()
      const downloadUrl = window.URL.createObjectURL(blob)
      const link = document.createElement('a')
      link.href = downloadUrl
      link.download = 'Optimized_Application.docx'
      document.body.appendChild(link)
      link.click()
      link.remove()

    } catch (error) {
      console.error(error)
      alert("Optimization failed. Check the console.")
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col items-center py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-md w-full space-y-8 bg-white p-8 rounded-xl shadow-lg">
        <h2 className="text-center text-3xl font-extrabold text-gray-900">
          ATS Resume Optimizer
        </h2>
        <form className="mt-8 space-y-6" onSubmit={handleSubmit}>
          <div>
            <label className="block text-sm font-medium text-gray-700">Job Description</label>
            <textarea
              className="mt-1 appearance-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-md focus:outline-none focus:ring-blue-500 focus:border-blue-500 focus:z-10 sm:text-sm"
              rows="6"
              placeholder="Paste the job description here..."
              value={jobDescription}
              onChange={(e) => setJobDescription(e.target.value)}
              required
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700">Upload Resume (.docx)</label>
            <input
              type="file"
              accept=".docx"
              className="mt-1 block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-md file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100"
              onChange={(e) => setFile(e.target.files[0])}
              required
            />
          </div>
          <button
            type="submit"
            disabled={isLoading}
            className="group relative w-full flex justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:bg-gray-400"
          >
            {isLoading ? 'Agents Working...' : 'Optimize Resume'}
          </button>
        </form>
      </div>
    </div>
  )
}

export default App