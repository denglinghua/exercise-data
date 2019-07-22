using System;

namespace RunData
{
    class RunData
    {
        public double Distance { get; }
        public double TotalTimeSeconds { get; }
        public long AvgPaceSeconds { get; }

        public RunData(double distance, double totalTimeSeconds)
        {
            this.Distance = Math.Truncate(distance * 100) / 100;
            this.TotalTimeSeconds = totalTimeSeconds;
            this.AvgPaceSeconds = (long)(totalTimeSeconds / distance);
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
