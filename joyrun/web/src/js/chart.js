import common from "./common.js";

function monthDistanceLine(data) {
  const xy = common.fillMissMonthData(data.series);
  const option = {
    title: {
      text: data.title,
      left: "center",
    },
    tooltip: {
      trigger: "axis",
      valueFormatter: (d) => d.toFixed(2),
    },
    xAxis: {
      type: "category",
      data: xy.x,
    },
    yAxis: {
      type: "value",
    },
    series: [
      {
        data: xy.y,
        type: "line",
        markLine: {
          data: [{ type: "average", name: "Avg" }],
          lineStyle: {
            color: "grey",
          },
          label: {
            position: "insideEndTop",
          },
          symbol: ["none", "none"],
        },
        lineStyle: {
          color: {
            x: 0,
            y: 0,
            x2: 0,
            y2: 1,
            type: "linear",
            colorStops: [
              {
                offset: 0,
                color: "#e65104",
              },
              {
                offset: 1,
                color: "#ffb74c",
              },
            ],
            global: false,
          },
        },
        showSymbol: false,
      },
    ],
  };

  return option;
}

function monthPaceLine(data) {
  const option = {
    title: {
      text: data.title,
      left: "center",
    },
    tooltip: {
      trigger: "axis",
      valueFormatter: common.createPaceFormatter(),
    },
    xAxis: {
      type: "category",
      data: data.series.x,
    },
    yAxis: {
      type: "value",
      inverse: true,
      min: "dataMin",
      axisLabel: {
        formatter: common.createPaceFormatter(),
      },
    },
    series: [
      {
        data: data.series.y,
        type: "line",
        markLine: {
          data: [{ type: "average", name: "Avg" }],
          label: {
            position: "insideEndTop",
            formatter: common.createPaceFormatter(),
          },
          lineStyle: {
            color: "grey",
          },
          symbol: ["none", "none"],
        },
        lineStyle: {
          color: {
            x: 0,
            y: 0,
            x2: 0,
            y2: 1,
            type: "linear",
            colorStops: [
              {
                offset: 0,
                color: "#1a5e1f",
              },
              {
                offset: 1,
                color: "#81c883",
              },
            ],
            global: false,
          },
        },
        showSymbol: false,
      },
    ],
  };

  return option;
}

function monthSessionLine(data) {
  const xy = common.fillMissMonthData(data.series);
  const option = {
    title: {
      text: data.title,
      left: "center",
    },
    tooltip: {
      trigger: "axis",
    },
    xAxis: {
      type: "category",
      data: xy.x,
    },
    yAxis: {
      type: "value",
    },
    series: [
      {
        data: xy.y,
        type: "line",
        markLine: {
          data: [{ type: "average", name: "Avg" }],
          lineStyle: {
            color: "grey",
          },
          label: {
            position: "insideEndTop",
          },
          symbol: ["none", "none"],
        },
        lineStyle: {
          color: {
            x: 0,
            y: 0,
            x2: 0,
            y2: 1,
            type: "linear",
            colorStops: [
              {
                offset: 0,
                color: "#1b237f",
              },
              {
                offset: 1,
                color: "#5b6bc0",
              },
            ],
            global: false,
          },
        },
        showSymbol: false,
      },
    ],
  };

  return option;
}

function paceDistanceScatter(data) {
  const minPace = Math.min(...data.series.map((d) => d[1]));
  const maxPace = Math.max(...data.series.map((d) => d[1]));
  const option = {
    title: {
      text: data.title,
      left: "center",
    },
    tooltip: {
      trigger: "axis",
      valueFormatter: common.createPaceFormatter(),
    },
    visualMap: {
      min: minPace,
      max: maxPace,
      dimension: 1,
      show: false,
      inRange: {
        color: ["#f50056", "#448aff"],
      },
    },
    xAxis: {},
    yAxis: {
      inverse: true,
      min: "dataMin",
      axisLabel: {
        formatter: common.createPaceFormatter(),
      },
    },
    series: [
      {
        symbolSize: 5,
        data: data.series, //.filter(d => d[1] < 600),
        type: "scatter",
      },
    ],
  };

  return option;
}

function weekHourHeatmap(data, days = ['一', '二', '三', '四', '五', '六', '日']) {
  // prettier-ignore
  const hours = [
    '12A', '1A', '2A', '3A', '4A', '5A', '6A', '7A', '8A', '9A', '10A', '11A',
    '12P', '1P', '2P', '3P', '4P', '5P', '6P', '7P', '8P', '9P', '10P', '11P'
  ];

  const option = {
    title: {
      text: data.title,
      left: "center",
    },
    tooltip: {
      position: "top",
    },
    xAxis: {
      type: "category",
      data: hours,
      splitArea: {
        show: true,
      },
    },
    yAxis: {
      type: "category",
      data: days,
      splitArea: {
        show: true,
      },
    },
    visualMap: {
      min: 0,
      max: 60,
      calculable: true,
      orient: "horizontal",
      left: "center",
      bottom: "15%",
      show: false,
      inRange: {
        color: ["#1d4877", "#1b8a5a", "#fbb021", "#f68838", "#ee3e32"],
      },
    },
    series: [
      {
        type: "heatmap",
        data: data.series,
        label: {
          show: true,
        },
        emphasis: {
          itemStyle: {
            shadowBlur: 10,
            shadowColor: "rgba(0, 0, 0, 0.5)",
          },
        },
        itemStyle: {
          borderWidth: 2,
          borderColor: "white",
        },
      },
    ],
  };

  return option;
}

export default {
  monthDistanceLine,
  monthPaceLine,
  monthSessionLine,
  paceDistanceScatter,
  weekHourHeatmap,
};
