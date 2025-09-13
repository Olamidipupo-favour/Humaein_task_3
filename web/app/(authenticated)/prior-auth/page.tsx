"use client";

import { useState } from "react";
import { motion } from "framer-motion";
import {
  FileText,
  CheckCircle,
  Clock,
  AlertTriangle,
  Download,
  Send,
} from "lucide-react";
import { useAuth } from "../../contexts/AuthContext";

export default function PriorAuthPage() {
  const [formData, setFormData] = useState({
    patient_id: "",
    service_type: "",
    diagnosis_codes: "",
    clinical_notes: "",
  });
  const [result, setResult] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const { token } = useAuth();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);

    try {
      const response = await fetch(
        `${process.env.NEXT_PUBLIC_API_BASE_URL}/rcm/prior-auth/draft`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`,
          },
          body: JSON.stringify(formData),
        },
      );

      const data = await response.json();
      setResult(data);
    } catch (error) {
      console.error("Prior auth generation failed:", error);
      setResult({
        success: false,
        error: "Failed to generate prior authorization",
      });
    } finally {
      setLoading(false);
    }
  };

  const handleInputChange = (
    e: React.ChangeEvent<
      HTMLInputElement | HTMLSelectElement | HTMLTextAreaElement
    >,
  ) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-2xl font-bold text-gray-900">
          Prior Authorization
        </h1>
        <p className="text-gray-600">
          Generate prior authorization requests and letters
        </p>
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
              Authorization Request
            </h3>
            <form onSubmit={handleSubmit} className="space-y-4">
              <div>
                <label className="label block mb-2">Patient ID</label>
                <input
                  type="text"
                  name="patient_id"
                  value={formData.patient_id}
                  onChange={handleInputChange}
                  placeholder="Enter patient ID"
                  className="input"
                  required
                />
              </div>

              <div>
                <label className="label block mb-2">Service Type</label>
                <select
                  name="service_type"
                  value={formData.service_type}
                  onChange={handleInputChange}
                  className="input"
                  required
                >
                  <option value="">Select service type</option>
                  <option value="surgery">Surgery</option>
                  <option value="imaging">Advanced Imaging</option>
                  <option value="specialist">Specialist Consultation</option>
                  <option value="therapy">Physical Therapy</option>
                  <option value="durable_medical">
                    Durable Medical Equipment
                  </option>
                  <option value="inpatient">Inpatient Care</option>
                  <option value="outpatient">Outpatient Procedure</option>
                </select>
              </div>

              <div>
                <label className="label block mb-2">Diagnosis Codes</label>
                <input
                  type="text"
                  name="diagnosis_codes"
                  value={formData.diagnosis_codes}
                  onChange={handleInputChange}
                  placeholder="e.g., I10, E11.9 (comma-separated)"
                  className="input"
                  required
                />
              </div>

              <div>
                <label className="label block mb-2">Clinical Notes</label>
                <textarea
                  name="clinical_notes"
                  value={formData.clinical_notes}
                  onChange={handleInputChange}
                  placeholder="Enter clinical documentation, medical necessity, treatment plan..."
                  className="input"
                  rows={4}
                  required
                />
              </div>

              <button
                type="submit"
                disabled={loading}
                className="w-full btn-primary py-3 text-base"
              >
                {loading ? (
                  <div className="flex items-center justify-center">
                    <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
                    Generating Authorization...
                  </div>
                ) : (
                  "Generate Prior Authorization"
                )}
              </button>
            </form>
          </div>
        </motion.div>

        {/* Results */}
        <motion.div
          initial={{ opacity: 0, x: 20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.5 }}
        >
          <div className="card">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">
              Authorization Results
            </h3>

            {!result ? (
              <div className="text-center py-8 text-gray-500">
                <FileText className="w-12 h-12 mx-auto mb-4 text-gray-400" />
                <p>Submit request details to generate prior authorization</p>
              </div>
            ) : result.success ? (
              <div className="space-y-4">
                <div className="flex items-center space-x-3">
                  <CheckCircle className="w-6 h-6 text-green-500" />
                  <span className="font-semibold text-green-700">
                    Authorization Generated
                  </span>
                </div>

                <div className="bg-green-50 p-4 rounded-lg">
                  <h4 className="font-medium text-green-800 mb-2">
                    Authorization Details
                  </h4>
                  <div className="space-y-2 text-sm">
                    <div className="flex justify-between">
                      <span>Authorization ID:</span>
                      <span className="font-medium">
                        {result.data.auth_id}
                      </span>
                    </div>
                    <div className="flex justify-between">
                      <span>Status:</span>
                      <span className="font-medium">{result.data.status}</span>
                    </div>
                    <div className="flex justify-between">
                      <span>Estimated Review Time:</span>
                      <span className="font-medium">
                        {result.data.estimated_days} business days
                      </span>
                    </div>
                  </div>
                </div>

                <div className="bg-blue-50 p-4 rounded-lg">
                  <h4 className="font-medium text-blue-800 mb-2">
                    Required Documentation
                  </h4>
                  <ul className="text-sm text-blue-700 space-y-1">
                    {result.data.required_documentation.map((doc: string, index: number) => (
                      <li key={index} className="flex items-center">
                        <CheckCircle className="w-4 h-4 mr-2" />
                        {doc}
                      </li>
                    ))}
                  </ul>
                </div>

                <div className="flex space-x-3">
                  <button className="flex-1 btn-secondary py-2 text-sm">
                    <Download className="w-4 h-4 mr-2" />
                    Download Letter
                  </button>
                  <button className="flex-1 btn-primary py-2 text-sm">
                    <Send className="w-4 h-4 mr-2" />
                    Submit to Payer
                  </button>
                </div>
              </div>
            ) : (
              <div className="space-y-4">
                <div className="flex items-center space-x-3">
                  <AlertTriangle className="w-6 h-6 text-red-500" />
                  <span className="font-semibold text-red-700">
                    Generation Failed
                  </span>
                </div>

                <div className="bg-red-50 p-4 rounded-lg">
                  <p className="text-red-700">
                    {result.error || "Failed to generate prior authorization"}
                  </p>
                </div>
              </div>
            )}
          </div>
        </motion.div>
      </div>
    </div>
  );
}
