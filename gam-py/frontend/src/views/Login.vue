<script>
export default {
  data() {
    return {
      form: {
        email: '',
        password: ''
      },
      loading: false,
      error: ''
    }
  },
  methods: {
    async handleLogin() {
      this.loading = true;
      this.error = '';
      
      try {
        const response = await fetch('http://localhost:9000/api/login.php', {
          method: 'POST',
          headers: { 
            'Content-Type': 'application/json',
            'Accept': 'application/json'
          },
          body: JSON.stringify({
            email: this.form.email,
            senha: this.form.password
          })
        });
        
        const text = await response.text();
        console.log("Resposta bruta do servidor:", text);

        let data;
        try {
            data = JSON.parse(text);
        } catch (e) {
            throw new Error("O servidor não retornou um JSON válido. Veja o console.");
        }
        
        if (data.error) {
          this.error = data.error;
          alert("ERRO DE SISTEMA: " + data.error);
          return;
        }

        if (data.success) {
          localStorage.setItem('user', JSON.stringify(data.usuario));
          localStorage.setItem('token', 'fake_token_' + Date.now());
          
          this.redirectUser(data.usuario.tipo);
          
        } else {
          this.error = data.message || 'Email ou senha incorretos';
          alert("Atenção: " + this.error);
        }
        
      } catch (error) {
        console.error('Erro completo:', error);
        this.error = 'Erro de conexão ou servidor';
        alert("Erro técnico: " + error.message);
      } finally {
        this.loading = false;
      }
    },
    
    redirectUser(tipo) {
      switch(tipo) {
        case 'professor':
          this.$router.push('/professor/dashboard');
          break;
        case 'admin':
          this.$router.push('/admin/dashboard');
          break;
        default:
          this.$router.push('/dashboard');
      }
    }
  }
}
</script>

<template>
  <div class="login-container">
    <div class="login-card">
      <!-- Cabeçalho -->
      <div class="login-header">
        <div class="logo">
          <span class="logo-icon">🎓</span>
          <h1>GAM - Login</h1>
        </div>
        <p class="subtitle">Sistema de Gestão Acadêmica</p>
      </div>

      <!-- Formulário -->
      <form @submit.prevent="handleLogin" class="login-form">
        <div class="form-group">
          <label for="email">Email</label>
          <div class="input-wrapper">
            <span class="input-icon">✉️</span>
            <input 
              type="email" 
              id="email"
              v-model="form.email" 
              placeholder="seu@email.com"
              required
              autocomplete="email"
              :disabled="loading"
            >
          </div>
        </div>

        <div class="form-group">
          <label for="password">Senha</label>
          <div class="input-wrapper">
            <span class="input-icon">🔒</span>
            <input 
              type="password" 
              id="password"
              v-model="form.password" 
              placeholder="Digite sua senha"
              required
              autocomplete="current-password"
              :disabled="loading"
            >
          </div>
        </div>

        <div class="form-options">
          <div class="remember-me">
            <input type="checkbox" id="remember">
            <label for="remember">Lembrar-me</label>
          </div>
          <router-link to="/forgot-password" class="forgot-password">
            Esqueceu a senha?
          </router-link>
        </div>

        <button 
          type="submit" 
          class="btn-login"
          :disabled="loading"
          :class="{ 'loading': loading }"
        >
          <span v-if="loading" class="btn-loading">
            <span class="spinner"></span> Entrando...
          </span>
          <span v-else>Entrar no Sistema</span>
        </button>

        <div v-if="error" class="error-message">
          <span class="error-icon">⚠️</span>
          <span>{{ error }}</span>
        </div>
      </form>

      <!-- Rodapé -->
      <div class="login-footer">
        <p>Não tem uma conta?</p>
        <router-link to="/cadastro" class="btn-register">
          Criar Nova Conta
        </router-link>
        <div class="back-home">
          <router-link to="/" class="back-link">
            ← Voltar para Home
          </router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* Importação da fonte Poppins */
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
  font-family: 'Poppins', sans-serif;
}

.login-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #2c5530 0%, #4a7c59 100%);
  padding: 20px;
}

.login-card {
  width: 100%;
  max-width: 420px;
  background: white;
  border-radius: 12px;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.15);
  overflow: hidden;
  padding: 40px;
}

