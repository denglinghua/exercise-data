<template>
  <q-page>
    <div class="q-pa-xs flex flex-center">
      <div style="width: 1000px; max-width: 100%;">
        <div class="row q-mb-md justify-center items-center">
          <q-chip icon="screen_rotation" size="sm" class="q-mr-sm" color="white" text-color="grey-6"
            v-if="portrait">横屏展示效果更好</q-chip>
        </div>
        <div class="row justify-center text-h6 q-mb-md q-mt-sm text-primary">
          Triathlon Exercise Data
        </div>
        <div class="column" v-if="dataLoaded">
          <div class="row q-mb-md" style="height: 500px;" v-for="c in charts" :key="c.name">
            <ChartBase :data="c.data.value" :createOption="c.option" />
          </div>
        </div>
      </div>
    </div>
    <q-inner-loading :showing="loading" />
    <q-resize-observer @resize="onResize" />
  </q-page>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getCurrentInstance } from 'vue'
import ChartBase from 'src/components/ChartBase.vue';
import chart from '../js/chart'
import triathlon from '../js/triathlon_chart'

const $api = getCurrentInstance().appContext.config.globalProperties.$api;

const dataLoaded = ref(false)
const loading = ref(false)

const activityTimeData = ref(null)
const weekHourData = ref(null)
const paceDistanceData = ref(null)
const monthDistanceData = ref(null)
const monthActivityFreqData = ref(null)
const runPlaceData = ref(null)

const charts = [
  { name: 'activityTime', data: activityTimeData, option: triathlon.activityTimePie },
  { name: 'workHour', data: weekHourData, option: chart.weekHourHeatmap },
  { name: 'monthActivityFreq', data: monthActivityFreqData, option: triathlon.monthActivityFreqAreaLine },
  { name: 'paceDistance', data: paceDistanceData, option: chart.paceDistanceScatter },
  { name: 'monthDistance', data: monthDistanceData, option: chart.monthDistanceLine },
  { name: 'runPlace', data: runPlaceData, option: triathlon.runPlaceWordCloud },
]

function loadData() {
  loading.value = true
  $api.get('/data/triathlon').then((res) => {

    activityTimeData.value = res.data.activity_type_time
    weekHourData.value = toWeekHour(res.data.week_hour)
    paceDistanceData.value = res.data.pace_distance
    monthDistanceData.value = toXY(res.data.month_run_distance)
    monthActivityFreqData.value = res.data.month_activity_freq
    runPlaceData.value = res.data.run_place

    dataLoaded.value = true
  }).catch(() => {
    //TODO: error display
    dataLoaded.value = false
  }).finally(() => {
    loading.value = false
  })
}

const portrait = ref(false)
function onResize(size) {
  portrait.value = window.matchMedia("(orientation: portrait)").matches;
}

function toXY(data) {
  const series = data.series.sort((a, b) => a[0].localeCompare(b[0]))
  const x = series.map((s) => s[0])
  const y = series.map((s) => s[1])
  data.series = { x: x, y: y }
  return data
}

function toWeekHour(data) {
  data.series = data.series.filter((s) => s[1] > 0)
    .map((s) => {
      let wh = s[0].split('-')
      return [parseInt(wh[1]), parseInt(wh[0]), s[1]]
    })
  return data
}

onMounted(() => {
  loadData()
})
</script>
