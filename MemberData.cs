using System;
using System.Collections.Generic;
using System.IO;

namespace RunData
{
    class MemberData
    {
        private Dictionary<long, Member> members = new Dictionary<long, Member>();

        public int MemberCount
        {
            get
            {
                return this.members.Count;
            }
        }

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
                this.members[m.JoyRunId] = m;
            }

            Logger.Info("    上期成员：{0} 人", this.members.Keys.Count);
        }

        public void Mark(Member m)
        {
            Member existMember;
            if (!members.TryGetValue(m.JoyRunId, out existMember))
            {
                m.JoinDate = DataSource.Instance.CurrentDateRange.Start;
                Logger.Info("    +：{0}", m);
            }
            else
            {
                m.JoinDate = existMember.JoinDate;
            }
            // 已经存在的member属性（name/group）可能会更新，所以要用最新的member放入
            m.IsActive = true;
            this.members[m.JoyRunId] = m;
        }

        public void RemoveInactiveMembers()
        {
            List<Member> l = new List<Member>(this.members.Values);
            foreach (Member m in l)
            {
                if (!m.IsActive)
                {
                    this.members.Remove(m.JoyRunId);
                    Logger.Info("    -：{0}", m);
                }
            }
        }

        public bool isNewMember(Member m)
        {
            if (members.ContainsKey(m.JoyRunId))
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
            sortedList.AddRange(this.members.Values);
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
