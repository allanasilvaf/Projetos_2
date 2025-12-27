<script>
export default {
  data() {
    return {
      form: {
        nome: '',
        sobrenome: '',
        email: '',
        cpf: '',
        senha: '',
        confirmarSenha: '',
        tipo: 'estudante',
        telefone: '',
        data_nascimento: '',
        curso_id: ''
      },
      loading: false,
      error: '',
      cursos: [] // Para carregar cursos do banco
    }
  },
  async mounted() {
    // Carregar cursos disponíveis
    await this.loadCursos();
  },
  methods: {
    async loadCursos() {
      try {
        const response = await fetch('http://localhost:8000/api/cursos.php');
        if (response.ok) {
          this.cursos = await response.json();
        }
      } catch (error) {
        console.error('Erro ao carregar cursos:', error);
      }
    },
    
    async handleCadastro() {
      // Validações
      if (this.form.senha !== this.form.confirmarSenha) {
        this.error = 'As senhas não conferem!';
        return;
      }
      
      if (this.form.senha.length < 6) {
        this.error = 'A senha deve ter no mínimo 6 caracteres';
        return;
      }
      
      this.loading = true;
      this.error = '';
      
      try {
        const response = await fetch('http://localhost:8000/api/register.php', {
          method: 'POST',
          headers: { 
            'Content-Type': 'application/json',
            'Accept': 'application/json'
          },
          body: JSON.stringify(this.form)
        });
        
        const data = await response.json();
        
        if (data.success) {
          this.$toast.success('Cadastro realizado com sucesso!', {
            position: 'top-right',
            duration: 3000
          });
          
          // Redirecionar para login após 2 segundos
          setTimeout(() => {
            this.$router.push('/login');
          }, 2000);
        } else {
          this.error = data.message || 'Erro no cadastro';
          this.$toast.error(this.error);
        }
        
      } catch (error) {
        console.error('Erro:', error);
        this.error = 'Erro de conexão com o servidor';
      } finally {
        this.loading = false;
      }
    },
    
    formatCPF() {
      // Formatar CPF automaticamente: 000.000.000-00
      let cpf = this.form.cpf.replace(/\D/g, '');
      if (cpf.length > 3) cpf = cpf.substring(0,3) + '.' + cpf.substring(3);
      if (cpf.length > 7) cpf = cpf.substring(0,7) + '.' + cpf.substring(7);
      if (cpf.length > 11) cpf = cpf.substring(0,11) + '-' + cpf.substring(11,13);
      this.form.cpf = cpf.substring(0,14);
    },
    
    formatTelefone() {
      // Formatar telefone: (00) 00000-0000
      let tel = this.form.telefone.replace(/\D/g, '');
      if (tel.length > 0) tel = '(' + tel.substring(0,2) + ') ' + tel.substring(2);
      if (tel.length > 10) tel = tel.substring(0,10) + '-' + tel.substring(10);
      this.form.telefone = tel.substring(0,15);
    }
  }
}
</script>

