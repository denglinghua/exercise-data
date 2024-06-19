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
          <div class="row q-mb-md" style="height: 400px;" v-for="c in charts" :key="c.name">
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

const $api = getCurrentInstance().appContext.config.globalProperties.$api;

const dataLoaded = ref(false)
const loading = ref(false)

const weekHourData = ref(null)
const paceDistanceData = ref(null)
const monthDistanceData = ref(null)

const charts = [
  //{ name: 'workHour', data: weekHourData, option: chart.weekHourHeatmap },
  { name: 'paceDistance', data: paceDistanceData, option: chart.paceDistanceScatter },
  { name: 'monthDistance', data: monthDistanceData, option: chart.monthDistanceLine },
]

function loadData() {
  loading.value = true
  $api.get('/data/triathlon').then((res) => {

    weekHourData.value = res.data.week_hour
    console.log(res.data.month_run_distance)
    paceDistanceData.value = res.data.pace_distance
    monthDistanceData.value = res.data.month_run_distance

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

onMounted(() => {
  loadData()
})
</script>
