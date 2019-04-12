<template>
  <div style="margin-top:50px; display: flex; flex-direction:column; align-items: center;">
    <h1 class="title">Statistics</h1>
    <on-top :active="loading">
      <box
        slot="parent"
        style="display:flex; flex-direction:column; align-items: center;"
        :style="`min-width : ${isMobileDevice ? 250 : 600}px; min-height : ${isMobileDevice ? 150 : 300}px`"
      >
        <h1 style="margin-bottom:0; text-align: center;" class="title">Total votes percentage</h1>

        <div style="display:flex; align-items:center; flex-wrap: wrap; justify-content: center;">
          <div v-show="!loading" style="display:flex; flex-direction:column; align-items:center">
            <span
              style="margin-bottom:15px"
              :style="`font-size : ${isMobileDevice ? 120 : 260}px;`"
            >
              <fa icon="cat"/>
            </span>
            <span :style="`font-size : ${isMobileDevice ? 46 : 96}px;`">
              <fa class="heart" :icon="[cats >= dogs ? 'fas' : 'far', 'heart']"/>
            </span>
          </div>
          <div
            style="display: flex; align-items: center; justify-content: center;"
            :style="`min-width : ${isMobileDevice ? 250 : 600}px; min-height : ${isMobileDevice ? 250 : 600}px`"
          >
            <GChart
              v-show="err === null && (cats > 0 || dogs > 0)"
              type="PieChart"
              :data="chartData"
              :options="chartOptions"
              @ready="onChartReady"
            />
            <div
              v-if="!loading && cats === 0 && dogs === 0"
              style="display:flex; align-items:center; flex-direction: column"
            >
              <p>No data to show</p>
              <button class="button is-primary" @click="fetchData">
                <fa icon="sync" style="margin-right:5"/>Retry
              </button>
            </div>
            <p v-if="!loading && err !== null" style="color:hsl(348, 100%, 61%)">{{err}}</p>
          </div>
          <div v-show="!loading" style="display:flex; flex-direction:column; align-items:center">
            <span
              style="margin-bottom:15px"
              :style="`font-size : ${isMobileDevice ? 120 : 260}px;`"
            >
              <fa icon="dog"/>
            </span>
            <span :style="`font-size : ${isMobileDevice ? 46 : 96}px;`">
              <fa class="heart" :icon="[cats >= dogs ? 'fas' : 'far', 'heart']"/>
            </span>
          </div>
        </div>
      </box>
      <spinner slot="child"/>
    </on-top>
  </div>
</template>

<script>
import { mapState, mapActions } from 'vuex'
import box from '~/components/box'
import spinner from '~/components/spinner.vue'
import onTop from '~/components/onTop.vue'
import { GChart } from 'vue-google-charts'
import { isMobile } from 'mobile-device-detect'

export default {
  components: {
    box,
    GChart,
    spinner,
    onTop
  },
  data() {
    return {
      chartReady: false,
      err: null
    }
  },
  computed: {
    ...mapState({
      theme: state => state.user.theme,
      cats: state => state.stats.cats,
      dogs: state => state.stats.dogs,
      dataLoading: state => state.stats.loading
    }),
    loading() {
      return this.dataLoading || !this.chartReady
    },
    chartData() {
      return [['', ''], ['Dog', this.dogs], ['Cat', this.cats]]
    },
    chartOptions() {
      return {
        width: isMobile ? 250 : 600,
        height: isMobile ? 250 : 600,
        legend: 'none',
        fontSize: isMobile ? 15 : 25,
        pieSliceTextStyle: { fontSize: isMobile ? 25 : 45 },
        chartArea: { width: '90%', height: '90%' },
        backgroundColor: this.theme === 'dark' ? '#1A1A1B' : 'white',
        pieSliceBorderColor: this.theme === 'dark' ? '#1A1A1B' : 'white',
        pieSliceText: 'label'
      }
    },
    isMobileDevice() {
      return isMobile
    }
  },
  created() {
    if (this.cats === -1) this.fetchData()
  },
  methods: {
    ...mapActions({ getResults: 'stats/getResults' }),
    onChartReady(chart, google) {
      this.chartReady = true
    },
    async fetchData() {
      this.err = await this.getResults()
    }
  }
}
</script>

<style scoped>
.heart {
  color: #ff007e;
}
</style>
