<template>
  <q-page>
    <div class="q-pa-xs flex flex-center">
      <div style="width: 1000px; max-width: 100%;">
        <q-tab-panels v-model="panel" animated>
          <q-tab-panel name="id">
            <div class="row justify-center">
              <q-input v-model="id" label="悦跑圈ID" type="number" error-message="这个ID没有数据" :error="noData"
                @keyup.enter="loadData" style="width:200px">
                <template v-slot:append>
                  <q-icon name="arrow_forward" color="primary" @click="loadData" />
                </template>
              </q-input>
            </div>
          </q-tab-panel>
          <q-tab-panel name="chart" class="q-px-none">
            <div class="row">
              <q-btn icon="arrow_back" flat dense color="primary" @click="panel = 'id'" />
            </div>
            <div class="row justify-center text-h6 q-mb-md text-primary">
              {{ runner }}
            </div>
            <div class="column">
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
          </q-tab-panel>
        </q-tab-panels>
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

const panel = ref('id')
const id = ref(process.env.DEV ? '86288420' : '')
const noData = ref(false)
const runner = ref(null)
const loading = ref(false)

const weekHourData = ref(null)
const paceDistanceData = ref(null)
const monthDistanceData = ref(null)
const monthPaceData = ref(null)

function getQueryId() {
  return $router.currentRoute.value.params.id
}

function loadData() {
  if (!id.value) {
    return
  }

  loading.value = true
  $api.get(`/data/${id.value}`).then((res) => {
    console.log(res.data)
    runner.value = res.data.runner
    weekHourData.value = res.data.dataset.week_hour
    paceDistanceData.value = res.data.dataset.pace_distance
    monthDistanceData.value = res.data.dataset.month_distance
    monthPaceData.value = res.data.dataset.month_pace
    noData.value = false
    panel.value = 'chart'
  }).catch(() => {
    runner.value = '没有这个ID的数据'
    noData.value = true
  }).finally(() => {
    loading.value = false
  })
}

onMounted(() => {
  const queryId = getQueryId()
  if (queryId) {
    id.value = queryId
    loadData()
  }
})
</script>
<style>
input::-webkit-outer-spin-button,
input::-webkit-inner-spin-button {
  -webkit-appearance: none;
}
</style>
