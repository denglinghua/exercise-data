using System;
using System.Collections.Generic;
using System.Text;

namespace RunData.DataAnalysis
{
    class GroupSetRepo
    {
        private static GroupSet CreateRangeGroupSet(string title, string groupColumn, List<SumGroup> groups)
        {
            return new GroupSet(title, groupColumn, groups, null);
        }
    }
}
