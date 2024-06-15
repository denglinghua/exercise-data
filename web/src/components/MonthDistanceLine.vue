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
  const option = {
    title: {
      text: props.data.title,
      left: 'center',
    },
    xAxis: {
      type: 'category',
      data: props.data.data.x,
    },
    yAxis: {
      type: 'value'
    },
    series: [
      {
        data: props.data.data.y,
        type: 'line',
        markLine: {
          data: [{ type: 'average', name: 'Avg' }],
          lineStyle: {
            color: 'grey'
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
              offset: 0, color: '#e65104'
            }, {
              offset: 1, color: '#ffb74c'
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
