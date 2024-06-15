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
  const option = {
    title: {
      text: props.data.title,
      left: 'center',
    },
    tooltip: {
      trigger: 'axis',
      valueFormatter: common.createPaceFormatter()
    },
    xAxis: {
      type: 'category',
      data: props.data.data.x,
    },
    yAxis: {
      type: 'value',
      inverse: true,
      min: 'dataMin',
      axisLabel: {
        formatter: common.createPaceFormatter()
      }
    },
    series: [
      {
        data: props.data.data.y,
        type: 'line',
        markLine: {
          data: [{ type: 'average', name: 'Avg' }],
          label: {
            formatter: common.createPaceFormatter()
          },
          lineStyle: {
            color: 'grey',
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
              offset: 0, color: '#1a5e1f'
            }, {
              offset: 1, color: '#81c883'
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
