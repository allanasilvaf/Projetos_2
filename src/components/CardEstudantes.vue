<template>
  <div class="card-estudantes">
    <h3>{{ titulo }}</h3>
    <p>Componente de estudantes funcionando!</p>
  </div>
</template>

<script>
export default {
  name: "CardEstudantes",
  props: {
    titulo: {
      type: String,
      default: "Lista de Estudantes"
    }
  }
}
</script>
