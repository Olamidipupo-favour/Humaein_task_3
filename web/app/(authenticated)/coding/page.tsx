"use client";

import { useState } from "react";
import { motion } from "framer-motion";
import {
  Code,
  CheckCircle,
  AlertTriangle,
  Brain,
  FileText,
  Copy,
} from "lucide-react";
import { useAuth } from "../../contexts/AuthContext";

export default function CodingPage() {
  const [formData, setFormData] = useState({
    clinical_notes: "",
    service_type: "",
    provider_specialty: "",
  });
  const [result, setResult] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const { token } = useAuth();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);

    try {
      const response = await fetch(
        `${process.env.NEXT_PUBLIC_API_BASE_URL}/rcm/coding/suggest`,
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
      console.error("Coding suggestion failed:", error);
      setResult({
        success: false,
        error: "Failed to generate coding suggestions",
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

  const copyToClipboard = (text: string) => {
    navigator.clipboard.writeText(text);
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-2xl font-bold text-gray-900">AI Medical Coding</h1>
        <p className="text-gray-600">
          Get intelligent ICD-10 and CPT code suggestions
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
              Clinical Information
            </h3>
            <form onSubmit={handleSubmit} className="space-y-4">
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
                  <option value="office_visit">Office Visit</option>
                  <option value="surgery">Surgery</option>
                  <option value="imaging">Imaging</option>
                  <option value="lab">Laboratory</option>
                  <option value="pharmacy">Pharmacy</option>
                  <option value="emergency">Emergency</option>
                  <option value="inpatient">Inpatient</option>
                  <option value="outpatient">Outpatient</option>
                </select>
              </div>

              <div>
                <label className="label block mb-2">Provider Specialty</label>
                <select
                  name="provider_specialty"
                  value={formData.provider_specialty}
                  onChange={handleInputChange}
                  className="input"
                  required
                >
                  <option value="">Select provider specialty</option>
                  <option value="internal_medicine">Internal Medicine</option>
                  <option value="family_medicine">Family Medicine</option>
                  <option value="cardiology">Cardiology</option>
                  <option value="orthopedics">Orthopedics</option>
                  <option value="neurology">Neurology</option>
                  <option value="oncology">Oncology</option>
                  <option value="pediatrics">Pediatrics</option>
                  <option value="surgery">Surgery</option>
                  <option value="emergency_medicine">Emergency Medicine</option>
                  <option value="radiology">Radiology</option>
                </select>
              </div>

              <div>
                <label className="label block mb-2">Clinical Notes</label>
                <textarea
                  name="clinical_notes"
                  value={formData.clinical_notes}
                  onChange={handleInputChange}
                  placeholder="Enter clinical documentation, diagnosis, symptoms, findings, procedures performed..."
                  className="input"
                  rows={6}
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
                    <Brain className="w-4 h-4 mr-2" />
                    Analyzing...
                  </div>
                ) : (
                  <>
                    <Brain className="w-4 h-4 mr-2" />
                    Generate Code Suggestions
                  </>
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
              AI Coding Suggestions
            </h3>

            {!result ? (
              <div className="text-center py-8 text-gray-500">
                <Code className="w-12 h-12 mx-auto mb-4 text-gray-400" />
                <p>
                  Submit clinical information to get AI-powered coding
                  suggestions
                </p>
              </div>
            ) : result.success ? (
              <div className="space-y-4">
                <div className="flex items-center space-x-3">
                  <CheckCircle className="w-6 h-6 text-green-500" />
                  <span className="font-semibold text-green-700">
                    Codes Generated
                  </span>
                </div>

                {/* ICD-10 Codes */}
                <div className="bg-blue-50 p-4 rounded-lg">
                  <h4 className="font-medium text-blue-800 mb-3 flex items-center">
                    <FileText className="w-4 h-4 mr-2" />
                    ICD-10 Diagnosis Codes
                  </h4>
                  <div className="space-y-2">
                    {result.icd_codes?.map((code: any, index: number) => (
                      <div key={index} className="bg-white p-3 rounded border">
                        <div className="flex items-center justify-between">
                          <div>
                            <span className="font-mono font-medium text-blue-600">
                              {code.code}
                            </span>
                            <span className="ml-2 text-sm text-gray-600">
                              {code.description}
                            </span>
                          </div>
                          <button
                            onClick={() => copyToClipboard(code.code)}
                            className="p-1 hover:bg-gray-100 rounded"
                          >
                            <Copy className="w-4 h-4 text-gray-400" />
                          </button>
                        </div>
                        <div className="mt-1">
                          <span className="text-xs bg-green-100 text-green-700 px-2 py-1 rounded">
                            Confidence:{" "}
                            {Math.round((code.confidence || 0.8) * 100)}%
                          </span>
                        </div>
                      </div>
                    )) || (
                      <div className="text-center py-4 text-gray-500">
                        <p>No ICD-10 codes generated</p>
                      </div>
                    )}
                  </div>
                </div>

                {/* CPT Codes */}
                <div className="bg-green-50 p-4 rounded-lg">
                  <h4 className="font-medium text-green-800 mb-3 flex items-center">
                    <Code className="w-4 h-4 mr-2" />
                    CPT Procedure Codes
                  </h4>
                  <div className="space-y-2">
                    {result.cpt_codes?.map((code: any, index: number) => (
                      <div key={index} className="bg-white p-3 rounded border">
                        <div className="flex items-center justify-between">
                          <div>
                            <span className="font-mono font-medium text-green-600">
                              {code.code}
                            </span>
                            <span className="ml-2 text-sm text-gray-600">
                              {code.description}
                            </span>
                          </div>
                          <button
                            onClick={() => copyToClipboard(code.code)}
                            className="p-1 hover:bg-gray-100 rounded"
                          >
                            <Copy className="w-4 h-4 text-gray-400" />
                          </button>
                        </div>
                        <div className="mt-1">
                          <span className="text-xs bg-green-100 text-green-700 px-2 py-1 rounded">
                            Confidence:{" "}
                            {Math.round((code.confidence || 0.8) * 100)}%
                          </span>
                          {code.rvu && (
                            <span className="ml-2 text-xs bg-blue-100 text-blue-700 px-2 py-1 rounded">
                              RVU: {code.rvu}
                            </span>
                          )}
                        </div>
                      </div>
                    )) || (
                      <div className="text-center py-4 text-gray-500">
                        <p>No CPT codes generated</p>
                      </div>
                    )}
                  </div>
                </div>

                {/* AI Status */}
                <div
                  className={`p-4 rounded-lg ${result.ai_used ? "bg-green-50" : "bg-yellow-50"}`}
                >
                  <h4
                    className={`font-medium mb-2 ${result.ai_used ? "text-green-800" : "text-yellow-800"}`}
                  >
                    {result.ai_used ? "✅ AI Analysis" : "⚠️ Fallback Mode"}
                  </h4>
                  <p
                    className={`text-sm ${result.ai_used ? "text-green-700" : "text-yellow-700"}`}
                  >
                    {result.ai_analysis || result.rationale}
                  </p>
                  {!result.ai_used && (
                    <p className="text-xs text-yellow-600 mt-2">
                      To enable AI coding suggestions, set the GOOGLE_API_KEY
                      environment variable in your backend configuration.
                    </p>
                  )}
                </div>

                {/* AI Rationale */}
                {result.rationale && result.ai_used && (
                  <div className="bg-gray-50 p-4 rounded-lg">
                    <h4 className="font-medium text-gray-800 mb-2">
                      Detailed Analysis
                    </h4>
                    <p className="text-sm text-gray-700">{result.rationale}</p>
                  </div>
                )}
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
                    {result.error || "Failed to generate coding suggestions"}
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
