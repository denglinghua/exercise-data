using System;
using System.Collections.Generic;
using System.IO;

namespace DataImport
{
    class CalendarSql
    {
        private DateTime from = DateTime.Parse("2015-01-01");
        private DateTime end = DateTime.Parse("2060-12-31");
        private const string SQL_FORMAT = "INSERT INTO run_calendar VALUES ('{0}', {1}, {2}, {3}, {4});";

        public CalendarSql()
        {

        }

        public void GenSql()
        {
            int weekNo = 1;
            List<string> sqls = new List<string>();
            DateTime d = from;
            while (d <= end)
            {
                int dayOfW = (int)d.DayOfWeek;
                if (dayOfW == 0) dayOfW = 7;

                int month = d.Month;
                int monthNo = d.Year * 100 + month;

                sqls.Add(string.Format(SQL_FORMAT, DateUtil.ToDateString(d), monthNo, month, dayOfW, weekNo));
                d = d.AddDays(1);
                if (d.DayOfWeek == DayOfWeek.Monday)
                {
                    weekNo = weekNo + 1;
                }
            }

            File.WriteAllText("run_calendar.sql", string.Join(Environment.NewLine, sqls.ToArray()));
        }
    }
}