<template>
  <q-page>
    <div class="q-pa-xs flex flex-center">
      <div style="width: 1000px; max-width: 100%;">
        <div class="row q-mb-md justify-between items-center">
          <q-btn icon="arrow_back" flat color="primary" @click="backHome" />
          <q-chip icon="screen_rotation" size="sm" class="q-mr-sm" color="white" text-color="grey-6"
            v-if="portrait">横屏展示效果更好</q-chip>
        </div>
        <div class="row justify-center text-h6 q-mb-md q-mt-sm text-primary">
          {{ runner }}
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
import { useRouter } from 'vue-router'
import ChartBase from 'src/components/ChartBase.vue';
import chart from '../js/chart'

const $api = getCurrentInstance().appContext.config.globalProperties.$api;
const $router = useRouter()

const dataLoaded = ref(false)
const runner = ref(null)
const loading = ref(false)

const weekHourData = ref(null)
const paceDistanceData = ref(null)
const monthDistanceData = ref(null)
const monthPaceData = ref(null)
const monthSessionData = ref(null)

const charts = [
  { name: 'workHour', data: weekHourData, option: chart.weekHourHeatmap },
  { name: 'paceDistance', data: paceDistanceData, option: chart.paceDistanceScatter },
  { name: 'monthSessions', data: monthSessionData, option: chart.monthSessionLine},
  { name: 'monthDistance', data: monthDistanceData, option: chart.monthDistanceLine },
  { name: 'monthPace', data: monthPaceData, option: chart.monthPaceLine },
]

function getQueryId() {
  return $router.currentRoute.value.params.id
}

function backHome() {
  $router.push({ name: 'home' })
}

function loadData(id) {
  loading.value = true
  $api.get(`/data/${id}`).then((res) => {

    runner.value = res.data.runner

    weekHourData.value = res.data.dataset.week_hour
    paceDistanceData.value = res.data.dataset.pace_distance
    monthDistanceData.value = res.data.dataset.month_distance
    monthPaceData.value = res.data.dataset.month_pace
    monthSessionData.value = res.data.dataset.month_sessions

    dataLoaded.value = true
  }).catch(() => {
    runner.value = '没有这个ID的数据'
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
  const queryId = getQueryId()
  if (queryId) {
    loadData(queryId)
  }
})
</script>
