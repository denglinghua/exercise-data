using System;
using System.Collections.Generic;
using System.Text;

namespace RunData
{
    class RunRecord
    {
        public Member Member { get; }
        public double Distance { get; }
        public double TotalTimeSeconds { get; }
        public short RunTimes { get; }
        public long AvgPaceSeconds { get; }
        public bool IsQualified { get; }
        public bool IsQualifiedOfAvgPace { get; }
        public bool IsQualifiedOfDistance { get; }        

        private static readonly short MAX_AVG_PACE = 8 * 60;
        private static readonly short MIN_DISTANCE = 10;  

        public RunRecord(long joyRunId, string name, string gender, string group, double distance, double totalTimeSeconds, short runTimes)
        {
            this.Member = new Member(joyRunId, name, gender, group);
            this.Distance = Math.Truncate(distance * 100) / 100;
            this.TotalTimeSeconds = totalTimeSeconds;
            this.RunTimes = runTimes;
            this.AvgPaceSeconds = (long)(totalTimeSeconds / distance);
            this.IsQualifiedOfAvgPace = this.AvgPaceSeconds <= MAX_AVG_PACE;
            this.IsQualifiedOfDistance = this.Distance >= MIN_DISTANCE;
            this.IsQualified = this.IsQualifiedOfAvgPace && this.IsQualifiedOfDistance;
        }

        public static string ToTimeSpanFromSeconds(double seconds)
        {
            TimeSpan t = TimeSpan.FromSeconds(seconds);
            return string.Format("{0:D2}:{1:D2}:{2:D2}", t.Hours, t.Minutes, t.Seconds);
        }
    }
}
