using System;
using System.Globalization;

namespace RunData
{
    class DateUtil
    {
        private static readonly string DATE_FORMAT = "yyyy-MM-dd";

        public static DateTime ParseDate(string s)
        {
            return DateTime.ParseExact(s, DATE_FORMAT, CultureInfo.InvariantCulture);
        }

        public static string ToDateString(DateTime d)
        {
            return d.ToString(DATE_FORMAT);
        }
    }
}
