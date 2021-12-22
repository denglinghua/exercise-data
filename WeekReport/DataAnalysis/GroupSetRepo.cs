using System;
using System.Collections.Generic;
using System.Text;

namespace RunData.DataAnalysis
{
    class GroupSetRepo
    {
        public static GroupSet CreateRunWeekDayGroupSet()
        {
            GroupSet g = new GroupSet("DayOfWeekGroup", "跑步日分布", "run_time", new DayOfWeekGroupStrategy());
            g.XTitle = "星期";
            return g;
        }

        public static GroupSet CreateRunHourGroupSet()
        {
            GroupSet g = new GroupSet("HourGroup", "跑步时辰分布", "run_time", new HourGroupStrategy());
            g.XTitle = "时";
            return g;
        }

        public static GroupSet CreateRunCountGroupSet()
        {
            GroupSet g = new GroupSet("RunCountGroup", "跑步次数分布", "run_times", new RunCountGroupStrategy());
            g.XTitle = "次";
            return g;
        }

        public static GroupSet CreateDistanceGroupSet()
        {
            GroupSet g = new GroupSet("DistanceGroup", "跑步距离分布", "distance", new RangeGroupStrategy(10, 100, 10));
            g.XTitle = "公里";

            return g;
        }

        public static GroupSet CreateAvgPaceGroupSet()
        {
            GroupSet g = new GroupSet("AvgPaceGroup", "跑步配速分布", "avg_pace",
                new RangeGroupStrategy(300, 480, 30, GroupOps.FormatPaceLabel));
            g.XTitle = "分配";

            return g;
        }

        public static GroupSet CreateTotalTimeGroupSet()
        {
            GroupSet g = new GroupSet("TotalTimeGroup", "跑步总用时分布", "total_time",
                new RangeGroupStrategy(3600, 36000, 3600, (val) => ((int)val / 3600).ToString()));
            g.XTitle = "小时";

            return g;
        }
    }
}
