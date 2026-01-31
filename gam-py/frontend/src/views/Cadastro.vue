<template>
  <div class="cadastro-container">
    <div class="cadastro-card">
      <div class="cadastro-header">
        <h1>📝 Cadastro</h1>
        <p class="subtitle">Crie sua conta no sistema</p>
      </div>
      
      <!-- Mensagens de status -->
      <div v-if="success" class="success-message">
        <p>✅ {{ successMessage }}</p>
        <p>Redirecionando para login...</p>
      </div>
      
      <div v-if="error" class="error-message">
        <p>⚠️ {{ error }}</p>
      </div>
      
      <form v-if="!success" @submit.prevent="handleCadastro" class="cadastro-form">
        <div class="form-group">
          <label for="nome">Nome completo *</label>
          <input 
            type="text" 
            id="nome"
            v-model="form.nome" 
            placeholder="Digite seu nome"
            required
            :disabled="loading"
          >
        </div>
        
        <div class="form-group">
          <label for="email">Email *</label>
          <input 
            type="email" 
            id="email"
            v-model="form.email" 
            placeholder="seu@email.com"
            required
            :disabled="loading"
          >
        </div>
        
        <div class="form-group">
          <label for="cpf">CPF *</label>
          <input 
            type="text" 
            id="cpf"
            v-model="form.cpf" 
            placeholder="000.000.000-00"
            required
            @input="formatarCPF"
            :disabled="loading"
          >
        </div>
        
        <div class="form-group">
          <label for="senha">Senha *</label>
          <input 
            type="password" 
            id="senha"
            v-model="form.senha" 
            placeholder="Mínimo 6 caracteres"
            required
            minlength="6"
            :disabled="loading"
          >
        </div>
        
        <div class="form-group">
          <label for="tipo">Tipo de usuário *</label>
          <select 
            id="tipo"
            v-model="form.tipo"
            required
            :disabled="loading"
          >
            <option value="estudante">Estudante</option>
            <option value="professor">Professor</option>
            <option value="admin">Administrador</option>
          </select>
        </div>
        
        <div v-if="form.tipo === 'estudante'" class="form-group">
          <label for="curso_id">Curso *</label>
          <select 
            id="curso_id"
            v-model="form.curso_id"
            :required="form.tipo === 'estudante'"
            :disabled="loading"
          >
            <option value="">Selecione um curso</option>
            <option value="1">Engenharia de Computação</option>
            <option value="2">Ciência da Computação</option>
            <option value="3">Sistemas de Informação</option>
            <option value="4">Engenharia de Software</option>
          </select>
        </div>
        
        <div class="form-group">
          <label for="telefone">Telefone</label>
          <input 
            type="tel" 
            id="telefone"
            v-model="form.telefone" 
            placeholder="(11) 99999-9999"
            @input="formatarTelefone"
            :disabled="loading"
          >
        </div>
        
        <button type="submit" :disabled="loading" class="btn-primary">
          {{ loading ? 'Cadastrando...' : 'Cadastrar' }}
        </button>
      </form>
      
      <div class="login-link">
        <p>Já tem uma conta?</p>
        <router-link to="/login" class="btn-login">
          Faça login aqui
        </router-link>
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
        data_nascimento: '',
        sobrenome: '',
        curso_id: ''
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
      
      if (cpf.length <= 3) {
        this.form.cpf = cpf
      } else if (cpf.length <= 6) {
        this.form.cpf = cpf.substring(0,3) + '.' + cpf.substring(3)
      } else if (cpf.length <= 9) {
        this.form.cpf = cpf.substring(0,3) + '.' + cpf.substring(3,6) + '.' + cpf.substring(6)
      } else {
        this.form.cpf = cpf.substring(0,3) + '.' + cpf.substring(3,6) + '.' + cpf.substring(6,9) + '-' + cpf.substring(9)
      }
    },
    
    formatarTelefone() {
      let telefone = this.form.telefone.replace(/\D/g, '')
      if (telefone.length > 11) telefone = telefone.substring(0, 11)
      
      if (telefone.length === 11) {
        this.form.telefone = '(' + telefone.substring(0,2) + ') ' + telefone.substring(2,7) + '-' + telefone.substring(7)
      } else if (telefone.length === 10) {
        this.form.telefone = '(' + telefone.substring(0,2) + ') ' + telefone.substring(2,6) + '-' + telefone.substring(6)
      } else {
        this.form.telefone = telefone
      }
    },
    
    async handleCadastro() {
      this.loading = true
      this.error = ''
      this.success = false
      
      try {
        // Validações básicas
        if (this.form.senha.length < 6) {
          throw new Error('A senha deve ter no mínimo 6 caracteres')
        }
        
        if (this.form.cpf.replace(/\D/g, '').length !== 11) {
          throw new Error('CPF inválido. Digite 11 números.')
        }
        
        if (this.form.tipo === 'estudante' && !this.form.curso_id) {
          throw new Error('Selecione um curso para estudantes')
        }
        
        // Preparar dados para envio
        const dadosCadastro = {
          nome: this.form.nome.trim(),
          sobrenome: this.form.sobrenome.trim(),
          email: this.form.email.trim(),
          cpf: this.form.cpf.replace(/\D/g, ''),
          senha: this.form.senha,
          tipo: this.form.tipo,
          telefone: this.form.telefone.replace(/\D/g, ''),
          data_nascimento: this.form.data_nascimento || null
        }
        
        // Adicionar curso_id apenas para estudantes
        if (this.form.tipo === 'estudante' && this.form.curso_id) {
          dadosCadastro.curso_id = parseInt(this.form.curso_id)
        }
        
        console.log('Enviando dados para cadastro:', dadosCadastro)
        
        // AJUSTE A URL CONFORME SUA CONFIGURAÇÃO!
        // Seu backend está em http://localhost:9000/ ou http://localhost/backend/?
        const response = await fetch('http://localhost:9000/api/cadastro.php', {
          method: 'POST',
          headers: { 
            'Content-Type': 'application/json',
            'Accept': 'application/json'
          },
          body: JSON.stringify(dadosCadastro)
        })
        
        const data = await response.json()
        console.log('Resposta da API:', data)
        
        if (data.success) {
          this.success = true
          this.successMessage = data.message
          
          // Redirecionar para login após 3 segundos
          setTimeout(() => {
            this.$router.push('/login')
          }, 3000)
          
        } else {
          throw new Error(data.message || 'Erro ao cadastrar usuário')
        }
        
      } catch (error) {
        console.error('Erro no cadastro:', error)
        this.error = error.message
      } finally {
        this.loading = false
      }
    }
  }
}
</script>

