using System;
using System.Collections.Generic;
using System.Text;

namespace RunData
{
    class NoRunRecord
    {
        public Member Member { get; }
        public string Reason { get; }
        private SortedDictionary<string, bool> times = new SortedDictionary<string, bool>(); // use dict as a set

        public NoRunRecord(Member member, string reason, DateRange dateRange) : this(member, reason, dateRange.ToString())
        {
        }

        public NoRunRecord(Member member, string reason, string time)
        {
            this.Member = member;
            this.Reason = reason;
            this.times[time] = true; //Dictionary[Key] => Add Or Update
        }

        public NoRunRecord(Member member, string reason, string[] times)
        {
            this.Member = member;
            this.Reason = reason;

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