/* Cabeçalho */
.login-header {
  text-align: center;
  margin-bottom: 40px;
}

.logo {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 15px;
  margin-bottom: 10px;
}

.logo-icon {
  font-size: 40px;
}

.login-header h1 {
  color: #2c5530;
  font-size: 28px;
  font-weight: 600;
  letter-spacing: -0.5px;
}

.subtitle {
  color: #6b8e6a;
  font-size: 15px;
  font-weight: 400;
}

/* Formulário */
.login-form {
  margin-bottom: 30px;
}

.form-group {
  margin-bottom: 24px;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  color: #2c5530;
  font-weight: 500;
  font-size: 14px;
}

.input-wrapper {
  position: relative;
}

.input-icon {
  position: absolute;
  left: 16px;
  top: 50%;
  transform: translateY(-50%);
  font-size: 18px;
  color: #6b8e6a;
}

.form-group input {
  width: 100%;
  padding: 16px 16px 16px 50px;
  border: 2px solid #e0e6dc;
  border-radius: 8px;
  font-size: 15px;
  color: #333;
  background: #f8f9f7;
  transition: all 0.3s ease;
}

.form-group input:focus {
  outline: none;
  border-color: #2c5530;
  background: white;
  box-shadow: 0 0 0 3px rgba(44, 85, 48, 0.1);
}

.form-group input:disabled {
  background: #f1f3f0;
  cursor: not-allowed;
}

.form-options {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
  font-size: 14px;
}

.remember-me {
  display: flex;
  align-items: center;
  gap: 8px;
}

.remember-me input[type="checkbox"] {
  width: 18px;
  height: 18px;
  accent-color: #2c5530;
}

.remember-me label {
  color: #6b8e6a;
  cursor: pointer;
}

.forgot-password {
  color: #2c5530;
  text-decoration: none;
  font-weight: 500;
  transition: color 0.3s;
}

.forgot-password:hover {
  color: #4a7c59;
  text-decoration: underline;
}

/* Botão de Login */
.btn-login {
  width: 100%;
  padding: 16px;
  background: #2c5530;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.btn-login:hover:not(:disabled) {
  background: #3a6b3f;
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(44, 85, 48, 0.3);
}

.btn-login:active:not(:disabled) {
  transform: translateY(0);
}

.btn-login:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.btn-loading {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
}

.spinner {
  width: 18px;
  height: 18px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-radius: 50%;
  border-top-color: white;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

/* Mensagem de Erro */
.error-message {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-top: 20px;
  padding: 16px;
  background: #fdeaea;
  color: #c53030;
  border-radius: 8px;
  border: 1px solid #feb2b2;
  font-size: 14px;
  animation: fadeIn 0.3s;
}

.error-icon {
  font-size: 20px;
}

/* Rodapé */
.login-footer {
  text-align: center;
  padding-top: 25px;
  border-top: 1px solid #e8efe7;
}

.login-footer p {
  color: #6b8e6a;
  margin-bottom: 16px;
  font-size: 15px;
}

.btn-register {
  display: inline-block;
  padding: 14px 32px;
  background: #4a7c59;
  color: white;
  text-decoration: none;
  border-radius: 8px;
  font-weight: 600;
  transition: all 0.3s;
  margin-bottom: 20px;
}

.btn-register:hover {
  background: #3a6b3f;
  transform: translateY(-2px);
  box-shadow: 0 6px 15px rgba(74, 124, 89, 0.3);
}

.back-home {
  margin-top: 15px;
}

.back-link {
  color: #6b8e6a;
  text-decoration: none;
  font-size: 14px;
  transition: color 0.3s;
}

.back-link:hover {
  color: #2c5530;
  text-decoration: underline;
}

/* Animações */
@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

/* Responsividade */
@media (max-width: 480px) {
  .login-card {
    padding: 30px 25px;
  }
  
  .login-header h1 {
    font-size: 24px;
  }
  
  .logo {
    flex-direction: column;
    gap: 10px;
  }
  
  .logo-icon {
    font-size: 35px;
  }
  
  .form-options {
    flex-direction: column;
    align-items: flex-start;
    gap: 10px;
  }
}

@media (max-width: 360px) {
  .login-card {
    padding: 25px 20px;
  }
  
  .btn-register {
    padding: 12px 24px;
    font-size: 14px;
  }
}
</style>