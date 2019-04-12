<template>
  <on-top :active="disableFetching">
    <box
      slot="parent"
      class="img-browser-container"
      :style="`width : ${isMobileDevice ? 300 : 840}px;min-height : ${isMobileDevice ? 300 : 500}px;`"
    >
      <h1 v-if="title !== null" style="text-align:center" class="title">{{title}}</h1>
      <div
        v-masonry
        v-infinite-scroll="fetchMore"
        transition-duration="0.3s"
        item-selector=".grid-item"
        infinite-scroll-distance="0"
        infinite-scroll-throttle-delay="200"
        infinite-scroll-disabled="disableFetching"
        class="masonry-container"
      >
        <div v-for="(image, index) in images" :key="index" v-masonry-tile class="grid-item">
          <img :src="image" class="img-item" @click="$emit('input', image)" @load="loaded += 1">
        </div>
      </div>
    </box>
    <spinner slot="child" background style="margin-top:15px; margin-bottom:15px"/>
  </on-top>
</template>

<script>
import box from './box.vue'
import spinner from '~/components/spinner.vue'
import onTop from '~/components/onTop.vue'
import { isMobile } from 'mobile-device-detect'

export default {
  components: {
    box,
    spinner,
    onTop
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
      loaded: 0,
      allowReFetch: true
    }
  },
  computed: {
    disableFetching() {
      return this.fetching || this.images.length > this.loaded
    },
    isMobileDevice() {
      return isMobile
    }
  },
  mounted() {
    if (typeof this.$redrawVueMasonry === 'function') {
      this.$redrawVueMasonry()
    }
  },
  methods: {
    fetchMore() {
      if (this.disableFetching || !this.allowReFetch) return
      this.allowReFetch = false
      setTimeout(() => {
        this.allowReFetch = true
      }, 6000)
      this.fetchMoreImages()
    }
  }
}
</script>

<style scoped>
.img-item {
  max-width: 250px;
  box-shadow: 0 2px 4px 0 rgba(0, 0, 0, 0.4);
  padding: 5px;
}

.img-item:hover {
  background-color: #ff007e;
  cursor: pointer;
  -webkit-user-drag: none;
}

.grid-item {
  margin: 5px;
}

.masonry-container {
  max-height: 600px !important;
  overflow: scroll;
  overflow-x: hidden;
}
</style>
