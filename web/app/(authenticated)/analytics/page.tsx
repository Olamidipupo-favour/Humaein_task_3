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

export default function AnalyticsPage() {
  const [timeRange, setTimeRange] = useState("30d");
  const [loading, setLoading] = useState(true);
  const [revenueData, setRevenueData] = useState([
    { month: "Jan", revenue: 240000, claims: 120 },
    { month: "Feb", revenue: 280000, claims: 135 },
    { month: "Mar", revenue: 220000, claims: 110 },
    { month: "Apr", revenue: 320000, claims: 145 },
    { month: "May", revenue: 290000, claims: 130 },
    { month: "Jun", revenue: 350000, claims: 140 },
  ]);
  const [denialReasons, setDenialReasons] = useState([
    { name: "Prior Auth Required", value: 35, color: "#EF4444" },
    { name: "Invalid Codes", value: 25, color: "#F59E0B" },
    { name: "Missing Documentation", value: 20, color: "#8B5CF6" },
    { name: "Eligibility Issues", value: 15, color: "#06B6D4" },
    { name: "Other", value: 5, color: "#10B981" },
  ]);
  const { token } = useAuth();

  const kpiCards = [
    {
      title: "Revenue Growth",
      value: "+12.5%",
      change: "+$45K",
      changeType: "positive",
      icon: TrendingUp,
      color: "bg-green-500",
    },
    {
      title: "Clean Claim Rate",
      value: "94.2%",
      change: "+2.1%",
      changeType: "positive",
      icon: CheckCircle,
      color: "bg-blue-500",
    },
    {
      title: "Avg Days to Payment",
      value: "28 days",
      change: "-3 days",
      changeType: "positive",
      icon: Clock,
      color: "bg-yellow-500",
    },
    {
      title: "Denial Rate",
      value: "5.8%",
      change: "-1.2%",
      changeType: "positive",
      icon: AlertTriangle,
      color: "bg-red-500",
    },
  ];

  useEffect(() => {
    const fetchAnalytics = async () => {
      if (!token) return;

      try {
        // Fetch revenue analytics
        const revenueResponse = await fetch(
          `${process.env.NEXT_PUBLIC_API_BASE_URL}/rcm/analytics/revenue`,
          {
            headers: {
              Authorization: `Bearer ${token}`,
              "Content-Type": "application/json",
            },
          },
        );
        const revenueData = await revenueResponse.json();

        if (revenueData.success) {
          setRevenueData(revenueData.data.revenue_trend);
        }

        // Fetch denial analytics
        const denialResponse = await fetch(
          `${process.env.NEXT_PUBLIC_API_BASE_URL}/rcm/analytics/denials`,
          {
            headers: {
              Authorization: `Bearer ${token}`,
              "Content-Type": "application/json",
            },
          },
        );
        const denialData = await denialResponse.json();

        if (denialData.success) {
          setDenialReasons(denialData.data.denial_reasons);
        }
      } catch (error) {
        console.error("Failed to fetch analytics:", error);
        // Keep default data on error
      } finally {
        setLoading(false);
      }
    };

    fetchAnalytics();
  }, [token]);

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
              <div className="text-3xl font-bold text-blue-600 mb-2">94.2%</div>
              <div className="text-sm text-gray-600">
                First-Pass Success Rate
              </div>
              <div className="text-xs text-green-600 mt-1">
                +2.1% from last month
              </div>
            </div>
            <div className="text-center">
              <div className="text-3xl font-bold text-green-600 mb-2">28</div>
              <div className="text-sm text-gray-600">
                Average Days to Payment
              </div>
              <div className="text-xs text-green-600 mt-1">
                -3 days improvement
              </div>
            </div>
            <div className="text-center">
              <div className="text-3xl font-bold text-yellow-600 mb-2">
                $2.5M
              </div>
              <div className="text-sm text-gray-600">Monthly Revenue</div>
              <div className="text-xs text-green-600 mt-1">+12.5% growth</div>
            </div>
          </div>
        </div>
      </motion.div>
    </div>
  );
}
