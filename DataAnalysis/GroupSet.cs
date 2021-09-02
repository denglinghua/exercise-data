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
        public List<SumGroup> Groups { get; }
        private GroupyStrategy groupyStrategy;
        private CalcGroupValueOp CalcGroupValue { get; }

        public GroupSet(string id, string title, string groupColumn, GroupyStrategy groupyStrategy, CalcGroupValueOp calcGroupValue = null)
        {
            this.Id = id;
            this.Title = title;
            this.XTitle = string.Empty;
            this.GroupColumn = groupColumn;
            this.groupyStrategy = groupyStrategy;
            groupyStrategy.GroupSet = this;
            this.Groups = groupyStrategy.CreateGroups();
            this.CalcGroupValue = calcGroupValue != null ? calcGroupValue : GroupOps.CalcGroupCountValue;
        }

        private void DoRowGroup(DataRow dataRow)
        {
            int groupIndex = this.groupyStrategy.FindGroup(dataRow[this.GroupColumn]);
            if (groupIndex >= 0)
            {
                SumGroup group = this.Groups[groupIndex];
                group.AddDataRow(dataRow);
            }
        }

        public override string ToString()
        {
            List<string> groupStrings = new List<string>();
            foreach (SumGroup group in this.Groups) groupStrings.Add(group.ToString());

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
                foreach (SumGroup group in groupSet.Groups)
                {
                    groupSet.CalcGroupValue(groupSet, group);
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

/*

    def get_axis_values(self):
        xlist = []
        ylist = []
        for row in self.rows:
            if (row.value > 0):
                xlist.append(row.label)
                ylist.append(row.value)
        
        return [xlist, ylist]
    
    # for data correctness check
    def check_data(self, context):      
        if self.check_data_func:
            total = sum(map(lambda r : r.value, self.rows))
            if (self.check_data_func(context, total)):
                print('O check OK %s' % self.title)
            else:
                print('X check FAILED %s' % self.title)
        else:
            print('- check no function %s' % self.title)

def check_data(check_data_func):
    def check_data_decorator(func):
        @wraps(func)
        def wrapped_function(*args, **kwargs):            
            group = func(*args, **kwargs)
            group.check_data_func = check_data_func
            return group
        return wrapped_function
    return check_data_decorator
*/
