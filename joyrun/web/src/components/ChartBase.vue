<template>
  <div ref="chartDiv" class="full-height full-width">
    <q-resize-observer @resize="onResize" />
  </div>
</template>

<script setup>
import { ref, watch, defineProps, onMounted } from 'vue'
// import everything from echarts, which will cause bigger bundle size
// import * as echarts from 'echarts'

// the following is a better way to import echarts, which import only what needed
// import echarts core module, which provides necessary interfaces for echarts usage.
import * as echarts from 'echarts/core';
import { BarChart, PieChart, LineChart, ScatterChart, HeatmapChart  } from 'echarts/charts';
import {
  VisualMapComponent,
  TitleComponent,
  TooltipComponent,
  GridComponent,
  DatasetComponent,
  TransformComponent,
  LegendComponent,
  MarkLineComponent,
  ToolboxComponent,
} from 'echarts/components';
import { LabelLayout, UniversalTransition } from 'echarts/features';
// import Canvas renderer, note that it is necessary to introduce CanvasRenderer or SVGRenderer
import { CanvasRenderer } from 'echarts/renderers';

// register components
echarts.use([
  VisualMapComponent,
  TitleComponent,
  TooltipComponent,
  GridComponent,
  DatasetComponent,
  TransformComponent,
  LegendComponent,
  MarkLineComponent,
  ToolboxComponent,
  BarChart, PieChart, LineChart, ScatterChart, HeatmapChart,
  LabelLayout,
  UniversalTransition,
  CanvasRenderer
]);

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
    toolbox: {
      show: true,
      feature: {
        saveAsImage: {}
      }
    }
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
