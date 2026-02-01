<template>
  <div class="cadastro-container">
    <div class="cadastro-card">
      <div class="cadastro-header">
        <div class="logo">
          <h1>Cadastro</h1>
          <p class="subtitle">Complete seus dados para acessar o sistema</p>
        </div>
      </div>

      <div v-if="success" class="success-message">
        <span class="status-icon">✅</span>
        <div>
          <strong>{{ successMessage }}</strong>
          <p>Redirecionando para o login...</p>
        </div>
      </div>

      <div v-if="error" class="error-message">
        <span class="status-icon">⚠️</span>
        <span>{{ error }}</span>
      </div>

      <form v-if="!success" @submit.prevent="handleCadastro" class="cadastro-form">
        
        <div class="form-grid">
          <div class="form-group">
            <label for="nome">Nome completo *</label>
            <div class="input-wrapper">
              <svg class="input-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
              </svg>
              <input type="text" id="nome" v-model="form.nome" placeholder="Seu nome" required :disabled="loading">
            </div>
          </div>

          <div class="form-group">
            <label for="email">Email *</label>
            <div class="input-wrapper">
              <svg class="input-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" d="M3 8l7.89 4.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
              </svg>
              <input type="email" id="email" v-model="form.email" placeholder="seu@email.com" required :disabled="loading">
            </div>
          </div>

          <div class="form-group">
            <label for="cpf">CPF *</label>
            <div class="input-wrapper">
              <svg class="input-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" d="M10 6H5a2 2 0 00-2 2v9a2 2 0 002 2h14a2 2 0 002-2V8a2 2 0 00-2-2h-5m-4 0V5a2 2 0 114 0v1m-4 0a2 2 0 104 0m-5 8a2 2 0 100-4 2 2 0 000 4zm0 0c1.306 0 2.417.835 2.83 2M9 14a3.001 3.001 0 00-2.83 2M15 11h3m-3 4h2" />
              </svg>
              <input type="text" id="cpf" v-model="form.cpf" placeholder="000.000.000-00" required @input="formatarCPF" :disabled="loading">
            </div>
          </div>

          <div class="form-group">
            <label for="telefone">Telefone</label>
            <div class="input-wrapper">
              <svg class="input-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z" />
              </svg>
              <input type="tel" id="telefone" v-model="form.telefone" placeholder="(00) 00000-0000" @input="formatarTelefone" :disabled="loading">
            </div>
          </div>

          <div class="form-group">
            <label for="curso_id">Curso *</label>
            <div class="input-wrapper">
              <svg class="input-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" d="M12 14l9-5-9-5-9 5 9 5z" />
                <path stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" d="M12 14l6.16-3.422a12.083 12.083 0 01.665 6.479A11.952 11.952 0 0012 20.055a11.952 11.952 0 00-6.824-2.998 12.078 12.078 0 01.665-6.479L12 14z" />
              </svg>
              <select id="curso_id" v-model="form.curso_id" required :disabled="loading">
                <option value="" disabled>Selecione um curso</option>
                <option value="1">Engenharia de Computação</option>
              </select>
            </div>
          </div>

          <div class="form-group">
            <label for="senha">Senha *</label>
            <div class="input-wrapper">
              <svg class="input-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
              </svg>
              <input type="password" id="senha" v-model="form.senha" placeholder="Mínimo 6 caracteres" required minlength="6" :disabled="loading">
            </div>
          </div>
        </div>

        <button type="submit" :disabled="loading" class="btn-primary" :class="{ 'loading': loading }">
          <span v-if="loading" class="btn-loading">
            <span class="spinner"></span> Cadastrando...
          </span>
          <span v-else>Finalizar Cadastro</span>
        </button>
      </form>

      <div class="cadastro-footer">
        <p>Já possui uma conta?</p>
        <router-link to="/login" class="btn-secondary">
          Fazer Login
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

