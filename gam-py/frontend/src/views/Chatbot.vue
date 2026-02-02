<template>
  <div class="chat-full-container">
    <div class="chat-sidebar">
      <div class="sidebar-header">
        <span class="code-icon">⚙️</span>
        <h3>Painel GAM</h3>
      </div>
      
      <div class="user-profile-centered">
        <div class="user-avatar-placeholder">
          <span class="user-initial">A</span>
        </div>
        <div class="profile-details">
          <strong class="user-name">Aluno Exemplo</strong>
          <span class="user-meta">3º Semestre • Ciência da Computação</span>
        </div>
        <div class="user-stats-badge">
          CRG Atual: <strong>8.75</strong>
        </div>
      </div>

      <div class="quick-actions">
        <h4>Comandos</h4>
        <ul>
          <li><a href="#" @click.prevent>Previsão Semestral</a></li>
          <li><a href="#" @click.prevent>Otimizar Grade</a></li>
          <li><a href="#" @click.prevent>Dúvidas Frequentes</a></li>
        </ul>
      </div>
    </div>

    <div class="chat-main-area">
      <div class="system-brand-premium">
        <div class="brand-content">
          <span class="code-icon">🤖</span>
          <span class="brand-text">Assistente Inteligente <span class="brand-highlight">GAMBOT</span></span>
        </div>
      </div>

      <div class="messages-display" ref="scrollBox">
        <div v-for="(msg, index) in mensagens" :key="index" :class="['message-wrapper', msg.autor]">
          <div class="message-bubble">
            <span v-if="msg.autor === 'bot'" class="bot-label">GAMBOT</span>
            <p class="text-content">{{ msg.texto }}</p>
            <div class="message-info">
              <span class="msg-date">{{ msg.data }}</span>
              <span class="msg-time">{{ msg.hora }}</span>
            </div>
          </div>
        </div>
        
        <div v-if="digitando" class="message-wrapper bot">
          <div class="message-bubble typing">
            <span>.</span><span>.</span><span>.</span>
          </div>
        </div>
      </div>

      <div class="input-area">
        <div class="input-wrapper">
          <input 
            v-model="novaMensagem" 
            @keyup.enter="enviarMensagem"
            placeholder="Converse com o Gambot..." 
            type="text"
          />
          <button @click="enviarMensagem" :disabled="!novaMensagem.trim()" class="btn-send">
            <span>➤</span>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Chatbot',
  data() {
    return {
      novaMensagem: '',
      digitando: false,
      mensagens: [
        { 
          autor: 'bot', 
          texto: 'Conexão estabelecida. Eu sou o Gambot! Como posso auxiliar na sua análise acadêmica hoje?', 
          hora: '12:00',
          data: '02/02/2026'
        }
      ]
    }
  },
  methods: {
    enviarMensagem() {
      if (!this.novaMensagem.trim()) return;

      const agora = new Date();
      this.mensagens.push({
        autor: 'user',
        texto: this.novaMensagem,
        hora: agora.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
        data: agora.toLocaleDateString('pt-BR')
      });

      this.novaMensagem = '';
      this.scrollParaBaixo();

      this.digitando = true;
      // Simulando a resposta do backend em Python
      setTimeout(() => {
        this.digitando = false;
        this.mensagens.push({
          autor: 'bot',
          texto: 'Análise processada pelo núcleo Gambot. Identifiquei que sua carga horária está equilibrada.',
          hora: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
          data: new Date().toLocaleDateString('pt-BR')
        });
        this.scrollParaBaixo();
      }, 1500);
    },
    scrollParaBaixo() {
      this.$nextTick(() => {
        const box = this.$refs.scrollBox;
        box.scrollTop = box.scrollHeight;
      });
    }
  }
}
</script>

