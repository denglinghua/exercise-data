using System;
using System.Collections.Generic;
using System.Text;

namespace RunData
{
    class NonBreakRecord
    {
        public Member Member { get; }
        public int Count { get; set; }
        public string Reason { get; }

        public NonBreakRecord(Member member, int count, string reason)
        {
            this.Member = member;
            this.Count = count;
            this.Reason = reason;
        }
    }
}
