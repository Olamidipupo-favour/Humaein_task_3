"use client";

import { useState, useEffect } from "react";
import { motion } from "framer-motion";
import {
  TrendingUp,
  TrendingDown,
  DollarSign,
  AlertTriangle,
  CheckCircle,
  Clock,
  Users,
  FileText,
  BarChart3,
  PieChart,
  RefreshCw,
} from "lucide-react";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  BarChart,
  Bar,
  PieChart as RechartsPieChart,
  Pie,
  Cell,
} from "recharts";

import { useAuth } from "../../contexts/AuthContext";

interface KPIData {
  revenue_growth?: {
    value: string;
    change: string;
    changeType: string;
  };
  clean_claim_rate?: {
    value: string;
    change: string;
    changeType: string;
  };
  avg_days_to_payment?: {
    value: string;
    change: string;
    changeType: string;
  };
  denial_rate?: {
    value: string;
    change: string;
    changeType: string;
  };
  first_pass_success_rate?: {
    value: string;
    change: string;
  };
  avg_days_to_payment_kpi?: {
    value: string;
    change: string;
  };
  monthly_revenue?: {
    value: string;
    change: string;
  };
}

interface DenialReason {
  name: string;
  value: number;
  color: string;
}

interface RevenueData {
  month: string;
  revenue: number;
  claims: number;
}

