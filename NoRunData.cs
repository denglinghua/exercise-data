using System;
using System.Collections.Generic;
using System.Text;
using System.IO;

namespace RunData
{
    class NoRunData
    {
        private Dictionary<Member, NoRunRecord> previousNoRunList = new Dictionary<Member, NoRunRecord>();
        private List<NoRunRecord> noRunList = new List<NoRunRecord>();

        public void AddPreviousNoRunRecord(Member member, string[] times)
        {
            this.previousNoRunList.Add(member, new NoRunRecord(member, string.Empty, times));
        }

        public void AddCurrentNoRunRecord(Member member, string reason, DateRange dateRange)
        {
            this.noRunList.Add(new NoRunRecord(member, reason, dateRange));
        }

        public void HandleData(List<long> leaveMemberIds)
        {
            this.MarkLeave(leaveMemberIds);

            this.Merge();
        }

        // 请假了相当于跑了，所以要从无跑步人员中移除，避免不达标上榜
        private void MarkLeave(List<long> leaveMemberIds)
        {
            Logger.Info("在当周不达标人员中标注请假");

            foreach (NoRunRecord rec in this.noRunList.ToArray())
            {
                if (leaveMemberIds.Contains(rec.Member.JoyRunId))
                {
                    this.noRunList.Remove(rec);
                }
            }
        }

        // 以当期未跑步去合并过往连续累计
        // 因为如果当期跑步了，或请假了，过往连续累计显然自然失效
        private void Merge()
        {
            Logger.Info("合并过往连续不达标数据");

            foreach (NoRunRecord rec in this.noRunList)
            {
                if (previousNoRunList.ContainsKey(rec.Member))
                {
                    rec.AddTime(previousNoRunList[rec.Member].GetTimes());
                }
            }
        }

        public Dictionary<string, List<NoRunRecord>> SumNoRunDataByGroup()
        {
            Dictionary<string, List<NoRunRecord>> sumData = new Dictionary<string, List<NoRunRecord>>();

            foreach (NoRunRecord rec in noRunList)
            {
                List<NoRunRecord> groupNoRunList;
                string group = rec.Member.GroupShortName;
                if (!sumData.ContainsKey(group))
                {
                    groupNoRunList = new List<NoRunRecord>();
                    sumData.Add(group, groupNoRunList);
                }
                else
                {
                    groupNoRunList = sumData[group];
                }
                groupNoRunList.Add(rec);
            }

            return sumData;
        }

        public void SavePreviousNoRunData()
        {
            Logger.Info("保存连续不达标数据");

            List<string> lines = new List<string>();
            foreach (NoRunRecord nr in this.noRunList)
            {
                lines.Add(String.Format("{0}\t{1}", nr.Member, string.Join(",", nr.GetTimes())));
            }


            File.WriteAllText(DataSource.NO_RUN_DATA_FILE, string.Join(Environment.NewLine, lines.ToArray()));
        }
    }
}
