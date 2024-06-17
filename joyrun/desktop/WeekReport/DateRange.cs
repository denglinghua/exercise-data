using System;
using System.Collections.Generic;
using System.Text;
using System.Globalization;

namespace RunData
{
    class DateRange
    {
        public DateTime Start { get; }
        public DateTime End { get; }

        public DateRange(DateTime start, DateTime end)
        {
            this.Start = start.Date;
            this.End = end.Date;
        }

        public static DateRange Create(string[] items, string format)
        {
            return new DateRange(DateTime.ParseExact(items[0], format, CultureInfo.InvariantCulture),
                DateTime.ParseExact(items[1], format, CultureInfo.InvariantCulture));
        }

        public override bool Equals(object obj)
        {
            DateRange dr = (DateRange)obj;
            return this.Start.Equals(dr.Start) && this.End.Equals(dr.End);
        }

        public override int GetHashCode()
        {
            return this.ToString().GetHashCode();
        }

        public override string ToString()
        {
            return String.Format("{0:yyyyMMdd}-{1:yyyyMMdd}", this.Start, this.End);
        }
    }
}
