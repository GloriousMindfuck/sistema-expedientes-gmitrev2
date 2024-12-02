import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Paper,
  Button,
  Box,
  IconButton,
  Tooltip,
} from '@mui/material';
import {
  Edit as EditIcon,
  Delete as DeleteIcon,
  FileDownload as ExportIcon,
} from '@mui/icons-material';
import { DataGrid } from '@mui/x-data-grid';
import axios from 'axios';

function ExpedientesList() {
  const navigate = useNavigate();
  const [expedientes, setExpedientes] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchExpedientes();
  }, []);

  const fetchExpedientes = async () => {
    try {
      const response = await axios.get('/api/expedientes');
      setExpedientes(response.data);
    } catch (error) {
      console.error('Error al cargar expedientes:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (id) => {
    if (window.confirm('¿Está seguro de eliminar este expediente?')) {
      try {
        await axios.delete(`/api/expedientes/${id}`);
        fetchExpedientes();
      } catch (error) {
        console.error('Error al eliminar:', error);
      }
    }
  };

  const handleExport = async () => {
    try {
      const response = await axios.get('/api/expedientes/exportar', {
        responseType: 'blob',
      });
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', 'expedientes.xlsx');
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
    {
      field: 'actions',
      headerName: 'Acciones',
      width: 130,
      renderCell: (params) => (
        <Box>
          <IconButton
            color="primary"
            onClick={() => navigate(`/editar/${params.row.id}`)}
          >
            <EditIcon />
          </IconButton>
          <IconButton
            color="error"
            onClick={() => handleDelete(params.row.id)}
          >
            <DeleteIcon />
          </IconButton>
        </Box>
      ),
    },
  ];

  return (
    <Paper sx={{ p: 2 }}>
      <Box sx={{ mb: 2, display: 'flex', justifyContent: 'flex-end' }}>
        <Button
          variant="contained"
          color="primary"
          startIcon={<ExportIcon />}
          onClick={handleExport}
          sx={{ mr: 2 }}
        >
          Exportar a Excel
        </Button>
        <Button
          variant="contained"
          onClick={() => navigate('/nuevo')}
        >
          Nuevo Expediente
        </Button>
      </Box>

      <DataGrid
        rows={expedientes}
        columns={columns}
        pageSize={10}
        rowsPerPageOptions={[10, 25, 50]}
        checkboxSelection
        disableSelectionOnClick
        autoHeight
        loading={loading}
      />
    </Paper>
  );
}

export default ExpedientesList;
