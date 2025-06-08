import React from 'react'
import { Paper, Typography, Box } from '@mui/material'
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  AreaChart,
  Area,
} from 'recharts'

interface CarbonTrend {
  date: string
  savings: number
  emissions: number
}

interface CarbonSavingsChartProps {
  data: CarbonTrend[]
}

const CarbonSavingsChart: React.FC<CarbonSavingsChartProps> = ({ data }) => {
  // Generate demo data if none provided
  const chartData = data.length > 0 ? data : Array.from({ length: 7 }, (_, i) => ({
    date: `Day ${i + 1}`,
    savings: Math.random() * 100 + 50,
    emissions: Math.random() * 200 + 100,
  }))

  return (
    <Paper sx={{ p: 3 }}>
      <Typography variant="h6" gutterBottom>
        Carbon Impact Analysis
      </Typography>
      
      {/* Emissions vs Savings Chart */}
      <Box mb={4}>
        <Typography variant="subtitle2" gutterBottom>
          Daily Carbon Emissions vs Savings
        </Typography>
        <ResponsiveContainer width="100%" height={300}>
          <AreaChart data={chartData}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="date" />
            <YAxis />
            <Tooltip 
              formatter={(value: number, name: string) => [
                `${value.toFixed(1)} kg CO₂`,
                name === 'savings' ? 'Carbon Saved' : 'Total Emissions'
              ]}
            />
            <Legend />
            <Area
              type="monotone"
              dataKey="emissions"
              stackId="1"
              stroke="#ff7043"
              fill="#ff7043"
              fillOpacity={0.6}
              name="Total Emissions"
            />
            <Area
              type="monotone"
              dataKey="savings"
              stackId="2"
              stroke="#4caf50"
              fill="#4caf50"
              fillOpacity={0.8}
              name="Carbon Saved"
            />
          </AreaChart>
        </ResponsiveContainer>
      </Box>

      {/* Savings Trend */}
      <Box>
        <Typography variant="subtitle2" gutterBottom>
          Carbon Savings Trend
        </Typography>
        <ResponsiveContainer width="100%" height={200}>
          <LineChart data={chartData}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="date" />
            <YAxis />
            <Tooltip 
              formatter={(value: number) => [`${value.toFixed(1)} kg CO₂`, 'Carbon Saved']}
            />
            <Legend />
            <Line 
              type="monotone" 
              dataKey="savings" 
              stroke="#4caf50" 
              strokeWidth={3}
              dot={{ fill: '#4caf50', strokeWidth: 2, r: 4 }}
              name="Carbon Saved"
            />
          </LineChart>
        </ResponsiveContainer>
      </Box>
    </Paper>
  )
}

export default CarbonSavingsChart
