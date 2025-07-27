import React, { useState } from 'react';
import { 
  Box, 
  Typography, 
  Card, 
  CardContent, 
  TextField, 
  Button, 
  Grid, 
  CircularProgress,
  Chip,
  Divider,
  Paper,
  FormControlLabel,
  Switch,
  Alert,
  AlertTitle
} from '@mui/material';
import { 
  Psychology, 
  Sentiment, 
  Analytics, 
  Language, 
  Send,
  BarChart
} from '@mui/icons-material';
import { useForm, Controller } from 'react-hook-form';
import { useMutation } from '@tanstack/react-query';
import { toast } from 'react-hot-toast';
import apiService from '../services/api';

// Types
interface EmotionAnalysisForm {
  text: string;
  analysisType: string;
  culturalContext: boolean;
}

interface EmotionResult {
  success: boolean;
  emotions: Record<string, number>;
  sentiment: {
    label: string;
    confidence: number;
    positive_score: number;
    negative_score: number;
    neutral_score: number;
  };
  cultural_elements: string[];
  metadata: Record<string, any>;
}

const EmotionAnalysis: React.FC = () => {
  const [analysisResult, setAnalysisResult] = useState<EmotionResult | null>(null);
  
  // Form setup
  const { control, handleSubmit, formState: { errors }, reset } = useForm<EmotionAnalysisForm>({
    defaultValues: {
      text: '',
      analysisType: 'comprehensive',
      culturalContext: true
    }
  });
  
  // Emotion analysis mutation
  const analyzeEmotionMutation = useMutation(
    (data: EmotionAnalysisForm) => apiService.analyzeEmotions(data),
    {
      onSuccess: (data) => {
        console.log('Emotion analysis completed successfully:', data);
        setAnalysisResult(data);
        toast.success('Emotion analysis completed!');
      },
      onError: (error: any) => {
        console.error('Failed to analyze emotions:', error);
        toast.error('Failed to analyze emotions');
        
        if (error.message) {
          toast.error(`Error: ${error.message}`);
        }
      }
    }
  );
  
  // Form submission
  const onSubmit = (data: EmotionAnalysisForm) => {
    console.log('Submitting emotion analysis request:', data);
    analyzeEmotionMutation.mutate(data);
    toast.loading('Analyzing emotions...', { id: 'emotion-analysis' });
  };
  
  // Reset form and results
  const handleReset = () => {
    reset();
    setAnalysisResult(null);
  };
  
  // Render emotion bar chart
  const renderEmotionBars = () => {
    if (!analysisResult) return null;
    
    // Sort emotions by score
    const sortedEmotions = Object.entries(analysisResult.emotions)
      .sort((a, b) => b[1] - a[1])
      .slice(0, 6); // Show top 6 emotions
    
    return (
      <Box sx={{ mt: 3 }}>
        <Typography variant="h6" gutterBottom>
          Emotion Analysis
        </Typography>
        
        {sortedEmotions.map(([emotion, score]) => (
          <Box key={emotion} sx={{ mb: 1 }}>
            <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 0.5 }}>
              <Typography variant="body2">{emotion}</Typography>
              <Typography variant="body2">{(score * 100).toFixed(1)}%</Typography>
            </Box>
            <Box sx={{ width: '100%', bgcolor: 'grey.300', borderRadius: 1, height: 10 }}>
              <Box
                sx={{
                  width: `${score * 100}%`,
                  bgcolor: getEmotionColor(emotion),
                  borderRadius: 1,
                  height: 10
                }}
              />
            </Box>
          </Box>
        ))}
      </Box>
    );
  };
  
  // Get color for emotion
  const getEmotionColor = (emotion: string): string => {
    const colors: Record<string, string> = {
      happiness: 'success.main',
      sadness: 'info.main',
      anger: 'error.main',
      fear: 'warning.dark',
      surprise: 'secondary.main',
      disgust: 'error.dark',
      love: 'error.light',
      pride: 'warning.main',
      shame: 'info.dark',
      guilt: 'info.light'
    };
    
    return colors[emotion] || 'primary.main';
  };
  
  // Render sentiment analysis
  const renderSentiment = () => {
    if (!analysisResult) return null;
    
    const { sentiment } = analysisResult;
    
    return (
      <Box sx={{ mt: 3 }}>
        <Typography variant="h6" gutterBottom>
          Sentiment Analysis
        </Typography>
        
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 2, mb: 2 }}>
          <Chip 
            label={sentiment.label.toUpperCase()} 
            color={
              sentiment.label === 'positive' ? 'success' :
              sentiment.label === 'negative' ? 'error' : 'default'
            }
            icon={<Sentiment />}
          />
          <Typography variant="body2">
            Confidence: {(sentiment.confidence * 100).toFixed(1)}%
          </Typography>
        </Box>
        
        <Grid container spacing={2}>
          <Grid item xs={4}>
            <Paper sx={{ p: 2, textAlign: 'center' }}>
              <Typography variant="body2" color="text.secondary">Positive</Typography>
              <Typography variant="h6">{(sentiment.positive_score * 100).toFixed(1)}%</Typography>
            </Paper>
          </Grid>
          <Grid item xs={4}>
            <Paper sx={{ p: 2, textAlign: 'center' }}>
              <Typography variant="body2" color="text.secondary">Neutral</Typography>
              <Typography variant="h6">{(sentiment.neutral_score * 100).toFixed(1)}%</Typography>
            </Paper>
          </Grid>
          <Grid item xs={4}>
            <Paper sx={{ p: 2, textAlign: 'center' }}>
              <Typography variant="body2" color="text.secondary">Negative</Typography>
              <Typography variant="h6">{(sentiment.negative_score * 100).toFixed(1)}%</Typography>
            </Paper>
          </Grid>
        </Grid>
      </Box>
    );
  };
  
  // Render cultural elements
  const renderCulturalElements = () => {
    if (!analysisResult || !analysisResult.cultural_elements || analysisResult.cultural_elements.length === 0) {
      return null;
    }
    
    return (
      <Box sx={{ mt: 3 }}>
        <Typography variant="h6" gutterBottom>
          Cultural Elements
        </Typography>
        
        <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
          {analysisResult.cultural_elements.map((element, index) => (
            <Chip 
              key={index}
              label={element}
              color="primary"
              variant="outlined"
              icon={<Language />}
            />
          ))}
        </Box>
      </Box>
    );
  };
  
  // Render metadata
  const renderMetadata = () => {
    if (!analysisResult || !analysisResult.metadata) return null;
    
    const { metadata } = analysisResult;
    
    return (
      <Box sx={{ mt: 3 }}>
        <Typography variant="h6" gutterBottom>
          Analysis Metadata
        </Typography>
        
        <Grid container spacing={2}>
          <Grid item xs={6} md={3}>
            <Paper sx={{ p: 2, textAlign: 'center' }}>
              <Typography variant="body2" color="text.secondary">Text Length</Typography>
              <Typography variant="h6">{metadata.text_length}</Typography>
            </Paper>
          </Grid>
          <Grid item xs={6} md={3}>
            <Paper sx={{ p: 2, textAlign: 'center' }}>
              <Typography variant="body2" color="text.secondary">Analysis Type</Typography>
              <Typography variant="h6">{metadata.analysis_type}</Typography>
            </Paper>
          </Grid>
          <Grid item xs={6} md={3}>
            <Paper sx={{ p: 2, textAlign: 'center' }}>
              <Typography variant="body2" color="text.secondary">Language</Typography>
              <Typography variant="h6">{metadata.language}</Typography>
            </Paper>
          </Grid>
          <Grid item xs={6} md={3}>
            <Paper sx={{ p: 2, textAlign: 'center' }}>
              <Typography variant="body2" color="text.secondary">AI Model</Typography>
              <Typography variant="h6">{metadata.model || 'AI Model'}</Typography>
            </Paper>
          </Grid>
        </Grid>
      </Box>
    );
  };
  
  return (
    <Box>
      <Box sx={{ mb: 4 }}>
        <Typography variant="h4" gutterBottom>
          Emotion Analysis
        </Typography>
        <Typography variant="body1" color="text.secondary">
          Advanced emotion detection and sentiment analysis for Telugu text
        </Typography>
      </Box>

      <Grid container spacing={3}>
        {/* Input Form */}
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', gap: 2, mb: 3 }}>
                <Psychology color="secondary" />
                <Typography variant="h6">Real AI-Powered Emotion Analysis</Typography>
              </Box>
              
              <form onSubmit={handleSubmit(onSubmit)}>
                <Controller
                  name="text"
                  control={control}
                  rules={{ required: 'Text is required' }}
                  render={({ field }) => (
                    <TextField
                      {...field}
                      label="Enter Telugu Text"
                      multiline
                      rows={6}
                      fullWidth
                      variant="outlined"
                      error={!!errors.text}
                      helperText={errors.text?.message}
                      placeholder="రాజు చాలా కోపంగా ఉన్నాడు. అతని కళ్ళలో నిప్పులు చిమ్ముతున్నాయి."
                      sx={{ mb: 3 }}
                    />
                  )}
                />
                
                <Box sx={{ mb: 3 }}>
                  <Controller
                    name="analysisType"
                    control={control}
                    render={({ field }) => (
                      <Box>
                        <Typography variant="body2" color="text.secondary" gutterBottom>
                          Analysis Type
                        </Typography>
                        <Box sx={{ display: 'flex', gap: 1 }}>
                          <Chip
                            label="Basic"
                            onClick={() => field.onChange('basic')}
                            color={field.value === 'basic' ? 'primary' : 'default'}
                            variant={field.value === 'basic' ? 'filled' : 'outlined'}
                          />
                          <Chip
                            label="Comprehensive"
                            onClick={() => field.onChange('comprehensive')}
                            color={field.value === 'comprehensive' ? 'primary' : 'default'}
                            variant={field.value === 'comprehensive' ? 'filled' : 'outlined'}
                          />
                          <Chip
                            label="Advanced"
                            onClick={() => field.onChange('advanced')}
                            color={field.value === 'advanced' ? 'primary' : 'default'}
                            variant={field.value === 'advanced' ? 'filled' : 'outlined'}
                          />
                        </Box>
                      </Box>
                    )}
                  />
                </Box>
                
                <Box sx={{ mb: 3 }}>
                  <Controller
                    name="culturalContext"
                    control={control}
                    render={({ field }) => (
                      <FormControlLabel
                        control={
                          <Switch
                            checked={field.value}
                            onChange={(e) => field.onChange(e.target.checked)}
                          />
                        }
                        label="Include Cultural Context"
                      />
                    )}
                  />
                </Box>
                
                <Box sx={{ display: 'flex', gap: 2 }}>
                  <Button
                    type="submit"
                    variant="contained"
                    color="primary"
                    startIcon={analyzeEmotionMutation.isLoading ? <CircularProgress size={20} color="inherit" /> : <Send />}
                    disabled={analyzeEmotionMutation.isLoading}
                  >
                    Analyze Emotions
                  </Button>
                  
                  <Button
                    variant="outlined"
                    onClick={handleReset}
                    disabled={analyzeEmotionMutation.isLoading}
                  >
                    Reset
                  </Button>
                </Box>
              </form>
            </CardContent>
          </Card>
        </Grid>
        
        {/* Results */}
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', gap: 2, mb: 3 }}>
                <BarChart color="primary" />
                <Typography variant="h6">Analysis Results</Typography>
              </Box>
              
              {analyzeEmotionMutation.isLoading && (
                <Box sx={{ display: 'flex', justifyContent: 'center', my: 4 }}>
                  <CircularProgress />
                </Box>
              )}
              
              {analyzeEmotionMutation.isError && (
                <Alert severity="error" sx={{ mb: 3 }}>
                  <AlertTitle>Error</AlertTitle>
                  Failed to analyze emotions. Please try again.
                </Alert>
              )}
              
              {analysisResult && (
                <>
                  {renderEmotionBars()}
                  <Divider sx={{ my: 3 }} />
                  {renderSentiment()}
                  <Divider sx={{ my: 3 }} />
                  {renderCulturalElements()}
                  <Divider sx={{ my: 3 }} />
                  {renderMetadata()}
                </>
              )}
              
              {!analyzeEmotionMutation.isLoading && !analysisResult && (
                <Box sx={{ textAlign: 'center', py: 4 }}>
                  <Typography variant="body1" color="text.secondary">
                    Enter Telugu text and click "Analyze Emotions" to see results
                  </Typography>
                </Box>
              )}
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Box>
  );
};

export default EmotionAnalysis;