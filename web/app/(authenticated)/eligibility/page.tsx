'use client'

import { useState } from 'react'
import { motion } from 'framer-motion'
import { CheckCircle, XCircle, Clock, AlertTriangle, User, Calendar, CreditCard } from 'lucide-react'
import { useAuth } from '../../contexts/AuthContext'

export default function EligibilityPage() {
  const [formData, setFormData] = useState({
    patientId: '',
    payerId: '',
    serviceDate: '',
    serviceType: ''
  })
  const [result, setResult] = useState<any>(null)
  const [loading, setLoading] = useState(false)
  const { token } = useAuth()

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)
    
    try {
      const response = await fetch('http://127.0.0.1:8000/rcm/eligibility/check', {
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
      console.error('Eligibility check failed:', error)
      setResult({ success: false, error: 'Failed to check eligibility' })
    } finally {
      setLoading(false)
    }
  }

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    })
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-2xl font-bold text-gray-900">Eligibility Verification</h1>
        <p className="text-gray-600">Check patient insurance coverage and benefits</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Form */}
        <motion.div
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.5 }}
          className="card"
        >
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Patient Information</h3>
          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label className="label block mb-2">
                <User className="inline w-4 h-4 mr-2" />
                Patient ID
              </label>
              <input
                type="text"
                name="patientId"
                value={formData.patientId}
                onChange={handleInputChange}
                placeholder="Enter patient ID"
                className="input"
                required
              />
            </div>

            <div>
              <label className="label block mb-2">
                <CreditCard className="inline w-4 h-4 mr-2" />
                Payer ID
              </label>
              <select
                name="payerId"
                value={formData.payerId}
                onChange={handleInputChange}
                className="input"
                required
              >
                <option value="">Select insurance provider</option>
                <option value="1">Blue Cross Blue Shield</option>
                <option value="2">Aetna</option>
                <option value="3">Cigna</option>
                <option value="4">UnitedHealth</option>
                <option value="5">Medicare</option>
              </select>
            </div>

            <div>
              <label className="label block mb-2">
                <Calendar className="inline w-4 h-4 mr-2" />
                Service Date
              </label>
              <input
                type="date"
                name="serviceDate"
                value={formData.serviceDate}
                onChange={handleInputChange}
                className="input"
                required
              />
            </div>

            <div>
              <label className="label block mb-2">
                Service Type
              </label>
              <select
                name="serviceType"
                value={formData.serviceType}
                onChange={handleInputChange}
                className="input"
                required
              >
                <option value="">Select service type</option>
                <option value="office_visit">Office Visit</option>
                <option value="surgery">Surgery</option>
                <option value="imaging">Imaging</option>
                <option value="lab">Laboratory</option>
                <option value="pharmacy">Pharmacy</option>
              </select>
            </div>

            <button
              type="submit"
              disabled={loading}
              className="w-full btn-primary py-3 text-base"
            >
              {loading ? (
                <div className="flex items-center justify-center">
                  <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
                  Checking Eligibility...
                </div>
              ) : (
                'Check Eligibility'
              )}
            </button>
          </form>
        </motion.div>

        {/* Results */}
        <motion.div
          initial={{ opacity: 0, x: 20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.5 }}
          className="card"
        >
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Eligibility Results</h3>
          
          {!result ? (
            <div className="text-center py-8 text-gray-500">
              <Clock className="w-12 h-12 mx-auto mb-4 text-gray-400" />
              <p>Submit patient information to check eligibility</p>
            </div>
          ) : result.success ? (
            <div className="space-y-4">
              <div className="flex items-center space-x-3">
                <CheckCircle className="w-6 h-6 text-green-500" />
                <span className="font-semibold text-green-700">Eligible</span>
              </div>
              
              <div className="bg-green-50 p-4 rounded-lg">
                <h4 className="font-medium text-green-800 mb-2">Coverage Details</h4>
                <div className="space-y-2 text-sm">
                  <div className="flex justify-between">
                    <span>Coverage Status:</span>
                    <span className="font-medium">Active</span>
                  </div>
                  <div className="flex justify-between">
                    <span>Copay:</span>
                    <span className="font-medium">${result.data?.copay || '25'}</span>
                  </div>
                  <div className="flex justify-between">
                    <span>Deductible Remaining:</span>
                    <span className="font-medium">${result.data?.deductible_remaining || '1,200'}</span>
                  </div>
                  <div className="flex justify-between">
                    <span>Out-of-Pocket Max:</span>
                    <span className="font-medium">${result.data?.out_of_pocket_max || '5,000'}</span>
                  </div>
                </div>
              </div>

              {result.data?.prior_auth_required && (
                <div className="bg-yellow-50 p-4 rounded-lg">
                  <div className="flex items-center space-x-2">
                    <AlertTriangle className="w-5 h-5 text-yellow-600" />
                    <span className="font-medium text-yellow-800">Prior Authorization Required</span>
                  </div>
                  <p className="text-sm text-yellow-700 mt-1">
                    This service requires prior authorization before treatment.
                  </p>
                </div>
              )}
            </div>
          ) : (
            <div className="space-y-4">
              <div className="flex items-center space-x-3">
                <XCircle className="w-6 h-6 text-red-500" />
                <span className="font-semibold text-red-700">Not Eligible</span>
              </div>
              
              <div className="bg-red-50 p-4 rounded-lg">
                <p className="text-red-700">{result.error || 'Patient is not eligible for this service'}</p>
              </div>
            </div>
          )}
        </motion.div>
      </div>
    </div>
  )
}