<style scoped>
.chat-full-container {
  display: flex;
  height: 100vh;
  background: #f0f2f5;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

/* SIDEBAR */
.chat-sidebar {
  width: 280px;
  background: #1a1a2e;
  padding: 30px 20px;
  display: flex;
  flex-direction: column;
  color: #fff;
}

.sidebar-header {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 40px;
  justify-content: center;
}

.sidebar-header h3 { font-size: 14px; text-transform: uppercase; letter-spacing: 1.5px; color: #8e8eb2; margin: 0; }

.user-profile-centered {
  text-align: center;
  padding: 25px 15px;
  background: rgba(255,255,255,0.05);
  border-radius: 20px;
  margin-bottom: 40px;
}

.user-avatar-placeholder {
  width: 70px;
  height: 70px;
  background: linear-gradient(135deg, #4ade80 0%, #2c5530 100%);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 15px;
  box-shadow: 0 4px 15px rgba(0,0,0,0.3);
}

.user-initial { color: white; font-size: 28px; font-weight: bold; }
.user-name { display: block; color: white; font-size: 16px; font-weight: 600; margin-bottom: 5px; }
.user-meta { display: block; color: #8e8eb2; font-size: 11px; margin-bottom: 15px; }

.user-stats-badge {
  display: inline-block;
  background: #111122;
  color: #a8a8cf;
  padding: 8px 16px;
  border-radius: 30px;
  font-size: 12px;
}
.user-stats-badge strong { color: #4ade80; }

.quick-actions h4 { font-size: 11px; color: #5c5c8a; text-transform: uppercase; margin-bottom: 20px; text-align: left; }
.quick-actions ul { list-style: none; padding: 0; text-align: left; }
.quick-actions li { margin-bottom: 15px; }
.quick-actions a { color: #a8a8cf; text-decoration: none; font-size: 14px; transition: 0.3s; }
.quick-actions a:hover { color: #4ade80; padding-left: 5px; }

/* ÁREA DE CHAT */
.chat-main-area {
  flex: 1;
  display: flex;
  flex-direction: column;
  background: #f0f2f5;
}

.system-brand-premium {
  height: 60px;
  background: #fff;
  display: flex; align-items: center; justify-content: center;
  border-bottom: 1px solid #e0e0e0;
}

.brand-text { color: #1a1a2e; font-size: 14px; font-weight: 700; }
.brand-highlight { color: #2c5530; letter-spacing: 1px; }

.messages-display {
  flex: 1;
  padding: 30px 50px;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.message-wrapper { display: flex; width: 100%; }
.message-wrapper.bot { justify-content: flex-start; }
.message-wrapper.user { justify-content: flex-end; }

.message-bubble {
  max-width: 65%;
  padding: 15px 20px;
  font-size: 15px;
  line-height: 1.5;
  box-shadow: 0 2px 5px rgba(0,0,0,0.05);
}

.bot .message-bubble {
  background: #ffffff;
  color: #333;
  border-radius: 18px 18px 18px 2px;
}

.user .message-bubble {
  background: #dcfce7;
  color: #166534;
  border-radius: 18px 18px 2px 18px;
}

/* ESTILO DO NOME GAMBOT */
.bot-label { 
  display: block; 
  font-size: 11px; 
  font-weight: 900; 
  color: #2c5530; 
  margin-bottom: 8px; 
  letter-spacing: 0.5px;
}

.text-content { margin: 0; white-space: pre-wrap; }

.message-info {
  display: flex;
  justify-content: flex-end;
  gap: 8px;
  margin-top: 10px;
  font-size: 10px;
  color: #999;
}

/* INPUT AREA */
.input-area {
  padding: 20px 50px 30px;
  background: #f0f2f5;
}

.input-wrapper {
  display: flex;
  background: #fff;
  border-radius: 12px;
  padding: 8px 12px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.05);
  align-items: center;
}

input {
  flex: 1;
  border: none;
  padding: 10px 15px;
  outline: none;
  font-size: 15px;
}

.btn-send {
  background: #2c5530;
  color: white;
  border: none;
  width: 40px;
  height: 40px;
  border-radius: 10px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
}

.typing span { animation: blink 1s infinite; font-size: 20px; color: #999; }
@keyframes blink { 0%, 100% { opacity: 0.2; } 50% { opacity: 1; } }
</style>