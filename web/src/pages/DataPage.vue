<template>
  <q-page>
    <div class="q-pa-xs flex flex-center">
      <div style="width: 1000px; max-width: 100%;">
        <div class="row q-mb-md">
          <q-btn icon="arrow_back" flat color="primary" @click="backHome" />
        </div>
        <div class="row justify-center text-h6 q-mb-md q-mt-sm text-primary">
          {{ runner }}
        </div>
        <div class="column" v-if="dataLoaded">
          <div class="row" style="height: 400px;">
            <WeekHourHeatMap :data="weekHourData" />
          </div>
          <div class="row" style="height: 400px;">
            <PaceDistanceScatter :data="paceDistanceData" />
          </div>
          <div class="row" style="height: 400px;">
            <MonthDistanceLine :data="monthDistanceData" />
          </div>
          <div class="row" style="height: 400px;">
            <MonthPaceLine :data="monthPaceData" />
          </div>
        </div>
      </div>
    </div>
    <q-inner-loading :showing="loading" />
  </q-page>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getCurrentInstance } from 'vue'
import { useRouter } from 'vue-router'
import WeekHourHeatMap from 'src/components/WeekHourHeatMap.vue'
import PaceDistanceScatter from 'src/components/PaceDistanceScatter.vue'
import MonthDistanceLine from 'src/components/MonthDistanceLine.vue'
import MonthPaceLine from 'src/components/MonthPaceLine.vue'

const $api = getCurrentInstance().appContext.config.globalProperties.$api;
const $router = useRouter()

const dataLoaded = ref(false)
const runner = ref(null)
const loading = ref(false)

const weekHourData = ref(null)
const paceDistanceData = ref(null)
const monthDistanceData = ref(null)
const monthPaceData = ref(null)

function getQueryId() {
  return $router.currentRoute.value.params.id
}

function backHome() {
  $router.push({name : 'home'})
}

function loadData(id) {
  loading.value = true
  $api.get(`/data/${id}`).then((res) => {

    runner.value = res.data.runner

    weekHourData.value = res.data.dataset.week_hour
    paceDistanceData.value = res.data.dataset.pace_distance
    monthDistanceData.value = res.data.dataset.month_distance
    monthPaceData.value = res.data.dataset.month_pace

    dataLoaded.value = true
  }).catch(() => {
    runner.value = '没有这个ID的数据'
    dataLoaded.value = false
  }).finally(() => {
    loading.value = false
  })
}

onMounted(() => {
  const queryId = getQueryId()
  if (queryId) {
    loadData(queryId)
  }
})
</script>
