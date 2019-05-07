using System;

namespace RunData
{
    // 一个统计周期内的跑步记录，目前是一周。
    class PeriodRunRecord
    {
        public Member Member { get; }
        public RunData Data { get; }
        public short RunTimes { get; }
        private bool isQualifiedOfAvgPace;
        public bool IsQualifiedOfDistance { get; }        

        public static readonly short MAX_AVG_PACE = (short)(8.5 * 60);
        public static readonly short MIN_DISTANCE = 10;  

        public PeriodRunRecord(long joyRunId, string name, string gender, string group, double distance, double totalTimeSeconds, short runTimes)
        {
            this.Member = new Member(joyRunId, name, gender, group);
            this.Data = new RunData(distance, totalTimeSeconds);
            this.RunTimes = runTimes;
            this.isQualifiedOfAvgPace = this.Data.AvgPaceSeconds <= MAX_AVG_PACE;
            this.IsQualifiedOfDistance = this.Data.Distance >= MIN_DISTANCE;
        }

        public bool IsQualifiedOfAvgPace
        {
            get
            {
                return this.isQualifiedOfAvgPace;
            }
        }

        // 对于跑量达标但配速没达标的（有越野），重新评估一下配速。
        public bool ReEvalQualifiedByDetail(RunRecordDetail detail)
        {
            bool changed = false;
            if (this.IsQualifiedOfDistance && !this.IsQualifiedOfAvgPace)
            {
                changed = detail.IsAvgPaceQualified();
                this.isQualifiedOfAvgPace = changed;
            }
            return changed;
        }
    }
}
