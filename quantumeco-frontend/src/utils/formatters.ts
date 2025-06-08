export const formatCurrency = (amount: number) => 
  new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD' }).format(amount)

export const formatCO2 = (kg: number) => 
  `${kg.toFixed(2)}kg CO₂e`

export const formatDate = (timestamp: string) => 
  new Date(timestamp).toLocaleDateString()
