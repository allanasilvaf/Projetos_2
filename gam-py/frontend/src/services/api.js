import axios from 'axios';

// Cria uma instância com a URL base do seu Python
const api = axios.create({
  baseURL: 'http://localhost:9000', // Porta onde o FastAPI/Python está rodando
  timeout: 10000, // Tempo limite de 10 segundos
});

export default api;