<script>
export default {
  name: 'CadastroPage',
  data() {
    return {
      form: {
        nome: '',
        email: '',
        senha: '',
        cpf: '',
        tipo: 'estudante',
        telefone: '',
        curso_id: '' // Inicia vazio para forçar o usuário a abrir o select
      },
      loading: false,
      error: '',
      success: false,
      successMessage: ''
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
    formatarTelefone() {
      let telefone = this.form.telefone.replace(/\D/g, '')
      if (telefone.length > 11) telefone = telefone.substring(0, 11)
      if (telefone.length === 11) this.form.telefone = '(' + telefone.substring(0,2) + ') ' + telefone.substring(2,7) + '-' + telefone.substring(7)
      else if (telefone.length === 10) this.form.telefone = '(' + telefone.substring(0,2) + ') ' + telefone.substring(2,6) + '-' + telefone.substring(6)
      else this.form.telefone = telefone
    },
    async handleCadastro() {
      this.loading = true; 
      this.error = '';
      try {
        if (!this.form.curso_id) throw new Error('Por favor, selecione seu curso')

        const dadosCadastro = {
          nome: this.form.nome.trim(),
          email: this.form.email.trim(),
          cpf: this.form.cpf.replace(/\D/g, ''),
          senha: this.form.senha,
          tipo: 'estudante', 
          telefone: this.form.telefone.replace(/\D/g, ''),
          curso_id: parseInt(this.form.curso_id)
        }

        const response = await fetch('http://localhost:9000/api/cadastro.php', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(dadosCadastro)
        })
        
        const data = await response.json()
        if (data.success) {
          this.success = true;
          this.successMessage = data.message;
          setTimeout(() => this.$router.push('/login'), 3000)
        } else {
          throw new Error(data.message || 'Erro ao realizar cadastro')
        }
      } catch (error) {
        this.error = error.message
      } finally {
        this.loading = false
      }
    }
  }
}
</script>

<style scoped>
/* Importação da Poppins para manter o padrão */
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
  font-family: 'Poppins', sans-serif;
}

.cadastro-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #2c5530 0%, #4a7c59 50%, #2c5530 100%);
  background-size: 200% 200%;
  animation: gradientAnimation 8s ease infinite;
  padding: 20px;
}

@keyframes gradientAnimation {
  0% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
  100% { background-position: 0% 50%; }
}

.cadastro-card {
  width: 100%;
  max-width: 750px;
  background: white;
  border-radius: 20px;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2);
  padding: 40px;
}

.cadastro-header {
  text-align: center;
  margin-bottom: 30px;
}

.cadastro-header h1 {
  color: #2c5530;
  font-size: 32px;
  font-weight: 600;
  margin-bottom: 5px;
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
  .form-grid {
    grid-template-columns: 1fr;
  }
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
  left: 14px;
  top: 50%;
  transform: translateY(-50%);
  width: 20px;
  height: 20px;
  color: #6b8e6a;
  stroke-width: 1.5;
}

.form-group input, .form-group select {
  width: 100%;
  padding: 14px 14px 14px 45px;
  border: 2px solid #e0e6dc;
  border-radius: 10px;
  font-size: 15px;
  background: #f8f9f7;
  transition: all 0.3s;
  color: #333;
}

.form-group input:focus, .form-group select:focus {
  outline: none;
  border-color: #2c5530;
  background: white;
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
  transition: all 0.3s;
  margin-top: 10px;
}

.btn-primary:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(44, 85, 48, 0.3);
}

.success-message, .error-message {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 16px;
  border-radius: 10px;
  margin-bottom: 20px;
}

.success-message { background: #e6f4ea; color: #1e7e34; border: 1px solid #b7e1cd; }
.error-message { background: #fdeaea; color: #c53030; border: 1px solid #feb2b2; }

.cadastro-footer {
  text-align: center;
  margin-top: 35px;
  padding-top: 25px;
  color: #6b8e6a;
  border-top: 1px solid #f0f0f0;
}

.btn-secondary {
  display: inline-block;
  margin-top: 12px;
  padding: 12px 30px;
  background: #4a7c59;
  color: white;
  text-decoration: none;
  border-radius: 8px;
  font-weight: 600;
  transition: 0.3s;
}

.btn-secondary:hover { 
  background: #3a6b3f; 
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(74, 124, 89, 0.3);
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