using System.Data;

namespace RunData.DataAnalysis
{
    delegate bool InGroupOp(GroupSet groupSet, SumGroup group, DataRow dataRow);
    delegate void CalcGroupValueOp(GroupSet groupSet, SumGroup group);

    static class GroupOps
    {
        public static bool InEqualsGroup(GroupSet groupSet, SumGroup group, DataRow dataRow)
        {
            int value = (int)group.MatchParam;
            int matchVal = (int)dataRow[groupSet.GroupColumn];
            return matchVal == value;
        }

        public static bool InRangeGroup(GroupSet groupSet, SumGroup group, DataRow dataRow)
        {
            GroupRange range = (GroupRange)group.MatchParam;
            float matchVal = (float)dataRow[groupSet.GroupColumn];
            return matchVal >= range.Start && matchVal < range.End;
        }

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
    }
}
