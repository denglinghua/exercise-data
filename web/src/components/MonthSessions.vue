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
  const data = common.fillMissMonthData(props.data.data)
  const option = {
    title: {
      text: props.data.title,
      left: 'center',
    },
    tooltip: {
      trigger: 'axis',
    },
    xAxis: {
      type: 'category',
      data: data.x,
    },
    yAxis: {
      type: 'value'
    },
    series: [
      {
        data: data.y,
        type: 'line',
        markLine: {
          data: [{ type: 'average', name: 'Avg' }],
          lineStyle: {
            color: 'grey'
          },
          label: {
            position: 'insideEndTop',
          },
          symbol: ['none', 'none'],
        },
        lineStyle: {
          color: {
            x: 0,
            y: 0,
            x2: 0,
            y2: 1,
            type: 'linear',
            colorStops: [{
              offset: 0, color: '#1b237f'
            }, {
              offset: 1, color: '#5b6bc0'
            }],
            global: false
          }
        },
        showSymbol: false
      }
    ]
  };

  chart.setOption(option);

}
</script>
