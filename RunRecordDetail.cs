using System.Collections.Generic;

namespace RunData
{
    class RunRecordDetail
    {
        private List<RunData> detail = new List<RunData>();

        public void Add(RunData data)
        {
            this.detail.Add(data);
        }

        // 在原始记录中，按配速从高到低挑选10公里以上最快速度的跑步记录，看平均配速是否达标
        // 最优配速组合都不能达标，肯定就不达标了
        public bool IsAvgPaceQualified()
        {
            this.detail.Sort((x, y) => x.AvgPaceSeconds.CompareTo(y.AvgPaceSeconds));

            double distance = 0, totalTime = 0;
            foreach (RunData r in this.detail)
            {
                if (distance >= PeriodRunRecord.MIN_DISTANCE) break;

                distance += r.Distance;
                totalTime += r.TotalTimeSeconds;
            }

            return (totalTime / distance) <= PeriodRunRecord.MAX_AVG_PACE;
        }
    }
}
