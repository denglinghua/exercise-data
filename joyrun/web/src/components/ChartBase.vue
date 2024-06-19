<template>
  <div ref="chartDiv" class="full-height full-width">
    <q-resize-observer @resize="onResize" />
  </div>
</template>

<script setup>
import { ref, watch, defineProps, onMounted } from 'vue'
import * as echarts from 'echarts'

const props = defineProps({
  // only used for watching, no parse here
  data: {
    type: Object,
  },
  createOption: {
    type: Function,
    default: () => { }
  },
})

const chartDiv = ref(null) // Ref chart container DOM element
let chart = null

function createChart() {
  chart = echarts.init(chartDiv.value)
  chart.setOption({
    backgroundColor: "white",
    grid: {
      left: "9%",
      right: "3%",
    },
  })
}

function setOption() {
  chart.setOption(props.createOption(props.data))
}

function onResize(size) {
  if (chart) {
    // console.log('resize', size)
    chart.resize()
  }
}

watch(() => props.data, (newVal, oldVal) => {
  setOption()
})

onMounted(() => {
  createChart()
  if (props.data) {
    setOption()
  }
})
</script>
