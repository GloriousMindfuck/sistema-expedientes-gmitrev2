import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import {
  Paper,
  TextField,
  Button,
  Grid,
  Typography,
  MenuItem,
  Box,
} from '@mui/material';
import axios from 'axios';

const COLORES = [
  'Blanco',
  'Negro',
  'Rosa Pastel',
  'Azul Pastel',
  'Verde Pastel',
  'Amarillo Pastel',
  'Lavanda',
  'Melocotón',
  'Menta',
  'Celeste',
  'Coral',
  'Lila',
];

const ESTADOS = [
  'Pagado',
  'Abierto',
  'Cerrado',
  'Pendiente',
  'Faltan Firmas',
];

function ExpedienteForm() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    numero: '',
    descripcion: '',
    color: '',
    color_bibliorato: '',
    estado: '',
    monto: '',
  });

  useEffect(() => {
    if (id) {
      axios.get(`/api/expedientes/${id}`)
        .then(response => {
          setFormData(response.data);
        })
        .catch(error => {
          console.error('Error al cargar expediente:', error);
        });
    }
  }, [id]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      if (id) {
        await axios.put(`/api/expedientes/${id}`, formData);
      } else {
        await axios.post('/api/expedientes', formData);
      }
      navigate('/');
    } catch (error) {
      console.error('Error al guardar:', error);
    }
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  return (
    <Paper sx={{ p: 4 }}>
      <Typography variant="h5" gutterBottom>
        {id ? 'Editar Expediente' : 'Nuevo Expediente'}
      </Typography>
      
      <form onSubmit={handleSubmit}>
        <Grid container spacing={3}>
          <Grid item xs={12} sm={6}>
            <TextField
              required
              fullWidth
              label="Número de Expediente"
              name="numero"
              value={formData.numero}
              onChange={handleChange}
            />
          </Grid>
          
          <Grid item xs={12}>
            <TextField
              fullWidth
              multiline
              rows={4}
              label="Descripción"
              name="descripcion"
              value={formData.descripcion}
              onChange={handleChange}
            />
          </Grid>
          
          <Grid item xs={12} sm={6}>
            <TextField
              select
              fullWidth
              label="Color"
              name="color"
              value={formData.color}
              onChange={handleChange}
            >
              {COLORES.map(color => (
                <MenuItem key={color} value={color}>
                  {color}
                </MenuItem>
              ))}
            </TextField>
          </Grid>
          
          <Grid item xs={12} sm={6}>
            <TextField
              select
              fullWidth
              label="Color de Bibliorato"
              name="color_bibliorato"
              value={formData.color_bibliorato}
              onChange={handleChange}
            >
              {COLORES.map(color => (
                <MenuItem key={color} value={color}>
                  {color}
                </MenuItem>
              ))}
            </TextField>
          </Grid>
          
          <Grid item xs={12} sm={6}>
            <TextField
              select
              required
              fullWidth
              label="Estado"
              name="estado"
              value={formData.estado}
              onChange={handleChange}
            >
              {ESTADOS.map(estado => (
                <MenuItem key={estado} value={estado}>
                  {estado}
                </MenuItem>
              ))}
            </TextField>
          </Grid>
          
          <Grid item xs={12} sm={6}>
            <TextField
              required
              fullWidth
              type="number"
              label="Monto"
              name="monto"
              value={formData.monto}
              onChange={handleChange}
            />
          </Grid>
        </Grid>
        
        <Box sx={{ mt: 3, display: 'flex', justifyContent: 'flex-end', gap: 2 }}>
          <Button
            variant="outlined"
            onClick={() => navigate('/')}
          >
            Cancelar
          </Button>
          <Button
            type="submit"
            variant="contained"
            color="primary"
          >
            Guardar
          </Button>
        </Box>
      </form>
    </Paper>
  );
}

export default ExpedienteForm;
