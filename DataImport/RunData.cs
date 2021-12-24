using System;

namespace DataImport
{
    class RunData
    {
        public long JoyRunId { get; }
        public string Name { get; }
        public string Gender { get; }
        public double Distance { get; }
        public double TotalTimeSeconds { get; }
        public string RunType { get; }
        public long AvgPaceSeconds { get; }
        public DateTime RunEndTime { get; }
        public int Cadence { get; }
        public int StrideLength { get; }

        public RunData(long joyRunId, string name, string gender,
            double distance, double totalTimeSeconds, string runType, DateTime endTime,
            int cadence, double strideLength)
        {
            this.JoyRunId = joyRunId;
            this.Name = name;
            this.Gender = gender;
            this.Distance = Math.Truncate(distance * 100) / 100;
            this.TotalTimeSeconds = totalTimeSeconds;
            this.AvgPaceSeconds = (long)(totalTimeSeconds / distance);
            this.RunType = runType;
            this.RunEndTime = endTime;
            this.Cadence = cadence;
            this.StrideLength = Convert.ToInt32(strideLength * 100);
        }

        public string TimeSpanOfAvgPace
        {
            get
            {
                return DateUtil.ToTimeSpanFromSeconds(this.AvgPaceSeconds);
            }
        }

        public string TimeSpanOfTotalTime
        {
            get
            {
                return DateUtil.ToTimeSpanFromSeconds(this.TotalTimeSeconds);
            }
        }

        public override int GetHashCode()
        {
            return HashCode.Combine(JoyRunId, RunEndTime);
        }

        public override bool Equals(object obj)
        {
            RunData rd = obj as RunData;
            return this.JoyRunId == rd.JoyRunId && this.RunEndTime.Equals(rd.RunEndTime);
        }
    }
}
