using System;
using System.Collections.Generic;
using System.Text;
using System.Globalization;

using System.IO;

namespace RunData
{
    class NonBreakData
    {
        private readonly string description;
        private DateTime curDataTime, prevDataTime;
        // 当期数据日期在往期数据之前（如果往期数据存在），就是非法当期数据了
        private bool invalidCurData = false;
        private Dictionary<Member, NonBreakRecord> prevData = new Dictionary<Member, NonBreakRecord>();
        private List<NonBreakRecord> curData = new List<NonBreakRecord>();

        private static readonly string DATE_FORMAT = "yyyy-MM-dd";

        public NonBreakData(string description, DateTime curDataTime)
        {
            this.description = description;
            this.curDataTime = curDataTime;
        }

        public List<NonBreakRecord> GetCurrentData()
        {
            return this.curData;
        }

        public void LoadPreviousData(string fileName)
        {
            if (!File.Exists(fileName))
            {
                return;
            }

            Logger.Info(string.Format("加载过往连续{0}数据", this.description));

            string[] lines = File.ReadAllLines(fileName);

            this.prevDataTime = DateTime.ParseExact(lines[0], DATE_FORMAT, CultureInfo.InvariantCulture);

            for (int i = 1; i < lines.Length; i++)
            {
                //88474417	Samryi	男	广·马帮_神马分队	3
                string[] a = lines[i].Split('\t');
                this.AddPreviousRecord(new Member(long.Parse(a[0]), a[1], a[2], a[3]), int.Parse(a[4]));
            }

            this.invalidCurData = this.prevDataTime > this.curDataTime;

            if (this.invalidCurData)
            {
                throw new Exception(string.Format("*** 当期[{0}]数据在过往[{1}]累计{2}数据之前，请检查数据。",
                    this.curDataTime.ToShortDateString(), this.prevDataTime.ToShortDateString(), this.description));
            }
        }

        private void AddPreviousRecord(Member member, int count)
        {
            this.prevData.Add(member, new NonBreakRecord(member, count, string.Empty));
        }

        public void AddCurrentRecord(Member member, string reason)
        {
            this.curData.Add(new NonBreakRecord(member, 1, reason));
        }

        public void Merge()
        {
            Logger.Info(string.Format("合并过往连续{0}数据", this.description));

            // 当前数据比过往数据新，连续累计次数才能更新。如果两个日期相同，是重复跑程序。
            // 如果当期数据比过往数据旧，数据非法了，会停止运行程序。
            int increaseCount = this.curDataTime > this.prevDataTime ? 1 : 0;

            foreach (NonBreakRecord r in this.curData)
            {
                if (this.prevData.ContainsKey(r.Member))
                {
                    r.Count = this.prevData[r.Member].Count + increaseCount;
                }
            }
        }

        public IDictionary<string, List<NonBreakRecord>> SumByGroup()
        {
            IDictionary<string, List<NonBreakRecord>> sumData = new SortedDictionary<string, List<NonBreakRecord>>();

            foreach (NonBreakRecord r in this.curData)
            {
                List<NonBreakRecord> groupData;
                string group = r.Member.GroupShortName;
                if (!sumData.ContainsKey(group))
                {
                    groupData = new List<NonBreakRecord>();
                    sumData.Add(group, groupData);
                }
                else
                {
                    groupData = sumData[group];
                }
                groupData.Add(r);
            }

            return sumData;
        }

        public void Save(string fileName)
        {
            Logger.Info(string.Format("保存连续{0}数据", this.description));

            List<string> lines = new List<string>();

            lines.Add(this.curDataTime.ToString(DATE_FORMAT));

            foreach (NonBreakRecord r in this.curData)
            {
                lines.Add(String.Format("{0}\t{1}", r.Member, r.Count));
            }


            File.WriteAllText(fileName, string.Join(Environment.NewLine, lines.ToArray()));
        }
    }
}


