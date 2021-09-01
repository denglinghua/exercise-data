using System;
using System.Collections.Generic;
using System.Data;

namespace RunData.DataAnalysis
{
    class AnalysisDataSource
    {
        public static DataTable CreateRunSumData(List<PeriodRunRecord> sumRunData)
        {
            DataTable dt = new DataTable();
            dt.Columns.Add("gender", typeof(string));
            dt.Columns.Add("distance", typeof(float));
            dt.Columns.Add("total_time", typeof(int));
            dt.Columns.Add("avg_pace", typeof(int));
            dt.Columns.Add("run_times", typeof(short));

            foreach (PeriodRunRecord r in sumRunData)
            {
                dt.Rows.Add(r.Member.Gender, r.Data.Distance, r.Data.TotalTimeSeconds, r.Data.AvgPaceSeconds, r.RunTimes);
            }

            return dt;
        }

        public static DataTable CreateRunDetailData(List<RunRecordDetail> detailRunData)
        {
            DataTable dt = new DataTable();
            dt.Columns.Add("run_time", typeof(DateTime));
            
            foreach (RunRecordDetail r in detailRunData)
            {
                foreach(RunData d in r.Detail)
                {
                    dt.Rows.Add(d.RunTime);
                }
            }

            return dt;
        }
    }
}
