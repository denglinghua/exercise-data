using System;
using System.Collections.Generic;
using System.Text;
using System.IO;

namespace RunData
{
    class NoRunData
    {
        private Dictionary<Member, List<DateRange>> previousNoRunData = new Dictionary<Member, List<DateRange>>();
        private List<NoRunRecord> currentNoRunData = new List<NoRunRecord>();

        public void AddPreviousNoRunRecord(Member member, DateRange dateRange)
        {
            if (DataSource.Instance.DateRange.Equals(dateRange))
            {
                return;
            }

            List<DateRange> drList;
            if (this.previousNoRunData.ContainsKey(member))
            {
                drList = this.previousNoRunData[member];
            }
            else
            {
                drList = new List<DateRange>();
                this.previousNoRunData.Add(member, drList);
            }

            if (!drList.Contains(dateRange))
            {
                drList.Add(dateRange);
            }
        }

        public void AddCurrentNoRunRecord(Member member, string reason)
        {
            this.currentNoRunData.Add(new NoRunRecord(member, reason, 1));
        }

        public void MarkLeave(List<long> leaveMemberIds)
        {
            foreach (NoRunRecord rec in this.currentNoRunData.ToArray())
            {
                if (leaveMemberIds.Contains(rec.Member.JoyRunId))
                {
                    this.currentNoRunData.Remove(rec);
                }
            }
        }

        public Dictionary<string, List<NoRunRecord>> SumNoRunData()
        {
            Dictionary<string, List<NoRunRecord>> sumData = new Dictionary<string, List<NoRunRecord>>();

            foreach (NoRunRecord rec in currentNoRunData)
            {
                if (!sumData.ContainsKey(rec.Member.GroupShortName))
                {
                    sumData.Add(rec.Member.GroupShortName, new List<NoRunRecord>());
                }
            }

            foreach (NoRunRecord rec in currentNoRunData)
            {
                Member m = rec.Member;
                List<NoRunRecord> list = sumData[rec.Member.GroupShortName];
                int count = this.previousNoRunData.ContainsKey(m) ? this.previousNoRunData[m].Count : 0;
                count = count + 1;
                list.Add(new NoRunRecord(m, rec.Reason, count));
            }

            return sumData;
        }

        private Dictionary<Member, List<DateRange>> GenNewPreviousNoRunData()
        {
            Dictionary<Member, List<DateRange>> newData = new Dictionary<Member, List<DateRange>>();

            foreach (NoRunRecord rec in currentNoRunData)
            {
                List<DateRange> l = new List<DateRange>();
                l.Add(DataSource.Instance.DateRange);
                Member m = rec.Member;
                if (this.previousNoRunData.ContainsKey(m))
                {
                    l.AddRange(this.previousNoRunData[m]);
                }

                newData.Add(m, l);
            }

            return newData;
        }

        public void SavePreviousNoRunData()
        {
            List<string> lines = new List<string>();
            Dictionary<Member, List<DateRange>> preNoRun = this.GenNewPreviousNoRunData();
            foreach (Member m in preNoRun.Keys)
            {
                foreach (DateRange dr in preNoRun[m])
                {
                    lines.Add(String.Format("{0}\t{1}", m, dr));
                }
            }


            File.WriteAllText(DataSource.NO_RUN_DATA_FILE, string.Join(Environment.NewLine, lines.ToArray()));
        }
    }  
}
