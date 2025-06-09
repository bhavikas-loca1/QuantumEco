import React from 'react';
import {
  Box,
  Card,
  CardContent,
  Typography,
  Chip,
  Avatar,
  List,
  ListItem,
  ListItemAvatar,
  ListItemText,
  Skeleton,
  Button,
} from '@mui/material';
import {
  RouteOutlined,
  Co2Outlined,
  SecurityOutlined,
  AssessmentOutlined,
  PlayArrowOutlined,
  CheckCircleOutlined,
  PendingOutlined,
  ErrorOutlined,
  VisibilityOutlined,
} from '@mui/icons-material';
import { type RecentActivity as RecentActivityType } from '../../Services/types';

interface RecentActivityProps {
  activities: RecentActivityType[];
  loading?: boolean;
}

/**
 * RecentActivity Component
 * Purpose: Displays recent system activities and optimizations
 * Features: Activity status indicators, impact values, timestamp formatting
 */
const RecentActivity: React.FC<RecentActivityProps> = ({ activities, loading = false }) => {
  const getActivityIcon = (activityType: string) => {
    const type = activityType.toLowerCase();
    if (type.includes('route') || type.includes('optimization')) {
      return <RouteOutlined />;
    }
    if (type.includes('carbon') || type.includes('emission') || type.includes('environmental')) {
      return <Co2Outlined />;
    }
    if (type.includes('certificate') || type.includes('blockchain') || type.includes('verification')) {
      return <SecurityOutlined />;
    }
    if (type.includes('demo') || type.includes('showcase') || type.includes('generation')) {
      return <PlayArrowOutlined />;
    }
    return <AssessmentOutlined />;
  };

  const getActivityColor = (activityType: string) => {
    const type = activityType.toLowerCase();
    if (type.includes('route') || type.includes('optimization')) {
      return 'primary.main';
    }
    if (type.includes('carbon') || type.includes('environmental')) {
      return 'success.main';
    }
    if (type.includes('certificate') || type.includes('blockchain')) {
      return 'info.main';
    }
    if (type.includes('demo')) {
      return 'secondary.main';
    }
    return 'grey.600';
  };

  const getStatusIcon = (status: string) => {
    switch (status.toLowerCase()) {
      case 'completed':
      case 'verified':
      case 'success':
        return <CheckCircleOutlined sx={{ color: 'success.main', fontSize: 16 }} />;
      case 'pending':
      case 'in_progress':
      case 'processing':
        return <PendingOutlined sx={{ color: 'warning.main', fontSize: 16 }} />;
      case 'failed':
      case 'error':
      case 'rejected':
        return <ErrorOutlined sx={{ color: 'error.main', fontSize: 16 }} />;
      default:
        return <CheckCircleOutlined sx={{ color: 'grey.500', fontSize: 16 }} />;
    }
  };

  const getStatusColor = (status: string) => {
    switch (status.toLowerCase()) {
      case 'completed':
      case 'verified':
      case 'success':
        return 'success';
      case 'pending':
      case 'in_progress':
      case 'processing':
        return 'warning';
      case 'failed':
      case 'error':
      case 'rejected':
        return 'error';
      default:
        return 'default';
    }
  };

  const formatTimestamp = (timestamp: string) => {
    try {
      const date = new Date(timestamp);
      const now = new Date();
      const diffInMinutes = Math.floor((now.getTime() - date.getTime()) / (1000 * 60));
      
      if (diffInMinutes < 1) {
        return 'Just now';
      } else if (diffInMinutes < 60) {
        return `${diffInMinutes}m ago`;
      } else if (diffInMinutes < 1440) {
        const hours = Math.floor(diffInMinutes / 60);
        return `${hours}h ago`;
      } else {
        const days = Math.floor(diffInMinutes / 1440);
        return `${days}d ago`;
      }
    } catch {
      return 'Recent';
    }
  };

  const formatImpactValue = (value?: number) => {
    if (value === undefined || value === null) return '';
    if (value >= 1000) {
      return `+${(value / 1000).toFixed(1)}K`;
    }
    return `+${value.toFixed(1)}`;
  };

  if (loading) {
    return (
      <Card sx={{ height: '100%' }}>
        <CardContent>
          <Typography variant="h6" gutterBottom>
            Recent Activity
          </Typography>
          <List sx={{ width: '100%' }}>
            {[1, 2, 3, 4, 5].map((i) => (
              <ListItem key={i} sx={{ px: 0 }}>
                <ListItemAvatar>
                  <Skeleton variant="circular" width={40} height={40} />
                </ListItemAvatar>
                <ListItemText
                  primary={<Skeleton variant="text" width="80%" height={20} />}
                  secondary={<Skeleton variant="text" width="60%" height={16} />}
                />
                <Skeleton variant="rectangular" width={60} height={24} />
              </ListItem>
            ))}
          </List>
        </CardContent>
      </Card>
    );
  }

  return (
    <Card sx={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
      <CardContent sx={{ flex: 1, display: 'flex', flexDirection: 'column' }}>
        {/* Header */}
        <Box
          sx={{
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'space-between',
            mb: 2,
          }}
        >
          <Typography variant="h6" sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
            <AssessmentOutlined color="primary" />
            Recent Activity
          </Typography>
          <Chip
            label={`${activities?.length || 0} items`}
            size="small"
            variant="outlined"
          />
        </Box>

        {/* Activities List */}
        <Box sx={{ flex: 1, overflow: 'auto' }}>
          {!activities || activities.length === 0 ? (
            <Box
              sx={{
                display: 'flex',
                flexDirection: 'column',
                alignItems: 'center',
                justifyContent: 'center',
                py: 4,
                color: 'text.secondary',
              }}
            >
              <AssessmentOutlined sx={{ fontSize: 48, mb: 2, opacity: 0.5 }} />
              <Typography variant="body1" sx={{ mb: 1 }}>
                No recent activity
              </Typography>
              <Typography variant="body2" sx={{ textAlign: 'center' }}>
                System activities will appear here as optimizations are performed
              </Typography>
            </Box>
          ) : (
            <List sx={{ width: '100%', py: 0 }}>
              {activities.map((activity, index) => (
                <ListItem
                  key={`${activity.timestamp}-${index}`}
                  sx={{
                    px: 0,
                    py: 1.5,
                    borderBottom: index < activities.length - 1 ? '1px solid' : 'none',
                    borderColor: 'divider',
                  }}
                >
                  <ListItemAvatar>
                    <Avatar
                      sx={{
                        bgcolor: getActivityColor(activity.activity_type),
                        width: 40,
                        height: 40,
                      }}
                    >
                      {getActivityIcon(activity.activity_type)}
                    </Avatar>
                  </ListItemAvatar>
                  
                  <ListItemText
                    primary={
                      <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mb: 0.5 }}>
                        <Typography variant="body2" sx={{ fontWeight: 500 }}>
                          {activity.description}
                        </Typography>
                        {getStatusIcon(activity.status)}
                      </Box>
                    }
                    secondary={
                      <Box sx={{ display: 'flex', alignItems: 'center', gap: 2, mt: 0.5 }}>
                        <Typography variant="caption" color="text.secondary">
                          {formatTimestamp(activity.timestamp)}
                        </Typography>
                        {activity.route_id && (
                          <Typography variant="caption" color="text.secondary">
                            Route: {activity.route_id.slice(-6)}
                          </Typography>
                        )}
                      </Box>
                    }
                  />
                  
                  <Box sx={{ display: 'flex', flexDirection: 'column', alignItems: 'flex-end', gap: 1 }}>
                    <Chip
                      label={activity.status}
                      size="small"
                      color={getStatusColor(activity.status)}
                      variant="outlined"
                    />
                    {activity.impact_value !== undefined && activity.impact_value > 0 && (
                      <Typography 
                        variant="caption" 
                        color="success.main"
                        sx={{ fontWeight: 'bold' }}
                      >
                        {formatImpactValue(activity.impact_value)}
                      </Typography>
                    )}
                  </Box>
                </ListItem>
              ))}
            </List>
          )}
        </Box>

        {/* View All Button */}
        {activities && activities.length > 0 && (
          <Box sx={{ mt: 2, textAlign: 'center' }}>
            <Button 
              variant="outlined" 
              size="small" 
              startIcon={<VisibilityOutlined />}
              sx={{ minWidth: 140 }}
            >
              View All Activity
            </Button>
          </Box>
        )}
      </CardContent>
    </Card>
  );
};

export default RecentActivity;
