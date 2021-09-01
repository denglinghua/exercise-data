using System;

namespace RunData
{
    class RunData
    {
        public double Distance { get; }
        public double TotalTimeSeconds { get; }
        public long AvgPaceSeconds { get; }
        public DateTime RunTime { get; }

        public RunData(double distance, double totalTimeSeconds)
        {
            this.Distance = Math.Truncate(distance * 100) / 100;
            this.TotalTimeSeconds = totalTimeSeconds;
            this.AvgPaceSeconds = (long)(totalTimeSeconds / distance);
        }

        public RunData(double distance, double totalTimeSeconds, DateTime endTime) : this(distance, totalTimeSeconds)
        {
            RunTime = endTime.AddSeconds(-totalTimeSeconds);
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
    }
}
