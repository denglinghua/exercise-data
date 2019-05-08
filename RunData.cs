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

        private static string ToTimeSpanFromSeconds(double seconds)
        {
            TimeSpan t = TimeSpan.FromSeconds(seconds);
            return string.Format("{0:D2}:{1:D2}:{2:D2}", t.Hours, t.Minutes, t.Seconds);
        }

        public string TimeSpanOfAvgPace
        {
            get
            {
                return ToTimeSpanFromSeconds(this.AvgPaceSeconds);
            }
        }

        public string TimeSpanOfTotalTime
        {
            get
            {
                return ToTimeSpanFromSeconds(this.TotalTimeSeconds);
            }
        }
    }
}
