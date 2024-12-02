import React, { useState } from 'react';
import {
  Paper,
  TextField,
  Button,
  Grid,
  Typography,
  Box,
} from '@mui/material';
import { DatePicker } from '@mui/x-date-pickers/DatePicker';
import { DataGrid } from '@mui/x-data-grid';
import axios from 'axios';

function SearchForm() {
  const [searchParams, setSearchParams] = useState({
    fecha_desde: null,
    fecha_hasta: null,
    descripcion: '',
    monto_min: '',
    monto_max: '',
  });
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);

  const handleSearch = async () => {
    setLoading(true);
    try {
      const response = await axios.get('/api/expedientes/buscar', {
        params: {
          ...searchParams,
          fecha_desde: searchParams.fecha_desde?.toISOString(),
          fecha_hasta: searchParams.fecha_hasta?.toISOString(),
        },
      });
      setResults(response.data);
    } catch (error) {
      console.error('Error en la búsqueda:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleExport = async () => {
    try {
      const response = await axios.get('/api/expedientes/exportar', {
        params: searchParams,
        responseType: 'blob',
      });
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', 'busqueda_expedientes.xlsx');
      document.body.appendChild(link);
      link.click();
      link.remove();
    } catch (error) {
      console.error('Error al exportar:', error);
    }
  };

  const columns = [
    { field: 'numero', headerName: 'Número', width: 130 },
    { field: 'descripcion', headerName: 'Descripción', width: 300 },
    { field: 'color', headerName: 'Color', width: 130 },
    { field: 'estado', headerName: 'Estado', width: 130 },
    { field: 'monto', headerName: 'Monto', width: 130, type: 'number' },
    { field: 'fecha_pago', headerName: 'Fecha de Pago', width: 130, type: 'date' },
  ];

  return (
    <Paper sx={{ p: 4 }}>
      <Typography variant="h5" gutterBottom>
        Búsqueda Avanzada
      </Typography>

      <Grid container spacing={3}>
        <Grid item xs={12} sm={6}>
          <DatePicker
            label="Fecha Desde"
            value={searchParams.fecha_desde}
            onChange={(date) => setSearchParams(prev => ({ ...prev, fecha_desde: date }))}
            renderInput={(params) => <TextField {...params} fullWidth />}
          />
        </Grid>

        <Grid item xs={12} sm={6}>
          <DatePicker
            label="Fecha Hasta"
            value={searchParams.fecha_hasta}
            onChange={(date) => setSearchParams(prev => ({ ...prev, fecha_hasta: date }))}
            renderInput={(params) => <TextField {...params} fullWidth />}
          />
        </Grid>

        <Grid item xs={12}>
          <TextField
            fullWidth
            label="Descripción"
            value={searchParams.descripcion}
            onChange={(e) => setSearchParams(prev => ({ ...prev, descripcion: e.target.value }))}
          />
        </Grid>

        <Grid item xs={12} sm={6}>
          <TextField
            fullWidth
            type="number"
            label="Monto Mínimo"
            value={searchParams.monto_min}
            onChange={(e) => setSearchParams(prev => ({ ...prev, monto_min: e.target.value }))}
          />
        </Grid>

        <Grid item xs={12} sm={6}>
          <TextField
            fullWidth
            type="number"
            label="Monto Máximo"
            value={searchParams.monto_max}
            onChange={(e) => setSearchParams(prev => ({ ...prev, monto_max: e.target.value }))}
          />
        </Grid>
      </Grid>

      <Box sx={{ mt: 3, mb: 3, display: 'flex', gap: 2 }}>
        <Button
          variant="contained"
          onClick={handleSearch}
        >
          Buscar
        </Button>
        {results.length > 0 && (
          <Button
            variant="outlined"
            onClick={handleExport}
          >
            Exportar Resultados
          </Button>
        )}
      </Box>

      {results.length > 0 && (
        <DataGrid
          rows={results}
          columns={columns}
          pageSize={10}
          rowsPerPageOptions={[10, 25, 50]}
          autoHeight
          loading={loading}
        />
      )}
    </Paper>
  );
}

export default SearchForm;
