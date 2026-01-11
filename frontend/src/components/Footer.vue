<template>
  <footer class="app-footer">
    <div class="footer-content">
      <p>&copy; 2024 基本情報勉強アプリ. All rights reserved.</p>
    </div>
  </footer>
</template>

<script>
export default {
  name: 'AppFooter'
};
</script>

<style scoped>
.app-footer {
  background-color: #f8f9fa;
  color: #6c757d;
  padding: 2rem 0;
  margin-top: auto;
  border-top: 1px solid #dee2e6;
}

.footer-content {
  max-width: 1200px;
  margin: 0 auto;
  text-align: center;
  padding: 0 2rem;
}

.app-footer p {
  margin: 0;
  font-size: 0.9rem;
}
</style>

