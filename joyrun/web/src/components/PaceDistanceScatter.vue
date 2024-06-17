<template>
  <ChartBase :init="init" :data="data" />
</template>
<script setup>
import { defineProps } from 'vue'
import ChartBase from 'src/components/ChartBase.vue'
import common from 'src/js/common'

const props = defineProps({
  data: {
    type: Object,
  },
})

function init(chart) {
  const minPace = Math.min(...props.data.data.map(d => d[1]))
  const maxPace = Math.max(...props.data.data.map(d => d[1]))
  const option = {
    title: {
      text: props.data.title,
      left: 'center',
    },
    tooltip: {
      trigger: 'axis',
      valueFormatter: common.createPaceFormatter()
    },
    visualMap: {
      min: minPace,
      max: maxPace,
      dimension: 1,
      show: false,
      inRange: {
        color: ['#f50056', '#448aff']
      }
    },
    xAxis: {},
    yAxis: {
      inverse: true,
      min: 'dataMin',
      axisLabel: {
        formatter: common.createPaceFormatter()
      }
    },
    series: [
      {
        symbolSize: 5,
        data: props.data.data, //.filter(d => d[1] < 600),
        type: 'scatter',
      }
    ]
  };

  chart.setOption(option);

}
</script>
