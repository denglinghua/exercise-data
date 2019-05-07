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

        // 只挑最快的几条记录，看是否达标
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