<template>
  <div class="cadastro-container">
    <h2>📝 Cadastro de Novo Usuário</h2>
    
    <form @submit.prevent="handleRegister">
      <div class="form-row">
        <div class="form-group">
          <label>Nome *</label>
          <input 
            type="text" 
            v-model="form.nome" 
            placeholder="Digite seu nome"
            required
          >
        </div>
        
        <div class="form-group">
          <label>Sobrenome *</label>
          <input 
            type="text" 
            v-model="form.sobrenome" 
            placeholder="Digite seu sobrenome"
            required
          >
        </div>
      </div>
      
      <div class="form-row">
        <div class="form-group">
          <label>Email *</label>
          <input 
            type="email" 
            v-model="form.email" 
            placeholder="seu@email.com"
            required
          >
        </div>
        
        <div class="form-group">
          <label>CPF *</label>
          <input 
            type="text" 
            v-model="form.cpf" 
            @input="formatCPF"
            placeholder="000.000.000-00"
            maxlength="14"
            required
          >
        </div>
      </div>
      
      <div class="form-row">
        <div class="form-group">
          <label>Senha *</label>
          <input 
            type="password" 
            v-model="form.senha" 
            placeholder="Mínimo 6 caracteres"
            minlength="6"
            required
          >
        </div>
        
        <div class="form-group">
          <label>Confirmar Senha *</label>
          <input 
            type="password" 
            v-model="form.confirmarSenha" 
            placeholder="Digite a senha novamente"
            required
          >
        </div>
      </div>
      
      <div class="form-row">
        <div class="form-group">
          <label>Telefone</label>
          <input 
            type="text" 
            v-model="form.telefone" 
            @input="formatTelefone"
            placeholder="(00) 00000-0000"
          >
        </div>
        
        <div class="form-group">
          <label>Data de Nascimento</label>
          <input 
            type="date" 
            v-model="form.data_nascimento"
          >
        </div>
      </div>
      
      <div class="form-group">
        <label>Tipo de Usuário *</label>
        <div class="radio-group">
          <label>
            <input 
              type="radio" 
              v-model="form.tipo" 
              value="estudante"
              checked
            >
            <span>👨‍🎓 Estudante</span>
          </label>
          
          <label>
            <input 
              type="radio" 
              v-model="form.tipo" 
              value="professor"
            >
            <span>👨‍🏫 Professor</span>
          </label>
          
          <label v-if="isAdminPage"> <!-- Apenas se for admin cadastrando -->
            <input 
              type="radio" 
              v-model="form.tipo" 
              value="admin"
            >
            <span>👑 Admin</span>
          </label>
        </div>
      </div>
      
      <div v-if="form.tipo === 'estudante'" class="form-group">
        <label>Curso</label>
        <select v-model="form.curso_id">
          <option value="">Selecione um curso</option>
          <option v-for="curso in cursos" :key="curso.id" :value="curso.id">
            {{ curso.nome }}
          </option>
        </select>
      </div>
      
      <div v-if="error" class="error-message">
        {{ error }}
      </div>
      
      <button type="submit" :disabled="loading" class="btn-primary">
        {{ loading ? 'Cadastrando...' : 'Finalizar Cadastro' }}
      </button>
      
      <div class="login-link">
        <p>Já tem uma conta? 
          <router-link to="/login">Faça login aqui</router-link>
        </p>
      </div>
    </form>
    
    <router-link to="/" class="back-link">
      ← Voltar para Home
    </router-link>
  </div>
</template>

<style scoped>
.cadastro-container {
  max-width: 600px;
  margin: 30px auto;
  padding: 30px;
  background: #f8f9fa;
  border-radius: 10px;
  box-shadow: 0 4px 6px rgba(0,0,0,0.1);
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
  margin-bottom: 20px;
}

@media (max-width: 600px) {
  .form-row {
    grid-template-columns: 1fr;
  }
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  font-weight: 600;
  color: #333;
}

.form-group input,
.form-group select {
  width: 100%;
  padding: 12px;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 16px;
}

.radio-group {
  display: flex;
  gap: 20px;
  margin-top: 10px;
}

.radio-group label {
  display: flex;
  align-items: center;
  cursor: pointer;
  font-weight: normal;
}

.radio-group input[type="radio"] {
  width: auto;
  margin-right: 8px;
}

.radio-group span {
  display: flex;
  align-items: center;
  gap: 5px;
}

.error-message {
  margin: 20px 0;
  padding: 12px;
  background: #ffebee;
  color: #c62828;
  border-radius: 6px;
}

.login-link {
  margin-top: 20px;
  text-align: center;
  color: #666;
}

.login-link a {
  color: #42b983;
  text-decoration: none;
}

.login-link a:hover {
  text-decoration: underline;
}
</style>