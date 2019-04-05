<template>
  <div class="img-browser-container">
    <no-ssr>
      <box class="box-container">
        <div
          v-masonry
          transition-duration="0.3s"
          item-selector=".grid-item"
          class="masonry-container"
        >
          <div v-masonry-tile class="grid-item" :key="index" v-for="(image, index) in images">
            <img :src="image" class="img-item">
          </div>
        </div>
      </box>
    </no-ssr>
  </div>
</template>

<script>
import box from './box.vue'
import { mapState, mapActions } from 'vuex'

export default {
  components: {
    box
  },
  computed: {
    ...mapState({
      images: state => state.images.dogs_urls
    })
  },
  methods: {
    ...mapActions({ fetchMoreImages: 'images/GetDogs' }),
    fetchMore() {
      this.fetchMoreImages()
    },
    zaza() {
      this.$redrawVueMasonry()
    }
  },
  mounted() {
    console.log('nul')

    if (typeof this.$redrawVueMasonry === 'function') {
      console.log('salope')

      this.$redrawVueMasonry()
    }
  }
}
</script>

<style scoped>
.img-item {
  max-width: 250px;
  box-shadow: 0 2px 4px 0 rgba(0, 0, 0, 0.4);
}
.grid-item {
  margin: 5px;
}
.img-browser-container {
  width: 820px;
}

.masonry-container {
  max-height: 600px !important;
  overflow: scroll;
  overflow-x: hidden;
}
</style>
