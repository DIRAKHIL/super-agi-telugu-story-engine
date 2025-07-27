import React, { useState } from 'react';
import {
  Box,
  Grid,
  Card,
  CardContent,
  Typography,
  TextField,
  Button,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Chip,
  Paper,
  CircularProgress,
  Alert,
  Accordion,
  AccordionSummary,
  AccordionDetails,
  Slider,
} from '@mui/material';
import {
  ExpandMore,
  AutoStories,
  Psychology,
  Language as Culture,
  Send,
  Refresh,
} from '@mui/icons-material';
import { useForm, Controller } from 'react-hook-form';
import { useMutation, useQuery } from 'react-query';
import toast from 'react-hot-toast';

import { apiService } from '../services/api.ts';

interface StoryFormData {
  prompt: string;
  genre: string;
  characters: string;
  setting: string;
  theme: string;
  maxLength: number;
  temperature: number;
  topP: number;
  topK: number;
}

const StoryGeneration: React.FC = () => {
  const [taskId, setTaskId] = useState<string | null>(null);
  const [storyResult, setStoryResult] = useState<any>(null);
  const [isPolling, setIsPolling] = useState(false);

  const { control, handleSubmit, reset, watch } = useForm<StoryFormData>({
    defaultValues: {
      prompt: '',
      genre: 'drama',
      characters: '',
      setting: 'modern',
      theme: 'family',
      maxLength: 2000,
      temperature: 0.8,
      topP: 0.9,
      topK: 50,
    },
  });

  // Fetch options
  const { data: genres, error: genresError, isLoading: genresLoading } = useQuery('story-genres', apiService.getStoryGenres);
  const { data: themes, error: themesError, isLoading: themesLoading } = useQuery('story-themes', apiService.getStoryThemes);
  const { data: settings, error: settingsError, isLoading: settingsLoading } = useQuery('story-settings', apiService.getStorySettings);

  // Debug logging
  React.useEffect(() => {
    console.log('Genres data:', genres, 'Error:', genresError, 'Loading:', genresLoading);
    console.log('Themes data:', themes, 'Error:', themesError, 'Loading:', themesLoading);
    console.log('Settings data:', settings, 'Error:', settingsError, 'Loading:', settingsLoading);
  }, [genres, themes, settings, genresError, themesError, settingsError, genresLoading, themesLoading, settingsLoading]);

  // Generate story mutation
  const generateStoryMutation = useMutation(apiService.generateStory, {
    onSuccess: (data) => {
      setTaskId(data.task_id);
      setIsPolling(true);
      toast.success('Story generation started!');
      pollTaskResult(data.task_id);
    },
    onError: (error: any) => {
      toast.error('Failed to start story generation');
      console.error(error);
    },
  });

  // Poll for task result
  const pollTaskResult = async (id: string) => {
    const maxAttempts = 60; // 5 minutes with 5-second intervals
    let attempts = 0;

    const poll = async () => {
      try {
        const result = await apiService.getStoryTask(id);
        
        if (result.status === 'completed') {
          setStoryResult(result);
          setIsPolling(false);
          toast.success('Story generated successfully!');
        } else if (result.status === 'failed') {
          setIsPolling(false);
          toast.error('Story generation failed');
        } else if (attempts < maxAttempts) {
          attempts++;
          setTimeout(poll, 5000); // Poll every 5 seconds
        } else {
          setIsPolling(false);
          toast.error('Story generation timed out');
        }
      } catch (error) {
        console.error('Polling error:', error);
        if (attempts < maxAttempts) {
          attempts++;
          setTimeout(poll, 5000);
        } else {
          setIsPolling(false);
          toast.error('Failed to get story result');
        }
      }
    };

    poll();
  };

  const onSubmit = (data: StoryFormData) => {
    const characters = data.characters
      ? data.characters.split(',').map(c => c.trim()).filter(c => c)
      : [];

    generateStoryMutation.mutate({
      ...data,
      characters,
    });
  };

  const handleReset = () => {
    reset();
    setTaskId(null);
    setStoryResult(null);
    setIsPolling(false);
  };

  return (
    <Box>
      {/* Header */}
      <Box sx={{ mb: 4 }}>
        <Typography variant="h4" gutterBottom>
          Telugu Story Generation
        </Typography>
        <Typography variant="body1" color="text.secondary">
          Generate authentic Telugu film stories using advanced AI models
        </Typography>
      </Box>

      <Grid container spacing={3}>
        {/* Story Generation Form */}
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                <AutoStories color="primary" />
                Story Configuration
              </Typography>

              <Box component="form" onSubmit={handleSubmit(onSubmit)} sx={{ mt: 2 }}>
                {/* Basic Configuration */}
                <Controller
                  name="prompt"
                  control={control}
                  rules={{ required: 'Story prompt is required' }}
                  render={({ field, fieldState }) => (
                    <TextField
                      {...field}
                      label="Story Prompt"
                      multiline
                      rows={4}
                      fullWidth
                      margin="normal"
                      placeholder="Enter your story idea or theme in Telugu or English..."
                      error={!!fieldState.error}
                      helperText={fieldState.error?.message}
                    />
                  )}
                />

                <Grid container spacing={2} sx={{ mt: 1 }}>
                  <Grid item xs={12} sm={6}>
                    <Controller
                      name="genre"
                      control={control}
                      render={({ field }) => (
                        <FormControl fullWidth>
                          <InputLabel>Genre</InputLabel>
                          <Select {...field} label="Genre">
                            {genres?.genres?.map((genre: any) => (
                              <MenuItem key={genre.id} value={genre.id}>
                                {genre.name} - {genre.description}
                              </MenuItem>
                            ))}
                          </Select>
                        </FormControl>
                      )}
                    />
                  </Grid>

                  <Grid item xs={12} sm={6}>
                    <Controller
                      name="theme"
                      control={control}
                      render={({ field }) => (
                        <FormControl fullWidth>
                          <InputLabel>Theme</InputLabel>
                          <Select {...field} label="Theme">
                            {themes?.themes?.map((theme: any) => (
                              <MenuItem key={theme.id} value={theme.id}>
                                {theme.name} - {theme.description}
                              </MenuItem>
                            ))}
                          </Select>
                        </FormControl>
                      )}
                    />
                  </Grid>
                </Grid>

                <Controller
                  name="setting"
                  control={control}
                  render={({ field }) => (
                    <FormControl fullWidth sx={{ mt: 2 }}>
                      <InputLabel>Setting</InputLabel>
                      <Select {...field} label="Setting">
                        {settings?.settings?.map((setting: any) => (
                          <MenuItem key={setting.id} value={setting.id}>
                            {setting.name} - {setting.description}
                          </MenuItem>
                        ))}
                      </Select>
                    </FormControl>
                  )}
                />

                <Controller
                  name="characters"
                  control={control}
                  render={({ field }) => (
                    <TextField
                      {...field}
                      label="Characters (comma-separated)"
                      fullWidth
                      margin="normal"
                      placeholder="రాము, సీత, లక్ష్మణ"
                      helperText="Enter character names separated by commas"
                    />
                  )}
                />

                {/* Advanced Configuration */}
                <Accordion sx={{ mt: 2 }}>
                  <AccordionSummary expandIcon={<ExpandMore />}>
                    <Typography>Advanced Settings</Typography>
                  </AccordionSummary>
                  <AccordionDetails>
                    <Grid container spacing={2}>
                      <Grid item xs={12}>
                        <Controller
                          name="maxLength"
                          control={control}
                          render={({ field }) => (
                            <Box>
                              <Typography gutterBottom>
                                Max Length: {field.value} words
                              </Typography>
                              <Slider
                                {...field}
                                min={500}
                                max={5000}
                                step={100}
                                marks={[
                                  { value: 500, label: '500' },
                                  { value: 2000, label: '2000' },
                                  { value: 5000, label: '5000' },
                                ]}
                              />
                            </Box>
                          )}
                        />
                      </Grid>

                      <Grid item xs={12} sm={4}>
                        <Controller
                          name="temperature"
                          control={control}
                          render={({ field }) => (
                            <Box>
                              <Typography gutterBottom>
                                Creativity: {field.value}
                              </Typography>
                              <Slider
                                {...field}
                                min={0.1}
                                max={1.0}
                                step={0.1}
                                marks={[
                                  { value: 0.1, label: 'Conservative' },
                                  { value: 0.8, label: 'Balanced' },
                                  { value: 1.0, label: 'Creative' },
                                ]}
                              />
                            </Box>
                          )}
                        />
                      </Grid>

                      <Grid item xs={12} sm={4}>
                        <Controller
                          name="topP"
                          control={control}
                          render={({ field }) => (
                            <Box>
                              <Typography gutterBottom>
                                Focus: {field.value}
                              </Typography>
                              <Slider
                                {...field}
                                min={0.1}
                                max={1.0}
                                step={0.1}
                              />
                            </Box>
                          )}
                        />
                      </Grid>

                      <Grid item xs={12} sm={4}>
                        <Controller
                          name="topK"
                          control={control}
                          render={({ field }) => (
                            <Box>
                              <Typography gutterBottom>
                                Diversity: {field.value}
                              </Typography>
                              <Slider
                                {...field}
                                min={10}
                                max={100}
                                step={10}
                              />
                            </Box>
                          )}
                        />
                      </Grid>
                    </Grid>
                  </AccordionDetails>
                </Accordion>

                {/* Action Buttons */}
                <Box sx={{ display: 'flex', gap: 2, mt: 3 }}>
                  <Button
                    type="submit"
                    variant="contained"
                    startIcon={isPolling ? <CircularProgress size={20} /> : <Send />}
                    disabled={generateStoryMutation.isLoading || isPolling}
                    sx={{ flex: 1 }}
                  >
                    {isPolling ? 'Generating...' : 'Generate Story'}
                  </Button>
                  <Button
                    variant="outlined"
                    startIcon={<Refresh />}
                    onClick={handleReset}
                    disabled={generateStoryMutation.isLoading || isPolling}
                  >
                    Reset
                  </Button>
                </Box>
              </Box>
            </CardContent>
          </Card>
        </Grid>

        {/* Story Result */}
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                <Psychology color="secondary" />
                Generated Story
              </Typography>

              {isPolling && (
                <Box sx={{ display: 'flex', alignItems: 'center', gap: 2, p: 3 }}>
                  <CircularProgress />
                  <Box>
                    <Typography variant="body1">
                      Generating your Telugu story...
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                      This may take a few minutes
                    </Typography>
                  </Box>
                </Box>
              )}

              {storyResult && storyResult.success && (
                <Box>
                  <Box sx={{ mb: 2 }}>
                    <Chip
                      label={`${storyResult.result?.metadata?.word_count || 0} words`}
                      color="primary"
                      size="small"
                      sx={{ mr: 1 }}
                    />
                    <Chip
                      label={`${storyResult.result?.metadata?.estimated_reading_time || 0} min read`}
                      color="secondary"
                      size="small"
                      sx={{ mr: 1 }}
                    />
                    <Chip
                      label={storyResult.result?.metadata?.genre || 'Unknown'}
                      variant="outlined"
                      size="small"
                    />
                  </Box>

                  <Paper sx={{ p: 3, bgcolor: 'grey.50', maxHeight: 400, overflow: 'auto' }}>
                    <Typography
                      variant="body1"
                      sx={{
                        whiteSpace: 'pre-wrap',
                        lineHeight: 1.8,
                        fontFamily: 'serif',
                      }}
                    >
                      {storyResult.result?.story}
                    </Typography>
                  </Paper>

                  <Box sx={{ mt: 2, display: 'flex', gap: 1 }}>
                    <Button variant="outlined" size="small">
                      Enhance Story
                    </Button>
                    <Button variant="outlined" size="small">
                      Analyze Emotions
                    </Button>
                    <Button variant="outlined" size="small">
                      Cultural Validation
                    </Button>
                  </Box>
                </Box>
              )}

              {storyResult && !storyResult.success && (
                <Alert severity="error" sx={{ mt: 2 }}>
                  <Typography variant="body2">
                    Story generation failed: {storyResult.error}
                  </Typography>
                </Alert>
              )}

              {!isPolling && !storyResult && (
                <Box sx={{ textAlign: 'center', py: 4 }}>
                  <AutoStories sx={{ fontSize: 64, color: 'grey.300', mb: 2 }} />
                  <Typography variant="body1" color="text.secondary">
                    Configure your story parameters and click "Generate Story" to begin
                  </Typography>
                </Box>
              )}
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* Features Info */}
      <Grid container spacing={3} sx={{ mt: 2 }}>
        <Grid item xs={12} md={4}>
          <Card sx={{ height: '100%' }}>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                <AutoStories color="primary" sx={{ mr: 1 }} />
                <Typography variant="h6">Real AI Models</Typography>
              </Box>
              <Typography variant="body2" color="text.secondary">
                Uses advanced transformer models specifically trained for Telugu language generation.
                No mock data or templates - every story is uniquely generated.
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={4}>
          <Card sx={{ height: '100%' }}>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                <Culture color="success" sx={{ mr: 1 }} />
                <Typography variant="h6">Cultural Authenticity</Typography>
              </Box>
              <Typography variant="body2" color="text.secondary">
                Incorporates Telugu cultural elements, family dynamics, festivals, and traditional values
                for authentic storytelling that resonates with Telugu audiences.
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={4}>
          <Card sx={{ height: '100%' }}>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                <Psychology color="secondary" sx={{ mr: 1 }} />
                <Typography variant="h6">Emotion Analysis</Typography>
              </Box>
              <Typography variant="body2" color="text.secondary">
                Advanced emotion detection and sentiment analysis to ensure proper emotional arcs
                and character development in generated stories.
              </Typography>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Box>
  );
};

export default StoryGeneration;