"use client";

import { useState, useEffect } from "react";
import { motion } from "framer-motion";
import {
  FileText,
  CheckCircle,
  AlertTriangle,
  Send,
  Search,
  Eye,
  List,
  Calendar,
  DollarSign,
  User,
  Building,
} from "lucide-react";
import { useAuth } from "../../contexts/AuthContext";

interface Claim {
  id: number;
  claim_id: string;
  claim_date: string;
  service_date: string;
  total_amount: number;
  status: string;
  submission_date?: string;
  patient: {
    first_name: string;
    last_name: string;
  };
  provider: {
    name: string;
  };
  payer: {
    name: string;
  };
}

export default function ClaimsPage() {
  const [activeTab, setActiveTab] = useState("list");
  const [formData, setFormData] = useState({
    claim_data: {
      patient_id: "",
      provider_id: "",
      diagnosis_codes: "",
      procedure_codes: "",
      service_date: "",
      amount: "",
    },
    payer_id: "",
    payer_rules: {},
  });
  const [result, setResult] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [trackingClaimId, setTrackingClaimId] = useState("");
  const [trackingResult, setTrackingResult] = useState<any>(null);
  const [payers, setPayers] = useState([]);
  const [claims, setClaims] = useState<Claim[]>([]);
  const [claimsLoading, setClaimsLoading] = useState(false);
  const [patients, setPatients] = useState([]);
  const [patientsLoading, setPatientsLoading] = useState(false);
  const [providers, setProviders] = useState([]);
  const [providersLoading, setProvidersLoading] = useState(false);
  const { token } = useAuth();

  useEffect(() => {
    const fetchPayers = async () => {
      try {
        const response = await fetch(`${process.env.NEXT_PUBLIC_API_BASE_URL}/rcm/payers`, {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });
        const data = await response.json();
        if (data.success) {
          setPayers(data.data);
        }
      } catch (error) {
        console.error("Failed to fetch payers:", error);
      }
    };

    const fetchClaims = async () => {
      setClaimsLoading(true);
      try {
        const response = await fetch(`${process.env.NEXT_PUBLIC_API_BASE_URL}/rcm/claims`, {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });
        const data = await response.json();
        if (data.success) {
          setClaims(data.data);
        }
      } catch (error) {
        console.error("Failed to fetch claims:", error);
      } finally {
        setClaimsLoading(false);
      }
    };

    const fetchPatients = async () => {
      setPatientsLoading(true);
      try {
        const response = await fetch(`${process.env.NEXT_PUBLIC_API_BASE_URL}/rcm/patients`, {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });
        const data = await response.json();
        if (data.success) {
          setPatients(data.data);
        }
      } catch (error) {
        console.error("Failed to fetch patients:", error);
      } finally {
        setPatientsLoading(false);
      }
    };

    const fetchProviders = async () => {
      setProvidersLoading(true);
      try {
        const response = await fetch(`${process.env.NEXT_PUBLIC_API_BASE_URL}/rcm/providers`, {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });
        const data = await response.json();
        if (data.success) {
          setProviders(data.data);
        }
      } catch (error) {
        console.error("Failed to fetch providers:", error);
      } finally {
        setProvidersLoading(false);
      }
    };

    if (token) {
      fetchPayers();
      fetchClaims();
      fetchPatients();
      fetchProviders();
    }
  }, [token]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);

    try {
      const endpoint = activeTab === "scrub" ? "claims/scrub" : "claims/submit";
      
      // Debug: Log what we're sending
      console.log("Sending form data:", formData);
      
      const response = await fetch(
        `${process.env.NEXT_PUBLIC_API_BASE_URL}/rcm/${endpoint}`,
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
      console.error("Claims operation failed:", error);
      setResult({ success: false, error: "Failed to process claim" });
    } finally {
      setLoading(false);
    }
  };

  const handleTrackClaim = async () => {
    if (!trackingClaimId.trim()) return;

    setLoading(true);
    try {
      const response = await fetch(
        `${process.env.NEXT_PUBLIC_API_BASE_URL}/rcm/claims/track/${trackingClaimId}`,
        {
          headers: {
            Authorization: `Bearer ${token}`,
            "Content-Type": "application/json",
          },
        },
      );

      const data = await response.json();
      setTrackingResult(data);
    } catch (error) {
      console.error("Claim tracking failed:", error);
      setTrackingResult({ success: false, error: "Failed to track claim" });
    } finally {
      setLoading(false);
    }
  };

  const handleInputChange = (
    e: React.ChangeEvent<
      HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement
    >,
  ) => {
    const { name, value } = e.target;

    if (name.startsWith("claim_data.")) {
      const fieldName = name.replace("claim_data.", "");
      setFormData({
        ...formData,
        claim_data: {
          ...formData.claim_data,
          [fieldName]: value,
        },
      });
    } else {
      setFormData({
        ...formData,
        [name]: value,
      });
    }
  };

  const tabs = [
    { id: "list", label: "Claims List", icon: List },
    { id: "scrub", label: "Claims Scrubbing", icon: Search },
    { id: "submit", label: "Submit Claims", icon: Send },
    { id: "track", label: "Track Claims", icon: Eye },
  ];

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-2xl font-bold text-gray-900">Claims Management</h1>
        <p className="text-gray-600">
          Scrub, submit, and track insurance claims
        </p>
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
                  ? "border-blue-500 text-blue-600"
                  : "border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300"
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
              {activeTab === "list" && "All Claims"}
              {activeTab === "scrub" && "Claims Scrubbing"}
              {activeTab === "submit" && "Submit Claim"}
              {activeTab === "track" && "Track Claim"}
            </h3>

            {activeTab === "list" ? (
              <div className="space-y-4">
                {claimsLoading ? (
                  <div className="flex items-center justify-center py-8">
                    <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
                    <span className="ml-2 text-gray-600">Loading claims...</span>
                  </div>
                ) : claims.length === 0 ? (
                  <div className="text-center py-8 text-gray-500">
                    <FileText className="w-12 h-12 mx-auto mb-4 text-gray-400" />
                    <p>No claims found. Seed demo data to see claims.</p>
                  </div>
                ) : (
                  <div className="space-y-3">
                    {claims.map((claim) => (
                      <div
                        key={claim.id}
                        className="bg-white border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow"
                      >
                        <div className="flex items-center justify-between mb-3">
                          <div className="flex items-center space-x-3">
                            <div className="bg-blue-100 p-2 rounded-lg">
                              <FileText className="w-5 h-5 text-blue-600" />
                            </div>
                            <div>
                              <h4 className="font-semibold text-gray-900">
                                {claim.claim_id}
                              </h4>
                              <p className="text-sm text-gray-600">
                                {claim.patient.first_name} {claim.patient.last_name}
                              </p>
                            </div>
                          </div>
                          <div className="text-right">
                            <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                              claim.status === 'paid' ? 'bg-green-100 text-green-800' :
                              claim.status === 'denied' ? 'bg-red-100 text-red-800' :
                              claim.status === 'pending' ? 'bg-yellow-100 text-yellow-800' :
                              claim.status === 'submitted' ? 'bg-blue-100 text-blue-800' :
                              'bg-gray-100 text-gray-800'
                            }`}>
                              {claim.status.charAt(0).toUpperCase() + claim.status.slice(1)}
                            </span>
                            <p className="text-sm font-semibold text-gray-900 mt-1">
                              ${claim.total_amount.toFixed(2)}
                            </p>
                          </div>
                        </div>
                        
                        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
                          <div className="flex items-center space-x-2">
                            <Calendar className="w-4 h-4 text-gray-400" />
                            <div>
                              <p className="text-gray-500">Service Date</p>
                              <p className="font-medium">
                                {new Date(claim.service_date).toLocaleDateString()}
                              </p>
                            </div>
                          </div>
                          
                          <div className="flex items-center space-x-2">
                            <User className="w-4 h-4 text-gray-400" />
                            <div>
                              <p className="text-gray-500">Provider</p>
                              <p className="font-medium">{claim.provider.name}</p>
                            </div>
                          </div>
                          
                          <div className="flex items-center space-x-2">
                            <Building className="w-4 h-4 text-gray-400" />
                            <div>
                              <p className="text-gray-500">Payer</p>
                              <p className="font-medium">{claim.payer.name}</p>
                            </div>
                          </div>
                          
                          <div className="flex items-center space-x-2">
                            <DollarSign className="w-4 h-4 text-gray-400" />
                            <div>
                              <p className="text-gray-500">Claim Date</p>
                              <p className="font-medium">
                                {new Date(claim.claim_date).toLocaleDateString()}
                              </p>
                            </div>
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            ) : activeTab === "track" ? (
              <div className="space-y-4">
                <div>
                  <label className="label block mb-2">Claim ID</label>
                  <input
                    type="text"
                    value={trackingClaimId}
                    onChange={(e) => setTrackingClaimId(e.target.value)}
                    placeholder="Enter claim ID to track"
                    className="input"
                  />
                </div>
                <button
                  onClick={handleTrackClaim}
                  disabled={loading || !trackingClaimId.trim()}
                  className="w-full btn-primary py-3 text-base"
                >
                  {loading ? (
                    <div className="flex items-center justify-center">
                      <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
                      Tracking...
                    </div>
                  ) : (
                    <>
                      <Eye className="w-4 h-4 mr-2" />
                      Track Claim
                    </>
                  )}
                </button>
              </div>
            ) : (
              <form onSubmit={handleSubmit} className="space-y-4">
                <div>
                  <div className="flex items-center justify-between mb-2">
                    <label className="label">Patient</label>
                    <button
                      type="button"
                      onClick={() => {
                        setPatientsLoading(true);
                        fetch(`${process.env.NEXT_PUBLIC_API_BASE_URL}/rcm/patients`, {
                          headers: { Authorization: `Bearer ${token}` },
                        })
                          .then(res => res.json())
                          .then(data => {
                            if (data.success) setPatients(data.data);
                          })
                          .catch(console.error)
                          .finally(() => setPatientsLoading(false));
                      }}
                      className="text-xs text-blue-600 hover:text-blue-800 underline"
                      disabled={patientsLoading}
                    >
                      {patientsLoading ? "Loading..." : "Refresh"}
                    </button>
                  </div>
                  <select
                    name="claim_data.patient_id"
                    value={formData.claim_data.patient_id}
                    onChange={handleInputChange}
                    className="input"
                    required
                  >
                    <option value="">Select a patient</option>
                    {patientsLoading ? (
                      <option disabled>Loading patients...</option>
                    ) : (
                      patients.map((patient: any) => (
                        <option key={patient.id} value={patient.insurance_id}>
                          {patient.first_name} {patient.last_name} ({patient.insurance_id})
                        </option>
                      ))
                    )}
                  </select>
                  {patients.length === 0 && !patientsLoading && (
                    <p className="text-sm text-gray-500 mt-1">
                      No patients found. Seed demo data to see patients.
                    </p>
                  )}
                </div>

                <div>
                  <div className="flex items-center justify-between mb-2">
                    <label className="label">Provider</label>
                    <button
                      type="button"
                      onClick={() => {
                        setProvidersLoading(true);
                        fetch(`${process.env.NEXT_PUBLIC_API_BASE_URL}/rcm/providers`, {
                          headers: { Authorization: `Bearer ${token}` },
                        })
                          .then(res => res.json())
                          .then(data => {
                            if (data.success) setProviders(data.data);
                          })
                          .catch(console.error)
                          .finally(() => setProvidersLoading(false));
                      }}
                      className="text-xs text-blue-600 hover:text-blue-800 underline"
                      disabled={providersLoading}
                    >
                      {providersLoading ? "Loading..." : "Refresh"}
                    </button>
                  </div>
                  <select
                    name="claim_data.provider_id"
                    value={formData.claim_data.provider_id}
                    onChange={handleInputChange}
                    className="input"
                    required
                  >
                    <option value="">Select a provider</option>
                    {providersLoading ? (
                      <option disabled>Loading providers...</option>
                    ) : (
                      providers.map((provider: any) => (
                        <option key={provider.id} value={provider.npi}>
                          {provider.name} - {provider.specialty} ({provider.npi})
                        </option>
                      ))
                    )}
                  </select>
                  {providers.length === 0 && !providersLoading && (
                    <p className="text-sm text-gray-500 mt-1">
                      No providers found. Seed demo data to see providers.
                    </p>
                  )}
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

                {activeTab === "submit" && (
                  <div>
                    <div className="flex items-center justify-between mb-2">
                      <label className="label">Payer</label>
                      <button
                        type="button"
                        onClick={() => {
                          fetch(`${process.env.NEXT_PUBLIC_API_BASE_URL}/rcm/payers`, {
                            headers: { Authorization: `Bearer ${token}` },
                          })
                            .then(res => res.json())
                            .then(data => {
                              if (data.success) setPayers(data.data);
                            })
                            .catch(console.error);
                        }}
                        className="text-xs text-blue-600 hover:text-blue-800 underline"
                      >
                        Refresh
                      </button>
                    </div>
                    <select
                      name="payer_id"
                      value={formData.payer_id}
                      onChange={handleInputChange}
                      className="input"
                      required
                    >
                      <option value="">Select a payer</option>
                      {payers.map((payer: any) => (
                        <option key={payer.id} value={payer.id}>
                          {payer.name} ({payer.payer_type})
                        </option>
                      ))}
                    </select>
                    {payers.length === 0 && (
                      <p className="text-sm text-gray-500 mt-1">
                        No payers found. Seed demo data to see payers.
                      </p>
                    )}
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
                      {activeTab === "scrub"
                        ? "Scrubbing Claim..."
                        : "Submitting Claim..."}
                    </div>
                  ) : (
                    <>
                      {activeTab === "scrub" ? (
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
            <h3 className="text-lg font-semibold text-gray-900 mb-4">
              Results
            </h3>

            {!result && !trackingResult ? (
              <div className="text-center py-8 text-gray-500">
                <FileText className="w-12 h-12 mx-auto mb-4 text-gray-400" />
                <p>
                  {activeTab === "scrub" &&
                    "Submit claim data to check for errors"}
                  {activeTab === "submit" &&
                    "Submit claim data to send to payer"}
                  {activeTab === "track" && "Enter claim ID to view status"}
                </p>
              </div>
            ) : result?.success || trackingResult?.success ? (
              <div className="space-y-4">
                {activeTab === "track" ? (
                  <>
                    <div className="flex items-center space-x-3">
                      <CheckCircle className="w-6 h-6 text-green-500" />
                      <span className="font-semibold text-green-700">
                        Claim Found
                      </span>
                    </div>

                    <div className="bg-green-50 p-4 rounded-lg">
                      <h4 className="font-medium text-green-800 mb-2">
                        Claim Details
                      </h4>
                      <div className="space-y-2 text-sm">
                        <div className="flex justify-between">
                          <span>Claim ID:</span>
                          <span className="font-medium">
                            {trackingResult.data.claim_id}
                          </span>
                        </div>
                        <div className="flex justify-between">
                          <span>Status:</span>
                          <span className="font-medium">
                            {trackingResult.data.status}
                          </span>
                        </div>
                        <div className="flex justify-between">
                          <span>Service Date:</span>
                          <span className="font-medium">
                            {new Date(
                              trackingResult.data.service_date,
                            ).toLocaleDateString()}
                          </span>
                        </div>
                        <div className="flex justify-between">
                          <span>Amount:</span>
                          <span className="font-medium">
                            ${trackingResult.data.total_amount}
                          </span>
                        </div>
                      </div>
                    </div>
                  </>
                ) : activeTab === "scrub" ? (
                  <>
                    <div className="flex items-center space-x-3">
                      <CheckCircle className="w-6 h-6 text-green-500" />
                      <span className="font-semibold text-green-700">
                        Scrubbing Complete
                      </span>
                    </div>

                    <div className="bg-green-50 p-4 rounded-lg">
                      <h4 className="font-medium text-green-800 mb-2">
                        Claim Status
                      </h4>
                      <div className="space-y-2 text-sm">
                        <div className="flex justify-between">
                          <span>Clean Claim Rate:</span>
                          <span className="font-medium">{result.data.clean_claim_rate}%</span>
                        </div>
                        <div className="flex justify-between">
                          <span>Issues Found:</span>
                          <span className="font-medium">{result.data.issues.length}</span>
                        </div>
                      </div>
                    </div>

                    <div className="bg-blue-50 p-4 rounded-lg">
                      <h4 className="font-medium text-blue-800 mb-2">
                        Recommendations
                      </h4>
                      <ul className="text-sm text-blue-700 space-y-1">
                        {result.data.recommendations.map((rec: string, index: number) => (
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
                      <span className="font-semibold text-green-700">
                        Claim Submitted
                      </span>
                    </div>

                    <div className="bg-green-50 p-4 rounded-lg">
                      <h4 className="font-medium text-green-800 mb-2">
                        Submission Details
                      </h4>
                      <div className="space-y-2 text-sm">
                        <div className="flex justify-between">
                          <span>Claim ID:</span>
                          <span className="font-medium">{result.data.claim_id}</span>
                        </div>
                        <div className="flex justify-between">
                          <span>Status:</span>
                          <span className="font-medium">{result.data.status}</span>
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
                  <span className="font-semibold text-red-700">
                    Operation Failed
                  </span>
                </div>

                <div className="bg-red-50 p-4 rounded-lg">
                  <p className="text-red-700">
                    {result?.error ||
                      trackingResult?.error ||
                      "Failed to process claim"}
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
