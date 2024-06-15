<template>
  <ChartBase :init="init" :data="data" />
</template>
<script setup>
import { defineProps } from 'vue'
import ChartBase from 'src/components/ChartBase.vue'

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
    visualMap: {
      min: minPace,
      max: maxPace,
      dimension: 1,
      show: false,
      inRange: {
        color: ['#f2c31a', '#24b7f2']
      }
    },
    xAxis: {},
    yAxis: {
      inverse: true,
      min: 'dataMin',
      axisLabel: {
        formatter: function (d) {
          let mins = Math.floor(d / 60)
          let secs = d % 60
          secs = ('0' + secs).slice(-2)
          return mins + ':' + secs
        }
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
