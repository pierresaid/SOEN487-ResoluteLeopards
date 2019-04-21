<template>
  <div>
    <button class="control button imgur-button" @click="isModalActive = true">Or browse Imgur</button>
    <b-modal :active.sync="isModalActive" scroll="keep">
      <image-browser
        :images="images"
        :fetch-more-images="fetchMoreImages"
        :fetching="fetching"
        :title="title"
        @input="$emit('input', $event); isModalActive = false"
      />
    </b-modal>
  </div>
</template>

<script>
import ImageBrowser from '../components/ImageBrowser.vue'

export default {
  components: {
    ImageBrowser
  },
  props: {
    images: {
      type: Array,
      default: () => {
        return []
      }
    },
    fetchMoreImages: {
      type: Function,
      default: () => {}
    },
    fetching: {
      type: Boolean,
      default: false
    },
    title: {
      type: String,
      default: null
    }
  },
  data() {
    return {
      isModalActive: false
    }
  }
}
</script>

<style>
.imgur-button {
  background-color: #1bb76e;
  color: white;
  font-weight: bold;
  border-color: rgb(27, 183, 110);
}

.modal-content {
  display: flex;
  justify-content: center;
}
</style>
