import React, { useState, useEffect } from 'react';
import { 
  Container, 
  Typography, 
  Box, 
  Paper, 
  CircularProgress,
  Alert,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Button,
  Grid,
  Card,
  CardContent
} from '@mui/material';
import { useDropzone } from 'react-dropzone';
import axios from 'axios';
import CloudUploadIcon from '@mui/icons-material/CloudUpload';
import DescriptionIcon from '@mui/icons-material/Description';

function App() {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [results, setResults] = useState(null);
  const [serverStatus, setServerStatus] = useState('checking');

  useEffect(() => {
    // Check server health on component mount
    checkServerHealth();
  }, []);

  const checkServerHealth = async () => {
    try {
      const response = await axios.get('http://localhost:5000/health');
      if (response.data.status === 'ok') {
        setServerStatus('connected');
      } else {
        setServerStatus('error');
      }
    } catch (err) {
      setServerStatus('error');
      setError('Backend server is not running. Please make sure the Python server is started.');
    }
  };

  const onDrop = async (acceptedFiles) => {
    const file = acceptedFiles[0];
    if (!file) return;

    setLoading(true);
    setError(null);
    setResults(null);

    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await axios.post('http://localhost:5000/upload', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      setResults(response.data.anomalies);
    } catch (err) {
      if (err.code === 'ERR_NETWORK') {
        setError('Cannot connect to the server. Please make sure the backend server is running.');
      } else {
        setError(err.response?.data?.error || 'An error occurred while processing the file');
      }
    } finally {
      setLoading(false);
    }
  };

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'text/csv': ['.csv'],
      'application/vnd.ms-excel': ['.xls'],
      'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet': ['.xlsx']
    },
    maxFiles: 1
  });

  const renderResults = () => {
    if (!results) return null;

    return (
      <Box mt={4}>
        <Typography variant="h5" gutterBottom color="primary">
          Analysis Results
        </Typography>
        
        {Object.entries(results).map(([category, items]) => (
          items.length > 0 && (
            <Card key={category} sx={{ mb: 3 }}>
              <CardContent>
                <Typography variant="h6" gutterBottom color="secondary">
                  {category.replace(/_/g, ' ').toUpperCase()}
                </Typography>
                <TableContainer component={Paper} variant="outlined">
                  <Table>
                    <TableHead>
                      <TableRow>
                        {Object.keys(items[0]).map((header) => (
                          <TableCell key={header} sx={{ fontWeight: 'bold' }}>
                            {header.replace(/_/g, ' ').toUpperCase()}
                          </TableCell>
                        ))}
                      </TableRow>
                    </TableHead>
                    <TableBody>
                      {items.map((item, index) => (
                        <TableRow key={index} hover>
                          {Object.values(item).map((value, i) => (
                            <TableCell key={i}>{value}</TableCell>
                          ))}
                        </TableRow>
                      ))}
                    </TableBody>
                  </Table>
                </TableContainer>
              </CardContent>
            </Card>
          )
        ))}
      </Box>
    );
  };

  return (
    <Container maxWidth="md">
      <Box my={4}>
        <Typography 
          variant="h3" 
          component="h1" 
          gutterBottom 
          align="center"
          color="primary"
          sx={{ fontWeight: 'bold' }}
        >
          Accounting Fraud Detection
        </Typography>

        {serverStatus === 'error' && (
          <Alert severity="error" sx={{ mb: 2 }}>
            Backend server is not running. Please start the Python server first.
            <Button 
              variant="contained" 
              color="primary" 
              size="small" 
              sx={{ ml: 2 }}
              onClick={checkServerHealth}
            >
              Retry Connection
            </Button>
          </Alert>
        )}

        <Grid container spacing={3}>
          <Grid item xs={12}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom color="primary">
                  How to Use
                </Typography>
                <Typography variant="body1" paragraph>
                  1. Start the backend server:
                </Typography>
                <Box component="pre" sx={{ 
                  backgroundColor: '#f5f5f5', 
                  p: 2, 
                  borderRadius: 1,
                  overflow: 'auto'
                }}>
                  python app.py
                </Box>
                <Typography variant="body1" paragraph>
                  2. Prepare your accounting file (CSV or Excel) with the following columns:
                </Typography>
                <Box component="ul" sx={{ pl: 3 }}>
                  <li>transaction_id</li>
                  <li>amount</li>
                  <li>date</li>
                  <li>description (optional)</li>
                  <li>category (optional)</li>
                </Box>
                <Typography variant="body1" paragraph>
                  3. Upload your file using the drop zone below
                </Typography>
                <Typography variant="body1">
                  4. Wait for the analysis to complete and review the results
                </Typography>
              </CardContent>
            </Card>
          </Grid>

          <Grid item xs={12}>
            <Paper
              {...getRootProps()}
              sx={{
                p: 4,
                textAlign: 'center',
                cursor: 'pointer',
                backgroundColor: isDragActive ? '#e3f2fd' : 'white',
                border: '2px dashed #1976d2',
                '&:hover': {
                  backgroundColor: '#f5f5f5',
                },
              }}
            >
              <input {...getInputProps()} />
              {loading ? (
                <Box sx={{ display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
                  <CircularProgress size={40} />
                  <Typography sx={{ mt: 2 }}>Analyzing your file...</Typography>
                </Box>
              ) : (
                <Box sx={{ display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
                  <CloudUploadIcon sx={{ fontSize: 60, color: '#1976d2', mb: 2 }} />
                  <Typography variant="h6" gutterBottom>
                    {isDragActive
                      ? 'Drop your file here'
                      : 'Drag and drop your accounting file here'}
                  </Typography>
                  <Typography variant="body2" color="text.secondary" gutterBottom>
                    or
                  </Typography>
                  <Button variant="contained" color="primary">
                    Select File
                  </Button>
                  <Typography variant="caption" sx={{ mt: 2 }}>
                    Supported formats: CSV, XLS, XLSX
                  </Typography>
                </Box>
              )}
            </Paper>
          </Grid>
        </Grid>

        {error && (
          <Alert severity="error" sx={{ mt: 2 }}>
            {error}
          </Alert>
        )}

        {renderResults()}
      </Box>
    </Container>
  );
}

export default App; 