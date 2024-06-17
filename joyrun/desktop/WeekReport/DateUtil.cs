using System;
using System.Globalization;

namespace RunData
{
    class DateUtil
    {
        private static readonly string DATE_FORMAT = "yyyy-MM-dd";
        private static readonly string DATE_TIME_FORMAT = "yyyy-MM-dd HH:mm:ss";

        public static DateTime ParseDate(string s)
        {
            return DateTime.ParseExact(s, DATE_FORMAT, CultureInfo.InvariantCulture);
        }

        public static DateTime ParseDateTime(string s)
        {
            return DateTime.ParseExact(s, DATE_TIME_FORMAT, CultureInfo.InvariantCulture);
        }

        public static string ToDateString(DateTime d)
        {
            return d.ToString(DATE_FORMAT);
        }

        // why use this method instead of TimeSpan.Parse ? coz time span string's hours greater than 24 
        public static double ParseTimeSpanToSeconds(string str)
        {
            string[] items = str.Split(':');
            int h = int.Parse(items[0]);
            int m = int.Parse(items[1]);
            int s = int.Parse(items[2]);
            return new TimeSpan(h, m, s).TotalSeconds;
        }

        public static string ToTimeSpanFromSeconds(double seconds)
        {
            TimeSpan t = TimeSpan.FromSeconds(seconds);
            return string.Format("{0:D2}:{1:D2}:{2:D2}", (int)t.TotalHours, t.Minutes, t.Seconds);
        }
    }
}
