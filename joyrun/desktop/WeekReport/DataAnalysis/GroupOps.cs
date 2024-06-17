using System;
using System.Data;

namespace RunData.DataAnalysis
{
    /// <summary>
    /// Group aggregate operation
    /// </summary>
    delegate void GroupAggOp(GroupSet groupSet, Group group);

    static class GroupOps
    {
        public static void GroupAggCount(GroupSet groupSet, Group group)
        {
            group.Value = group.DataRows.Count;
        }

        public static void GroupAggSum(GroupSet groupSet, Group group)
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
