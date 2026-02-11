<template>
  <div class="login-container">
    <div class="login-card">
      <div class="login-header">
        <div class="logo">
          <h1>Login</h1>
          <p class="subtitle">Bem-vindo de volta! Acesse sua conta.</p>
        </div>
      </div>

      <div v-if="error" class="error-message">
        <span class="status-icon">⚠️</span>
        <span>{{ error }}</span>
      </div>

      <form @submit.prevent="handleLogin" class="login-form">
        <div class="form-stack">
          <div class="form-group">
            <label for="email">Email</label>
            <div class="input-wrapper">
              <svg class="input-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" d="M3 8l7.89 4.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
              </svg>
              <input 
                type="email" 
                id="email" 
                v-model="form.email" 
                placeholder="seu@email.com" 
                required 
                :disabled="loading"
              >
            </div>
          </div>

          <div class="form-group">
            <label for="password">Senha</label>
            <div class="input-wrapper">
              <svg class="input-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
              </svg>
              <input 
                type="password" 
                id="password" 
                v-model="form.password" 
                placeholder="Sua senha" 
                required 
                :disabled="loading"
              >
            </div>
          </div>
        </div>

        <div class="form-options">
          <router-link to="/Forgotpassword" class="forgot-password">
            Esqueceu a senha?
          </router-link>
        </div>

        <button type="submit" :disabled="loading" class="btn-primary" :class="{ 'loading': loading }">
          <span v-if="loading" class="btn-loading">
            <span class="spinner"></span> Autenticando...
          </span>
          <span v-else>Entrar</span>
        </button>
      </form>

      <div class="login-footer">
        <p>Ainda não tem uma conta?</p>
        <router-link to="/cadastro" class="btn-secondary">
          Cadastrar
        </router-link>
        <div class="back-home">
          <router-link to="/" class="back-link">
            ← Voltar para a Página Inicial
          </router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'LoginPage',
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
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ email: this.form.email, senha: this.form.password })
        });
        const data = await response.json();
        if (data.success) {
          localStorage.setItem('user', JSON.stringify(data.usuario));
          this.redirectUser(data.usuario.tipo);
        } else {
          this.error = data.message || 'Credenciais inválidas';
        }
      } catch (error) {
        this.error = 'Erro na comunicação com o servidor.';
      } finally {
        this.loading = false;
      }
    },
    redirectUser(tipo) {
      const routes = { 'professor': '/professor/dashboard', 'admin': '/admin/dashboard' };
      this.$router.push(routes[tipo] || '/ajustes');
    }
  }
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');

.login-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #2c5530 0%, #4a7c59 50%, #2c5530 100%);
  background-size: 200% 200%;
  animation: gradientAnimation 8s ease infinite;
  padding: 20px;
  font-family: 'Poppins', sans-serif;
}

@keyframes gradientAnimation {
  0% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
  100% { background-position: 0% 50%; }
}

.login-card {
  width: 100%;
  max-width: 750px; /* MESMA LARGURA DO CADASTRO */
  background: white;
  border-radius: 20px;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2);
  padding: 40px;
}

.login-header {
  text-align: center;
  margin-bottom: 30px;
}

.login-header h1 {
  color: #2c5530;
  font-size: 32px;
  font-weight: 600;
}

.subtitle {
  color: #6b8e6a;
  font-size: 15px;
}

.form-stack {
  display: flex;
  flex-direction: column;
  gap: 20px;
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  color: #2c5530;
  font-weight: 500;
  font-size: 14px;
  text-align: left;
}

.input-wrapper {
  position: relative;
}

.input-icon {
  position: absolute;
  left: 14px;
  top: 50%;
  transform: translateY(-50%);
  width: 20px;
  height: 20px;
  color: #6b8e6a;
}

.form-group input {
  width: 100%;
  padding: 14px 14px 14px 45px;
  border: 2px solid #e0e6dc;
  border-radius: 10px;
  font-size: 15px;
  background: #f8f9f7;
  transition: all 0.3s;
}

.form-group input:focus {
  outline: none;
  border-color: #2c5530;
  background: white;
  box-shadow: 0 0 0 3px rgba(44, 85, 48, 0.1);
}

.form-options {
  display: flex;
  justify-content: flex-end;
  margin-bottom: 25px;
}

.forgot-password {
  font-size: 13px;
  color: #4a7c59;
  text-decoration: none;
  font-weight: 500;
}

.btn-primary {
  width: 100%;
  padding: 16px;
  background: linear-gradient(135deg, #2c5530 0%, #4a7c59 100%);
  color: white;
  border: none;
  border-radius: 12px;
  font-size: 18px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
}

.btn-primary:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(44, 85, 48, 0.3);
}

.error-message {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 16px;
  background: #fdeaea;
  color: #c53030;
  border: 1px solid #feb2b2;
  border-radius: 10px;
  margin-bottom: 20px;
}

.login-footer {
  text-align: center;
  margin-top: 35px;
  padding-top: 25px;
  border-top: 1px solid #f0f0f0;
}

.login-footer p {
  color: #6b8e6a;
  margin-bottom: 15px;
}

.btn-secondary {
  display: inline-block;
  padding: 12px 30px;
  background: #4a7c59;
  color: white;
  text-decoration: none;
  border-radius: 8px;
  font-weight: 600;
  transition: 0.3s;
}

.back-link {
  display: block;
  margin-top: 20px;
  color: #6b8e6a;
  text-decoration: none;
  font-size: 14px;
}

.spinner {
  width: 18px;
  height: 18px;
  border: 2px solid rgba(255,255,255,0.3);
  border-radius: 50%;
  border-top-color: white;
  animation: spin 0.8s linear infinite;
  display: inline-block;
}

@keyframes spin { to { transform: rotate(360deg); } }
</style>