using System;
using System.Collections.Generic;
using System.Text;

namespace RunData
{
    class NonBreakRunRecord
    {
        public Member Member { get; }        
        private SortedDictionary<string, bool> times = new SortedDictionary<string, bool>();

        public NonBreakRunRecord(Member member, DateRange dateRange) : this(member, dateRange.ToString())
        {
        }

        public NonBreakRunRecord(Member member, string time)
        {
            this.Member = member;
            this.times[time] = true; //Dictionary[Key] => Add Or Update
        }

        public NonBreakRunRecord(Member member, string[] times)
        {
            this.Member = member;

            this.AddTime(times);
        }

        public void AddTime(string[] times)
        {
            foreach (string time in times)
            {
                this.times[time] = true;
            }
        }

        public string[] GetTimes()
        {
            string[] t = new string[this.times.Count];
            this.times.Keys.CopyTo(t, 0);
            return t;
        }
    }
}
