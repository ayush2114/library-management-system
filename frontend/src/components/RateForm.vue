<template>
    <div class="modal">
      <div class="modal-content">
        <h4>Rate this Ebook</h4>
        <form @submit.prevent="handleSubmit">
          <div class="form-group">
            <label for="rating">Rating:</label>
            <select v-model="rating" class="form-control" required>
              <option value="" disabled>Select a rating</option>
              <option v-for="num in 5" :key="num" :value="num">{{ num }}</option>
            </select>
          </div>
          <div class="form-group text-right">
            <button type="button" class="btn btn-secondary" @click="close">Cancel</button>
            <button type="submit" class="btn btn-primary">Submit</button>
          </div>
        </form>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    props: {
      user_id: Number,
      ebook_id: Number
    },
    data() {
      return {
        rating: null
      };
    },
    methods: {
      close() {
        this.$emit('close');
      },
      handleSubmit() {
        if (this.rating) {
          this.$emit('submit-rating', this.user_id, this.ebook_id, this.rating);
          this.close();
        }
      }
    }
  }
  </script>
  
  <style scoped>
  .modal {
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.5);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 1;
  }
  
  .modal-content {
    padding: 20px;
    width: 300px;
  }
  
  .form-group {
    margin-bottom: 15px;
  }
  
  .btn {
    margin-left: 10px;
  }
  </style>
  