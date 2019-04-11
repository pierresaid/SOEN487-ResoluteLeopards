<template>
  <div style="margin-top:50px; display: flex; flex-direction:column; align-items: center;">
    <h1 class="title">Statistics</h1>
    <on-top :active="loading">
      <box
        slot="parent"
        style="display:flex; min-width:600px; min-height:300px; flex-direction:column; align-items: center;"
      >
        <h1 style="margin-bottom:0" class="title">Total votes percentage</h1>

        <div style="display:flex; align-items:center">
          <div v-show="!loading" style="display:flex; flex-direction:column; align-items:center">
            <fa icon="cat" style="font-size:260px; margin-bottom:15px"/>
            <fa class="heart" :icon="[cats >= dogs ? 'fas' : 'far', 'heart']"/>
          </div>
          <div style="min-width:600px; min-height:600px">
            <GChart
              type="PieChart"
              :data="chartData"
              :options="chartOptions"
              @ready="onChartReady"
            />
          </div>
          <div v-show="!loading" style="display:flex; flex-direction:column; align-items:center">
            <fa icon="dog" style="font-size:260px; margin-bottom:15px"/>
            <fa class="heart" :icon="[dogs >= cats ? 'fas' : 'far', 'heart']"/>
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

export default {
  components: {
    box,
    GChart,
    spinner,
    onTop
  },
  data() {
    return {
      chartReady: false
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
        width: 600,
        height: 600,
        legend: 'none',
        fontSize: 25,
        pieSliceTextStyle: { fontSize: 45 },
        chartArea: { width: '90%', height: '90%' },
        backgroundColor: this.theme === 'dark' ? '#1A1A1B' : 'white',
        pieSliceBorderColor: this.theme === 'dark' ? '#1A1A1B' : 'white',
        pieSliceText: 'label'
      }
    }
  },
  created() {
    if (this.cats === -1) this.getResults()
  },
  methods: {
    ...mapActions({ getResults: 'stats/getResults' }),
    onChartReady(chart, google) {
      this.chartReady = true
    }
  }
}
</script>

<style scoped>
.heart {
  color: #ff007e;
  font-size: 96px;
}
</style>
