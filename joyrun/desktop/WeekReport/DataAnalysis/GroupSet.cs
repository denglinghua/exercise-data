using System;
using System.Collections.Generic;
using System.Text;
using System.Data;

namespace RunData.DataAnalysis
{
    class GroupSet
    {
        // for html chart element
        public string Id { get; }
        public string Title { get; }
        public string XTitle { get; set; }
        public string GroupColumn { get; }
        public string SumColumn { get; set; }
        public List<Group> Groups { get; }
        private GroupyStrategy groupyStrategy;
        private GroupAggOp GroupAgg { get; }

        public GroupSet(string id, string title, string groupColumn, GroupyStrategy groupyStrategy, GroupAggOp groupAgg = null)
        {
            this.Id = id;
            this.Title = title;
            this.XTitle = string.Empty;
            this.GroupColumn = groupColumn;
            this.groupyStrategy = groupyStrategy;
            groupyStrategy.GroupSet = this;
            this.Groups = groupyStrategy.CreateGroups();
            this.GroupAgg = groupAgg != null ? groupAgg : GroupOps.GroupAggCount;
        }

        private void DoRowGroup(DataRow dataRow)
        {
            int groupIndex = this.groupyStrategy.MapGroup(dataRow[this.GroupColumn]);
            if (groupIndex >= 0)
            {
                Group group = this.Groups[groupIndex];
                group.AddDataRow(dataRow);
            }
        }

        public override string ToString()
        {
            List<string> groupStrings = new List<string>();
            foreach (Group group in this.Groups) groupStrings.Add(group.ToString());

            return string.Format("{{{0},{1},[{2}]}}",
                this.Title, this.GroupColumn, string.Join(",", groupStrings.ToArray()));
        }

        public static void DoGroup(DataTable table, List<GroupSet> groupSets)
        {
            foreach (DataRow dr in table.Rows)
            {
                foreach (GroupSet groupSet in groupSets)
                {
                    groupSet.DoRowGroup(dr);
                }
            }

            foreach (GroupSet groupSet in groupSets)
            {
                foreach (Group group in groupSet.Groups)
                {
                    groupSet.GroupAgg(groupSet, group);
                }
            }
        }

        public static void PrintGroupSets(List<GroupSet> groupSets)
        {
            foreach (GroupSet gs in groupSets)
            {
                Logger.Info(gs.ToString());
            }
        }
    }
}