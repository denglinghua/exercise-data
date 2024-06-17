using System;
using System.Collections.Generic;
using System.Data;

namespace RunData.DataAnalysis
{
    abstract class GroupyStrategy
    {
        public GroupSet GroupSet { get; set; }
        public abstract List<Group> CreateGroups();
        public abstract int MapGroup(object groupValue);
    }

    class DayOfWeekGroupStrategy : GroupyStrategy
    {
        public override List<Group> CreateGroups()
        {
            string[] days = new string[] { "一", "二", "三", "四", "五", "六", "日" };
            List<Group> groups = new List<Group>();
            foreach (string day in days) groups.Add(new Group(day));

            return groups;
        }

        public override int MapGroup(object groupValue)
        {
            DateTime time = (DateTime)groupValue;
            int index = (int)time.DayOfWeek - 1;
            return index >= 0 ? index : 6;
        }
    }

    class HourGroupStrategy : GroupyStrategy
    {
        public override List<Group> CreateGroups()
        {
            List<Group> groups = new List<Group>();
            for (int h = 0; h < 24; h++) groups.Add(new Group(string.Format("{0}", h)));

            return groups;
        }

        public override int MapGroup(object groupValue)
        {
            DateTime time = (DateTime)groupValue;
            return time.Hour;
        }
    }

    class RunCountGroupStrategy : GroupyStrategy
    {
        private static readonly short MAX_COUNT = 16;
        public override List<Group> CreateGroups()
        {
            List<Group> groups = new List<Group>();
            for (int c = 1; c < MAX_COUNT; c++) groups.Add(new Group(string.Format("{0}", c)));
            groups.Add(new Group(string.Format(">{0}", MAX_COUNT - 1)));

            return groups;
        }

        public override int MapGroup(object groupValue)
        {
            short count = (short)groupValue;
            if (count > MAX_COUNT) count = MAX_COUNT;
            return count - 1;
        }
    }

    class RangeGroupStrategy : GroupyStrategy
    {
        private int start;
        private int end;
        private int step;
        private LabelFormatter format;

        public RangeGroupStrategy(int start, int end, int step) : this(start, end, step,
            (val) => string.Format("{0}", val))
        {
        }

        public RangeGroupStrategy(int start, int end, int step, LabelFormatter format)
        {
            this.start = start;
            this.end = end;
            this.step = step;
            this.format = format;
        }

        public override List<Group> CreateGroups()
        {
            return CreateRangeSeries(Range(start, end, step), format);
        }

        public override int MapGroup(object groupValue)
        {
            int groupCount = this.GroupSet.Groups.Count;
            double val = Convert.ToDouble(groupValue);
            if (val < this.start) return 0;
            if (val >= this.end) return groupCount - 1;

            int index = (int)Math.Truncate((val - this.start) / this.step);
            return index + 1;
        }

        public delegate string LabelFormatter(object val);

        static List<Group> CreateRangeSeries(IEnumerable<int> iter, LabelFormatter format)
        {
            List<Group> ranges = new List<Group>();
            List<int> values = new List<int>(iter);

            int first = values[0];
            ranges.Add(new Group("<" + format(first)));

            for (int i = 0; i < values.Count - 1; i++)
            {
                int start = values[i];
                int end = values[i + 1];
                string s = format(start);
                string e = format(end);
                ranges.Add(new Group(string.Format("{0}-{1}", s, e)));
            }

            int last = values[values.Count - 1];
            ranges.Add(new Group(">=" + format(last)));

            return ranges;
        }

        static IEnumerable<int> Range(int start, int stop, int step = 1)
        {
            for (var i = start; i <= stop; i += step)
            {
                yield return i;
            }
        }       
    }
}
