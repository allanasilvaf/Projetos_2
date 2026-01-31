<script>
export default {
  data() {
    return {
      form: {
        email: '',
        password: ''
      },
      loading: false,
      error: '',
      showDemoCredentials: false // Adicione esta linha
    }
  },
  methods: {
async handleLogin() {
      this.loading = true;
      this.error = '';
      
      try {
        // 1. Conexão com a API
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
        
        // 2. Transforma a resposta em texto primeiro para debug
        const text = await response.text();
        console.log("Resposta bruta do servidor:", text);

        // Tenta converter para JSON
        let data;
        try {
            data = JSON.parse(text);
        } catch (e) {
            throw new Error("O servidor não retornou um JSON válido. Veja o console.");
        }
        
        // --- AQUI ESTAVA O PROBLEMA ---
        
        // CASO 1: Erro crítico do Banco (ex: senha errada no database.php)
        if (data.error) {
          this.error = data.error;
          alert("ERRO DE SISTEMA: " + data.error); // Usamos alert em vez de toast
          return;
        }

        // CASO 2: Login Sucesso
        if (data.success) {
          localStorage.setItem('user', JSON.stringify(data.user));
          localStorage.setItem('token', 'fake_token_' + Date.now());
          
          // Redireciona
          this.redirectUser(data.user.tipo);
          
        } else {
          // CASO 3: Senha ou Email incorretos (Lógica de negócio)
          this.error = data.message || 'Email ou senha incorretos';
          alert("Atenção: " + this.error); // Usamos alert em vez de toast
        }
        
      } catch (error) {
        console.error('Erro completo:', error);
        this.error = 'Erro de conexão ou servidor';
        alert("Erro técnico: " + error.message); // Usamos alert em vez de toast
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
  },
  mounted() {
    // REMOVA estas linhas que preenchem automaticamente:
    // this.form.email = 'professor@faculdade.edu';
    // this.form.password = '123456';
  }
}
</script>

<template>
  <div class="login-container">
    <h2>🔐 Login GAM</h2>
    
    <form @submit.prevent="handleLogin">
      <div class="form-group">
        <label>Email:</label>
        <input 
          type="email" 
          v-model="form.email" 
          placeholder="seu@email.com"
          required
          autocomplete="email"
        >
      </div>
      
      <div class="form-group">
        <label>Senha:</label>
        <input 
          type="password" 
          v-model="form.password" 
          placeholder="Digite sua senha"
          required
          autocomplete="current-password"
        >
      </div>
      
      <div class="form-footer">
        <router-link to="/forgot-password" class="forgot-password">
          Esqueceu a senha?
        </router-link>
      </div>
      
      <button type="submit" :disabled="loading" class="btn-primary">
        {{ loading ? 'Entrando...' : 'Entrar' }}
      </button>
      
      <div v-if="error" class="error-message">
        {{ error }}
      </div>
      
      <!-- Botão para mostrar credenciais de teste (opcional) -->
      <div class="demo-section">
        <button 
          type="button" 
          @click="showDemoCredentials = !showDemoCredentials"
          class="btn-secondary"
        >
          {{ showDemoCredentials ? 'Ocultar' : 'Mostrar' }} credenciais de teste
        </button>
        
        <div v-if="showDemoCredentials" class="demo-credentials">
          <p><small><strong>Atenção:</strong> Apenas para desenvolvimento</small></p>
          <p><small>👨‍🏫 Professor: professor@faculdade.edu | prof123</small></p>
          <p><small>👨‍🎓 Aluno: aluno@faculdade.edu | aluno123</small></p>
          <p><small>👑 Admin: admin@faculdade.edu | admin123</small></p>
        </div>
      </div>
    </form>
    
    <div class="cadastro-section">
      <p>Não tem uma conta?</p>
      <router-link to="/cadastro" class="btn-register">
        Cadastre-se aqui
      </router-link>
    </div>
    
    <router-link to="/" class="back-link">
      ← Voltar para Home
    </router-link>
  </div>
</template>

<style scoped>
.login-container {
  max-width: 400px;
  margin: 50px auto;
  padding: 30px;
  background: #f8f9fa;
  border-radius: 10px;
  box-shadow: 0 4px 6px rgba(0,0,0,0.1);
}

.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  margin-bottom: 5px;
  font-weight: 600;
  color: #333;
}

.form-group input {
  width: 100%;
  padding: 12px;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 16px;
  transition: border-color 0.3s;
}

.form-group input:focus {
  outline: none;
  border-color: #42b983;
  box-shadow: 0 0 0 2px rgba(66, 185, 131, 0.1);
}

.form-footer {
  display: flex;
  justify-content: flex-end;
  margin-bottom: 20px;
}

.forgot-password {
  font-size: 14px;
  color: #666;
  text-decoration: none;
}

.forgot-password:hover {
  color: #42b983;
  text-decoration: underline;
}

.btn-primary {
  width: 100%;
  padding: 14px;
  background: #42b983;
  color: white;
  border: none;
  border-radius: 6px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.3s, transform 0.1s;
}

.btn-primary:hover:not(:disabled) {
  background: #3aa876;
  transform: translateY(-1px);
}

.btn-primary:active:not(:disabled) {
  transform: translateY(0);
}

.btn-primary:disabled {
  background: #ccc;
  cursor: not-allowed;
}

.btn-secondary {
  width: 100%;
  padding: 10px;
  background: #e9ecef;
  color: #666;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 14px;
  cursor: pointer;
  margin-top: 15px;
  transition: background 0.3s;
}

.btn-secondary:hover {
  background: #dee2e6;
}

.error-message {
  margin-top: 15px;
  padding: 12px;
  background: #ffebee;
  color: #c62828;
  border-radius: 6px;
  font-size: 14px;
}

.demo-section {
  margin-top: 20px;
}

.demo-credentials {
  margin-top: 10px;
  padding: 15px;
  background: #fff3cd;
  border: 1px solid #ffeaa7;
  border-radius: 6px;
  font-size: 12px;
  color: #856404;
}

.demo-credentials p {
  margin: 5px 0;
}

.cadastro-section {
  margin-top: 25px;
  padding-top: 20px;
  border-top: 1px solid #eee;
  text-align: center;
}

.cadastro-section p {
  margin-bottom: 10px;
  color: #666;
}

.btn-cadastro {
  display: inline-block;
  padding: 10px 20px;
  background: #3498db;
  color: white;
  border-radius: 6px;
  text-decoration: none;
  font-weight: 600;
  transition: background 0.3s;
}

.btn-cadastro:hover {
  background: #2980b9;
}

.back-link {
  display: block;
  margin-top: 20px;
  text-align: center;
  color: #666;
  text-decoration: none;
  font-size: 14px;
}

.back-link:hover {
  color: #42b983;
  text-decoration: underline;
}
</style>