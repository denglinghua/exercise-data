using System;
using System.Collections.Generic;

namespace RunData.DataAnalysis
{
    static class GroupUtil
    {
        static IEnumerable<int> Range(int start, int stop, int step = 1)
        {
            for (var i = start; i < stop; i += step)
            {
                yield return i;
            }
        }

        static List<GroupRange> CreateRangeSeries(IEnumerable<int> iter, string format = "{0}")
        {
            List<GroupRange> ranges = new List<GroupRange>();
            List<int> values = new List<int>(iter);

            int first = values[0];
            ranges.Add(new GroupRange(string.Format("<" + format, first), 0, first));

            for (int i = 0; i < values.Count - 1; i++)
            {
                int start = values[i];
                int end = values[i + 1];
                string s = string.Format(format, start);
                string e = string.Format(format, end);
                ranges.Add(new GroupRange(string.Format("{0}-{1}", s, e), start, end));
            }

            int last = values[values.Count - 1];
            ranges.Add(new GroupRange(string.Format(">" + format, last), last, Int32.MaxValue));

            return ranges;
        }
    }
}
