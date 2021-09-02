using System;
using System.Data;

namespace RunData.DataAnalysis
{
    delegate void CalcGroupValueOp(GroupSet groupSet, SumGroup group);

    static class GroupOps
    {
        public static void CalcGroupCountValue(GroupSet groupSet, SumGroup group)
        {
            group.Value = group.DataRows.Count;
        }

        public static void CalcGroupSumValue(GroupSet groupSet, SumGroup group)
        {
            float total = 0;
            foreach (DataRow dr in group.DataRows)
            {
                total += (float)dr[groupSet.SumColumn];
            }

            group.Value = total;
        }

        public static string FormatPaceLabel(object val)
        {
            TimeSpan t = TimeSpan.FromSeconds(Convert.ToDouble(val));
            return string.Format("{0}:{1:D2}", t.Minutes, t.Seconds);
        }
    }
}