export default function AnalyticsPage() {
  const [timeRange, setTimeRange] = useState("30d");
  const [loading, setLoading] = useState(true);
  const [revenueData, setRevenueData] = useState<RevenueData[]>([]);
  const [denialReasons, setDenialReasons] = useState<DenialReason[]>([]);
  const [kpis, setKpis] = useState<KPIData | null>(null);
  const [debugInfo, setDebugInfo] = useState<any>(null);
  const { token } = useAuth();

  const fetchAnalytics = async () => {
    if (!token) return;

    try {
      setLoading(true);
      const [revenueRes, denialsRes, kpisRes] = await Promise.all([
        fetch(
          `${process.env.NEXT_PUBLIC_API_BASE_URL}/rcm/analytics/revenue?timeRange=${timeRange}`,
          {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          }
        ),
        fetch(
          `${process.env.NEXT_PUBLIC_API_BASE_URL}/rcm/analytics/denials?timeRange=${timeRange}`,
          {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          }
        ),
        fetch(
          `${process.env.NEXT_PUBLIC_API_BASE_URL}/rcm/analytics/kpis?timeRange=${timeRange}`,
          {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          }
        ),
      ]);

        // Handle each response individually
        if (revenueRes.ok) {
          const revenueData = await revenueRes.json();
          console.log("Revenue API response:", revenueData);
          if (revenueData.success) {
            setRevenueData(revenueData.data?.revenue_trend || []);
          } else {
            console.error("Revenue API returned unsuccessful response:", revenueData);
            setRevenueData([]);
          }
        } else {
          console.error("Failed to fetch revenue data:", revenueRes.status);
          setRevenueData([]);
        }

        if (denialsRes.ok) {
          const denialsData = await denialsRes.json();
          console.log("Denials API response:", denialsData);
          if (denialsData.success) {
            setDenialReasons(denialsData.data?.denial_reasons || []);
          } else {
            console.error("Denials API returned unsuccessful response:", denialsData);
            setDenialReasons([]);
          }
        } else {
          console.error("Failed to fetch denials data:", denialsRes.status);
          setDenialReasons([]);
        }

        if (kpisRes.ok) {
          const kpisData = await kpisRes.json();
          console.log("KPIs API response:", kpisData);
          if (kpisData.success) {
            setKpis(kpisData.data || null);
          } else {
            console.error("KPIs API returned unsuccessful response:", kpisData);
            setKpis(null);
          }
        } else {
          console.error("Failed to fetch KPIs data:", kpisRes.status);
          setKpis(null);
        }

        // Store debug info
        setDebugInfo({
          revenueData: revenueData,
          denialReasons: denialReasons,
          kpis: kpis,
          timestamp: new Date().toISOString()
        });
      } catch (error) {
        console.error("Failed to fetch analytics:", error);
      } finally {
        setLoading(false);
      }
    };

  useEffect(() => {
    fetchAnalytics();
  }, [token, timeRange]);

  const kpiCards = kpis
    ? [
        {
          title: "Revenue Growth",
          value: kpis.revenue_growth?.value || "0%",
          change: kpis.revenue_growth?.change || "0",
          changeType: kpis.revenue_growth?.changeType || "neutral",
          icon: TrendingUp,
          color: "bg-green-500",
        },
        {
          title: "Clean Claim Rate",
          value: kpis.clean_claim_rate?.value || "0%",
          change: kpis.clean_claim_rate?.change || "0",
          changeType: kpis.clean_claim_rate?.changeType || "neutral",
          icon: CheckCircle,
          color: "bg-blue-500",
        },
        {
          title: "Avg Days to Payment",
          value: kpis.avg_days_to_payment?.value || "0 days",
          change: kpis.avg_days_to_payment?.change || "0",
          changeType: kpis.avg_days_to_payment?.changeType || "neutral",
          icon: Clock,
          color: "bg-yellow-500",
        },
        {
          title: "Denial Rate",
          value: kpis.denial_rate?.value || "0%",
          change: kpis.denial_rate?.change || "0",
          changeType: kpis.denial_rate?.changeType || "neutral",
          icon: AlertTriangle,
          color: "bg-red-500",
        },
      ]
    : [];

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">
            Analytics & Insights
          </h1>
          <p className="text-gray-600">Comprehensive RCM performance metrics</p>
        </div>
        <div className="flex items-center space-x-4">
          <button
            onClick={async () => {
              try {
                const response = await fetch(`${process.env.NEXT_PUBLIC_API_BASE_URL}/rcm/seed-demo-data`, {
                  method: 'POST',
                  headers: {
                    Authorization: `Bearer ${token}`,
                  },
                });
                if (response.ok) {
                  alert('Demo data seeded successfully! Refreshing analytics...');
                  fetchAnalytics();
                } else {
                  alert('Failed to seed demo data');
                }
              } catch (error) {
                console.error('Error seeding demo data:', error);
                alert('Error seeding demo data');
              }
            }}
            className="flex items-center space-x-2 px-3 py-2 text-sm bg-green-600 text-white rounded-md hover:bg-green-700"
          >
            <span>Seed Demo Data</span>
          </button>
          <button
            onClick={fetchAnalytics}
            disabled={loading}
            className="flex items-center space-x-2 px-3 py-2 text-sm bg-blue-600 text-white rounded-md hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <RefreshCw className={`h-4 w-4 ${loading ? 'animate-spin' : ''}`} />
            <span>Refresh</span>
          </button>
          <div className="flex space-x-2">
            {["7d", "30d", "90d", "1y"].map((range) => (
              <button
                key={range}
                onClick={() => setTimeRange(range)}
                className={`px-3 py-1 text-sm rounded-md ${
                  timeRange === range
                    ? "bg-blue-100 text-blue-700"
                    : "text-gray-500 hover:text-gray-700"
                }`}
              >
                {range}
              </button>
            ))}
          </div>
        </div>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {kpiCards.map((card, index) => (
          <motion.div
            key={card.title}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.3, delay: index * 0.1 }}
          >
            <div className="card">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-gray-600">
                    {card.title}
                  </p>
                  <p className="text-2xl font-bold text-gray-900">
                    {card.value}
                  </p>
                  <div className="flex items-center mt-1">
                    {card.changeType === "positive" ? (
                      <TrendingUp className="h-4 w-4 text-green-500" />
                    ) : (
                      <TrendingDown className="h-4 w-4 text-red-500" />
                    )}
                    <span
                      className={`text-sm font-medium ml-1 ${
                        card.changeType === "positive"
                          ? "text-green-600"
                          : "text-red-600"
                      }`}
                    >
                      {card.change}
                    </span>
                    <span className="text-sm text-gray-500 ml-1">
                      vs last period
                    </span>
                  </div>
                </div>
                <div className={`p-3 rounded-lg ${card.color}`}>
                  <card.icon className="h-6 w-6 text-white" />
                </div>
              </div>
            </div>
          </motion.div>
        ))}
      </div>

      {/* Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Revenue Trend */}
        <motion.div
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.5 }}
        >
          <div className="card">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">
              Revenue Trend
            </h3>
            <ResponsiveContainer width="100%" height={300}>
              <LineChart data={revenueData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="month" />
                <YAxis />
                <Tooltip
                  formatter={(value, name) => [
                    name === "revenue" ? `$${value.toLocaleString()}` : value,
                    name === "revenue" ? "Revenue" : "Claims",
                  ]}
                />
                <Line
                  type="monotone"
                  dataKey="revenue"
                  stroke="#10B981"
                  strokeWidth={2}
                />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </motion.div>

        {/* Denial Reasons */}
        <motion.div
          initial={{ opacity: 0, x: 20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.5 }}
        >
          <div className="card">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">
              Denial Reasons
            </h3>
            <ResponsiveContainer width="100%" height={300}>
              <RechartsPieChart>
                <Pie
                  data={denialReasons}
                  cx="50%"
                  cy="50%"
                  innerRadius={60}
                  outerRadius={100}
                  paddingAngle={5}
                  dataKey="value"
                >
                  {denialReasons.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.color} />
                  ))}
                </Pie>
                <Tooltip />
              </RechartsPieChart>
            </ResponsiveContainer>
            <div className="flex flex-wrap justify-center gap-2 mt-4">
              {denialReasons.map((item) => (
                <div key={item.name} className="flex items-center">
                  <div
                    className="w-3 h-3 rounded-full mr-2"
                    style={{ backgroundColor: item.color }}
                  ></div>
                  <span className="text-sm text-gray-600">
                    {item.name} ({item.value}%)
                  </span>
                </div>
              ))}
            </div>
          </div>
        </motion.div>
      </div>

      {/* Performance Metrics */}
      {kpis && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.3 }}
        >
          <div className="card">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">
              Performance Metrics
            </h3>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              <div className="text-center">
                <div className="text-3xl font-bold text-blue-600 mb-2">
                  {kpis.first_pass_success_rate?.value || "0%"}
                </div>
                <div className="text-sm text-gray-600">
                  First-Pass Success Rate
                </div>
                <div className="text-xs text-green-600 mt-1">
                  {kpis.first_pass_success_rate?.change || "0"}
                </div>
              </div>
              <div className="text-center">
                <div className="text-3xl font-bold text-green-600 mb-2">
                  {kpis.avg_days_to_payment_kpi?.value || "0"}
                </div>
                <div className="text-sm text-gray-600">
                  Average Days to Payment
                </div>
                <div className="text-xs text-green-600 mt-1">
                  {kpis.avg_days_to_payment_kpi?.change || "0"}
                </div>
              </div>
              <div className="text-center">
                <div className="text-3xl font-bold text-yellow-600 mb-2">
                  {kpis.monthly_revenue?.value || "$0"}
                </div>
                <div className="text-sm text-gray-600">Monthly Revenue</div>
                <div className="text-xs text-green-600 mt-1">
                  {kpis.monthly_revenue?.change || "0"}
                </div>
              </div>
            </div>
          </div>
        </motion.div>
      )}

      {/* Debug Panel */}
      {debugInfo && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.4 }}
        >
          <div className="card">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">
              Debug Information
            </h3>
            <div className="bg-gray-100 p-4 rounded-lg">
              <pre className="text-xs text-gray-700 overflow-auto max-h-64">
                {JSON.stringify(debugInfo, null, 2)}
              </pre>
            </div>
          </div>
        </motion.div>
      )}
    </div>
  );
}