<style scoped>
.cadastro-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #2c5530 0%, #4a7c59 100%);
  padding: 20px;
}

.cadastro-card {
  width: 100%;
  max-width: 500px;
  background: white;
  border-radius: 12px;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.15);
  overflow: hidden;
  padding: 40px;
}

.cadastro-header {
  text-align: center;
  margin-bottom: 30px;
}

.cadastro-header h1 {
  color: #2c5530;
  font-size: 28px;
  font-weight: 600;
  margin-bottom: 10px;
}

.subtitle {
  color: #6b8e6a;
  font-size: 15px;
}

.success-message {
  background: #d4edda;
  color: #155724;
  padding: 15px;
  border-radius: 8px;
  margin-bottom: 20px;
  text-align: center;
}

.error-message {
  background: #f8d7da;
  color: #721c24;
  padding: 15px;
  border-radius: 8px;
  margin-bottom: 20px;
  text-align: center;
}

.cadastro-form {
  margin-bottom: 30px;
}

.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  color: #2c5530;
  font-weight: 500;
  font-size: 14px;
}

.form-group input,
.form-group select {
  width: 100%;
  padding: 14px;
  border: 2px solid #e0e6dc;
  border-radius: 8px;
  font-size: 15px;
  color: #333;
  background: #f8f9f7;
  transition: all 0.3s ease;
}

.form-group input:focus,
.form-group select:focus {
  outline: none;
  border-color: #2c5530;
  background: white;
  box-shadow: 0 0 0 3px rgba(44, 85, 48, 0.1);
}

.form-group input:disabled,
.form-group select:disabled {
  background: #f0f0f0;
  cursor: not-allowed;
}

.btn-primary {
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
  margin-top: 10px;
}

.btn-primary:hover:not(:disabled) {
  background: #3a6b3f;
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(44, 85, 48, 0.3);
}

.btn-primary:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.login-link {
  text-align: center;
  padding-top: 20px;
  border-top: 1px solid #e8efe7;
}

.login-link p {
  color: #6b8e6a;
  margin-bottom: 12px;
}

.btn-login {
  display: inline-block;
  padding: 12px 24px;
  background: #4a7c59;
  color: white;
  text-decoration: none;
  border-radius: 8px;
  font-weight: 600;
  transition: all 0.3s;
}

.btn-login:hover {
  background: #3a6b3f;
  transform: translateY(-2px);
  box-shadow: 0 6px 15px rgba(74, 124, 89, 0.3);
}

@media (max-width: 480px) {
  .cadastro-card {
    padding: 30px 25px;
  }
}
</style>