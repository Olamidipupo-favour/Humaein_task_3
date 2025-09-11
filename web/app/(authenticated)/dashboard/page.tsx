'use client'

import { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import { useAuth } from '../../contexts/AuthContext'
import { 
  TrendingUp, 
  TrendingDown, 
  DollarSign, 
  AlertTriangle, 
  CheckCircle, 
  Clock,
  Users,
  FileText
} from 'lucide-react'
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, BarChart, Bar, PieChart, Pie, Cell } from 'recharts'

export default function DashboardPage() {
  const [stats, setStats] = useState({
    totalClaims: 0,
    pendingClaims: 0,
    paidClaims: 0,
    deniedClaims: 0,
    totalRevenue: 0,
    avgDaysToPayment: 0,
    denialRate: 0,
    cleanClaimRate: 0
  })

  const [loading, setLoading] = useState(true)
  const { token } = useAuth()

  useEffect(() => {
    const fetchStats = async () => {
      if (!token) return
      
      try {
        const response = await fetch('http://145.223.88.159:8000/rcm/dashboard/stats', {
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json',
          },
        })
        const data = await response.json()
        
        if (data.success) {
          setStats({
            totalClaims: data.data.total_claims,
            pendingClaims: data.data.pending_claims,
            paidClaims: data.data.paid_claims,
            deniedClaims: data.data.denied_claims,
            totalRevenue: data.data.total_revenue,
            avgDaysToPayment: data.data.avg_days_to_payment,
            denialRate: data.data.denial_rate,
            cleanClaimRate: data.data.clean_claim_rate
          })
        }
      } catch (error) {
        console.error('Failed to fetch dashboard stats:', error)
        // Fallback to demo data
        setStats({
          totalClaims: 1250,
          pendingClaims: 45,
          paidClaims: 1100,
          deniedClaims: 105,
          totalRevenue: 2500000,
          avgDaysToPayment: 28,
          denialRate: 8.4,
          cleanClaimRate: 91.6
        })
      } finally {
        setLoading(false)
      }
    }

    fetchStats()
  }, [token])

  const chartData = [
    { month: 'Jan', claims: 120, denials: 10 },
    { month: 'Feb', claims: 135, denials: 12 },
    { month: 'Mar', claims: 110, denials: 8 },
    { month: 'Apr', claims: 145, denials: 15 },
    { month: 'May', claims: 130, denials: 11 },
    { month: 'Jun', claims: 140, denials: 13 },
  ]

  const pieData = [
    { name: 'Paid', value: 88, color: '#10B981' },
    { name: 'Pending', value: 3.6, color: '#F59E0B' },
    { name: 'Denied', value: 8.4, color: '#EF4444' },
  ]

  const statCards = [
    {
      title: 'Total Claims',
      value: stats.totalClaims.toLocaleString(),
      change: '+12%',
      changeType: 'positive',
      icon: FileText,
      color: 'bg-blue-500'
    },
    {
      title: 'Total Revenue',
      value: `$${(stats.totalRevenue / 1000000).toFixed(1)}M`,
      change: '+8.5%',
      changeType: 'positive',
      icon: DollarSign,
      color: 'bg-green-500'
    },
    {
      title: 'Pending Claims',
      value: stats.pendingClaims,
      change: '-5%',
      changeType: 'negative',
      icon: Clock,
      color: 'bg-yellow-500'
    },
    {
      title: 'Denial Rate',
      value: `${stats.denialRate}%`,
      change: '-2.1%',
      changeType: 'negative',
      icon: AlertTriangle,
      color: 'bg-red-500'
    }
  ]

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-2xl font-bold text-gray-900">Dashboard</h1>
        <p className="text-gray-600">Overview of your RCM performance</p>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {statCards.map((card, index) => (
          <motion.div
            key={card.title}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.3, delay: index * 0.1 }}
          >
            <div className="card">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600">{card.title}</p>
                <p className="text-2xl font-bold text-gray-900">{card.value}</p>
                <div className="flex items-center mt-1">
                  {card.changeType === 'positive' ? (
                    <TrendingUp className="h-4 w-4 text-green-500" />
                  ) : (
                    <TrendingDown className="h-4 w-4 text-red-500" />
                  )}
                  <span className={`text-sm font-medium ml-1 ${
                    card.changeType === 'positive' ? 'text-green-600' : 'text-red-600'
                  }`}>
                    {card.change}
                  </span>
                  <span className="text-sm text-gray-500 ml-1">from last month</span>
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
        {/* Claims Trend */}
        <motion.div
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.5 }}
        >
          <div className="card">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Claims Trend</h3>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={chartData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="month" />
              <YAxis />
              <Tooltip />
              <Line type="monotone" dataKey="claims" stroke="#3B82F6" strokeWidth={2} />
              <Line type="monotone" dataKey="denials" stroke="#EF4444" strokeWidth={2} />
            </LineChart>
          </ResponsiveContainer>
          </div>
        </motion.div>

        {/* Claim Status Distribution */}
        <motion.div
          initial={{ opacity: 0, x: 20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.5 }}
        >
          <div className="card">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Claim Status Distribution</h3>
          <ResponsiveContainer width="100%" height={300}>
            <PieChart>
              <Pie
                data={pieData}
                cx="50%"
                cy="50%"
                innerRadius={60}
                outerRadius={100}
                paddingAngle={5}
                dataKey="value"
              >
                {pieData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={entry.color} />
                ))}
              </Pie>
              <Tooltip />
            </PieChart>
          </ResponsiveContainer>
          <div className="flex justify-center space-x-4 mt-4">
            {pieData.map((item) => (
              <div key={item.name} className="flex items-center">
                <div className="w-3 h-3 rounded-full mr-2" style={{ backgroundColor: item.color }}></div>
                <span className="text-sm text-gray-600">{item.name}</span>
              </div>
            ))}
          </div>
          </div>
        </motion.div>
      </div>

      {/* Recent Activity */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, delay: 0.3 }}
      >
        <div className="card">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Recent Activity</h3>
        <div className="space-y-4">
          {[
            { action: 'Claim submitted', details: 'CLM-20241201-1234', time: '2 minutes ago', status: 'success' },
            { action: 'Eligibility verified', details: 'PAT-SA-001', time: '5 minutes ago', status: 'success' },
            { action: 'Prior auth approved', details: 'PA-20241201-5678', time: '1 hour ago', status: 'success' },
            { action: 'Claim denied', details: 'CLM-20241130-9876', time: '2 hours ago', status: 'error' },
            { action: 'Payment received', details: '$1,250.00', time: '3 hours ago', status: 'success' },
          ].map((activity, index) => (
            <div key={index} className="flex items-center space-x-3">
              <div className={`p-2 rounded-full ${
                activity.status === 'success' ? 'bg-green-100' : 'bg-red-100'
              }`}>
                {activity.status === 'success' ? (
                  <CheckCircle className="h-4 w-4 text-green-600" />
                ) : (
                  <AlertTriangle className="h-4 w-4 text-red-600" />
                )}
              </div>
              <div className="flex-1">
                <p className="text-sm font-medium text-gray-900">{activity.action}</p>
                <p className="text-sm text-gray-500">{activity.details}</p>
              </div>
              <span className="text-sm text-gray-400">{activity.time}</span>
            </div>
          ))}
        </div>
        </div>
      </motion.div>
    </div>
  )
}