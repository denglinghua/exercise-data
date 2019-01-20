using System;
using System.Collections.Generic;
using System.IO;

namespace RunData
{
    class MemberData
    {
        private Dictionary<Member, Member> members = new Dictionary<Member, Member>(); // use as a set

        public void LoadPreviousData(string fileName)
        {
            if (!File.Exists(fileName))
            {
                return;
            }

            Logger.Info("加载之前的所有成员名单");

            string[] lines = File.ReadAllLines(fileName);

            for (int i = 0; i < lines.Length; i++)
            {
                //88474417	Samryi	男	广·马帮_神马分队	2018-1-1
                string[] a = lines[i].Split('\t');
                Member m = Member.Create(a);
                m.JoinDate = DateUtil.ParseDate(a[4]);
                this.members[m] = m;
            }

            Logger.Info("    上期成员：{0} 人", this.members.Keys.Count);
        }

        public void TryAdd(Member m)
        {
            if (!members.ContainsKey(m))
            {
                m.JoinDate = DataSource.Instance.CurrentDateRange.Start;
                this.members[m] = m;
            }
            else
            {
                m.JoinDate = this.members[m].JoinDate;
            }
        }

        public bool isNewMember(Member m)
        {
            if (members.ContainsKey(m))
            {
                return m.JoinDate == DataSource.Instance.CurrentDateRange.Start;
            }
            else
            {
                throw new RunDataException(m.ToString() + " 成员从哪里来的？");
            }
        }

        public void Save(string fileName)
        {
            Logger.Info("保存成员数据");

            // sort only for debug
            List<Member> sortedList = new List<Member>();
            sortedList.AddRange(this.members.Keys);
            sortedList.Sort(delegate (Member a, Member b)
            {
                return a.JoinDate.CompareTo(b.JoinDate);
            });


            List<string> lines = new List<string>();
            foreach (Member m in sortedList)
            {
                lines.Add(String.Format("{0}\t{1}", m, DateUtil.ToDateString(m.JoinDate)));
            }


            File.WriteAllText(fileName, string.Join(Environment.NewLine, lines.ToArray()));
        }
    }
}
