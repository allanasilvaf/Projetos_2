<template>
  <div class="forgot-container">
    <div class="forgot-card">
      <div class="forgot-header">
        <div class="logo">
          <h1>Recuperação de Acesso</h1>
          <p class="subtitle" v-if="step === 1">Valide sua identidade com os dados cadastrados.</p>
          <p class="subtitle" v-else>Crie uma nova senha de acesso para sua conta.</p>
        </div>
      </div>

      <div v-if="error" class="error-message">
        <span class="status-icon">⚠️</span>
        <span>{{ error }}</span>
      </div>

      <div v-if="success" class="success-message">
        <span class="status-icon">✅</span>
        <span>Senha atualizada com sucesso! Redirecionando...</span>
      </div>

      <form v-if="!success" @submit.prevent="handleFormAction" class="forgot-form">
        
        <div class="form-grid">
          <template v-if="step === 1">
            <div class="form-group">
              <label for="email">E-mail Cadastrado *</label>
              <div class="input-wrapper">
                <svg class="input-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" d="M3 8l7.89 4.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                </svg>
                <input type="email" id="email" v-model="form.email" placeholder="seu@email.com" required :disabled="loading">
              </div>
            </div>

            <div class="form-group">
              <label for="cpf">CPF para Validação *</label>
              <div class="input-wrapper">
                <svg class="input-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" d="M10 6H5a2 2 0 00-2 2v9a2 2 0 002 2h14a2 2 0 002-2V8a2 2 0 00-2-2h-5m-4 0V5a2 2 0 114 0v1" />
                </svg>
                <input type="text" id="cpf" v-model="form.cpf" placeholder="000.000.000-00" required @input="formatarCPF" :disabled="loading">
              </div>
            </div>
          </template>

          <template v-else>
            <div class="form-group">
              <label for="novaSenha">Nova Senha *</label>
              <div class="input-wrapper">
                <svg class="input-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
                </svg>
                <input type="password" id="novaSenha" v-model="form.novaSenha" placeholder="Mínimo 6 caracteres" required minlength="6">
              </div>
            </div>

            <div class="form-group">
              <label for="confirmarSenha">Confirmar Nova Senha *</label>
              <div class="input-wrapper">
                <svg class="input-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                <input type="password" id="confirmarSenha" v-model="form.confirmarSenha" placeholder="Repita a nova senha" required>
              </div>
            </div>
          </template>
        </div>

        <button type="submit" :disabled="loading" class="btn-primary" :class="{ 'loading': loading }">
          <span v-if="loading" class="spinner"></span>
          <span>{{ step === 1 ? 'Validar Identidade' : 'Redefinir Senha' }}</span>
        </button>
      </form>

      <div class="forgot-footer">
        <router-link to="/login" class="back-link">
          ← Voltar para o Login
        </router-link>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Forgotpassword',
  data() {
    return {
      step: 1, // 1 = Validar, 2 = Trocar Senha
      form: {
        email: '',
        cpf: '',
        novaSenha: '',
        confirmarSenha: ''
      },
      loading: false,
      error: '',
      success: false
    }
  },
  methods: {
    formatarCPF() {
      let cpf = this.form.cpf.replace(/\D/g, '')
      if (cpf.length > 11) cpf = cpf.substring(0, 11)
      if (cpf.length <= 3) this.form.cpf = cpf
      else if (cpf.length <= 6) this.form.cpf = cpf.substring(0,3) + '.' + cpf.substring(3)
      else if (cpf.length <= 9) this.form.cpf = cpf.substring(0,3) + '.' + cpf.substring(3,6) + '.' + cpf.substring(6)
      else this.form.cpf = cpf.substring(0,3) + '.' + cpf.substring(3,6) + '.' + cpf.substring(6,9) + '-' + cpf.substring(9)
    },
    async handleFormAction() {
      this.loading = true;
      this.error = '';

      try {
        if (this.step === 1) {
          const response = await fetch('http://localhost:9000/api/validasenha.php', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ 
              email: this.form.email, 
              cpf: this.form.cpf.replace(/\D/g, '') 
            })
          });
          const data = await response.json();
          
          if (data.success) {
            this.step = 2;
          } else {
            this.error = data.message || 'Dados não conferem com nossos registros.';
          }
        } else {
          if (this.form.novaSenha !== this.form.confirmarSenha) {
            this.error = "As senhas não coincidem!";
            this.loading = false;
            return;
          }

          const response = await fetch('http://localhost:9000/api/redefinirsenha.php', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ 
              email: this.form.email, 
              novaSenha: this.form.novaSenha 
            })
          });
          const data = await response.json();

          if (data.success) {
            this.success = true;
            setTimeout(() => this.$router.push('/login'), 3000);
          } else {
            this.error = data.message || 'Erro ao atualizar senha.';
          }
        }
      } catch (e) {
        this.error = 'Erro de comunicação com o servidor.';
        console.error(e);
      } finally {
        this.loading = false;
      }
    }
  }
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');

.forgot-container {
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

.forgot-card {
  width: 100%;
  max-width: 750px; /* LARGURA PADRONIZADA COM LOGIN/CADASTRO */
  background: white;
  border-radius: 20px;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2);
  padding: 40px;
}

.forgot-header {
  text-align: center;
  margin-bottom: 30px;
}

.forgot-header h1 {
  color: #2c5530;
  font-size: 28px;
  font-weight: 600;
}

.subtitle {
  color: #6b8e6a;
  font-size: 15px;
}

.form-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 24px;
  margin-bottom: 25px;
}

@media (max-width: 600px) {
  .form-grid { grid-template-columns: 1fr; }
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  color: #2c5530;
  font-weight: 500;
  font-size: 14px;
  text-align: left;
}

.input-wrapper { position: relative; }

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
  box-shadow: 0 0 0 3px rgba(44, 85, 48, 0.1);
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
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 10px;
}

.error-message, .success-message {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 16px;
  border-radius: 10px;
  margin-bottom: 20px;
  font-size: 14px;
}

.error-message { background: #fdeaea; color: #c53030; border: 1px solid #feb2b2; }
.success-message { background: #e6f4ea; color: #1e7e34; border: 1px solid #b7e1cd; }

.forgot-footer {
  text-align: center;
  margin-top: 30px;
  padding-top: 20px;
  border-top: 1px solid #f0f0f0;
}

.back-link {
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
}

@keyframes spin { to { transform: rotate(360deg); } }
</style>