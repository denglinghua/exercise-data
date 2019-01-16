using System;
using System.Collections.Generic;
using System.Text;

namespace RunData
{
    class NoRunRecord
    {
        public Member Member { get; }
        public string Reason { get; }
        public int Count { get; }

        public NoRunRecord(Member member, string reason, int count)
        {
            this.Member = member;
            this.Reason = reason;
            this.Count = count;
        }
    }
}
