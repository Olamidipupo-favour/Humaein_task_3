'use client'

import { useState } from 'react'
import { motion } from 'framer-motion'
import { FileText, CheckCircle, AlertTriangle, Send, Search, Eye } from 'lucide-react'
import { useAuth } from '../../contexts/AuthContext'

export default function ClaimsPage() {
  const [activeTab, setActiveTab] = useState('scrub')
  const [formData, setFormData] = useState({
    claim_data: {
      patient_id: '',
      provider_id: '',
      diagnosis_codes: '',
      procedure_codes: '',
      service_date: '',
      amount: ''
    },
    payer_id: '',
    payer_rules: {}
  })
  const [result, setResult] = useState<any>(null)
  const [loading, setLoading] = useState(false)
  const { token } = useAuth()

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)
    
    try {
      const endpoint = activeTab === 'scrub' ? 'scrub' : 'submit'
      const response = await fetch(`http://127.0.0.1:8000/rcm/claims/${endpoint}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,
        },
        body: JSON.stringify(formData),
      })
      
      const data = await response.json()
      setResult(data)
    } catch (error) {
      console.error('Claims operation failed:', error)
      setResult({ success: false, error: 'Failed to process claim' })
    } finally {
      setLoading(false)
    }
  }

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) => {
    const { name, value } = e.target
    
    if (name.startsWith('claim_data.')) {
      const fieldName = name.replace('claim_data.', '')
      setFormData({
        ...formData,
        claim_data: {
          ...formData.claim_data,
          [fieldName]: value
        }
      })
    } else {
      setFormData({
        ...formData,
        [name]: value
      })
    }
  }

  const tabs = [
    { id: 'scrub', label: 'Claims Scrubbing', icon: Search },
    { id: 'submit', label: 'Submit Claims', icon: Send },
    { id: 'track', label: 'Track Claims', icon: Eye }
  ]

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-2xl font-bold text-gray-900">Claims Management</h1>
        <p className="text-gray-600">Scrub, submit, and track insurance claims</p>
      </div>

      {/* Tabs */}
      <div className="border-b border-gray-200">
        <nav className="-mb-px flex space-x-8">
          {tabs.map((tab) => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className={`py-2 px-1 border-b-2 font-medium text-sm flex items-center space-x-2 ${
                activeTab === tab.id
                  ? 'border-blue-500 text-blue-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
              }`}
            >
              <tab.icon className="w-4 h-4" />
              <span>{tab.label}</span>
            </button>
          ))}
        </nav>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Form */}
        <motion.div
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.5 }}
        >
          <div className="card">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">
            {activeTab === 'scrub' && 'Claims Scrubbing'}
            {activeTab === 'submit' && 'Submit Claim'}
            {activeTab === 'track' && 'Track Claim'}
          </h3>
          
          {activeTab === 'track' ? (
            <div className="space-y-4">
              <div>
                <label className="label block mb-2">Claim ID</label>
                <input
                  type="text"
                  placeholder="Enter claim ID to track"
                  className="input"
                />
              </div>
              <button className="w-full btn-primary py-3 text-base">
                <Eye className="w-4 h-4 mr-2" />
                Track Claim
              </button>
            </div>
          ) : (
            <form onSubmit={handleSubmit} className="space-y-4">
              <div>
                <label className="label block mb-2">Patient ID</label>
                <input
                  type="text"
                  name="claim_data.patient_id"
                  value={formData.claim_data.patient_id}
                  onChange={handleInputChange}
                  placeholder="Enter patient ID"
                  className="input"
                  required
                />
              </div>

              <div>
                <label className="label block mb-2">Provider ID</label>
                <input
                  type="text"
                  name="claim_data.provider_id"
                  value={formData.claim_data.provider_id}
                  onChange={handleInputChange}
                  placeholder="Enter provider ID"
                  className="input"
                  required
                />
              </div>

              <div>
                <label className="label block mb-2">Service Date</label>
                <input
                  type="date"
                  name="claim_data.service_date"
                  value={formData.claim_data.service_date}
                  onChange={handleInputChange}
                  className="input"
                  required
                />
              </div>

              <div>
                <label className="label block mb-2">Diagnosis Codes</label>
                <input
                  type="text"
                  name="claim_data.diagnosis_codes"
                  value={formData.claim_data.diagnosis_codes}
                  onChange={handleInputChange}
                  placeholder="e.g., I10, E11.9"
                  className="input"
                  required
                />
              </div>

              <div>
                <label className="label block mb-2">Procedure Codes</label>
                <input
                  type="text"
                  name="claim_data.procedure_codes"
                  value={formData.claim_data.procedure_codes}
                  onChange={handleInputChange}
                  placeholder="e.g., 99213, 36415"
                  className="input"
                  required
                />
              </div>

              <div>
                <label className="label block mb-2">Claim Amount</label>
                <input
                  type="number"
                  name="claim_data.amount"
                  value={formData.claim_data.amount}
                  onChange={handleInputChange}
                  placeholder="Enter claim amount"
                  className="input"
                  step="0.01"
                  required
                />
              </div>

              {activeTab === 'submit' && (
                <div>
                  <label className="label block mb-2">Payer ID</label>
                  <select
                    name="payer_id"
                    value={formData.payer_id}
                    onChange={handleInputChange}
                    className="input"
                    required
                  >
                    <option value="">Select payer</option>
                    <option value="1">Blue Cross Blue Shield</option>
                    <option value="2">Aetna</option>
                    <option value="3">Cigna</option>
                    <option value="4">UnitedHealth</option>
                    <option value="5">Medicare</option>
                  </select>
                </div>
              )}

              <button
                type="submit"
                disabled={loading}
                className="w-full btn-primary py-3 text-base"
              >
                {loading ? (
                  <div className="flex items-center justify-center">
                    <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
                    {activeTab === 'scrub' ? 'Scrubbing Claim...' : 'Submitting Claim...'}
                  </div>
                ) : (
                  <>
                    {activeTab === 'scrub' ? (
                      <>
                        <Search className="w-4 h-4 mr-2" />
                        Scrub Claim
                      </>
                    ) : (
                      <>
                        <Send className="w-4 h-4 mr-2" />
                        Submit Claim
                      </>
                    )}
                  </>
                )}
              </button>
            </form>
          )}
          </div>
        </motion.div>

        {/* Results */}
        <motion.div
          initial={{ opacity: 0, x: 20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.5 }}
        >
          <div className="card">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Results</h3>
          
          {!result ? (
            <div className="text-center py-8 text-gray-500">
              <FileText className="w-12 h-12 mx-auto mb-4 text-gray-400" />
              <p>
                {activeTab === 'scrub' && 'Submit claim data to check for errors'}
                {activeTab === 'submit' && 'Submit claim data to send to payer'}
                {activeTab === 'track' && 'Enter claim ID to view status'}
              </p>
            </div>
          ) : result.success ? (
            <div className="space-y-4">
              {activeTab === 'scrub' ? (
                <>
                  <div className="flex items-center space-x-3">
                    <CheckCircle className="w-6 h-6 text-green-500" />
                    <span className="font-semibold text-green-700">Scrubbing Complete</span>
                  </div>
                  
                  <div className="bg-green-50 p-4 rounded-lg">
                    <h4 className="font-medium text-green-800 mb-2">Claim Status</h4>
                    <div className="space-y-2 text-sm">
                      <div className="flex justify-between">
                        <span>Clean Claim Rate:</span>
                        <span className="font-medium">95.2%</span>
                      </div>
                      <div className="flex justify-between">
                        <span>Issues Found:</span>
                        <span className="font-medium">2</span>
                      </div>
                    </div>
                  </div>

                  <div className="bg-blue-50 p-4 rounded-lg">
                    <h4 className="font-medium text-blue-800 mb-2">Recommendations</h4>
                    <ul className="text-sm text-blue-700 space-y-1">
                      {[
                        'Verify patient eligibility before submission',
                        'Ensure all required documentation is attached',
                        'Double-check diagnosis and procedure codes'
                      ].map((rec, index) => (
                        <li key={index} className="flex items-center">
                          <CheckCircle className="w-4 h-4 mr-2" />
                          {rec}
                        </li>
                      ))}
                    </ul>
                  </div>
                </>
              ) : (
                <>
                  <div className="flex items-center space-x-3">
                    <CheckCircle className="w-6 h-6 text-green-500" />
                    <span className="font-semibold text-green-700">Claim Submitted</span>
                  </div>
                  
                  <div className="bg-green-50 p-4 rounded-lg">
                    <h4 className="font-medium text-green-800 mb-2">Submission Details</h4>
                    <div className="space-y-2 text-sm">
                      <div className="flex justify-between">
                        <span>Claim ID:</span>
                        <span className="font-medium">CLM-20241201-1234</span>
                      </div>
                      <div className="flex justify-between">
                        <span>Status:</span>
                        <span className="font-medium">Submitted</span>
                      </div>
                      <div className="flex justify-between">
                        <span>Expected Response:</span>
                        <span className="font-medium">3-5 business days</span>
                      </div>
                    </div>
                  </div>
                </>
              )}
            </div>
          ) : (
            <div className="space-y-4">
              <div className="flex items-center space-x-3">
                <AlertTriangle className="w-6 h-6 text-red-500" />
                <span className="font-semibold text-red-700">Operation Failed</span>
              </div>
              
              <div className="bg-red-50 p-4 rounded-lg">
                <p className="text-red-700">{result.error || 'Failed to process claim'}</p>
              </div>
            </div>
          )}
          </div>
        </motion.div>
      </div>
    </div>
  )
}
